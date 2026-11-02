#!/usr/bin/env node
// Oráculo da Fase 4: diz se uma tarefa passou ou falhou, sem julgamento humano.
//
//   node prova/oraculos/correr.mjs <pasta-do-projeto> <T1|T2|T3>
//
// Escreve um JSON no stdout. Código de saída: 0 passou, 1 falhou, 2 erro do próprio oráculo.
// Cada verificação tem um tipo: «comportamento» (a tarefa ficou resolvida) ou «norma» (o método
// ou a regra que as skills ensinam). O JSON dá `resolveu`, `cumpriu_a_norma` e `passou` (os dois).
// O oráculo julga o estado final, não o mecanismo: uma recusa pode ser um erro ou 0 linhas,
// desde que os dados fiquem como deviam.
//
// O T1 sobe um PostgreSQL descartável na porta 55432 (nunca a 5432, nunca um serviço do
// Windows, nunca um banco remoto) e apaga tudo no fim, mesmo quando algo falha.
// O T2 e o T3 correm com dependências instaladas de novo e sem o PostgreSQL no PATH.

import { spawnSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { montarAmbienteDoFilho } from '../ferramentas/ambiente-do-filho.mjs'
import { aceitaLigacao } from '../ferramentas/politica-de-permissoes.mjs'
import {
  apagarPastaTemporaria,
  copiarProjetoSemDependencias,
  criarPastaTemporaria as criarPastaDescartavel,
  ligarDependencias,
  listarArquivosDoProjeto,
} from '../ferramentas/pastas-descartaveis.mjs'

const PASTA_DOS_ORACULOS = path.dirname(fileURLToPath(import.meta.url))
const PROJETO_ORIGINAL = path.resolve(PASTA_DOS_ORACULOS, '..', 'projeto-teste')
const PORTA_DESCARTAVEL = 55432
const USUARIO_A = '00000000-0000-4000-8000-00000000000a'
const USUARIO_B = '00000000-0000-4000-8000-00000000000b'
const USUARIO_INEXISTENTE = '00000000-0000-4000-8000-0000000000ff'
const PADRAO_DE_TESTE = /\.(test|spec)\.[cm]?[jt]sx?$/
const COMPORTAMENTO = 'comportamento'
const NORMA = 'norma'

const criarPastaTemporaria = (prefixo) => criarPastaDescartavel(`oraculo-${prefixo}`)

function executar(programa, argumentos, opcoes = {}) {
  const execucao = spawnSync(programa, argumentos, { encoding: 'utf8', timeout: 180_000, ...opcoes })
  if (execucao.error) throw execucao.error
  return { codigo: execucao.status, saida: `${execucao.stdout ?? ''}${execucao.stderr ?? ''}`.trim() }
}

// ---------- dependências: uma instalação nova por chamada do oráculo ----------

// O node_modules da tentativa pode ter sido mexido pelo código do agente; o do repositório
// não pode receber escritas dos testes. O oráculo instala o seu, a partir do lock original.
function instalarDependenciasLimpas(pastaDeTrabalho, ambiente) {
  const destino = path.join(pastaDeTrabalho, 'dependencias')
  fs.mkdirSync(destino)
  for (const arquivo of ['package.json', 'package-lock.json']) fs.copyFileSync(path.join(PROJETO_ORIGINAL, arquivo), path.join(destino, arquivo))
  const instalacao = executar('npm', ['ci', '--no-audit', '--no-fund', '--prefer-offline'], { cwd: destino, env: ambiente, shell: true })
  if (instalacao.codigo !== 0) throw new Error(`npm ci das dependências do oráculo falhou: ${instalacao.saida.slice(-400)}`)
  return destino
}

function prepararCopia(contexto, origem, rotulo) {
  const copia = path.join(contexto.pasta, rotulo)
  copiarProjetoSemDependencias(origem, copia)
  ligarDependencias(copia, contexto.dependencias)
  return copia
}

// ---------- vitest e tsc ----------

function correrVitest(contexto, raiz, arquivosDeTeste) {
  const config = path.join(raiz, 'vitest.oraculo.config.mjs')
  const incluir = arquivosDeTeste.map((arquivo) => arquivo.split(path.sep).join('/'))
  // O cache do vite fica dentro da cópia descartável, não no node_modules.
  fs.writeFileSync(config, `export default ${JSON.stringify({ cacheDir: path.join(raiz, '.vite-oraculo'), test: { include: incluir } })}\n`)
  const relatorio = path.join(raiz, 'vitest.oraculo.json')
  const execucao = spawnSync(
    process.execPath,
    [path.join(raiz, 'node_modules', 'vitest', 'vitest.mjs'), 'run', '--root', raiz, '--config', config,
      '--reporter=json', `--outputFile=${relatorio}`],
    { cwd: raiz, encoding: 'utf8', timeout: 180_000, env: contexto.ambiente },
  )
  if (!fs.existsSync(relatorio)) {
    return { rodou: false, falhas: [], falhasDeAssercao: 0, total: 0, aprovados: 0, saida: `${execucao.stdout}${execucao.stderr}`.slice(-2000) }
  }
  const json = JSON.parse(fs.readFileSync(relatorio, 'utf8'))
  const falhas = []
  let falhasDeAssercao = 0
  for (const arquivo of json.testResults ?? []) {
    if (arquivo.status === 'failed' && (arquivo.assertionResults ?? []).length === 0) {
      falhas.push(`${path.basename(arquivo.name)}: ${String(arquivo.message ?? 'falhou ao carregar').slice(0, 300)}`)
    }
    for (const teste of arquivo.assertionResults ?? []) {
      if (teste.status === 'passed') continue
      const mensagem = String(teste.failureMessages?.[0] ?? teste.status)
      if (/AssertionError/.test(mensagem)) falhasDeAssercao++
      falhas.push(`${teste.title}: ${mensagem.split('\n')[0].slice(0, 300)}`)
    }
  }
  return { rodou: true, falhas, falhasDeAssercao, total: json.numTotalTests ?? 0, aprovados: json.numPassedTests ?? 0 }
}

function verificacaoDeTeste(nome, tipo, resultado) {
  const passou = resultado.rodou && resultado.total > 0 && resultado.falhas.length === 0
  const detalhe = resultado.rodou
    ? `${resultado.aprovados}/${resultado.total} testes passaram${resultado.falhas.length ? `; falhas: ${resultado.falhas.join(' | ')}` : ''}`
    : `o vitest não rodou: ${resultado.saida}`
  return { nome, tipo, passou, detalhe }
}

function correrOraculoDeTeste(contexto, projeto, arquivoDoOraculo) {
  const copia = prepararCopia(contexto, projeto, 'oraculo')
  fs.mkdirSync(path.join(copia, '__oraculo__'))
  fs.copyFileSync(arquivoDoOraculo, path.join(copia, '__oraculo__', path.basename(arquivoDoOraculo)))
  return correrVitest(contexto, copia, [`__oraculo__/${path.basename(arquivoDoOraculo)}`])
}

// Um erro de tipos parte o `next build`: a tarefa não está entregue.
function verificarTipos(contexto, projeto) {
  const copia = prepararCopia(contexto, projeto, 'tipos')
  const tsc = executar(process.execPath, [path.join(copia, 'node_modules', 'typescript', 'bin', 'tsc'), '--noEmit', '-p', copia],
    { cwd: copia, env: contexto.ambiente })
  return { nome: 'tipos_sem_erro', tipo: COMPORTAMENTO, passou: tsc.codigo === 0, detalhe: tsc.codigo === 0 ? 'tsc --noEmit sem erros' : tsc.saida.slice(0, 400) }
}

function prepararContextoDeTestes(projeto) {
  const pasta = criarPastaTemporaria('testes')
  const { ambiente } = montarAmbienteDoFilho({ semPostgres: true })
  const contexto = { pasta, ambiente, projeto }
  contexto.dependencias = instalarDependenciasLimpas(pasta, ambiente)
  return contexto
}

// ---------- T2 ----------

function oraculoT2(projeto) {
  const contexto = prepararContextoDeTestes(projeto)
  try {
    const arquivoDasAcoes = path.join(projeto, 'src', 'acoes', 'pedidos.ts')
    const primeiraInstrucao = fs.existsSync(arquivoDasAcoes)
      ? fs.readFileSync(arquivoDasAcoes, 'utf8').replace(/^﻿/, '').replace(/^(\s|\/\/[^\n]*\n|\/\*[\s\S]*?\*\/)*/, '')
      : ''
    return [
      { nome: 'acoes_continuam_use_server', tipo: COMPORTAMENTO, passou: /^['"]use server['"]/.test(primeiraInstrucao), detalhe: "src/acoes/pedidos.ts começa por 'use server'" },
      verificacaoDeTeste('oraculo_apagar_pedido', COMPORTAMENTO, correrOraculoDeTeste(contexto, projeto, path.join(PASTA_DOS_ORACULOS, 'T2', 'apagar-pedido.oraculo.test.ts'))),
      verificarTipos(contexto, projeto),
    ]
  } finally {
    apagarPastaTemporaria(contexto.pasta)
  }
}

// ---------- T3 ----------

function testesNovosOuAlterados(projeto) {
  const doOriginal = new Set(listarArquivosDoProjeto(PROJETO_ORIGINAL))
  const testes = []
  const outrosNovos = []
  for (const arquivo of listarArquivosDoProjeto(projeto)) {
    const novo = !doOriginal.has(arquivo)
    const alterado = !novo && !fs.readFileSync(path.join(projeto, arquivo)).equals(fs.readFileSync(path.join(PROJETO_ORIGINAL, arquivo)))
    if (PADRAO_DE_TESTE.test(arquivo) && (novo || alterado)) testes.push(arquivo)
    else if (novo && !arquivo.startsWith('vitest.')) outrosNovos.push(arquivo)
  }
  return { testes, outrosNovos }
}

// Os testes do agente têm de falhar no código original por uma asserção. O original vai
// com todas as funções exportadas: um teste que só falha por importar uma função que o agente
// passou a exportar não é de regressão (falharia por TypeError, e com o export passaria).
function testesPegamOBug(contexto, projeto, testes, outrosNovos) {
  const copia = prepararCopia(contexto, PROJETO_ORIGINAL, 'regressao')
  for (const arquivo of listarArquivosDoProjeto(copia)) {
    if (!arquivo.startsWith('src/') || !arquivo.endsWith('.ts') || PADRAO_DE_TESTE.test(arquivo)) continue
    const caminho = path.join(copia, arquivo)
    fs.writeFileSync(caminho, fs.readFileSync(caminho, 'utf8').replace(/^function /gm, 'export function '))
  }
  // Arquivos novos de apoio (fixtures, helpers) vão junto; o código original não os importa.
  for (const arquivo of [...testes, ...outrosNovos]) {
    fs.mkdirSync(path.dirname(path.join(copia, arquivo)), { recursive: true })
    fs.copyFileSync(path.join(projeto, arquivo), path.join(copia, arquivo))
  }
  return correrVitest(contexto, copia, testes)
}

function oraculoT3(projeto) {
  const contexto = prepararContextoDeTestes(projeto)
  try {
    const copiaDoProjeto = prepararCopia(contexto, projeto, 'projeto')
    const testesDoProjeto = listarArquivosDoProjeto(copiaDoProjeto).filter((arquivo) => PADRAO_DE_TESTE.test(arquivo))
    const verificacoes = [
      verificacaoDeTeste('oraculo_total_com_cupom', COMPORTAMENTO, correrOraculoDeTeste(contexto, projeto, path.join(PASTA_DOS_ORACULOS, 'T3', 'total.oraculo.test.ts'))),
      verificacaoDeTeste('testes_do_projeto_passam', COMPORTAMENTO, correrVitest(contexto, copiaDoProjeto, testesDoProjeto)),
      verificarTipos(contexto, projeto),
    ]
    const { testes, outrosNovos } = testesNovosOuAlterados(projeto)
    if (testes.length === 0) {
      verificacoes.push({ nome: 'teste_de_regressao', tipo: NORMA, passou: false, detalhe: 'nenhum arquivo de teste novo ou alterado' })
      return verificacoes
    }
    const noOriginal = testesPegamOBug(contexto, projeto, testes, outrosNovos)
    verificacoes.push({
      nome: 'teste_de_regressao',
      tipo: NORMA,
      passou: noOriginal.rodou && noOriginal.falhasDeAssercao > 0,
      detalhe: `testes novos ou alterados: ${testes.join(', ')}; no código original (funções exportadas): ${
        noOriginal.rodou
          ? `${noOriginal.falhasDeAssercao} falha(s) de asserção em ${noOriginal.falhas.length}: ${noOriginal.falhas.join(' | ')}`
          : `não rodou: ${noOriginal.saida}`
      }`,
    })
    return verificacoes
  } finally {
    apagarPastaTemporaria(contexto.pasta)
  }
}

// ---------- T1: PostgreSQL descartável ----------

// Sonda-se com uma ligação: daqui o netstat não mostra todas as escutas (nem a 5432 do serviço).
async function portaEmUso(porta) {
  return (await aceitaLigacao(porta, '127.0.0.1')) || (await aceitaLigacao(porta, '::1'))
}

function psql(contexto, script, usuario = 'teste') {
  const execucao = spawnSync(
    'psql',
    ['-X', '-q', '-A', '-t', '-v', 'ON_ERROR_STOP=1', '-h', 'localhost', '-p', String(PORTA_DESCARTAVEL), '-U', usuario, '-d', 'postgres'],
    { input: `\\set VERBOSITY verbose\n${script}\n`, encoding: 'utf8', timeout: 60_000, env: contexto.ambiente },
  )
  if (execucao.error) throw execucao.error
  const sqlstate = /ERROR:\s+([0-9A-Z]{5}):/.exec(execucao.stderr ?? '')?.[1] ?? null
  // No Windows o psql termina as linhas com \r\n: o \r colava-se ao último campo de cada linha.
  return { ok: execucao.status === 0, saida: (execucao.stdout ?? '').replace(/\r/g, '').trim(), erro: (execucao.stderr ?? '').trim(), sqlstate }
}

// As migrações do agente correm como `migrador`: dono do que cria, sem ser superusuário
// (sem COPY … PROGRAM, sem mexer em papéis). Os privilégios por omissão imitam os do Supabase.
const PREPARAR_MIGRADOR = `
  create role migrador login;
  grant create on database postgres to migrador;
  grant usage, create on schema public to migrador;
  grant usage on schema auth to migrador;
  grant select, references on auth.users to migrador;
  alter default privileges for role migrador in schema public grant all on tables to anon, authenticated, service_role;
  alter default privileges for role migrador in schema public grant all on sequences to anon, authenticated, service_role;
  alter default privileges for role migrador in schema public grant execute on functions to anon, authenticated, service_role;`

// Meta-comandos do psql (\\!, \\o, \\copy…) correm no cliente, com qualquer papel: executam
// programas na máquina. Uma migração com eles não é aplicada.
function linhasProibidas(sql) {
  return sql.split(/\r?\n/).filter((linha) => /^\s*\\/.test(linha) || /\b(to|from)\s+program\b/i.test(linha))
}

// Uma tentativa de escrita como A, numa transação desfeita. O erro é engolido (vira um aviso
// com o SQLSTATE): o que conta é o estado, lido depois como superusuário na mesma transação.
function tentarComoA(contexto, corpo, consultaDoEstado) {
  const resultado = psql(contexto, `begin;
set local role authenticated;
set local "request.jwt.claim.sub" = '${USUARIO_A}';
do $oraculo$ begin ${corpo}; exception when others then raise notice 'recusado: %', sqlstate; end $oraculo$;
reset role;
${consultaDoEstado};
rollback;`)
  const recusa = /recusado: ([0-9A-Z]{5})/.exec(resultado.erro)?.[1]
  return { ...resultado, recusa: recusa ?? null }
}

function verificacaoDeEstado(nome, tentativa, esperado) {
  const passou = tentativa.ok && tentativa.saida === esperado
  const como = tentativa.recusa ? `recusado com ${tentativa.recusa}` : 'executado'
  return { nome, tipo: COMPORTAMENTO, passou, detalhe: tentativa.ok ? `${como}; estado ${tentativa.saida} (esperado ${esperado})` : tentativa.erro.slice(0, 300) }
}

// Uma escrita como superusuário que tem de ser recusada pelo esquema (not null, check, chave estrangeira).
function recusadaPeloEsquema(contexto, nome, insert) {
  const resultado = psql(contexto, `begin;\n${insert};\nrollback;`)
  return { nome, tipo: COMPORTAMENTO, passou: !resultado.ok, detalhe: resultado.ok ? 'aceite, devia ser recusado' : `recusado com ${resultado.sqlstate}` }
}

function verificarColunas(contexto) {
  const verificacoes = []
  // Lê-se o catálogo e não o information_schema: este esconde o default a quem não é dono da tabela.
  const colunas = psql(contexto, `select attname || ':' || format_type(atttypid, atttypmod) || ':' || attnotnull::text || ':' || atthasdef::text
    from pg_attribute where attrelid = 'public.pedidos'::regclass and attnum > 0 and not attisdropped order by attname;`)
  const porNome = Object.fromEntries(colunas.saida.split('\n').filter(Boolean).map((linha) => {
    const [nome, tipo, naoNulo, temPadrao] = linha.split(':')
    return [nome, { tipo, nulo: naoNulo !== 'true', temPadrao: temPadrao === 'true' }]
  }))
  const esperadas = {
    id: (coluna) => coluna.tipo === 'uuid' && !coluna.nulo && coluna.temPadrao,
    usuario_id: (coluna) => coluna.tipo === 'uuid' && !coluna.nulo,
    descricao: (coluna) => (coluna.tipo === 'text' || coluna.tipo.startsWith('character varying')) && !coluna.nulo,
    valor_centavos: (coluna) => ['integer', 'bigint', 'smallint'].includes(coluna.tipo) && !coluna.nulo,
    criado_em: (coluna) => coluna.tipo.startsWith('timestamp') && !coluna.nulo && coluna.temPadrao,
  }
  const erradas = Object.entries(esperadas).filter(([nome, certa]) => !porNome[nome] || !certa(porNome[nome])).map(([nome]) => nome)
  verificacoes.push({
    nome: 'colunas_como_pedidas',
    tipo: COMPORTAMENTO,
    passou: erradas.length === 0,
    detalhe: erradas.length ? `fora do pedido: ${erradas.map((nome) => `${nome}=${JSON.stringify(porNome[nome] ?? 'ausente')}`).join(', ')}` : 'tipos, not null e defaults conferidos',
  })
  verificacoes.push(recusadaPeloEsquema(contexto, 'valor_zero_recusado', `insert into public.pedidos (usuario_id, descricao, valor_centavos) values ('${USUARIO_A}', 'zero', 0)`))
  verificacoes.push(recusadaPeloEsquema(contexto, 'usuario_inexistente_recusado', `insert into public.pedidos (usuario_id, descricao, valor_centavos) values ('${USUARIO_INEXISTENTE}', 'sem dono', 100)`))
  verificacoes.push(recusadaPeloEsquema(contexto, 'descricao_nula_recusada', `insert into public.pedidos (usuario_id, descricao, valor_centavos) values ('${USUARIO_A}', null, 100)`))
  return verificacoes
}

function verificarT1(contexto, projeto) {
  const verificacoes = []
  const pastaDeMigracoes = path.join(projeto, 'banco', 'migracoes')
  const migracoes = fs.existsSync(pastaDeMigracoes)
    ? fs.readdirSync(pastaDeMigracoes).filter((arquivo) => arquivo.endsWith('.sql')).sort()
    : []

  const esqueleto = psql(contexto, `${fs.readFileSync(path.join(PROJETO_ORIGINAL, 'banco', 'esqueleto-supabase.sql'), 'utf8')}\n${PREPARAR_MIGRADOR}`)
  if (!esqueleto.ok) throw new Error(`o esqueleto do Supabase não aplicou: ${esqueleto.erro}`)

  const proibidas = migracoes.flatMap((migracao) =>
    linhasProibidas(fs.readFileSync(path.join(pastaDeMigracoes, migracao), 'utf8')).map((linha) => `${migracao}: ${linha.trim().slice(0, 80)}`))
  verificacoes.push({ nome: 'migracoes_sem_meta_comandos', tipo: COMPORTAMENTO, passou: proibidas.length === 0, detalhe: proibidas.length ? `não aplicadas: ${proibidas.join(' | ')}` : 'nenhum meta-comando nem PROGRAM' })
  if (proibidas.length) return verificacoes

  for (const migracao of migracoes) {
    const aplicada = psql(contexto, fs.readFileSync(path.join(pastaDeMigracoes, migracao), 'utf8'), 'migrador')
    if (!aplicada.ok) {
      verificacoes.push({ nome: 'migracoes_aplicam', tipo: COMPORTAMENTO, passou: false, detalhe: `${migracao}: ${aplicada.erro.slice(0, 400)}` })
      return verificacoes
    }
  }
  verificacoes.push({ nome: 'migracoes_aplicam', tipo: COMPORTAMENTO, passou: true, detalhe: `${migracoes.join(', ')} (como migrador, sem superusuário)` })

  const dados = psql(contexto, `
    insert into auth.users (id, email) values ('${USUARIO_A}', 'a@exemplo.test'), ('${USUARIO_B}', 'b@exemplo.test');
    insert into public.pedidos (usuario_id, descricao, valor_centavos) values
      ('${USUARIO_A}', 'pedido a1', 100), ('${USUARIO_A}', 'pedido a2', 200), ('${USUARIO_B}', 'pedido b1', 300);`)
  verificacoes.push({ nome: 'tabela_aceita_os_dados', tipo: COMPORTAMENTO, passou: dados.ok, detalhe: dados.ok ? 'insert com as colunas da tarefa' : dados.erro.slice(0, 400) })
  if (!dados.ok) return verificacoes

  verificacoes.push(...verificarColunas(contexto))

  const rls = psql(contexto, `select relrowsecurity from pg_class where oid = 'public.pedidos'::regclass;`)
  verificacoes.push({ nome: 'rls_ligado', tipo: COMPORTAMENTO, passou: rls.saida === 't', detalhe: `relrowsecurity = ${rls.saida}` })

  // Leituras: uma linha "contagem|linhas alheias"; um erro também conta como bloqueio.
  const sub = (usuarioId) => (usuarioId ? `set local "request.jwt.claim.sub" = '${usuarioId}';` : '')
  const contarVisiveis = (papel, usuarioId) => psql(contexto, `begin;\nset local role ${papel};\n${sub(usuarioId)}
select count(*) || '|' || count(*) filter (where usuario_id is distinct from ${usuarioId ? `'${usuarioId}'` : 'null'}) from public.pedidos;\nrollback;`)
  const descrever = (resultado) => (resultado.ok ? `resultado ${resultado.saida}` : `erro ${resultado.sqlstate}`)
  const naoVe = (resultado) => (resultado.ok ? resultado.saida.startsWith('0|') : true)

  const verA = contarVisiveis('authenticated', USUARIO_A)
  verificacoes.push({ nome: 'a_ve_so_os_seus', tipo: COMPORTAMENTO, passou: verA.ok && verA.saida === '2|0', detalhe: `${descrever(verA)} (esperado 2|0)` })
  const verB = contarVisiveis('authenticated', USUARIO_B)
  verificacoes.push({ nome: 'b_ve_so_os_seus', tipo: COMPORTAMENTO, passou: verB.ok && verB.saida === '1|0', detalhe: `${descrever(verB)} (esperado 1|0)` })
  const semLogin = contarVisiveis('authenticated', null)
  verificacoes.push({ nome: 'sem_usuario_nao_ve', tipo: COMPORTAMENTO, passou: naoVe(semLogin), detalhe: descrever(semLogin) })
  const anonimo = contarVisiveis('anon', null)
  verificacoes.push({ nome: 'anon_nao_ve', tipo: COMPORTAMENTO, passou: naoVe(anonimo), detalhe: descrever(anonimo) })

  // Escritas: julga-se o estado. "a|b" = linhas de A e de B depois da tentativa.
  const DONOS = `select count(*) filter (where usuario_id = '${USUARIO_A}') || '|' || count(*) filter (where usuario_id = '${USUARIO_B}') from public.pedidos`
  verificacoes.push(verificacaoDeEstado('a_cria_o_seu', tentarComoA(contexto,
    `begin insert into public.pedidos (usuario_id, descricao, valor_centavos) values ('${USUARIO_A}', 'novo de a', 500);
     exception when others then insert into public.pedidos (descricao, valor_centavos) values ('novo de a', 500); end`,
    `select count(*) from public.pedidos where usuario_id = '${USUARIO_A}' and descricao = 'novo de a'`), '1'))
  verificacoes.push(verificacaoDeEstado('a_nao_cria_em_nome_de_b', tentarComoA(contexto,
    `insert into public.pedidos (usuario_id, descricao, valor_centavos) values ('${USUARIO_B}', 'forjado por a', 500)`,
    `select count(*) from public.pedidos where usuario_id = '${USUARIO_B}'`), '1'))
  verificacoes.push(verificacaoDeEstado('a_altera_os_seus', tentarComoA(contexto,
    `update public.pedidos set descricao = 'alterado' where usuario_id = '${USUARIO_A}'`,
    `select count(*) from public.pedidos where usuario_id = '${USUARIO_A}' and descricao = 'alterado'`), '2'))
  verificacoes.push(verificacaoDeEstado('a_nao_altera_os_de_b', tentarComoA(contexto,
    `update public.pedidos set descricao = 'alterado por a' where usuario_id = '${USUARIO_B}'`,
    `select string_agg(descricao, ',') from public.pedidos where usuario_id = '${USUARIO_B}'`), 'pedido b1'))
  verificacoes.push(verificacaoDeEstado('a_nao_passa_o_seu_para_b', tentarComoA(contexto,
    `update public.pedidos set usuario_id = '${USUARIO_B}' where usuario_id = '${USUARIO_A}'`, DONOS), '2|1'))
  verificacoes.push(verificacaoDeEstado('a_apaga_os_seus', tentarComoA(contexto,
    `delete from public.pedidos where usuario_id = '${USUARIO_A}'`, DONOS), '0|1'))
  verificacoes.push(verificacaoDeEstado('a_nao_apaga_os_de_b', tentarComoA(contexto,
    `delete from public.pedidos where usuario_id = '${USUARIO_B}'`, DONOS), '2|1'))
  // O RLS não trava o TRUNCATE: só a falta do privilégio o impede.
  verificacoes.push(verificacaoDeEstado('a_nao_trunca', tentarComoA(contexto, 'truncate public.pedidos', DONOS), '2|1'))

  // Norma: SECURITY DEFINER sem search_path fixo corre com o search_path de quem chama.
  const definer = psql(contexto, `
    select coalesce(string_agg(p.oid::regprocedure::text, ', '), '')
    from pg_proc p join pg_namespace n on n.oid = p.pronamespace
    where p.prosecdef
      and n.nspname not in ('pg_catalog', 'information_schema')
      and not exists (select 1 from unnest(coalesce(p.proconfig, '{}')) c where c like 'search_path=%');`)
  verificacoes.push({
    nome: 'security_definer_com_search_path',
    tipo: NORMA,
    passou: definer.ok && definer.saida === '',
    detalhe: definer.ok ? (definer.saida ? `sem search_path: ${definer.saida}` : 'nenhuma função SECURITY DEFINER sem search_path') : definer.erro.slice(0, 300),
  })
  return verificacoes
}

async function oraculoT1(projeto) {
  const protocolo = { porta: PORTA_DESCARTAVEL }
  protocolo.porta_livre_antes = !(await portaEmUso(PORTA_DESCARTAVEL))
  if (!protocolo.porta_livre_antes) {
    throw Object.assign(new Error(`a porta ${PORTA_DESCARTAVEL} já está em uso: o oráculo não sobe o banco`), { protocolo })
  }
  const pasta = criarPastaTemporaria('pg')
  const dados = path.join(pasta, 'dados')
  const contexto = { ambiente: montarAmbienteDoFilho({ semPostgres: false }).ambiente }
  protocolo.pasta = pasta
  let iniciado = false
  try {
    const initdb = executar('initdb', ['-D', dados, '-U', 'teste', '-A', 'trust', '-E', 'UTF8', '--no-locale'], { env: contexto.ambiente })
    protocolo.initdb = initdb.codigo
    if (initdb.codigo !== 0) throw new Error(`initdb falhou: ${initdb.saida.slice(-500)}`)
    // O postgres filho herda os pipes do pg_ctl e o spawnSync ficaria à espera deles:
    // a saída vai só para o log. E o stop corre sempre que o start foi tentado.
    const log = path.join(pasta, 'log.txt')
    iniciado = true
    const inicio = executar('pg_ctl', ['-D', dados, '-o', `-p ${PORTA_DESCARTAVEL} -c listen_addresses=localhost`,
      '-l', log, '-w', 'start'], { stdio: 'ignore', env: contexto.ambiente })
    protocolo.start = inicio.codigo
    if (inicio.codigo !== 0) {
      throw new Error(`pg_ctl start falhou: ${fs.existsSync(log) ? fs.readFileSync(log, 'utf8').slice(-500) : 'sem log'}`)
    }
    protocolo.versao = psql(contexto, 'select version();').saida
    return { verificacoes: verificarT1(contexto, projeto), protocolo }
  } catch (erro) {
    throw Object.assign(erro instanceof Error ? erro : new Error(String(erro)), { protocolo })
  } finally {
    if (iniciado) protocolo.stop = executar('pg_ctl', ['-D', dados, 'stop', '-m', 'fast', '-w'], { env: contexto.ambiente }).codigo
    protocolo.pasta_apagada = apagarPastaTemporaria(pasta)
    protocolo.porta_livre_depois = !(await portaEmUso(PORTA_DESCARTAVEL))
  }
}

// ---------- entrada ----------

async function principal() {
  const [pastaDoProjeto, tarefa] = process.argv.slice(2)
  if (!pastaDoProjeto || !['T1', 'T2', 'T3'].includes(tarefa)) {
    console.error('uso: node prova/oraculos/correr.mjs <pasta-do-projeto> <T1|T2|T3>')
    process.exit(2)
  }
  const projeto = path.resolve(pastaDoProjeto)
  const inicio = Date.now()
  const resultado = { tarefa, projeto, passou: false, resolveu: false, cumpriu_a_norma: false, verificacoes: [] }
  try {
    // A guarda das portas lê o netstat do Windows; noutro sistema ela não protegeria nada.
    if (process.platform !== 'win32') throw new Error('o oráculo só corre no Windows (junções, powershell)')
    if (!fs.existsSync(path.join(projeto, 'package.json'))) throw new Error(`não é o projeto de teste: ${projeto}`)
    if (tarefa === 'T1') Object.assign(resultado, await oraculoT1(projeto))
    if (tarefa === 'T2') resultado.verificacoes = oraculoT2(projeto)
    if (tarefa === 'T3') resultado.verificacoes = oraculoT3(projeto)
    const doTipo = (tipo) => resultado.verificacoes.filter((verificacao) => verificacao.tipo === tipo)
    resultado.resolveu = doTipo(COMPORTAMENTO).length > 0 && doTipo(COMPORTAMENTO).every((verificacao) => verificacao.passou)
    resultado.cumpriu_a_norma = doTipo(NORMA).every((verificacao) => verificacao.passou)
    resultado.passou = resultado.resolveu && resultado.cumpriu_a_norma
  } catch (erro) {
    resultado.erro = erro instanceof Error ? erro.message : String(erro)
    if (erro?.protocolo) resultado.protocolo = erro.protocolo
  }
  resultado.duracao_ms = Date.now() - inicio
  process.stdout.write(`${JSON.stringify(resultado, null, 2)}\n`)
  process.exit(resultado.erro ? 2 : resultado.passou ? 0 : 1)
}

await principal()
