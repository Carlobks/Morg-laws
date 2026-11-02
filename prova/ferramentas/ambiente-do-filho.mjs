// O ambiente dos processos filhos (o `claude -p`, o oráculo, o git da cópia).
// Monta-se por lista de permitidas, e não tirando o que se conhece: a sessão que lança
// as corridas (a app desktop, um terminal, um CI) injeta variáveis que mudam o comportamento.

import fs from 'node:fs'
import path from 'node:path'

const VARIAVEIS_PERMITIDAS = [
  'PATH', 'PATHEXT', 'SystemRoot', 'SystemDrive', 'ComSpec', 'windir', 'OS',
  'TEMP', 'TMP', 'USERPROFILE', 'USERNAME', 'APPDATA', 'LOCALAPPDATA', 'HOMEDRIVE', 'HOMEPATH',
  'ProgramData', 'ProgramFiles', 'ProgramFiles(x86)', 'CommonProgramFiles',
  'NUMBER_OF_PROCESSORS', 'PROCESSOR_ARCHITECTURE',
]

// Fixas e escolhidas: iguais em todas as corridas, seja qual for a máquina.
const VARIAVEIS_FIXAS = {
  DISABLE_AUTOUPDATER: '1',
  // O git da cópia não lê a configuração do sistema nem a do usuário (e-mail, hooks, assinatura).
  GIT_CONFIG_NOSYSTEM: '1',
}

const PROGRAMAS_DO_POSTGRES = ['psql.exe', 'pg_ctl.exe', 'initdb.exe', 'psql', 'pg_ctl', 'initdb']

/**
 * @param {object} opcoes
 * @param {boolean} opcoes.semPostgres tira do PATH as pastas com psql, pg_ctl ou initdb
 * @param {string} opcoes.gitConfigGlobal arquivo vazio que faz de configuração global do git
 */
export function montarAmbienteDoFilho({ semPostgres, gitConfigGlobal }) {
  const ambiente = {}
  const permitidas = new Set(VARIAVEIS_PERMITIDAS.map((nome) => nome.toUpperCase()))
  for (const [nome, valor] of Object.entries(process.env)) {
    if (permitidas.has(nome.toUpperCase())) ambiente[nome] = valor
  }
  Object.assign(ambiente, VARIAVEIS_FIXAS)
  if (gitConfigGlobal) {
    fs.writeFileSync(gitConfigGlobal, '')
    ambiente.GIT_CONFIG_GLOBAL = gitConfigGlobal
  }

  const chave = Object.keys(ambiente).find((nome) => nome.toUpperCase() === 'PATH') ?? 'PATH'
  const pastas = (ambiente[chave] ?? '').split(path.delimiter).filter(Boolean)
  const temPostgres = (pasta) => PROGRAMAS_DO_POSTGRES.some((programa) => fs.existsSync(path.join(pasta, programa)))
  const pastasDoPostgres = semPostgres ? pastas.filter(temPostgres) : []
  ambiente[chave] = pastas.filter((pasta) => !pastasDoPostgres.includes(pasta)).join(path.delimiter)

  const descartadas = Object.keys(process.env).filter((nome) => !permitidas.has(nome.toUpperCase())).sort()
  return {
    ambiente,
    registro: {
      nomes_passados: Object.keys(ambiente).sort(),
      nomes_descartados: descartadas,
      path: { pastas_antes: pastas.length, pastas_depois: pastas.length - pastasDoPostgres.length, removidas: pastasDoPostgres },
    },
  }
}
