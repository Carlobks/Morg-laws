// A política de permissões das tentativas da Fase 4: igual nas duas condições.
// Só passa o que está na lista; o modo dontAsk recusa tudo o resto sem perguntar.
//
// Sintaxe confirmada em code.claude.com/docs/en/permissions (Claude Code 2.1.311):
// - `./caminho` é relativo à pasta atual (a cópia); os padrões seguem o gitignore.
// - As escritas (Edit, Write) são julgadas pelas regras `Edit(...)`; `Write(caminho)` nunca casa.
// - `Bash(npm test *)` também casa com `npm test` sem argumentos; num comando composto
//   (`&&`, `;`, `|`…) cada parte tem de estar permitida.
// - Uma negação vence sempre uma permissão; um nome de ferramenta sozinho a tira do contexto.
//
// Também aqui: a versão e o modelo fixos, e a vigilância do PostgreSQL e dos processos da corrida.

import { execFile, spawnSync } from 'node:child_process'
import net from 'node:net'
import { promisify } from 'node:util'

export const VERSAO_FIXA_DO_CLAUDE_CODE = '2.1.311'
// O ID completo, não o apelido `sonnet`: um apelido pode passar a outro modelo entre corridas.
export const MODELO_FIXO = 'claude-sonnet-5-5'
export const MODO_DE_PERMISSAO = 'dontAsk'

// Read, Glob e Grep dentro da cópia não pedem licença; fora dela, o dontAsk recusa.
// Não entram como nome sozinho: `Grep` ou `Glob` sem caminho permitiriam procurar em qualquer pasta
// (a primeira prova da política achou assim os arquivos de ../antes).
export const REGRAS_PERMITIDAS = [
  { regra: 'Read(./**)', motivo: 'ler o projeto (as regras de Read valem também para o Glob e o Grep)' },
  { regra: 'Skill', motivo: 'abrir as skills (na condição «com»)' },
  { regra: 'Edit(./src/**)', motivo: 'o código e os testes das tarefas T2 e T3 (cobre o Write)' },
  { regra: 'Edit(./banco/migracoes/**)', motivo: 'a migração da tarefa T1 (cobre o Write)' },
  { regra: 'Bash(npm test *)', motivo: 'correr os testes' },
  { regra: 'Bash(npm run tipos *)', motivo: 'conferir os tipos' },
  { regra: 'Bash(npx vitest run *)', motivo: 'correr um arquivo de teste' },
  // A cópia é um repositório local, sem remoto: as regras da condição «com» mandam commitar,
  // e recusar o git pesaria só nesse braço (B5 da auditoria 4.3).
  { regra: 'Bash(git status *)', motivo: 'git local: ver o estado' },
  { regra: 'Bash(git diff *)', motivo: 'git local: ver o diff' },
  { regra: 'Bash(git add *)', motivo: 'git local: preparar o commit' },
  { regra: 'Bash(git commit *)', motivo: 'git local: commitar' },
  { regra: 'Bash(git log *)', motivo: 'git local: ver o histórico' },
]

export const REGRAS_NEGADAS = [
  { regra: 'WebFetch', motivo: 'sem rede: a solução não pode vir de fora, e o custo e o tempo ficam comparáveis' },
  { regra: 'WebSearch', motivo: 'sem rede, pelo mesmo motivo' },
  { regra: 'PowerShell', motivo: 'um segundo shell sem as regras de Bash; os comandos ficam só em Bash' },
  { regra: 'Agent', motivo: 'sem subagentes: o trabalho e o custo ficam na sessão medida' },
  { regra: 'Task', motivo: 'nome antigo da ferramenta de subagentes' },
  { regra: 'Workflow', motivo: 'orquestra subagentes' },
  { regra: 'Edit(./package.json)', motivo: 'o npm test executa o script que estiver lá: mudar o script mudaria o que «npm test» corre' },
  { regra: 'Edit(./package-lock.json)', motivo: 'as dependências ficam fixas' },
  { regra: 'Edit(./vitest.config.*)', motivo: 'a configuração escolhe que testes correm durante a tentativa' },
  { regra: 'Edit(./tsconfig.json)', motivo: 'a configuração do npm run tipos' },
  { regra: 'Edit(./node_modules/**)', motivo: 'o npm test da tentativa corre com estas dependências; o oráculo instala as suas, limpas' },
  { regra: 'Edit(./.git/**)', motivo: 'os hooks e a configuração do repositório da cópia' },
  { regra: 'Bash(git push *)', motivo: 'a cópia não tem remoto, e nada sai da máquina' },
  { regra: 'Bash(git remote *)', motivo: 'sem remoto' },
  { regra: 'Bash(git config *)', motivo: 'a identidade e os hooks do repositório da cópia ficam fixos' },
  { regra: 'Bash(git diff *--output*)', motivo: '--output escreve o diff num arquivo, também fora da cópia' },
  { regra: 'Bash(git log *--output*)', motivo: '--output escreve num arquivo, também fora da cópia' },
]

