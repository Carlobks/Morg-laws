// Motor das catracas com linha de base (Morg-laws: não piorar). Usado pelos 6 moldes desta pasta.
//
// Cada catraca mede, por arquivo, o EXCESSO sobre a regra ({ "src/a.ts": { "linhasAcima": 12 } }; zero não
// aparece) e compara-o com a linha de base em tests/linhas-de-base/<regra>.json. O formato é o mesmo dos moldes
// Python (linha_de_base.py), e as três verificações também, cada uma num teste:
// - não piora: nenhuma métrica passa da base; um arquivo fora da base nasce limpo;
// - sem folga: a base não deixa mais do que existe hoje (quem corrige desce a base no mesmo commit);
// - só encolhe: a base não tem entrada nova nem valor maior do que a da base de comparação. Na máquina, a de
//   comparação é a do último commit (HEAD). No CI e numa PR, o índice é o próprio commit: MORG_BASE_DE_COMPARACAO
//   diz com que commit comparar (a ponta anterior do ramo de destino), e o checkout precisa do histórico
//   (fetch-depth: 0). Uma regra pode deixar a base subir com uma linha na mensagem do commit (marcaParaSubir; a dos
//   alarmes é `Alarme-novo:`): na máquina quem a confere é o commit-msg (o pre-commit corre antes da mensagem); no
//   CI, este teste procura-a nos commits do intervalo.
// Lê do índice do git (o que vai no commit), nunca do disco: o trabalho a meio de outra sessão na mesma pasta não
// trava o commit desta. Um arquivo novo conta depois do `git add`.
// Projeto que já viola: rode uma vez com MORG_CRIAR_LINHA_DE_BASE=1. A base que falta é criada com os valores de
// hoje; uma que existe mas ainda não está no último commit ganha as métricas que lhe faltam (um projeto com as duas
// línguas partilha a pasta). O teste falha até ela entrar no git. Uma base já commitada nunca muda.
// Limites conhecidos: mudar de caminho um arquivo que está na base (`git mv`) conta como entrada nova; corrija-o ou
// faça um commit só da base, revisto. Apagar a base num commit e criá-la no seguinte passa: só a revisão o apanha.
// Instalar: copiar esta pasta para tests/catracas/ do projeto (precisa do vitest e do typescript).
import { execFileSync, spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'

// Ajuste ao projeto.
const PASTA_DAS_LINHAS_DE_BASE = 'tests/linhas-de-base'

/** O excesso de cada arquivo sobre a regra: { "src/a.ts": { "linhasAcima": 12 } }. */
export type ExcessoPorArquivo = Record<string, Record<string, number>>
type JulgaAMetrica = (caminho: string, metrica: string) => boolean
type DetalheDaMetrica = (caminho: string, metrica: string) => string
type Conferencia = { atuais: ExcessoPorArquivo, criada: string | null, base: ExcessoPorArquivo,
    daComparacao: ExcessoPorArquivo | null }
/** O que uma regra pode pedir a mais: a marca que deixa a base subir e o texto a juntar a cada métrica que passa. */
export type OpcoesDaCatraca = { marcaParaSubir?: string, detalhe?: DetalheDaMetrica }

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

/** O commit com que o «só encolhe» compara: MORG_BASE_DE_COMPARACAO (no CI) ou o último commit. */
export function baseDeComparacao(): string {
    return process.env.MORG_BASE_DE_COMPARACAO || 'HEAD'
}

/** O texto das mensagens dos commits entre `commit` e o HEAD (vazio na máquina, onde `commit` é o HEAD). */
function mensagensDesde(commit: string): string {
    const resultado = spawnSync('git', ['log', '--format=%B', `${commit}..HEAD`], { cwd: RAIZ_DO_PROJETO, encoding: 'utf8' })
    return resultado.status === 0 ? resultado.stdout : ''
}

/** Mensagens de cada métrica de `valores` que passa do mesmo valor em `teto` (o que falta conta como 0). */
export function acimaDe(valores: ExcessoPorArquivo, teto: ExcessoPorArquivo, frase: string,
    detalhe: DetalheDaMetrica = () => ''): string[] {
    const noTeto = (caminho: string, metrica: string) => teto[caminho]?.[metrica] ?? 0
    return Object.keys(valores).sort().flatMap((caminho) => Object.entries(valores[caminho])
        .sort(([a], [b]) => a.localeCompare(b))
        .filter(([metrica, valor]) => valor > noTeto(caminho, metrica))
        .map(([metrica, valor]) => `${caminho}: ${metrica} ${valor} (${frase} ${noTeto(caminho, metrica)})${detalhe(caminho, metrica)}`))
}

function ordenarAsChaves(valores: ExcessoPorArquivo): ExcessoPorArquivo {
    return Object.fromEntries(Object.keys(valores).sort().filter((caminho) => Object.keys(valores[caminho]).length > 0)
        .map((caminho) => [caminho, Object.fromEntries(Object.entries(valores[caminho]).sort(([a], [b]) => a.localeCompare(b)))]))
}

/** As métricas de `atuais` que a base `existente` ainda não tem. */
function metricasQueFaltam(atuais: ExcessoPorArquivo, existente: ExcessoPorArquivo): ExcessoPorArquivo {
    return Object.fromEntries(Object.entries(atuais).map(([caminho, metricas]) => [caminho,
        Object.fromEntries(Object.entries(metricas).filter(([metrica]) => !(metrica in (existente[caminho] ?? {}))))]))
}

/** Com MORG_CRIAR_LINHA_DE_BASE=1, cria a base que falta ou junta-lhe as métricas que lhe faltam, se ela ainda não
 *  estiver no último commit; devolve a mensagem, ou null se nada mudou. */
export function criarOuCompletar(regra: string, atuais: ExcessoPorArquivo): string | null {
    const destino = join(RAIZ_DO_PROJETO, caminhoDaBase(regra))
    if (process.env.MORG_CRIAR_LINHA_DE_BASE !== '1' || lerLinhaDeBase(regra, 'HEAD:') !== null) return null
    const existente: ExcessoPorArquivo = existsSync(destino) ? JSON.parse(readFileSync(destino, 'utf8')).valores ?? {} : {}
    const faltam = metricasQueFaltam(atuais, existente)
    if (existsSync(destino) && Object.values(faltam).every((metricas) => Object.keys(metricas).length === 0)) return null
    const juntas = Object.fromEntries([...new Set([...Object.keys(existente), ...Object.keys(faltam)])]
        .map((caminho) => [caminho, { ...existente[caminho], ...faltam[caminho] }]))
    mkdirSync(dirname(destino), { recursive: true })
    writeFileSync(destino, `${JSON.stringify({ regra, valores: ordenarAsChaves(juntas) }, null, 2)}\n`)
    return `linha de base gravada em ${caminhoDaBase(regra)}: confira-a e faça git add`
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
        const criada = criarOuCompletar(regra, atuais)
        conferido = { atuais, criada, base: lerLinhaDeBase(regra) ?? {}, daComparacao: lerLinhaDeBase(regra, `${baseDeComparacao()}:`) }
        return conferido
    }
}

