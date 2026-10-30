#!/usr/bin/env node
// Lê o transcript que o Claude Code grava em ~/.claude/projects/<pasta>/<sessão>.jsonl.
// Ele guarda o contexto que o modelo recebeu (anexos), o que o stream-json não mostra:
// é aqui que aparecem hooks, memória, CLAUDE.md e a lista de skills vista pelo modelo.
//
//   node prova/ferramentas/ler-transcript.mjs <transcript.jsonl>

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ANEXO_DE_HOOK = /hook/i
const ANEXO_DE_MEMORIA = /memory|claude_?md|nested/i

export function localizarTranscript(init) {
  const pastaDaMemoria = init?.memory_paths?.auto
  if (!pastaDaMemoria || !init.session_id) return null
  const arquivo = path.join(path.dirname(path.resolve(pastaDaMemoria)), `${init.session_id}.jsonl`)
  return fs.existsSync(arquivo) ? arquivo : null
}

export function resumirTranscript(arquivo) {
  const registros = fs.readFileSync(arquivo, 'utf8').split(/\r?\n/).filter(Boolean).map((linha) => JSON.parse(linha))
  const anexos = registros.filter((registro) => registro.type === 'attachment').map((registro) => registro.attachment ?? {})
  const tiposDeAnexo = [...new Set(anexos.map((anexo) => anexo.type))].sort()
  const skillsVistasPeloModelo = [...new Set(anexos.filter((anexo) => anexo.type === 'skill_listing').flatMap((anexo) => anexo.names ?? []))].sort()
  const contexto = anexos.find((anexo) => anexo.type === 'session_context')?.context ?? {}
  return {
    tipos_de_anexo: tiposDeAnexo,
    anexos_de_hook: tiposDeAnexo.filter((tipo) => ANEXO_DE_HOOK.test(tipo)),
    anexos_de_memoria: tiposDeAnexo.filter((tipo) => ANEXO_DE_MEMORIA.test(tipo)),
    chaves_do_contexto_da_sessao: Object.keys(contexto),
    skills_vistas_pelo_modelo: skillsVistasPeloModelo,
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  console.log(JSON.stringify(resumirTranscript(process.argv[2]), null, 2))
}
