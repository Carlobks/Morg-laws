#!/usr/bin/env node
// Uma tentativa da Fase 4: cópia limpa do projeto de teste, a condição montada,
// uma corrida de `claude -p`, o .jsonl, o diff e o veredito do oráculo.
//
//   node prova/correr-tentativa.mjs --tarefa <T1|T2|T3|isolamento> --condicao <sem|com>
//        [--saida <pasta>] [--orcamento 0.5] [--manter-copia]
//
// «sem»: a cópia sem nada. «com»: a cópia mais o AGENTS.md, um CLAUDE.md com @AGENTS.md
// e as 10 skills em .claude/skills/, como as deixa o `npx skills add`.
// Os resultados ficam fora do repositório (têm caminhos da máquina): por omissão em
// ~/.morg-laws/fase-4/corridas/<id>/.

import { spawnSync } from 'node:child_process'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import {
  apagarPastaTemporaria,
  copiarProjetoSemDependencias,
  criarPastaTemporaria,
} from './ferramentas/pastas-descartaveis.mjs'
import { localizarTranscript, resumirTranscript } from './ferramentas/ler-transcript.mjs'

const PASTA_DA_PROVA = path.dirname(fileURLToPath(import.meta.url))
const RAIZ_DO_REPOSITORIO = path.resolve(PASTA_DA_PROVA, '..')
const PROJETO_ORIGINAL = path.join(PASTA_DA_PROVA, 'projeto-teste')
const PEDIDO_DE_ISOLAMENTO = 'Responda só OK.'
const ARQUIVOS_DE_REGRAS_PROCURADOS = ['CLAUDE.md', 'CLAUDE.local.md', 'AGENTS.md', '.claude', '.mcp.json']

// Variáveis que a app desktop e a sessão que lança a corrida injetam no ambiente.
// Mudam o comportamento do filho (esforço, socket da app, sessão-mãe), por isso saem.
const VARIAVEL_DA_SESSAO_MAE = /^(CLAUDE|CLAUDECODE$|MCP_)/

function lerArgumentos(argv) {
  const opcoes = { orcamento: '0.5', manterCopia: false }
  for (let i = 0; i < argv.length; i++) {
    const nome = argv[i]
    if (nome === '--tarefa') opcoes.tarefa = argv[++i]
    else if (nome === '--condicao') opcoes.condicao = argv[++i]
    else if (nome === '--saida') opcoes.saida = argv[++i]
    else if (nome === '--orcamento') opcoes.orcamento = argv[++i]
    else if (nome === '--manter-copia') opcoes.manterCopia = true
    else throw new Error(`opção desconhecida: ${nome}`)
  }
  if (!['T1', 'T2', 'T3', 'isolamento'].includes(opcoes.tarefa)) throw new Error('--tarefa tem de ser T1, T2, T3 ou isolamento')
  if (!['sem', 'com'].includes(opcoes.condicao)) throw new Error('--condicao tem de ser sem ou com')
  return opcoes
}

