// A política de permissões das tentativas da Fase 4: igual nas duas condições.
// Só passa o que está na lista; o modo dontAsk recusa tudo o resto sem perguntar.
//
// Sintaxe confirmada em code.claude.com/docs/en/permissions (Claude Code 2.1.311):
// - `./caminho` é relativo à pasta atual (a cópia); os padrões seguem o gitignore.
// - As escritas (Edit, Write) são julgadas pelas regras `Edit(...)`; `Write(caminho)` nunca casa.
// - `Bash(npm test *)` também casa com `npm test` sem argumentos; num comando composto
//   (`&&`, `;`, `|`…) cada parte tem de estar permitida.
// - Uma negação vence sempre uma permissão; um nome de ferramenta sozinho a tira do contexto.

import { spawnSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'

export const VERSAO_FIXA_DO_CLAUDE_CODE = '2.1.311'
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
  { regra: 'Edit(./vitest.config.*)', motivo: 'a configuração escolhe que testes correm; o oráculo do T3 corre os testes do projeto com ela' },
  { regra: 'Edit(./tsconfig.json)', motivo: 'a configuração do npm run tipos' },
  {
    regra: 'Edit(./node_modules/**)',
    motivo: 'o oráculo corre com o node_modules da tentativa (por junção na cópia dele): mudar uma dependência mudaria o veredito',
  },
]

export function argumentosDaPolitica() {
  return [
    '--permission-mode', MODO_DE_PERMISSAO,
    '--allowedTools', ...REGRAS_PERMITIDAS.map(({ regra }) => regra),
    '--disallowedTools', ...REGRAS_NEGADAS.map(({ regra }) => regra),
  ]
}

export function lerVersaoDoClaudeCode() {
  const execucao = spawnSync('claude', ['--version'], { encoding: 'utf8', timeout: 60_000 })
  return /^(\d+\.\d+\.\d+)/.exec((execucao.stdout ?? '').trim())?.[1] ?? null
}

// ---------- PATH sem PostgreSQL ----------

const PROGRAMAS_DO_POSTGRES = ['psql.exe', 'pg_ctl.exe', 'initdb.exe', 'psql', 'pg_ctl', 'initdb']

export function tirarPostgresDoPath(ambiente) {
  const chave = Object.keys(ambiente).find((nome) => nome.toUpperCase() === 'PATH') ?? 'PATH'
  const pastas = (ambiente[chave] ?? '').split(path.delimiter).filter(Boolean)
  const temPostgres = (pasta) => PROGRAMAS_DO_POSTGRES.some((programa) => fs.existsSync(path.join(pasta, programa)))
  const removidas = pastas.filter(temPostgres)
  ambiente[chave] = pastas.filter((pasta) => !temPostgres(pasta)).join(path.delimiter)
  return { chave, removidas, pastas_antes: pastas.length, pastas_depois: pastas.length - removidas.length }
}

// ---------- vigilância: portas do Postgres e serviços postgresql* ----------

const PORTAS_VIGIADAS = [5432, 55432]

function quemEscuta() {
  const netstat = spawnSync('netstat', ['-ano'], { encoding: 'utf8' })
  const escutas = []
  for (const linha of (netstat.stdout ?? '').split(/\r?\n/)) {
    const colunas = linha.trim().split(/\s+/)
    if (colunas.length < 4 || !/^TCP$/i.test(colunas[0])) continue
    const [, local, remoto] = colunas
    // Só as escutas (o endereço remoto é 0.0.0.0:0 ou [::]:0): ligações de passagem não contam.
    if (!/^(0\.0\.0\.0|\[::\]):0$/.test(remoto)) continue
    if (PORTAS_VIGIADAS.some((porta) => local.endsWith(`:${porta}`))) escutas.push(`${local} pid=${colunas.at(-1)}`)
  }
  return escutas.sort()
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

export function fotografarPostgres() {
  return { momento: new Date().toISOString(), escutas: quemEscuta(), servicos: servicosDoPostgres() }
}

export function compararFotografias(antes, depois) {
  const mudou = (a, b) => JSON.stringify(a) !== JSON.stringify(b)
  const diferencas = []
  if (mudou(antes.escutas, depois.escutas)) diferencas.push(`escutas: ${antes.escutas.join(', ') || 'nenhuma'} → ${depois.escutas.join(', ') || 'nenhuma'}`)
  if (mudou(antes.servicos, depois.servicos)) diferencas.push(`serviços: ${antes.servicos.join(', ')} → ${depois.servicos.join(', ')}`)
  return diferencas
}
