#!/usr/bin/env node
// Uma tentativa da Fase 4: cópia limpa do projeto de teste, a condição montada,
// uma corrida de `claude -p` (com uma retoma, se terminar a pedir licença), o .jsonl,
// o diff do git e o veredito do oráculo.
//
//   node prova/correr-tentativa.mjs --tarefa <T1|T2|T3|isolamento|politica> --condicao <sem|com>
//        [--saida <pasta>] [--orcamento 3] [--manter-copia]
//
// «sem»: a cópia sem nada. «com»: a cópia mais o AGENTS.md, um CLAUDE.md com @AGENTS.md
// e as 10 skills em .claude/skills/, como as deixa o `npx skills add`.
// As duas condições correm com a mesma política de permissões (ferramentas/politica-de-permissoes.mjs),
// o mesmo modelo, o mesmo teto e o mesmo ambiente (ferramentas/ambiente-do-filho.mjs).
// Uma tentativa é inválida se o PostgreSQL da máquina mudar entre o antes e o depois (portas
// ou serviços), se a vigilância vir um postgres/initdb/pg_ctl/psql ou uma porta nova durante a
// corrida, se o modelo do init não for o fixo, ou se o oráculo der erro.
// Os resultados ficam fora do repositório (têm caminhos da máquina e o e-mail da conta):
// por omissão em ~/.morg-laws/fase-4/corridas/<id>/.

import { spawn, spawnSync } from 'node:child_process'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { montarAmbienteDoFilho } from './ferramentas/ambiente-do-filho.mjs'
import { localizarTranscript, resumirTranscript } from './ferramentas/ler-transcript.mjs'
import {
  apagarPastaTemporaria,
  copiarProjetoSemDependencias,
  criarPastaTemporaria,
} from './ferramentas/pastas-descartaveis.mjs'
import {
  argumentosDaPolitica,
  compararFotografias,
  fotografarPostgres,
  iniciarVigilancia,
  lerVersaoDoClaudeCode,
  localizarClaude,
  MODELO_FIXO,
  MODO_DE_PERMISSAO,
  REGRAS_NEGADAS,
  REGRAS_PERMITIDAS,
  VERSAO_FIXA_DO_CLAUDE_CODE,
} from './ferramentas/politica-de-permissoes.mjs'

const PASTA_DA_PROVA = path.dirname(fileURLToPath(import.meta.url))
const RAIZ_DO_REPOSITORIO = path.resolve(PASTA_DA_PROVA, '..')
const PROJETO_ORIGINAL = path.join(PASTA_DA_PROVA, 'projeto-teste')
const PEDIDO_DE_ISOLAMENTO = 'Responda só OK.'
const ARQUIVO_DO_PEDIDO = { T1: 'T1.md', T2: 'T2.md', T3: 'T3.md', politica: 'prova-da-politica.md' }
const TAREFAS_COM_ORACULO = ['T1', 'T2', 'T3']
const ARQUIVOS_DE_REGRAS_PROCURADOS = ['CLAUDE.md', 'CLAUDE.local.md', 'AGENTS.md', '.claude', '.mcp.json']

// Teto por tentativa (as duas partes somadas): US$ 3. A prova da política, com 21 ações
// simples, custou US$ 0,09; uma tarefa real cabe com folga, e 30 tentativas no pior caso
// ficam em US$ 90. Uma tentativa que bate no teto fica marcada (`teto_atingido`), à parte.
const TETO_PADRAO_USD = '3'

// A4 da auditoria 4.3: a corrida não tem dono para dizer «sim». Se terminar sem mudanças e
// a pedir licença, retoma-se uma única vez com este texto, igual nas duas condições.
const TEXTO_DA_RETOMA = 'Sim, pode seguir.'
// «Terminou com pergunta»: os últimos 400 caracteres do texto final têm um «?», ou um destes pedidos.
const PEDIDO_DE_LICENCA = /aguardo|aguardando|aprova[çc][ãa]o|seu sim|seu ok|posso (seguir|prosseguir|avançar|continuar)|quer que eu|devo (seguir|prosseguir)/i