function executar(programa, argumentos, opcoes = {}) {
  const execucao = spawnSync(programa, argumentos, { encoding: 'utf8', timeout: 300_000, ...opcoes })
  if (execucao.error) throw execucao.error
  return { codigo: execucao.status, saida: `${execucao.stdout ?? ''}${execucao.stderr ?? ''}`.trim() }
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

function ambienteLimpo() {
  const ambiente = { ...process.env }
  const removidas = Object.keys(ambiente).filter((nome) => VARIAVEL_DA_SESSAO_MAE.test(nome)).sort()
  for (const nome of removidas) delete ambiente[nome]
  return { ambiente, removidas }
}

function resumirSessao(arquivoJsonl) {
  const eventos = fs.readFileSync(arquivoJsonl, 'utf8').split(/\r?\n/).filter(Boolean).map((linha) => {
    try {
      return JSON.parse(linha)
    } catch {
      return { type: 'linha_invalida', texto: linha.slice(0, 200) }
    }
  })
  const init = eventos.find((evento) => evento.type === 'system' && evento.subtype === 'init') ?? null
  const resultado = eventos.find((evento) => evento.type === 'result') ?? null
  const outrosDeSistema = eventos
    .filter((evento) => evento.type === 'system' && evento.subtype !== 'init')
    .map((evento) => evento.subtype ?? 'sem_subtipo')
  return {
    init_bruto: init,
    init: init && {
      modelo: init.model,
      cwd: init.cwd,
      modo_de_permissao: init.permissionMode,
      versao: init.claude_code_version,
      estilo_de_saida: init.output_style,
      fonte_da_chave: init.apiKeySource,
      skills: init.skills ?? null,
      plugins: init.plugins ?? null,
      servidores_mcp: init.mcp_servers ?? null,
      slash_commands: init.slash_commands ?? null,
      agentes: init.agents ?? null,
      ferramentas: init.tools ?? null,
      campos: Object.keys(init),
    },
    resultado: resultado && {
      subtipo: resultado.subtype,
      erro: resultado.is_error,
      texto: typeof resultado.result === 'string' ? resultado.result.slice(0, 500) : null,
      custo_usd: resultado.total_cost_usd,
      duracao_ms: resultado.duration_ms,
      turnos: resultado.num_turns,
      uso: resultado.usage,
      uso_por_modelo: resultado.modelUsage,
    },
    outros_eventos_de_sistema: outrosDeSistema,
    total_de_eventos: eventos.length,
  }
}

function principal() {
  const opcoes = lerArgumentos(process.argv.slice(2))
  const carimbo = new Date().toISOString().replace(/[:.]/g, '-')
  const id = `${opcoes.tarefa}-${opcoes.condicao}-${carimbo}`
  const saida = path.resolve(opcoes.saida ?? path.join(os.homedir(), '.morg-laws', 'fase-4', 'corridas', id))
  fs.mkdirSync(saida, { recursive: true })

  const pasta = criarPastaTemporaria('tentativa')
  const copia = path.join(pasta, 'projeto')
  const meta = { id, tarefa: opcoes.tarefa, condicao: opcoes.condicao, inicio: new Date().toISOString() }
  try {
    copiarProjetoSemDependencias(PROJETO_ORIGINAL, copia)
    const instalacao = executar('npm', ['ci', '--no-audit', '--no-fund', '--prefer-offline'], { cwd: copia, shell: true })
    if (instalacao.codigo !== 0) throw new Error(`npm ci falhou: ${instalacao.saida.slice(-500)}`)
    meta.isolamento_da_pasta = conferirQueEstaForaDeRepositorios(copia)
    if (meta.isolamento_da_pasta.dentro_de_repositorio_git || meta.isolamento_da_pasta.regras_nas_pastas_acima.length) {
      throw new Error(`a cópia herdaria regras de fora: ${JSON.stringify(meta.isolamento_da_pasta)}`)
    }
    if (opcoes.condicao === 'com') meta.skills_montadas = montarCondicaoCom(copia)

    const antes = path.join(pasta, 'antes')
    copiarProjetoSemDependencias(copia, antes)

    const pedido = opcoes.tarefa === 'isolamento'
      ? PEDIDO_DE_ISOLAMENTO
      : fs.readFileSync(path.join(PASTA_DA_PROVA, 'tarefas', `${opcoes.tarefa}.md`), 'utf8')
    const argumentos = ['-p', pedido, '--model', 'sonnet', '--output-format', 'stream-json', '--verbose',
      '--setting-sources', 'project', '--strict-mcp-config', '--max-budget-usd', opcoes.orcamento]
    const { ambiente, removidas } = ambienteLimpo()
    meta.comando = ['claude', ...argumentos.map((argumento) => (argumento === pedido ? '<pedido>' : argumento))].join(' ')
    meta.pedido = pedido
    meta.variaveis_removidas_do_ambiente = removidas

    const arquivoJsonl = path.join(saida, 'sessao.jsonl')
    const jsonl = fs.openSync(arquivoJsonl, 'w')
    const erros = fs.openSync(path.join(saida, 'stderr.txt'), 'w')
    const inicioDaCorrida = Date.now()
    const corrida = spawnSync('claude', argumentos, {
      cwd: copia,
      env: ambiente,
      stdio: ['ignore', jsonl, erros],
      timeout: 45 * 60_000,
    })
    fs.closeSync(jsonl)
    fs.closeSync(erros)
    meta.claude = { codigo: corrida.status, erro: corrida.error?.message ?? null, duracao_ms: Date.now() - inicioDaCorrida }

    const depois = path.join(pasta, 'depois')
    copiarProjetoSemDependencias(copia, depois)
    const diff = executar('git', ['diff', '--no-index', '--no-color', 'antes', 'depois'], { cwd: pasta })
    fs.writeFileSync(path.join(saida, 'diff.patch'), diff.saida ? `${diff.saida}\n` : '')
    meta.diff_vazio = diff.codigo === 0

    if (opcoes.tarefa !== 'isolamento') {
      const oraculo = spawnSync(process.execPath, [path.join(PASTA_DA_PROVA, 'oraculos', 'correr.mjs'), copia, opcoes.tarefa], {
        encoding: 'utf8',
        timeout: 600_000,
      })
      fs.writeFileSync(path.join(saida, 'oraculo.json'), oraculo.stdout)
      meta.oraculo_passou = JSON.parse(oraculo.stdout).passou
    }

    const { init_bruto: initBruto, ...resumo } = resumirSessao(arquivoJsonl)
    meta.resumo = resumo
    // O transcript guarda o contexto que o modelo recebeu: hooks, memória e skills vistas.
    const transcript = localizarTranscript(initBruto)
    if (transcript) {
      fs.copyFileSync(transcript, path.join(saida, 'transcript.jsonl'))
      meta.transcript = { origem: transcript, ...resumirTranscript(transcript) }
    }
    meta.memoria_automatica = initBruto?.memory_paths ?? null
  } catch (erro) {
    meta.erro = erro instanceof Error ? erro.message : String(erro)
  } finally {
    meta.fim = new Date().toISOString()
    if (opcoes.manterCopia) meta.copia_mantida = copia
    else meta.pasta_temporaria_apagada = apagarPastaTemporaria(pasta)
    fs.writeFileSync(path.join(saida, 'meta.json'), `${JSON.stringify(meta, null, 2)}\n`)
  }
  console.log(JSON.stringify({ id, saida, erro: meta.erro ?? null, oraculo_passou: meta.oraculo_passou ?? null,
    custo_usd: meta.resumo?.resultado?.custo_usd ?? null }, null, 2))
  process.exit(meta.erro ? 2 : 0)
}

principal()
