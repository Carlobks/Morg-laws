// Motor das catracas com linha de base (Morg-laws: não piorar). Usado pelos 6 moldes desta pasta.
//
// Cada catraca mede, por arquivo, o EXCESSO sobre a regra ({ "src/a.ts": { "linhasAcima": 12 } }; zero não
// aparece) e compara-o com a linha de base em tests/linhas-de-base/<regra>.json. O formato é o mesmo dos moldes
// Python (linha_de_base.py), e as três verificações também, cada uma num teste:
// - não piora: nenhuma métrica passa da base; um arquivo fora da base nasce limpo;
// - sem folga: a base não deixa mais do que existe hoje (quem corrige desce a base no mesmo commit);
// - só encolhe: a base do índice não tem entrada nova nem valor maior do que a do último commit.
// Lê do índice do git (o que vai no commit), nunca do disco: o trabalho a meio de outra sessão na mesma pasta não
// trava o commit desta. Um arquivo novo conta depois do `git add`.
// Projeto que já viola: rode uma vez com MORG_CRIAR_LINHA_DE_BASE=1. A base que falta é criada com os valores de
// hoje, e o teste falha até ela entrar no git. Uma base que já existe nunca é reescrita.
// Instalar: copiar esta pasta para tests/catracas/ do projeto (precisa do vitest e do typescript).
import { execFileSync } from 'node:child_process'
import { existsSync, mkdirSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'

// Ajuste ao projeto.
const PASTA_DAS_LINHAS_DE_BASE = 'tests/linhas-de-base'

/** O excesso de cada arquivo sobre a regra: { "src/a.ts": { "linhasAcima": 12 } }. */
export type ExcessoPorArquivo = Record<string, Record<string, number>>
type JulgaAMetrica = (caminho: string, metrica: string) => boolean
type Conferencia = { atuais: ExcessoPorArquivo, criada: string | null, base: ExcessoPorArquivo,
    doUltimoCommit: ExcessoPorArquivo | null }

const MEMORIA_DO_GIT = 256 * 1024 * 1024
export const RAIZ_DO_PROJETO = execFileSync('git', ['rev-parse', '--show-toplevel'], {
    cwd: dirname(fileURLToPath(import.meta.url)), encoding: 'utf8',
}).trim()

function correrGit(argumentos: string[], entrada = ''): Buffer {
    return execFileSync('git', argumentos, { cwd: RAIZ_DO_PROJETO, input: entrada, maxBuffer: MEMORIA_DO_GIT })
}

/** Os caminhos que o índice do git conhece (o que vai no próximo commit). */
export function arquivosDoIndice(): string[] {
    return correrGit(['ls-files', '-z']).toString('utf8').split('\0').filter(Boolean)
}

/** Map caminho → texto dos arquivos pedidos, como estão em `origem` (':' é o índice; 'HEAD:', o último commit). */
export function lerDoGit(caminhos: string[], origem = ':'): Map<string, string> {
    const saida = correrGit(['cat-file', '--batch'], caminhos.map((caminho) => `${origem}${caminho}\n`).join(''))
    const textos = new Map<string, string>()
    let posicao = 0
    for (const caminho of caminhos) {
        const fim = saida.indexOf(0x0a, posicao)
        const cabecalho = saida.subarray(posicao, fim).toString('utf8')
        if (cabecalho.endsWith(' missing')) {
            posicao = fim + 1
            continue
        }
        const tamanho = Number(cabecalho.split(' ')[2])
        textos.set(caminho, saida.subarray(fim + 1, fim + 1 + tamanho).toString('utf8').replace(/^﻿/, ''))
        posicao = fim + 1 + tamanho + 1
    }
    return textos
}

/** Um caminho sob uma das pastas de fora (`vendor/` na raiz ou em qualquer subpasta). */
export function estaFora(caminho: string, pastasDeFora: string[]): boolean {
    return pastasDeFora.some((fora) => caminho.startsWith(fora) || caminho.includes(`/${fora}`))
}

const caminhoDaBase = (regra: string) => `${PASTA_DAS_LINHAS_DE_BASE}/${regra}.json`

/** Os valores da linha de base da regra em `origem`; null se ela não existir lá. */
export function lerLinhaDeBase(regra: string, origem = ':'): ExcessoPorArquivo | null {
    const texto = lerDoGit([caminhoDaBase(regra)], origem).get(caminhoDaBase(regra))
    return texto === undefined ? null : ((JSON.parse(texto) as { valores?: ExcessoPorArquivo }).valores ?? {})
}

/** Mensagens de cada métrica de `valores` que passa do mesmo valor em `teto` (o que falta conta como 0). */
export function acimaDe(valores: ExcessoPorArquivo, teto: ExcessoPorArquivo, frase: string): string[] {
    const noTeto = (caminho: string, metrica: string) => teto[caminho]?.[metrica] ?? 0
    return Object.keys(valores).sort().flatMap((caminho) => Object.entries(valores[caminho])
        .sort(([a], [b]) => a.localeCompare(b))
        .filter(([metrica, valor]) => valor > noTeto(caminho, metrica))
        .map(([metrica, valor]) => `${caminho}: ${metrica} ${valor} (${frase} ${noTeto(caminho, metrica)})`))
}

function ordenarAsChaves(valores: ExcessoPorArquivo): ExcessoPorArquivo {
    return Object.fromEntries(Object.keys(valores).sort().map((caminho) => [caminho,
        Object.fromEntries(Object.entries(valores[caminho]).sort(([a], [b]) => a.localeCompare(b)))]))
}

/** Com MORG_CRIAR_LINHA_DE_BASE=1, grava a base que ainda não existe; devolve a mensagem, ou null. */
export function criarSeFaltar(regra: string, atuais: ExcessoPorArquivo): string | null {
    const destino = join(RAIZ_DO_PROJETO, caminhoDaBase(regra))
    if (process.env.MORG_CRIAR_LINHA_DE_BASE !== '1' || existsSync(destino) || lerLinhaDeBase(regra) !== null) return null
    mkdirSync(dirname(destino), { recursive: true })
    writeFileSync(destino, `${JSON.stringify({ regra, valores: ordenarAsChaves(atuais) }, null, 2)}\n`)
    return `linha de base criada em ${caminhoDaBase(regra)}: confira-a e faça git add`
}

/** Só o que esta regra julga: uma base partilhada com o molde Python pode ter métricas da outra língua. */
function soOQueJulga(base: ExcessoPorArquivo, julga: JulgaAMetrica): ExcessoPorArquivo {
    return Object.fromEntries(Object.entries(base).map(([caminho, metricas]) => [caminho,
        Object.fromEntries(Object.entries(metricas).filter(([metrica]) => julga(caminho, metrica)))]))
}

/** Uma medição por regra: os três testes julgam o mesmo estado do índice. */
function conferirUmaVez(regra: string, medir: () => ExcessoPorArquivo): () => Conferencia {
    let conferido: Conferencia | null = null
    return () => {
        if (conferido) return conferido
        const atuais = medir()
        const criada = criarSeFaltar(regra, atuais)
        conferido = { atuais, criada, base: lerLinhaDeBase(regra) ?? {}, doUltimoCommit: lerLinhaDeBase(regra, 'HEAD:') }
        return conferido
    }
}

function registrarAsTresVerificacoes(conferir: () => Conferencia, conselho: string, julga: JulgaAMetrica): void {
    it('não piora', () => {
        const { atuais, criada, base } = conferir()
        expect([...(criada ? [criada] : []), ...acimaDe(atuais, base, 'a base deixa')], conselho).toEqual([])
    }, 120_000)
    it('a linha de base não tem folga', () => {
        const { atuais, base } = conferir()
        expect(acimaDe(soOQueJulga(base, julga), atuais, 'hoje há'), 'desça a linha de base no mesmo commit').toEqual([])
    })
    it('a linha de base só encolhe', () => {
        const { base, doUltimoCommit } = conferir()
        const novas = doUltimoCommit === null ? [] : acimaDe(base, doUltimoCommit, 'o último commit deixava')
        expect(novas, 'a linha de base só desce: corrija o código em vez de a subir').toEqual([])
    })
}

/** As três verificações de uma regra, cada uma num `it`. `medir()` devolve o excesso de hoje. */
export function testarCatraca(regra: string, conselho: string, medir: () => ExcessoPorArquivo, julga: JulgaAMetrica): void {
    const conferir = conferirUmaVez(regra, medir)
    describe(`catraca ${regra}`, () => registrarAsTresVerificacoes(conferir, conselho, julga))
}