/** A subida que a marca na mensagem deixa passar: no CI, se um commit do intervalo a traz. */
function subidaComAMarca(marca: string): boolean {
    const comAMarca = new RegExp(`^${marca.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')} *\\S`, 'm')
    return comAMarca.test(mensagensDesde(baseDeComparacao()))
}

function registrarAsTresVerificacoes(conferir: () => Conferencia, conselho: string, julga: JulgaAMetrica,
    { marcaParaSubir, detalhe }: OpcoesDaCatraca): void {
    it('não piora', () => {
        const { atuais, criada, base } = conferir()
        expect([...(criada ? [criada] : []), ...acimaDe(atuais, base, 'a base deixa', detalhe)], conselho).toEqual([])
    }, 120_000)
    it('a linha de base não tem folga', () => {
        const { atuais, base } = conferir()
        expect(acimaDe(soOQueJulga(base, julga), atuais, 'hoje há'), 'desça a linha de base no mesmo commit').toEqual([])
    })
    it('a linha de base só encolhe', (contexto) => {
        const { base, daComparacao } = conferir()
        const novas = daComparacao === null ? [] : acimaDe(base, daComparacao, 'a base de comparação deixava')
        const comMarca = novas.length > 0 && marcaParaSubir !== undefined
        if (comMarca && baseDeComparacao() === 'HEAD') contexto.skip('a subida pede a marca na mensagem; o commit-msg confere-a')
        const aceitas = comMarca && subidaComAMarca(marcaParaSubir) ? [] : novas
        expect(aceitas, 'a linha de base só desce: corrija o código em vez de a subir').toEqual([])
    })
}

/** As três verificações de uma regra, cada uma num `it`. `medir()` devolve o excesso de hoje. */
export function testarCatraca(regra: string, conselho: string, medir: () => ExcessoPorArquivo, julga: JulgaAMetrica,
    opcoes: OpcoesDaCatraca = {}): void {
    const conferir = conferirUmaVez(regra, medir)
    describe(`catraca ${regra}`, () => registrarAsTresVerificacoes(conferir, conselho, julga, opcoes))
}
