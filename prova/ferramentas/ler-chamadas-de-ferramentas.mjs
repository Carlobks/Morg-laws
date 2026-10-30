#!/usr/bin/env node
// Lista, por ordem, cada chamada de ferramenta do transcript e o tool_result que ela recebeu.
// Serve para ler o que o ambiente fez (executou ou recusou), não o que o agente diz que fez.
//
//   node prova/ferramentas/ler-chamadas-de-ferramentas.mjs <transcript.jsonl>

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const TEXTO_DE_RECUSA = /permission|denied|haven't granted|not allowed|blocked|requires approval/i

function textoDoResultado(conteudo) {
  if (typeof conteudo === 'string') return conteudo
  if (Array.isArray(conteudo)) return conteudo.map((parte) => (typeof parte?.text === 'string' ? parte.text : '')).join('\n')
  return JSON.stringify(conteudo ?? '')
}

function resumirEntrada(nome, entrada = {}) {
  if (nome === 'Bash' || nome === 'PowerShell') return entrada.command
  if (['Read', 'Edit', 'Write'].includes(nome)) return entrada.file_path
  if (nome === 'Grep') return `${entrada.pattern} em ${entrada.path ?? '.'}`
  if (nome === 'Glob') return `${entrada.pattern} em ${entrada.path ?? '.'}`
  if (nome === 'WebFetch') return entrada.url
  return JSON.stringify(entrada).slice(0, 120)
}

export function lerChamadasDeFerramentas(arquivo) {
  const registros = fs.readFileSync(arquivo, 'utf8').split(/\r?\n/).filter(Boolean).map((linha) => JSON.parse(linha))
  const chamadas = []
  const porId = new Map()
  for (const registro of registros) {
    const conteudo = registro.message?.content
    if (!Array.isArray(conteudo)) continue
    for (const parte of conteudo) {
      if (registro.type === 'assistant' && parte.type === 'tool_use') {
        const chamada = { ferramenta: parte.name, alvo: resumirEntrada(parte.name, parte.input), resultado: null }
        porId.set(parte.id, chamada)
        chamadas.push(chamada)
      }
      if (registro.type === 'user' && parte.type === 'tool_result' && porId.has(parte.tool_use_id)) {
        const texto = textoDoResultado(parte.content).replace(/\s+/g, ' ').trim()
        const recusada = Boolean(parte.is_error) && TEXTO_DE_RECUSA.test(texto)
        porId.get(parte.tool_use_id).resultado = {
          erro: Boolean(parte.is_error),
          veredito: recusada ? 'recusada' : parte.is_error ? 'executada com erro' : 'executada',
          texto: texto.slice(0, 220),
        }
      }
    }
  }
  return chamadas
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  for (const [indice, chamada] of lerChamadasDeFerramentas(process.argv[2]).entries()) {
    const resultado = chamada.resultado ?? { veredito: 'sem tool_result', texto: '' }
    console.log(`${indice + 1}. ${chamada.ferramenta} ${chamada.alvo}\n   → ${resultado.veredito}: ${resultado.texto}`)
  }
}
