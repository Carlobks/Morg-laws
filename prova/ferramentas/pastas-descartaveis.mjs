// Pastas descartáveis para o oráculo e para as tentativas da Fase 4.
// O node_modules entra por junção (link de pasta do Windows), e a junção é desfeita
// antes de apagar, para que a remoção nunca siga o link até ao node_modules verdadeiro.

import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

const PASTAS_IGNORADAS = new Set(['node_modules', '.git'])

export function listarArquivosDoProjeto(raiz, relativo = '') {
  const encontrados = []
  for (const entrada of fs.readdirSync(path.join(raiz, relativo), { withFileTypes: true })) {
    if (PASTAS_IGNORADAS.has(entrada.name)) continue
    const caminho = path.posix.join(relativo.split(path.sep).join('/'), entrada.name)
    if (entrada.isDirectory()) encontrados.push(...listarArquivosDoProjeto(raiz, caminho))
    else if (entrada.isFile()) encontrados.push(caminho)
  }
  return encontrados
}

export function copiarProjetoSemDependencias(origem, destino) {
  fs.cpSync(origem, destino, {
    recursive: true,
    filter: (fonte) => !PASTAS_IGNORADAS.has(path.basename(fonte)),
  })
}

export function ligarDependencias(copia, ...projetosCandidatos) {
  const alvo = projetosCandidatos.map((projeto) => path.join(projeto, 'node_modules')).find((pasta) => fs.existsSync(pasta))
  if (!alvo) throw new Error('Nenhum node_modules encontrado: rode npm ci em prova/projeto-teste.')
  fs.symlinkSync(alvo, path.join(copia, 'node_modules'), 'junction')
}

export function apagarPastaTemporaria(pasta) {
  if (!fs.existsSync(pasta)) return true
  const juncoes = []
  const procurar = (dir) => {
    for (const entrada of fs.readdirSync(dir, { withFileTypes: true })) {
      const caminho = path.join(dir, entrada.name)
      if (entrada.isSymbolicLink()) juncoes.push(caminho)
      else if (entrada.isDirectory() && entrada.name !== 'node_modules') procurar(caminho)
    }
  }
  procurar(pasta)
  for (const juncao of juncoes) {
    try {
      fs.unlinkSync(juncao)
    } catch {
      fs.rmdirSync(juncao)
    }
  }
  for (let tentativa = 0; tentativa < 5; tentativa++) {
    try {
      fs.rmSync(pasta, { recursive: true, force: true })
      break
    } catch {
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 500)
    }
  }
  return !fs.existsSync(pasta)
}

export function criarPastaTemporaria(prefixo) {
  return fs.mkdtempSync(path.join(os.tmpdir(), `morg-${prefixo}-`))
}
