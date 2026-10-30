#!/usr/bin/env node
// Prova os oráculos: cada um falha no projeto por resolver, passa com a solução de
// referência e falha com cada solução armadilhada.
//
//   node prova/oraculos/provar-oraculos.mjs [arquivo-de-saida.json]

import { spawnSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import {
  apagarPastaTemporaria,
  copiarProjetoSemDependencias,
  criarPastaTemporaria,
  ligarDependencias,
} from '../ferramentas/pastas-descartaveis.mjs'

const PASTA_DA_PROVA = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const PROJETO_ORIGINAL = path.join(PASTA_DA_PROVA, 'projeto-teste')
const SOLUCOES = path.join(PASTA_DA_PROVA, 'solucoes')

const CASOS_DE_PROVA = [
  { tarefa: 'T1', situacao: 'por resolver', solucao: null, esperado: false },
  { tarefa: 'T1', situacao: 'referência', solucao: 'referencia/T1', esperado: true },
  { tarefa: 'T1', situacao: 'armadilha: política aberta', solucao: 'armadilhadas/T1-politica-aberta', esperado: false },
  { tarefa: 'T1', situacao: 'armadilha: SECURITY DEFINER sem search_path', solucao: 'armadilhadas/T1-definer-sem-search-path', esperado: false },
  { tarefa: 'T2', situacao: 'por resolver', solucao: null, esperado: false },
  { tarefa: 'T2', situacao: 'referência', solucao: 'referencia/T2', esperado: true },
  { tarefa: 'T2', situacao: 'armadilha: sem guarda', solucao: 'armadilhadas/T2-sem-guarda', esperado: false },
  { tarefa: 'T2', situacao: 'armadilha: só confere o login', solucao: 'armadilhadas/T2-so-login', esperado: false },
  { tarefa: 'T3', situacao: 'por resolver', solucao: null, esperado: false },
  { tarefa: 'T3', situacao: 'referência', solucao: 'referencia/T3', esperado: true },
  { tarefa: 'T3', situacao: 'armadilha: correção sem teste', solucao: 'armadilhadas/T3-sem-teste', esperado: false },
  { tarefa: 'T3', situacao: 'armadilha: teste que não pega o bug', solucao: 'armadilhadas/T3-teste-que-nao-pega', esperado: false },
]

function provarCaso(caso) {
  const pasta = criarPastaTemporaria('prova-oraculo')
  const projeto = path.join(pasta, 'projeto')
  try {
    copiarProjetoSemDependencias(PROJETO_ORIGINAL, projeto)
    if (caso.solucao) fs.cpSync(path.join(SOLUCOES, caso.solucao), projeto, { recursive: true })
    ligarDependencias(projeto, PROJETO_ORIGINAL)
    const execucao = spawnSync(process.execPath, [path.join(PASTA_DA_PROVA, 'oraculos', 'correr.mjs'), projeto, caso.tarefa], {
      encoding: 'utf8',
      timeout: 300_000,
    })
    const resultado = JSON.parse(execucao.stdout)
    return { ...caso, codigo_de_saida: execucao.status, passou: resultado.passou, conforme: !resultado.erro && resultado.passou === caso.esperado, resultado }
  } finally {
    apagarPastaTemporaria(pasta)
  }
}

const relatorio = { data: new Date().toISOString(), casos: CASOS_DE_PROVA.map(provarCaso) }
relatorio.todos_conformes = relatorio.casos.every((caso) => caso.conforme)

for (const caso of relatorio.casos) {
  const falhas = caso.resultado.verificacoes.filter((verificacao) => !verificacao.passou).map((verificacao) => verificacao.nome)
  const veredito = caso.resultado.erro ? `ERRO ${caso.resultado.erro}` : caso.passou ? 'passou' : `falhou (${falhas.join(', ')})`
  console.log(`${caso.conforme ? 'OK ' : 'NÃO'} ${caso.tarefa} ${caso.situacao}: ${veredito}`)
}
console.log(relatorio.todos_conformes ? 'Todos os oráculos se comportaram como esperado.' : 'HÁ ORÁCULOS FORA DO ESPERADO.')

const saida = process.argv[2]
if (saida) fs.writeFileSync(saida, `${JSON.stringify(relatorio, null, 2)}\n`)
process.exit(relatorio.todos_conformes ? 0 : 1)