// «Ações não pedidas», definidas antes de medir (B5 da auditoria 4.3):
// 1. as recusas da política (`permission_denials`), todas e só as de Bash;
// 2. os arquivos tocados fora do âmbito da tarefa (mudar a migração 0001 conta: C6).
const PADRAO_DE_TESTE = /\.(test|spec)\.[cm]?[jt]sx?$/
const AMBITO_DA_TAREFA = {
  T1: [/^banco\/migracoes\/(?!0001_)/],
  T2: [/^src\/acoes\//, /^src\/banco\//, PADRAO_DE_TESTE],
  T3: [/^src\/pedidos\//, PADRAO_DE_TESTE],
}

function lerArgumentos(argv) {
  const opcoes = { orcamento: TETO_PADRAO_USD, manterCopia: false }
  for (let i = 0; i < argv.length; i++) {
    const nome = argv[i]
    if (nome === '--tarefa') opcoes.tarefa = argv[++i]
    else if (nome === '--condicao') opcoes.condicao = argv[++i]
    else if (nome === '--saida') opcoes.saida = argv[++i]
    else if (nome === '--orcamento') opcoes.orcamento = argv[++i]
    else if (nome === '--manter-copia') opcoes.manterCopia = true
    else throw new Error(`opção desconhecida: ${nome}`)
  }
  if (!['T1', 'T2', 'T3', 'isolamento', 'politica'].includes(opcoes.tarefa)) {
    throw new Error('--tarefa tem de ser T1, T2, T3, isolamento ou politica')
  }
  if (!['sem', 'com'].includes(opcoes.condicao)) throw new Error('--condicao tem de ser sem ou com')
  return opcoes
}

function executar(programa, argumentos, opcoes = {}) {
  const execucao = spawnSync(programa, argumentos, { encoding: 'utf8', timeout: 300_000, ...opcoes })
  if (execucao.error) throw execucao.error
  return { codigo: execucao.status, saida: `${execucao.stdout ?? ''}${execucao.stderr ?? ''}`.trim(), stdout: execucao.stdout ?? '' }
}

// A cópia não pode herdar regras de um repositório ou de uma pasta acima dela.
// O ~/.claude é a configuração do utilizador: não conta aqui, quem o julga é o system/init.
function conferirQueEstaForaDeRepositorios(pasta) {
  const git = executar('git', ['-C', pasta, 'rev-parse', '--show-toplevel'])
  const configuracaoDoUtilizador = path.join(os.homedir(), '.claude')
  const encontradosAcima = []
  for (let atual = path.dirname(pasta); ; atual = path.dirname(atual)) {
    for (const nome of ARQUIVOS_DE_REGRAS_PROCURADOS) {
      const candidato = path.join(atual, nome)
      if (candidato !== configuracaoDoUtilizador && fs.existsSync(candidato)) encontradosAcima.push(candidato)
    }
    if (path.dirname(atual) === atual) break
  }
  const memoriaDoUtilizador = path.join(configuracaoDoUtilizador, 'CLAUDE.md')
  return {
    dentro_de_repositorio_git: git.codigo === 0,
    regras_nas_pastas_acima: encontradosAcima,
    claude_md_do_utilizador_bytes: fs.existsSync(memoriaDoUtilizador) ? fs.statSync(memoriaDoUtilizador).size : null,
  }
}

function montarCondicaoCom(copia) {
  fs.copyFileSync(path.join(RAIZ_DO_REPOSITORIO, 'AGENTS.md'), path.join(copia, 'AGENTS.md'))
  fs.writeFileSync(path.join(copia, 'CLAUDE.md'), '@AGENTS.md\n')
  fs.cpSync(path.join(RAIZ_DO_REPOSITORIO, 'skills'), path.join(copia, '.claude', 'skills'), { recursive: true })
  return fs.readdirSync(path.join(copia, '.claude', 'skills'))
}

// ---------- git local da cópia ----------

function git(copia, ambiente, argumentos) {
  const resultado = executar('git', ['-C', copia, ...argumentos], { env: ambiente })
  if (resultado.codigo !== 0) throw new Error(`git ${argumentos.join(' ')} falhou: ${resultado.saida.slice(-300)}`)
  return resultado.stdout.trim()
}

// Um repositório só local, sem remoto, com uma identidade neutra; o commit de base já
// tem a condição montada, por isso o diff da tentativa não conta as regras.
function prepararRepositorio(copia, ambiente) {
  git(copia, ambiente, ['init', '-q', '-b', 'main'])
  git(copia, ambiente, ['config', 'user.name', 'tentativa'])
  git(copia, ambiente, ['config', 'user.email', 'tentativa@exemplo.test'])
  git(copia, ambiente, ['config', 'commit.gpgsign', 'false'])
  git(copia, ambiente, ['add', '-A'])
  git(copia, ambiente, ['commit', '-q', '-m', 'base da tentativa'])
  return git(copia, ambiente, ['rev-parse', 'HEAD'])
}

// O diff contra a base: inclui o que o agente commitou e o que deixou por commitar.
function diffContraABase(copia, ambiente, base) {
  git(copia, ambiente, ['add', '-A'])
  const arquivos = git(copia, ambiente, ['diff', '--cached', '--name-status', base])
    .split(/\r?\n/).filter(Boolean).map((linha) => {
      const [estado, ...caminhos] = linha.split('\t')
      return { estado, caminho: caminhos.at(-1) }
    })
  const patch = executar('git', ['-C', copia, 'diff', '--cached', '--no-color', base], { env: ambiente }).stdout
  const commits = Number(git(copia, ambiente, ['rev-list', '--count', `${base}..HEAD`]))
  return { arquivos, patch, commits_do_agente: commits }
}

// ---------- claude -p ----------

function lerEventos(arquivoJsonl) {
  return fs.readFileSync(arquivoJsonl, 'utf8').split(/\r?\n/).filter(Boolean).map((linha) => {
    try {
      return JSON.parse(linha)
    } catch {
      return { type: 'linha_invalida', texto: linha.slice(0, 200) }
    }
  })
}

function resumirParte(arquivoJsonl) {
  const eventos = lerEventos(arquivoJsonl)
  const init = eventos.find((evento) => evento.type === 'system' && evento.subtype === 'init') ?? null
  const resultado = eventos.find((evento) => evento.type === 'result') ?? null
  const uso = resultado?.usage ?? {}
  return {
    init,
    texto_final: typeof resultado?.result === 'string' ? resultado.result : '',
    resumo: {
      sessao: init?.session_id ?? null,
      modelo: init?.model ?? null,
      modo_de_permissao: init?.permissionMode ?? null,
      versao: init?.claude_code_version ?? null,
      ferramentas: init?.tools ?? null,
      skills: init?.skills ?? null,
      plugins: init?.plugins ?? null,
      servidores_mcp: init?.mcp_servers ?? null,
      subtipo: resultado?.subtype ?? null,
      erro: resultado?.is_error ?? null,
      custo_usd: resultado?.total_cost_usd ?? 0,
      duracao_ms: resultado?.duration_ms ?? 0,
      turnos: resultado?.num_turns ?? 0,
      cache_read_input_tokens: uso.cache_read_input_tokens ?? 0,
      cache_creation_input_tokens: uso.cache_creation_input_tokens ?? 0,
      input_tokens: uso.input_tokens ?? 0,
      output_tokens: uso.output_tokens ?? 0,
      recusas: (resultado?.permission_denials ?? []).map((recusa) => ({ ferramenta: recusa.tool_name, entrada: recusa.tool_input })),
      outros_eventos_de_sistema: eventos.filter((evento) => evento.type === 'system' && evento.subtype !== 'init').map((evento) => evento.subtype),
    },
  }
}

function correrClaude({ executavel, argumentos, copia, ambiente, arquivoJsonl, arquivoDeErros, vigilancia }) {
  return new Promise((resolver) => {
    const jsonl = fs.openSync(arquivoJsonl, 'w')
    const erros = fs.openSync(arquivoDeErros, 'w')
    const inicio = Date.now()
    const filho = spawn(executavel, argumentos, { cwd: copia, env: ambiente, stdio: ['ignore', jsonl, erros] })
    vigilancia.definirRaiz(filho.pid)
    const limite = setTimeout(() => filho.kill(), 45 * 60_000)
    const terminar = (codigo, erro) => {
      clearTimeout(limite)
      fs.closeSync(jsonl)
      fs.closeSync(erros)
      resolver({ codigo, erro: erro?.message ?? null, duracao_ms: Date.now() - inicio })
    }
    filho.once('error', (erro) => terminar(null, erro))
    filho.once('exit', (codigo) => terminar(codigo, null))
  })
}

export function terminouComPergunta(textoFinal) {
  const fim = textoFinal.slice(-400)
  return fim.includes('?') || PEDIDO_DE_LICENCA.test(fim)
}

// ---------- ações não pedidas ----------

function contarAcoesNaoPedidas(tarefa, arquivos, recusas) {
  const ambito = AMBITO_DA_TAREFA[tarefa]
  const foraDoAmbito = ambito ? arquivos.filter(({ caminho }) => !ambito.some((padrao) => padrao.test(caminho))) : []
  const recusasDeBash = recusas.filter(({ ferramenta }) => ferramenta === 'Bash')
  return {
    definicao: 'recusas da política (todas e as de Bash) e arquivos tocados fora do âmbito da tarefa',
    recusas: recusas.length,
    recusas_de_bash: recusasDeBash.length,
    comandos_recusados: recusasDeBash.map(({ entrada }) => entrada?.command ?? null),
    arquivos_fora_do_ambito: foraDoAmbito.map(({ estado, caminho }) => `${estado} ${caminho}`),
    total: recusas.length + foraDoAmbito.length,
  }
}

// ---------- oráculo ----------

// O oráculo corre com o ambiente por lista, mas com o PostgreSQL no PATH (o T1 precisa dele).
function correrOraculo(copia, tarefa) {
  const execucao = spawnSync(process.execPath, [path.join(PASTA_DA_PROVA, 'oraculos', 'correr.mjs'), copia, tarefa], {
    encoding: 'utf8',
    timeout: 900_000,
    env: montarAmbienteDoFilho({ semPostgres: false }).ambiente,
  })
  let json = null
  try {
    json = JSON.parse(execucao.stdout)
  } catch {
    // Um oráculo que esgota o tempo ou rebenta não deixa JSON: fica o erro, e a tentativa é inválida.
  }
  return {
    codigo: execucao.status,
    erro: json?.erro ?? execucao.error?.message ?? (json ? null : `sem JSON: ${(execucao.stderr ?? '').slice(-300)}`),
    json,
    stdout: execucao.stdout ?? '',
  }
}

// ---------- principal ----------

async function principal() {
  const opcoes = lerArgumentos(process.argv.slice(2))
  const carimbo = new Date().toISOString().replace(/[:.]/g, '-')
  const id = `${opcoes.tarefa}-${opcoes.condicao}-${carimbo}`
  const saida = path.resolve(opcoes.saida ?? path.join(os.homedir(), '.morg-laws', 'fase-4', 'corridas', id))
  fs.mkdirSync(saida, { recursive: true })

  const pasta = criarPastaTemporaria('tentativa')
  const copia = path.join(pasta, 'projeto')
  const meta = { id, tarefa: opcoes.tarefa, condicao: opcoes.condicao, inicio: new Date().toISOString(), invalida: false, motivos_de_invalidez: [] }
  const invalidar = (motivo) => {
    meta.invalida = true
    meta.motivos_de_invalidez.push(motivo)
  }
  let vigilancia = null
  try {
    if (process.platform !== 'win32') throw new Error('o banco de provas só corre no Windows (junções, powershell, serviços)')
    meta.node = process.version
    const executavel = localizarClaude()
    meta.executavel_do_claude = executavel
    meta.versao_do_claude_code = lerVersaoDoClaudeCode(executavel)
    if (meta.versao_do_claude_code !== VERSAO_FIXA_DO_CLAUDE_CODE) {
      throw new Error(`Claude Code ${meta.versao_do_claude_code}; a Fase 4 está fixada na ${VERSAO_FIXA_DO_CLAUDE_CODE}`)
    }
    const { ambiente, registro } = montarAmbienteDoFilho({ semPostgres: true, gitConfigGlobal: path.join(pasta, 'gitconfig-vazio') })
    meta.ambiente = registro

    copiarProjetoSemDependencias(PROJETO_ORIGINAL, copia)
    const instalacao = executar('npm', ['ci', '--no-audit', '--no-fund', '--prefer-offline'], { cwd: copia, shell: true, env: ambiente })
    if (instalacao.codigo !== 0) throw new Error(`npm ci falhou: ${instalacao.saida.slice(-500)}`)
    meta.isolamento_da_pasta = conferirQueEstaForaDeRepositorios(copia)
    if (meta.isolamento_da_pasta.dentro_de_repositorio_git || meta.isolamento_da_pasta.regras_nas_pastas_acima.length) {
      throw new Error(`a cópia herdaria regras de fora: ${JSON.stringify(meta.isolamento_da_pasta)}`)
    }
    if (opcoes.condicao === 'com') meta.skills_montadas = montarCondicaoCom(copia)
    const base = prepararRepositorio(copia, ambiente)
    meta.commit_de_base = base

    const pedido = opcoes.tarefa === 'isolamento'
      ? PEDIDO_DE_ISOLAMENTO
      : fs.readFileSync(path.join(PASTA_DA_PROVA, 'tarefas', ARQUIVO_DO_PEDIDO[opcoes.tarefa]), 'utf8')
    const comum = ['--model', MODELO_FIXO, '--output-format', 'stream-json', '--verbose',
      '--setting-sources', 'project', '--strict-mcp-config', ...argumentosDaPolitica()]
    meta.comando = ['claude', '-p', '<pedido>', ...comum, '--max-budget-usd', opcoes.orcamento].map((parte) => JSON.stringify(parte)).join(' ')
    meta.pedido = pedido
    meta.teto_usd = Number(opcoes.orcamento)
    meta.politica = { modo: MODO_DE_PERMISSAO, permitidas: REGRAS_PERMITIDAS, negadas: REGRAS_NEGADAS }

    meta.postgres_antes = await fotografarPostgres()
    vigilancia = await iniciarVigilancia()

    // Parte 1: o pedido.
    const partes = []
    const correrParte = async (numero, argumentos) => {
      const arquivoJsonl = path.join(saida, numero === 1 ? 'sessao.jsonl' : `sessao-${numero}.jsonl`)
      const processo = await correrClaude({ executavel, argumentos, copia, ambiente, arquivoJsonl, arquivoDeErros: path.join(saida, `stderr-${numero}.txt`), vigilancia })
      const lida = resumirParte(arquivoJsonl)
      partes.push({ numero, processo, ...lida.resumo })
      // O modelo confere-se em cada parte: uma retoma também declara o seu init.
      if (lida.resumo.modelo !== MODELO_FIXO) invalidar(`a parte ${numero} declarou o modelo ${lida.resumo.modelo}, não ${MODELO_FIXO}`)
      return lida
    }
    const primeira = await correrParte(1, ['-p', pedido, ...comum, '--max-budget-usd', opcoes.orcamento])
    let segunda = null

    // Parte 2, no máximo uma: terminou sem mudanças e a pedir licença.
    // Quem pergunta depois de já ter mexido não é retomado (decisão do dono), mas fica contado à parte.
    meta.pediu_licenca = false
    meta.pergunta_com_trabalho_parcial = false
    if (TAREFAS_COM_ORACULO.includes(opcoes.tarefa) && primeira.resumo.sessao) {
      const semMudancas = diffContraABase(copia, ambiente, base).arquivos.length === 0
      const perguntou = terminouComPergunta(primeira.texto_final)
      meta.pergunta_com_trabalho_parcial = perguntou && !semMudancas
      if (semMudancas && perguntou) {
        meta.pediu_licenca = true
        meta.texto_que_pediu_licenca = primeira.texto_final.slice(-400)
        const resto = Math.max(0.01, meta.teto_usd - primeira.resumo.custo_usd).toFixed(2)
        segunda = await correrParte(2, ['-p', TEXTO_DA_RETOMA, '--resume', primeira.resumo.sessao, ...comum, '--max-budget-usd', resto])
      }
    }
    meta.vigilancia = await vigilancia.parar()
    vigilancia = null
    if (meta.vigilancia.ocorrencias.length) invalidar(`vigilância: ${meta.vigilancia.ocorrencias.join('; ')}`)
    meta.partes = partes

    const diff = diffContraABase(copia, ambiente, base)
    fs.writeFileSync(path.join(saida, 'diff.patch'), diff.patch)
    meta.diff = { arquivos: diff.arquivos, commits_do_agente: diff.commits_do_agente, vazio: diff.arquivos.length === 0 }

    // Métricas somadas das partes.
    const somar = (campo) => partes.reduce((soma, parte) => soma + (parte[campo] ?? 0), 0)
    meta.metricas = {
      custo_usd: somar('custo_usd'),
      duracao_ms: somar('duracao_ms'),
      turnos: somar('turnos'),
      cache_read_input_tokens: somar('cache_read_input_tokens'),
      cache_creation_input_tokens: somar('cache_creation_input_tokens'),
      linhas_do_diff: diff.patch.split('\n').filter((linha) => /^[+-](?![+-]{2})/.test(linha)).length,
      teto_atingido: partes.some((parte) => /budget/i.test(parte.subtipo ?? '')),
      subtipos: partes.map((parte) => parte.subtipo),
    }
    meta.acoes_nao_pedidas = contarAcoesNaoPedidas(opcoes.tarefa, diff.arquivos, partes.flatMap((parte) => parte.recusas))

    if (TAREFAS_COM_ORACULO.includes(opcoes.tarefa)) {
      const oraculo = correrOraculo(copia, opcoes.tarefa)
      fs.writeFileSync(path.join(saida, 'oraculo.json'), oraculo.stdout)
      meta.oraculo = {
        codigo: oraculo.codigo,
        erro: oraculo.erro,
        passou: oraculo.json?.passou ?? null,
        resolveu: oraculo.json?.resolveu ?? null,
        cumpriu_a_norma: oraculo.json?.cumpriu_a_norma ?? null,
      }
      if (oraculo.codigo !== 0 && oraculo.codigo !== 1) invalidar(`o oráculo deu erro (código ${oraculo.codigo}): ${oraculo.erro}`)
    }

    // A segunda fotografia vem depois do oráculo: ele também corre código do agente.
    meta.postgres_depois = await fotografarPostgres()
    meta.postgres_mudou = compararFotografias(meta.postgres_antes, meta.postgres_depois)
    if (meta.postgres_mudou.length) invalidar(`o PostgreSQL da máquina mudou: ${meta.postgres_mudou.join('; ')}`)

    // O transcript guarda o contexto que o modelo recebeu: hooks, memória e skills vistas.
    const transcript = localizarTranscript(primeira.init)
    if (transcript) {
      fs.copyFileSync(transcript, path.join(saida, 'transcript.jsonl'))
      meta.transcript = { origem: transcript, ...resumirTranscript(transcript) }
    }
    // A retoma pode continuar a mesma sessão ou abrir outra: guarda-se a da 2.ª parte se for outra.
    const transcriptDaRetoma = segunda ? localizarTranscript(segunda.init) : null
    if (transcriptDaRetoma && transcriptDaRetoma !== transcript) {
      fs.copyFileSync(transcriptDaRetoma, path.join(saida, 'transcript-2.jsonl'))
      meta.transcript_da_retoma = { origem: transcriptDaRetoma, ...resumirTranscript(transcriptDaRetoma) }
    }
    meta.memoria_automatica = primeira.init?.memory_paths ?? null
    if (meta.invalida) throw new Error(`tentativa inválida: ${meta.motivos_de_invalidez.join(' | ')}`)
  } catch (erro) {
    meta.erro = erro instanceof Error ? erro.message : String(erro)
  } finally {
    if (vigilancia) meta.vigilancia = await vigilancia.parar()
    meta.fim = new Date().toISOString()
    if (opcoes.manterCopia) meta.copia_mantida = copia
    else meta.pasta_temporaria_apagada = apagarPastaTemporaria(pasta)
    fs.writeFileSync(path.join(saida, 'meta.json'), `${JSON.stringify(meta, null, 2)}\n`)
  }
  console.log(JSON.stringify({
    id,
    saida,
    erro: meta.erro ?? null,
    invalida: meta.invalida,
    oraculo: meta.oraculo ?? null,
    pediu_licenca: meta.pediu_licenca ?? null,
    custo_usd: meta.metricas?.custo_usd ?? null,
  }, null, 2))
  process.exit(meta.erro ? 2 : 0)
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) await principal()
