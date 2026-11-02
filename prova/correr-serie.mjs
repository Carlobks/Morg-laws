#!/usr/bin/env node
// Uma série da Fase 4: N tentativas por condição de uma tarefa, intercaladas em pares
// (sem/com ou com/sem). A ordem de cada par sai de uma semente e fica gravada antes de correr,
// para que o cache de prompt, que aquece entre corridas seguidas, não favoreça um braço.
//
//   node prova/correr-serie.mjs --tarefa <T1|T2|T3> [--tentativas 5] [--semente 1] [--saida <pasta>]
//
// Grava em ~/.morg-laws/fase-4/series/<tarefa>-<data>/: ordem.json e uma pasta por tentativa.
// Depois: node prova/agregar.mjs <pasta-da-serie>

import { spawnSync } from 'node:child_process'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const PASTA_DA_PROVA = path.dirname(fileURLToPath(import.meta.url))

// mulberry32: um gerador pequeno e repetível a partir da semente.
function geradorComSemente(semente) {
  let estado = semente >>> 0
  return () => {
    estado = (estado + 0x6d2b79f5) >>> 0
    let valor = estado
    valor = Math.imul(valor ^ (valor >>> 15), valor | 1)
    valor ^= valor + Math.imul(valor ^ (valor >>> 7), valor | 61)
    return ((valor ^ (valor >>> 14)) >>> 0) / 4294967296
  }
}

export function sortearOrdem(tentativas, semente) {
  const aleatorio = geradorComSemente(semente)
  const ordem = []
  for (let par = 1; par <= tentativas; par++) {
    const primeiro = aleatorio() < 0.5 ? 'sem' : 'com'
    const segundo = primeiro === 'sem' ? 'com' : 'sem'
    ordem.push({ par, condicao: primeiro }, { par, condicao: segundo })
  }
  return ordem
}

function lerArgumentos(argv) {
  const opcoes = { tentativas: 5, semente: 1 }
  for (let i = 0; i < argv.length; i++) {
    const nome = argv[i]
    if (nome === '--tarefa') opcoes.tarefa = argv[++i]
    else if (nome === '--tentativas') opcoes.tentativas = Number(argv[++i])
    else if (nome === '--semente') opcoes.semente = Number(argv[++i])
    else if (nome === '--saida') opcoes.saida = argv[++i]
    else throw new Error(`opção desconhecida: ${nome}`)
  }
  if (!['T1', 'T2', 'T3'].includes(opcoes.tarefa)) throw new Error('--tarefa tem de ser T1, T2 ou T3')
  if (!Number.isInteger(opcoes.tentativas) || opcoes.tentativas < 1) throw new Error('--tentativas tem de ser um inteiro positivo')
  return opcoes
}

function principal() {
  const opcoes = lerArgumentos(process.argv.slice(2))
  const carimbo = new Date().toISOString().replace(/[:.]/g, '-')
  const pastaDaSerie = path.resolve(opcoes.saida ?? path.join(os.homedir(), '.morg-laws', 'fase-4', 'series', `${opcoes.tarefa}-${carimbo}`))
  fs.mkdirSync(pastaDaSerie, { recursive: true })
  const ordem = sortearOrdem(opcoes.tentativas, opcoes.semente)
  fs.writeFileSync(path.join(pastaDaSerie, 'ordem.json'), `${JSON.stringify({ ...opcoes, gravada_em: new Date().toISOString(), ordem }, null, 2)}\n`)

  for (const [indice, { par, condicao }] of ordem.entries()) {
    const saida = path.join(pastaDaSerie, `${String(indice + 1).padStart(2, '0')}-par${par}-${condicao}`)
    console.log(`→ ${indice + 1}/${ordem.length}: ${opcoes.tarefa} ${condicao} (par ${par})`)
    const execucao = spawnSync(process.execPath, [path.join(PASTA_DA_PROVA, 'correr-tentativa.mjs'),
      '--tarefa', opcoes.tarefa, '--condicao', condicao, '--saida', saida], { stdio: 'inherit' })
    // Uma tentativa inválida fica gravada e a série continua; o agregador conta-a à parte.
    if (execucao.status !== 0) console.log(`  tentativa ${indice + 1} terminou com o código ${execucao.status}`)
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) principal()
