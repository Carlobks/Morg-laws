#!/usr/bin/env node
// Oráculo da Fase 4: diz se uma tarefa passou ou falhou, sem julgamento humano.
//
//   node prova/oraculos/correr.mjs <pasta-do-projeto> <T1|T2|T3>
//
// Escreve um JSON no stdout. Código de saída: 0 passou, 1 falhou, 2 erro do próprio oráculo.
// O T1 sobe um PostgreSQL descartável na porta 55432 (nunca a 5432, nunca um serviço do
// Windows, nunca um banco remoto) e apaga tudo no fim, mesmo quando algo falha.

import { spawnSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
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
const PADRAO_DE_TESTE = /\.(test|spec)\.[cm]?[jt]sx?$/

const criarPastaTemporaria = (prefixo) => criarPastaDescartavel(`oraculo-${prefixo}`)

// ---------- vitest ----------

function correrVitest(raiz, arquivosDeTeste, rotulo) {
  const config = path.join(raiz, `vitest.${rotulo}.config.mjs`)
  const incluir = arquivosDeTeste.map((arquivo) => arquivo.split(path.sep).join('/'))
  fs.writeFileSync(config, `export default { test: { include: ${JSON.stringify(incluir)} } }\n`)
  const relatorio = path.join(raiz, `vitest.${rotulo}.json`)
  const execucao = spawnSync(
    process.execPath,
    [path.join(raiz, 'node_modules', 'vitest', 'vitest.mjs'), 'run', '--root', raiz, '--config', config,
      '--reporter=json', `--outputFile=${relatorio}`],
    { cwd: raiz, encoding: 'utf8', timeout: 180_000 },
  )
  if (!fs.existsSync(relatorio)) {
    return { rodou: false, falhas: [], total: 0, aprovados: 0, saida: (execucao.stdout + execucao.stderr).slice(-2000) }
  }
  const json = JSON.parse(fs.readFileSync(relatorio, 'utf8'))
  const falhas = []
  for (const arquivo of json.testResults ?? []) {
    if (arquivo.status === 'failed' && (arquivo.assertionResults ?? []).length === 0) {
      falhas.push(`${path.basename(arquivo.name)}: ${String(arquivo.message ?? 'falhou ao carregar').slice(0, 300)}`)
    }
    for (const teste of arquivo.assertionResults ?? []) {
      if (teste.status !== 'passed') {
        falhas.push(`${teste.title}: ${String(teste.failureMessages?.[0] ?? teste.status).split('\n')[0].slice(0, 300)}`)
      }
    }
  }
  return { rodou: true, falhas, total: json.numTotalTests ?? 0, aprovados: json.numPassedTests ?? 0 }
}

function correrOraculoDeTeste(projeto, arquivoDoOraculo) {
  const pasta = criarPastaTemporaria('vitest')
  const copia = path.join(pasta, 'projeto')
  try {
    copiarProjetoSemDependencias(projeto, copia)
    ligarDependencias(copia, projeto, PROJETO_ORIGINAL)
    fs.mkdirSync(path.join(copia, '__oraculo__'))
    fs.copyFileSync(arquivoDoOraculo, path.join(copia, '__oraculo__', path.basename(arquivoDoOraculo)))
    return correrVitest(copia, [`__oraculo__/${path.basename(arquivoDoOraculo)}`], 'oraculo')
  } finally {
    apagarPastaTemporaria(pasta)
  }
}

function verificacaoDeTeste(nome, resultado) {
  const passou = resultado.rodou && resultado.total > 0 && resultado.falhas.length === 0
  const detalhe = resultado.rodou
    ? `${resultado.aprovados}/${resultado.total} testes passaram${resultado.falhas.length ? `; falhas: ${resultado.falhas.join(' | ')}` : ''}`
    : `o vitest não rodou: ${resultado.saida}`
  return { nome, passou, detalhe }
}

// ---------- T2 ----------

function oraculoT2(projeto) {
  const arquivoDasAcoes = path.join(projeto, 'src', 'acoes', 'pedidos.ts')
  const primeiraInstrucao = fs.existsSync(arquivoDasAcoes)
    ? fs.readFileSync(arquivoDasAcoes, 'utf8').replace(/^﻿/, '').replace(/^(\s|\/\/[^\n]*\n|\/\*[\s\S]*?\*\/)*/, '')
    : ''
  return [
    {
      nome: 'acoes_continuam_use_server',
      passou: /^['"]use server['"]/.test(primeiraInstrucao),
      detalhe: "src/acoes/pedidos.ts começa por 'use server'",
    },
    verificacaoDeTeste('oraculo_apagar_pedido', correrOraculoDeTeste(projeto, path.join(PASTA_DOS_ORACULOS, 'T2', 'apagar-pedido.oraculo.test.ts'))),
  ]
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

// Os testes do agente têm de falhar no código original: é isso que os faz de regressão.
function testesPegamOBug(projeto, testes, outrosNovos) {
  const pasta = criarPastaTemporaria('regressao')
  const copia = path.join(pasta, 'projeto')
  try {
    copiarProjetoSemDependencias(PROJETO_ORIGINAL, copia)
    ligarDependencias(copia, PROJETO_ORIGINAL)
    // Arquivos novos de apoio (fixtures, helpers) vão junto; o código original não os importa.
    for (const arquivo of [...testes, ...outrosNovos]) {
      fs.mkdirSync(path.dirname(path.join(copia, arquivo)), { recursive: true })
      fs.copyFileSync(path.join(projeto, arquivo), path.join(copia, arquivo))
    }
    return correrVitest(copia, testes, 'regressao')
  } finally {
    apagarPastaTemporaria(pasta)
  }
}

function testesDoProjetoPassam(projeto) {
  const pasta = criarPastaTemporaria('projeto')
  const copia = path.join(pasta, 'projeto')
  try {
    copiarProjetoSemDependencias(projeto, copia)
    ligarDependencias(copia, projeto, PROJETO_ORIGINAL)
    const testes = listarArquivosDoProjeto(copia).filter((arquivo) => PADRAO_DE_TESTE.test(arquivo))
    return correrVitest(copia, testes, 'projeto')
  } finally {
    apagarPastaTemporaria(pasta)
  }
}

function oraculoT3(projeto) {
  const verificacoes = [
    verificacaoDeTeste('oraculo_total_com_cupom', correrOraculoDeTeste(projeto, path.join(PASTA_DOS_ORACULOS, 'T3', 'total.oraculo.test.ts'))),
    verificacaoDeTeste('testes_do_projeto_passam', testesDoProjetoPassam(projeto)),
  ]
  const { testes, outrosNovos } = testesNovosOuAlterados(projeto)
  if (testes.length === 0) {
    verificacoes.push({ nome: 'teste_de_regressao', passou: false, detalhe: 'nenhum arquivo de teste novo ou alterado' })
    return verificacoes
  }
  const noOriginal = testesPegamOBug(projeto, testes, outrosNovos)
  verificacoes.push({
    nome: 'teste_de_regressao',
    passou: noOriginal.rodou && noOriginal.falhas.length > 0,
    detalhe: `testes novos ou alterados: ${testes.join(', ')}; no código original: ${
      noOriginal.rodou ? `${noOriginal.falhas.length} falha(s) ${noOriginal.falhas.join(' | ')}` : `não rodou: ${noOriginal.saida}`
    }`,
  })
  return verificacoes
}

// ---------- T1: PostgreSQL descartável ----------

function portaEmUso(porta) {
  const netstat = spawnSync('netstat', ['-ano'], { encoding: 'utf8' })
  return netstat.stdout.split(/\r?\n/).some((linha) => {
    const colunas = linha.trim().split(/\s+/)
    return colunas.length >= 2 && /^TCP|^UDP/i.test(colunas[0]) && colunas[1].endsWith(`:${porta}`)
  })
}

function executar(programa, argumentos, opcoes = {}) {
  const execucao = spawnSync(programa, argumentos, { encoding: 'utf8', timeout: 120_000, ...opcoes })
  if (execucao.error) throw execucao.error
  return { codigo: execucao.status, saida: `${execucao.stdout ?? ''}${execucao.stderr ?? ''}`.trim() }
}

function psql(script) {
  const execucao = spawnSync(
    'psql',
    ['-X', '-q', '-A', '-t', '-v', 'ON_ERROR_STOP=1', '-h', 'localhost', '-p', String(PORTA_DESCARTAVEL), '-U', 'teste', '-d', 'postgres'],
    { input: `\\set VERBOSITY verbose\n${script}\n`, encoding: 'utf8', timeout: 60_000 },
  )
  if (execucao.error) throw execucao.error
  const sqlstate = /ERROR:\s+([0-9A-Z]{5}):/.exec(execucao.stderr ?? '')?.[1] ?? null
  return { ok: execucao.status === 0, saida: (execucao.stdout ?? '').trim(), erro: (execucao.stderr ?? '').trim(), sqlstate }
}

// Corre um trecho como um papel da API, dentro de uma transação que é sempre desfeita.
function comoPapel(papel, usuarioId, sql) {
  const sub = usuarioId ? `set local "request.jwt.claim.sub" = '${usuarioId}';` : ''
  return psql(`begin;\nset local role ${papel};\n${sub}\n${sql}\nrollback;`)
}

function verificarT1(projeto) {
  const verificacoes = []
  const pastaDeMigracoes = path.join(projeto, 'banco', 'migracoes')
  const migracoes = fs.existsSync(pastaDeMigracoes)
    ? fs.readdirSync(pastaDeMigracoes).filter((arquivo) => arquivo.endsWith('.sql')).sort()
    : []

  const esqueleto = psql(fs.readFileSync(path.join(PROJETO_ORIGINAL, 'banco', 'esqueleto-supabase.sql'), 'utf8'))
  if (!esqueleto.ok) throw new Error(`o esqueleto do Supabase não aplicou: ${esqueleto.erro}`)

  for (const migracao of migracoes) {
    const aplicada = psql(fs.readFileSync(path.join(pastaDeMigracoes, migracao), 'utf8'))
    if (!aplicada.ok) {
      verificacoes.push({ nome: 'migracoes_aplicam', passou: false, detalhe: `${migracao}: ${aplicada.erro.slice(0, 400)}` })
      return verificacoes
    }
  }
  verificacoes.push({ nome: 'migracoes_aplicam', passou: true, detalhe: migracoes.join(', ') })

  const dados = psql(`
    insert into auth.users (id, email) values ('${USUARIO_A}', 'a@exemplo.test'), ('${USUARIO_B}', 'b@exemplo.test');
    insert into public.pedidos (usuario_id, descricao, valor_centavos) values
      ('${USUARIO_A}', 'pedido a1', 100), ('${USUARIO_A}', 'pedido a2', 200), ('${USUARIO_B}', 'pedido b1', 300);`)
  verificacoes.push({ nome: 'tabela_com_as_colunas_pedidas', passou: dados.ok, detalhe: dados.ok ? 'insert com as colunas da tarefa' : dados.erro.slice(0, 400) })
  if (!dados.ok) return verificacoes

  const rls = psql(`select relrowsecurity from pg_class where oid = 'public.pedidos'::regclass;`)
  verificacoes.push({ nome: 'rls_ligado', passou: rls.saida === 't', detalhe: `relrowsecurity = ${rls.saida}` })

  // Uma linha "contagem|linhas alheias" por consulta; um erro de permissão também conta como bloqueio.
  const contarVisiveis = (papel, usuarioId) =>
    comoPapel(papel, usuarioId, `select count(*) || '|' || count(*) filter (where usuario_id is distinct from ${usuarioId ? `'${usuarioId}'` : 'null'}) from public.pedidos;`)
  const contarAfetadas = (usuarioId, comando) =>
    comoPapel('authenticated', usuarioId, `with afetadas as (${comando} returning 1) select count(*) from afetadas;`)
  const bloqueouOuZero = (resultado) => (resultado.ok ? resultado.saida === '0' : resultado.sqlstate === '42501')
  const descrever = (resultado) => (resultado.ok ? `resultado ${resultado.saida}` : `erro ${resultado.sqlstate}`)

  const verA = contarVisiveis('authenticated', USUARIO_A)
  verificacoes.push({ nome: 'a_ve_so_os_seus', passou: verA.ok && verA.saida === '2|0', detalhe: `${descrever(verA)} (esperado 2|0)` })
  const verB = contarVisiveis('authenticated', USUARIO_B)
  verificacoes.push({ nome: 'b_ve_so_os_seus', passou: verB.ok && verB.saida === '1|0', detalhe: `${descrever(verB)} (esperado 1|0)` })
  const semLogin = contarVisiveis('authenticated', null)
  verificacoes.push({ nome: 'sem_usuario_nao_ve', passou: semLogin.ok ? semLogin.saida.startsWith('0|') : semLogin.sqlstate === '42501', detalhe: descrever(semLogin) })
  const anonimo = contarVisiveis('anon', null)
  verificacoes.push({ nome: 'anon_nao_ve', passou: anonimo.ok ? anonimo.saida.startsWith('0|') : anonimo.sqlstate === '42501', detalhe: descrever(anonimo) })

  const criaOSeu = contarAfetadas(USUARIO_A, `insert into public.pedidos (usuario_id, descricao, valor_centavos) values ('${USUARIO_A}', 'novo de a', 500)`)
  verificacoes.push({ nome: 'a_cria_o_seu', passou: criaOSeu.ok && criaOSeu.saida === '1', detalhe: descrever(criaOSeu) })
  const criaParaB = contarAfetadas(USUARIO_A, `insert into public.pedidos (usuario_id, descricao, valor_centavos) values ('${USUARIO_B}', 'forjado por a', 500)`)
  verificacoes.push({ nome: 'a_nao_cria_em_nome_de_b', passou: !criaParaB.ok && criaParaB.sqlstate === '42501', detalhe: descrever(criaParaB) })

  const alteraOSeu = contarAfetadas(USUARIO_A, `update public.pedidos set descricao = 'alterado' where usuario_id = '${USUARIO_A}'`)
  verificacoes.push({ nome: 'a_altera_os_seus', passou: alteraOSeu.ok && alteraOSeu.saida === '2', detalhe: descrever(alteraOSeu) })
  const alteraDeB = contarAfetadas(USUARIO_A, `update public.pedidos set descricao = 'alterado por a' where usuario_id = '${USUARIO_B}'`)
  verificacoes.push({ nome: 'a_nao_altera_os_de_b', passou: bloqueouOuZero(alteraDeB), detalhe: descrever(alteraDeB) })
  const transfere = contarAfetadas(USUARIO_A, `update public.pedidos set usuario_id = '${USUARIO_B}' where usuario_id = '${USUARIO_A}'`)
  verificacoes.push({ nome: 'a_nao_passa_o_seu_para_b', passou: bloqueouOuZero(transfere), detalhe: descrever(transfere) })

  const apagaOSeu = contarAfetadas(USUARIO_A, `delete from public.pedidos where usuario_id = '${USUARIO_A}'`)
  verificacoes.push({ nome: 'a_apaga_os_seus', passou: apagaOSeu.ok && apagaOSeu.saida === '2', detalhe: descrever(apagaOSeu) })
  const apagaDeB = contarAfetadas(USUARIO_A, `delete from public.pedidos where usuario_id = '${USUARIO_B}'`)
  verificacoes.push({ nome: 'a_nao_apaga_os_de_b', passou: bloqueouOuZero(apagaDeB), detalhe: descrever(apagaDeB) })

  // SECURITY DEFINER sem search_path fixo: corre com o search_path de quem chama.
  const definer = psql(`
    select coalesce(string_agg(p.oid::regprocedure::text, ', '), '')
    from pg_proc p join pg_namespace n on n.oid = p.pronamespace
    where p.prosecdef
      and n.nspname not in ('pg_catalog', 'information_schema')
      and not exists (select 1 from unnest(coalesce(p.proconfig, '{}')) c where c like 'search_path=%');`)
  verificacoes.push({
    nome: 'security_definer_com_search_path',
    passou: definer.ok && definer.saida === '',
    detalhe: definer.ok ? (definer.saida ? `sem search_path: ${definer.saida}` : 'nenhuma função SECURITY DEFINER sem search_path') : definer.erro.slice(0, 300),
  })
  return verificacoes
}

function oraculoT1(projeto) {
  const protocolo = { porta: PORTA_DESCARTAVEL }
  protocolo.porta_livre_antes = !portaEmUso(PORTA_DESCARTAVEL)
  if (!protocolo.porta_livre_antes) {
    throw Object.assign(new Error(`a porta ${PORTA_DESCARTAVEL} já está em uso: o oráculo não sobe o banco`), { protocolo })
  }
  const pasta = criarPastaTemporaria('pg')
  const dados = path.join(pasta, 'dados')
  protocolo.pasta = pasta
  let iniciado = false
  try {
    const initdb = executar('initdb', ['-D', dados, '-U', 'teste', '-A', 'trust', '-E', 'UTF8', '--no-locale'])
    protocolo.initdb = initdb.codigo
    if (initdb.codigo !== 0) throw new Error(`initdb falhou: ${initdb.saida.slice(-500)}`)
    // O postgres filho herda os pipes do pg_ctl e o spawnSync ficaria à espera deles:
    // a saída vai só para o log. E o stop corre sempre que o start foi tentado.
    const log = path.join(pasta, 'log.txt')
    iniciado = true
    const inicio = executar('pg_ctl', ['-D', dados, '-o', `-p ${PORTA_DESCARTAVEL} -c listen_addresses=localhost`,
      '-l', log, '-w', 'start'], { stdio: 'ignore' })
    protocolo.start = inicio.codigo
    if (inicio.codigo !== 0) {
      throw new Error(`pg_ctl start falhou: ${fs.existsSync(log) ? fs.readFileSync(log, 'utf8').slice(-500) : 'sem log'}`)
    }
    protocolo.versao = psql('select version();').saida
    return { verificacoes: verificarT1(projeto), protocolo }
  } catch (erro) {
    throw Object.assign(erro instanceof Error ? erro : new Error(String(erro)), { protocolo })
  } finally {
    if (iniciado) protocolo.stop = executar('pg_ctl', ['-D', dados, 'stop', '-m', 'fast', '-w']).codigo
    protocolo.pasta_apagada = apagarPastaTemporaria(pasta)
    protocolo.porta_livre_depois = !portaEmUso(PORTA_DESCARTAVEL)
  }
}

// ---------- entrada ----------

function principal() {
  const [pastaDoProjeto, tarefa] = process.argv.slice(2)
  if (!pastaDoProjeto || !['T1', 'T2', 'T3'].includes(tarefa)) {
    console.error('uso: node prova/oraculos/correr.mjs <pasta-do-projeto> <T1|T2|T3>')
    process.exit(2)
  }
  const projeto = path.resolve(pastaDoProjeto)
  const inicio = Date.now()
  const resultado = { tarefa, projeto, passou: false, verificacoes: [] }
  try {
    if (!fs.existsSync(path.join(projeto, 'package.json'))) throw new Error(`não é o projeto de teste: ${projeto}`)
    if (tarefa === 'T1') Object.assign(resultado, oraculoT1(projeto))
    if (tarefa === 'T2') resultado.verificacoes = oraculoT2(projeto)
    if (tarefa === 'T3') resultado.verificacoes = oraculoT3(projeto)
    resultado.passou = resultado.verificacoes.length > 0 && resultado.verificacoes.every((verificacao) => verificacao.passou)
  } catch (erro) {
    resultado.erro = erro instanceof Error ? erro.message : String(erro)
    if (erro?.protocolo) resultado.protocolo = erro.protocolo
  }
  resultado.duracao_ms = Date.now() - inicio
  process.stdout.write(`${JSON.stringify(resultado, null, 2)}\n`)
  process.exit(resultado.erro ? 2 : resultado.passou ? 0 : 1)
}

principal()