export function argumentosDaPolitica() {
  return [
    '--permission-mode', MODO_DE_PERMISSAO,
    '--allowedTools', ...REGRAS_PERMITIDAS.map(({ regra }) => regra),
    '--disallowedTools', ...REGRAS_NEGADAS.map(({ regra }) => regra),
  ]
}

// O runner lança o claude sem shell, e sem shell o Windows só acha um .exe: um claude.cmd (o atalho
// que um `npm i -g` pode deixar no PATH) não serve. Por isso procura-se o .exe e diz-se porque falha.
export function localizarClaude() {
  const onde = spawnSync('where.exe', ['claude'], { encoding: 'utf8' })
  const caminhos = (onde.stdout ?? '').split(/\r?\n/).map((linha) => linha.trim()).filter(Boolean)
  const executavel = caminhos.find((caminho) => caminho.toLowerCase().endsWith('.exe'))
  if (!executavel) {
    throw new Error(`não achei um claude.exe no PATH (achei: ${caminhos.join(', ') || 'nada'}). Instale o Claude Code nativo, que deixa um claude.exe.`)
  }
  return executavel
}

export function lerVersaoDoClaudeCode(executavel) {
  const execucao = spawnSync(executavel, ['--version'], { encoding: 'utf8', timeout: 60_000 })
  return /^(\d+\.\d+\.\d+)/.exec((execucao.stdout ?? '').trim())?.[1] ?? null
}

// ---------- vigilância: portas do Postgres e serviços postgresql* (antes e depois) ----------
// As portas são sondadas com uma ligação TCP, e não lidas no netstat: a partir do shell
// em que as corridas são lançadas, o netstat e o Get-NetTCPConnection mostram só algumas
// escutas (nem a do serviço do Windows na 5432, que aceita ligações).

const PORTAS_VIGIADAS = [5432, 5433, 5434, 5435, 5436, 5437, 5438, 5439, 55432]

export function aceitaLigacao(porta, host) {
  return new Promise((resolver) => {
    const socket = net.connect({ port: porta, host, timeout: 1500 })
    socket.once('connect', () => { socket.destroy(); resolver(true) })
    socket.once('timeout', () => { socket.destroy(); resolver(false) })
    socket.once('error', () => resolver(false))
  })
}

async function portasQueAceitam() {
  const abertas = []
  for (const porta of PORTAS_VIGIADAS) {
    for (const host of ['127.0.0.1', '::1']) if (await aceitaLigacao(porta, host)) abertas.push(`${host === '::1' ? '[::1]' : host}:${porta}`)
  }
  return abertas
}

function servicosDoPostgres() {
  const execucao = spawnSync(
    'powershell.exe',
    ['-NoProfile', '-NonInteractive', '-Command',
      "Get-Service -Name 'postgresql*' -ErrorAction SilentlyContinue | ForEach-Object { $_.Name + '=' + $_.Status }"],
    { encoding: 'utf8', timeout: 60_000 },
  )
  return (execucao.stdout ?? '').split(/\r?\n/).map((linha) => linha.trim()).filter(Boolean).sort()
}

export async function fotografarPostgres() {
  return { momento: new Date().toISOString(), portas_que_aceitam: await portasQueAceitam(), servicos: servicosDoPostgres() }
}

