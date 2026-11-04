// Alarmes silenciados só com motivo, e nunca mais do que hoje (Morg-laws: sem silenciar alarme; não piorar).
//
// A regra é de texto e é a do molde Python test_alarmes.py, com os mesmos padrões, extensões e pastas: as duas
// línguas julgam os mesmos arquivos e dão o mesmo veredito. Conta os `noqa`, `pragma: no cover`,
// `node:coverage disable`, `biome-ignore`, `eslint-disable`, `@ts-expect-error`, `@ts-ignore` e `SuppressMessage`
// do código (a pasta tests/ fica de fora: lá são exemplos), em `//` e em `/* */` (a forma do JSX). Cada um tem o
// motivo na mesma linha, depois de " — ": um comentário na linha de cima não conta, porque pode ser um TODO.
// A contagem POR TIPO, no projeto inteiro, não sobe: a linha de base guarda-a em `{ "*": { "<tipo>": n } }`, por
// isso mudar um alarme de arquivo não conta, e a falha diz onde estão os alarmes desse tipo. Quem tira um desce a
// base no mesmo commit. Um alarme novo justificado sobe a base com a linha `Alarme-novo: <motivo>` na mensagem do
// commit: o commit-msg (mensagem_commit.py) e o CI conferem-na. Só o Python confere se o `noqa` é de uma regra que
// o ruff tem ligada.
// Linha de base: tests/linhas-de-base/alarmes.json (linha-de-base.ts), a mesma do molde Python.
// Limites conhecidos: as extensões `.mts`, `.cts` e `.cjs` ficam de fora (acrescente-as no bloco abaixo, nas duas
// línguas); só se vê a diretiva no início de um comentário de linha ou de bloco.
// Instalar: copiar esta pasta para tests/catracas/ do projeto e ajustar o bloco abaixo.
import { describe, expect, it } from 'vitest'
import { arquivosDoIndice, estaFora, lerDoGit, testarCatraca, type ExcessoPorArquivo } from './linha-de-base.js'

// Ajuste ao projeto. Os mesmos do molde Python test_alarmes.py.
const EXTENSOES_COM_ALARMES_CONTADOS = ['.py', '.js', '.mjs', '.jsx', '.ts', '.tsx', '.ps1', '.psm1', '.html']
const FORA_DOS_ALARMES_CONTADOS = ['tests/', 'vendor/', 'node_modules/']

