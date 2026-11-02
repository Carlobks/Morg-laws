#!/usr/bin/env node
// Agrega as tentativas de uma ou mais séries: contagens e medianas por tarefa e condição.
// A publicação é descritiva (C5 da auditoria 4.3): com 5 tentativas por braço não há força
// estatística para concluir que as regras melhoram ou pioram; mostram-se os números.
// Lê só os campos agregados do meta.json, nunca o transcript (que traz o e-mail da conta).
//
//   node prova/agregar.mjs <pasta-da-serie> [<outra-pasta>…] [--json]

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

function lerTentativas(pastas) {
  const tentativas = []
  for (const pasta of pastas) {
    for (const entrada of fs.readdirSync(pasta, { withFileTypes: true })) {
      const arquivo = path.join(pasta, entrada.name, 'meta.json')
      if (entrada.isDirectory() && fs.existsSync(arquivo)) tentativas.push(JSON.parse(fs.readFileSync(arquivo, 'utf8')))
    }
  }
  return tentativas
}

export function mediana(valores) {
  const ordenados = valores.filter((valor) => typeof valor === 'number' && Number.isFinite(valor)).sort((a, b) => a - b)
  if (ordenados.length === 0) return null
  const meio = Math.floor(ordenados.length / 2)
  return ordenados.length % 2 ? ordenados[meio] : (ordenados[meio - 1] + ordenados[meio]) / 2
}

export function agregar(tentativas) {
  const grupos = new Map()
  for (const tentativa of tentativas) {
    const chave = `${tentativa.tarefa}|${tentativa.condicao}`
    if (!grupos.has(chave)) grupos.set(chave, [])
    grupos.get(chave).push(tentativa)
  }
  return [...grupos.entries()].sort().map(([chave, grupo]) => {
    const [tarefa, condicao] = chave.split('|')
    // As inválidas contam-se, mas não entram nas outras contagens nem nas medianas.
    const validas = grupo.filter((tentativa) => !tentativa.invalida && !tentativa.erro)
    const contar = (condicaoDaContagem) => validas.filter(condicaoDaContagem).length
    const valores = (ler) => validas.map(ler)
    return {
      tarefa,
      condicao,
      tentativas: grupo.length,
      invalidas: grupo.length - validas.length,
      validas: validas.length,
      passou: contar((tentativa) => tentativa.oraculo?.passou === true),
      resolveu: contar((tentativa) => tentativa.oraculo?.resolveu === true),
      cumpriu_a_norma: contar((tentativa) => tentativa.oraculo?.cumpriu_a_norma === true),
      pediu_licenca: contar((tentativa) => tentativa.pediu_licenca === true),
      pergunta_com_trabalho_parcial: contar((tentativa) => tentativa.pergunta_com_trabalho_parcial === true),
      teto_atingido: contar((tentativa) => tentativa.metricas?.teto_atingido === true),
      mediana_custo_usd: mediana(valores((tentativa) => tentativa.metricas?.custo_usd)),
      mediana_duracao_s: mediana(valores((tentativa) => (tentativa.metricas?.duracao_ms ?? NaN) / 1000)),
      mediana_turnos: mediana(valores((tentativa) => tentativa.metricas?.turnos)),
      mediana_linhas_do_diff: mediana(valores((tentativa) => tentativa.metricas?.linhas_do_diff)),
      mediana_acoes_nao_pedidas: mediana(valores((tentativa) => tentativa.acoes_nao_pedidas?.total)),
    }
  })
}

function principal() {
  const argumentos = process.argv.slice(2)
  const comoJson = argumentos.includes('--json')
  const pastas = argumentos.filter((argumento) => argumento !== '--json')
  if (pastas.length === 0) {
    console.error('uso: node prova/agregar.mjs <pasta-da-serie> [<outra-pasta>…] [--json]')
    process.exit(2)
  }
  const linhas = agregar(lerTentativas(pastas))
  if (comoJson) {
    console.log(JSON.stringify(linhas, null, 2))
    return
  }
  const colunas = ['tarefa', 'condicao', 'validas', 'invalidas', 'passou', 'resolveu', 'cumpriu_a_norma', 'pediu_licenca', 'pergunta_com_trabalho_parcial', 'teto_atingido',
    'mediana_custo_usd', 'mediana_duracao_s', 'mediana_turnos', 'mediana_linhas_do_diff', 'mediana_acoes_nao_pedidas']
  console.log(`| ${colunas.join(' | ')} |`)
  console.log(`|${colunas.map(() => '---').join('|')}|`)
  for (const linha of linhas) console.log(`| ${colunas.map((coluna) => (linha[coluna] ?? '—')).join(' | ')} |`)
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) principal()