export function compararFotografias(antes, depois) {
  const mudou = (a, b) => JSON.stringify(a) !== JSON.stringify(b)
  const diferencas = []
  if (mudou(antes.portas_que_aceitam, depois.portas_que_aceitam)) {
    diferencas.push(`portas: ${antes.portas_que_aceitam.join(', ') || 'nenhuma'} → ${depois.portas_que_aceitam.join(', ') || 'nenhuma'}`)
  }
  if (mudou(antes.servicos, depois.servicos)) diferencas.push(`serviços: ${antes.servicos.join(', ')} → ${depois.servicos.join(', ')}`)
  return diferencas
}

// ---------- vigilância durante a corrida: processos dos descendentes do claude e portas ----------
// O código do agente sai da política pelo `npm test` (B4 da auditoria 4.3). Sem sandbox, isto
// pelo menos vê um postgres, initdb, pg_ctl ou psql novo, e uma porta do Postgres que passe a
// aceitar ligações. Uma escuta noutra porta qualquer não é visível daqui (ver acima).

const executarAssincrono = promisify(execFile)
const PROGRAMAS_VIGIADOS = new Set(['postgres.exe', 'initdb.exe', 'pg_ctl.exe', 'psql.exe'])

async function listarProcessos() {
  const { stdout } = await executarAssincrono('powershell.exe', ['-NoProfile', '-NonInteractive', '-Command',
    'Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,Name | ConvertTo-Json -Compress'],
  { maxBuffer: 32 * 1024 * 1024, timeout: 30_000 })
  return JSON.parse(stdout).map((processo) => ({ pid: processo.ProcessId, pai: processo.ParentProcessId, nome: String(processo.Name).toLowerCase() }))
}

export async function iniciarVigilancia(intervaloMs = 5000) {
  const linhaDeBase = await listarProcessos()
  const portasDaBase = new Set(await portasQueAceitam())
  const pidsDaBase = new Set(linhaDeBase.map(({ pid }) => pid))
  const postgresDaBase = new Set(linhaDeBase.filter(({ nome }) => nome === 'postgres.exe').map(({ pid }) => pid))
  const descendentes = new Set()
  const ocorrencias = []
  let raiz = null
  let amostras = 0
  let falhasDeAmostra = 0
  let emCurso = Promise.resolve()

  const amostrar = async () => {
    try {
      const [processos, portas] = await Promise.all([listarProcessos(), portasQueAceitam()])
      amostras++
      if (raiz) {
        // Os descendentes acumulam: um pai que já morreu continua a contar para os filhos.
        let cresceu = true
        while (cresceu) {
          cresceu = false
          for (const { pid, pai } of processos) {
            if ((pai === raiz || descendentes.has(pai)) && !descendentes.has(pid)) {
              descendentes.add(pid)
              cresceu = true
            }
          }
        }
      }
      for (const processo of processos) {
        const novo = !pidsDaBase.has(processo.pid)
        // Um postgres filho do serviço do Windows é uma ligação ao serviço, não um servidor novo.
        if (novo && PROGRAMAS_VIGIADOS.has(processo.nome) && !postgresDaBase.has(processo.pai)) {
          const origem = descendentes.has(processo.pid) ? 'da corrida' : 'de fora da corrida'
          ocorrencias.push(`processo ${processo.nome} pid=${processo.pid} pai=${processo.pai} (${origem})`)
        }
      }
      for (const porta of portas) if (!portasDaBase.has(porta)) ocorrencias.push(`a porta ${porta} passou a aceitar ligações`)
      for (const porta of portasDaBase) if (!portas.includes(porta)) ocorrencias.push(`a porta ${porta} deixou de aceitar ligações`)
    } catch {
      falhasDeAmostra++
    }
  }
  const relogio = setInterval(() => { emCurso = emCurso.then(amostrar) }, intervaloMs)
  return {
    definirRaiz(pid) { raiz = pid },
    async parar() {
      clearInterval(relogio)
      await emCurso
      await amostrar()
      return {
        intervalo_ms: intervaloMs,
        amostras,
        falhas_de_amostra: falhasDeAmostra,
        descendentes: descendentes.size,
        portas_da_base: [...portasDaBase],
        ocorrencias: [...new Set(ocorrencias)],
      }
    },
  }
}