// Só a diretiva verdadeira (um comentário que fala dela não conta). Iguais aos do test_alarmes.py.
const PADROES_DOS_ALARMES: Record<string, RegExp> = {
    'noqa': /^\s*[^#\s].*#\s*noqa\b/,
    'pragma: no cover': /^\s*[^#\s].*#\s*pragma:\s*no cover/,
    'node:coverage disable': /^\s*\/\*\s*node:coverage (?:disable|ignore)/,
    'biome-ignore': /^\s*\/\/\s*biome-ignore/,
    'eslint-disable': /(?:\/\/|\/\*)\s*eslint-disable/,
    '@ts-expect-error': /(?:\/\/|\/\*)\s*@ts-expect-error/,
    '@ts-ignore': /(?:\/\/|\/\*)\s*@ts-ignore/,
    'SuppressMessage': /\[\s*(?:System\.)?Diagnostics\.CodeAnalysis\.SuppressMessage/,
}
// As quebras de linha que o splitlines() do Python conhece: as duas línguas contam as mesmas linhas.
const QUEBRA_COMO_NO_PYTHON = /\r\n|[\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029]/

type AlarmeAchado = { tipo: string, linha: number, texto: string }

function alarmesDoTexto(texto: string): AlarmeAchado[] {
    const linhas = texto.split(QUEBRA_COMO_NO_PYTHON)
    if (linhas.at(-1) === '') linhas.pop()
    return linhas.flatMap((textoDaLinha, indice) => Object.entries(PADROES_DOS_ALARMES)
        .filter(([, padrao]) => padrao.test(textoDaLinha))
        .map(([tipo]) => ({ tipo, linha: indice + 1, texto: textoDaLinha })))
}

const contaAlarmes = (caminho: string) => EXTENSOES_COM_ALARMES_CONTADOS.some((extensao) => caminho.endsWith(extensao))
    && !estaFora(caminho, FORA_DOS_ALARMES_CONTADOS)

function alarmesDoIndice(): Map<string, AlarmeAchado[]> {
    const textos = lerDoGit(arquivosDoIndice().filter(contaAlarmes))
    return new Map([...textos].map(([caminho, texto]) => [caminho, alarmesDoTexto(texto)]))
}

const TODO_O_PROJETO = '*' // a chave da contagem por tipo na linha de base

/** { "*": { tipo: quantos } } dos alarmes de todos os arquivos (vazio se não houver nenhum). */
function contagemPorTipo(alarmesPorArquivo: Map<string, AlarmeAchado[]>): ExcessoPorArquivo {
    const contagem: Record<string, number> = {}
    for (const { tipo } of [...alarmesPorArquivo.values()].flat()) contagem[tipo] = (contagem[tipo] ?? 0) + 1
    return Object.keys(contagem).length > 0 ? { [TODO_O_PROJETO]: contagem } : {}
}

/** Onde estão os alarmes de um tipo: o texto que se junta à mensagem de uma contagem que sobe. */
function ondeEstao(alarmesPorArquivo: Map<string, AlarmeAchado[]>, tipo: string): string {
    const lugares = [...alarmesPorArquivo].flatMap(([caminho, alarmes]) => alarmes
        .filter((alarme) => alarme.tipo === tipo).map(({ linha }) => `${caminho}:${linha}`))
    return ` — em ${lugares.join(', ')}`
}

describe('detector de alarmes', () => {
    it('pega a diretiva em // e em /* */ e deixa o texto que fala dela', () => {
        const barra = '/' // montado por partes, para este arquivo não ter as diretivas
        const texto = [`${barra}/ eslint-disable-next-line no-console — o CLI escreve no terminal`,
            `const a = <div>{${barra}* @ts-expect-error — tipo da lib */}</div>`, "const aviso = 'não use eslint-disable'",
            'import os  # noqa: F401', '# noqa: F401 num comentário solto'].join('\n')
        expect(alarmesDoTexto(texto).map(({ tipo, linha }) => `${linha} ${tipo}`))
            .toEqual(['1 eslint-disable', '2 @ts-expect-error', '4 noqa'])
    })

    it('conta por tipo em todo o projeto e diz onde estão', () => {
        const alarmes = new Map([['a.ts', [{ tipo: 'eslint-disable', linha: 1, texto: '' }, { tipo: 'noqa', linha: 2, texto: '' }]],
            ['b.ts', [{ tipo: 'eslint-disable', linha: 4, texto: '' }]]])
        expect(contagemPorTipo(alarmes)).toEqual({ '*': { 'eslint-disable': 2, 'noqa': 1 } })
        expect(contagemPorTipo(new Map())).toEqual({})
        expect(ondeEstao(alarmes, 'eslint-disable')).toBe(' — em a.ts:1, b.ts:4')
    })
})

describe('alarmes com motivo', () => {
    it('cada alarme tem o motivo na mesma linha, depois de —', () => {
        const semMotivo = [...alarmesDoIndice()].flatMap(([caminho, alarmes]) => alarmes
            .filter(({ texto }) => !texto.includes(' — ')).map(({ tipo, linha }) => `${caminho}:${linha} ${tipo}`))
        expect(semMotivo, 'falta o motivo na mesma linha, depois de —').toEqual([])
    })
})

let alarmesMedidos = new Map<string, AlarmeAchado[]>()

testarCatraca('alarmes', "corrija o apontado em vez de silenciar; um alarme justificado leva 'Alarme-novo: <motivo>' no commit",
    () => contagemPorTipo(alarmesMedidos = alarmesDoIndice()),
    (caminho) => caminho === TODO_O_PROJETO,
    { marcaParaSubir: 'Alarme-novo:', detalhe: (_, tipo) => ondeEstao(alarmesMedidos, tipo) })
