// Funções JS/TS até 20 linhas (Morg-laws: decisão do dono; o que já viola não piora).
//
// Uma função curta faz uma coisa só, e o agente acerta a mudança à primeira. Conta-se como no molde Python
// test_tamanho_das_funcoes.py: da linha onde a função começa (depois dos decoradores) à linha onde fecha, com as
// linhas em branco e os comentários. Entram as funções, os métodos, os construtores, os acessores e as arrow
// functions, também nos testes. O corpo de um `describe` não se mede: é como uma classe do Python, que também não
// se mede; cada `it` dentro dele mede-se, como um método.
// Por arquivo: `funcoesAcima` (quantas passam) e `linhasAcima` (quantas linhas passam, somadas). A medida é por
// arquivo e não por função: uma base por nome de função deixaria escapar quem a renomeasse.
// Linha de base: tests/linhas-de-base/tamanho-de-funcao.json (linha-de-base.ts).
// Instalar: copiar esta pasta para tests/catracas/ do projeto e ajustar o bloco abaixo.
import ts from 'typescript'
import { describe, expect, it } from 'vitest'
import { arquivosDoIndice, estaFora, lerDoGit, testarCatraca, type ExcessoPorArquivo } from './linha-de-base.js'
import { eCodigoJsOuTs, lerArvore, linhaDaPosicao } from './ler-codigo-ts.js'

// Ajuste ao projeto. O limite é o do molde Python test_tamanho_das_funcoes.py.
const LIMITE_DE_LINHAS_POR_FUNCAO = 20
const FORA_DO_TAMANHO_DE_FUNCAO = ['vendor/', 'node_modules/']
const BLOCOS_QUE_AGRUPAM_TESTES = new Set(['describe', 'suite'])

type NoDeFuncao = ts.FunctionLikeDeclaration

function eFuncaoComCorpo(no: ts.Node): no is NoDeFuncao {
    const funcao = ts.isFunctionDeclaration(no) || ts.isFunctionExpression(no) || ts.isArrowFunction(no)
        || ts.isMethodDeclaration(no) || ts.isConstructorDeclaration(no) || ts.isGetAccessorDeclaration(no)
        || ts.isSetAccessorDeclaration(no)
    return funcao && (no as NoDeFuncao).body !== undefined
}

/** O primeiro nome de `describe.each([...])`, `describe.skip`…: 'describe'. */
function nomeDaRaizDaChamada(expressao: ts.Expression): string | null {
    if (ts.isIdentifier(expressao)) return expressao.text
    if (ts.isPropertyAccessExpression(expressao) || ts.isCallExpression(expressao)) return nomeDaRaizDaChamada(expressao.expression)
    return ts.isTaggedTemplateExpression(expressao) ? nomeDaRaizDaChamada(expressao.tag) : null
}

/** A função é o corpo de um `describe` (passada como argumento a ele). */
function eCorpoDeUmDescribe(no: NoDeFuncao): boolean {
    const pai = no.parent
    if (!ts.isCallExpression(pai) || !pai.arguments.includes(no as ts.Expression)) return false
    return BLOCOS_QUE_AGRUPAM_TESTES.has(nomeDaRaizDaChamada(pai.expression) ?? '')
}

/** Linhas da função: da primeira depois dos decoradores à da chave que fecha. */
function linhasDaFuncao(arvore: ts.SourceFile, no: NoDeFuncao): number {
    const decoradores = ts.canHaveDecorators(no) ? ts.getDecorators(no) : undefined
    const fimDosDecoradores = decoradores?.length ? decoradores[decoradores.length - 1].end : null
    const inicio = fimDosDecoradores === null ? no.getStart(arvore)
        : fimDosDecoradores + arvore.text.slice(fimDosDecoradores).search(/\S/)
    return linhaDaPosicao(arvore, no.end) - linhaDaPosicao(arvore, inicio) + 1
}

/** Os tamanhos de todas as funções medidas de um arquivo. */
function tamanhosDasFuncoes(caminho: string, texto: string): number[] {
    const arvore = lerArvore(caminho, texto)
    const tamanhos: number[] = []
    const visitar = (no: ts.Node): void => {
        if (eFuncaoComCorpo(no) && !eCorpoDeUmDescribe(no)) tamanhos.push(linhasDaFuncao(arvore, no))
        ts.forEachChild(no, visitar)
    }
    visitar(arvore)
    return tamanhos
}

function excessoDasFuncoes(textos: Map<string, string>): ExcessoPorArquivo {
    const excessos: ExcessoPorArquivo = {}
    for (const [caminho, texto] of textos) {
        const acima = tamanhosDasFuncoes(caminho, texto).filter((linhas) => linhas > LIMITE_DE_LINHAS_POR_FUNCAO)
        if (acima.length === 0) continue
        const linhasAcima = acima.reduce((soma, linhas) => soma + linhas - LIMITE_DE_LINHAS_POR_FUNCAO, 0)
        excessos[caminho] = { funcoesAcima: acima.length, linhasAcima }
    }
    return excessos
}

const medeAsFuncoes = (caminho: string) => eCodigoJsOuTs(caminho) && !estaFora(caminho, FORA_DO_TAMANHO_DE_FUNCAO)

const corpoComLinhas = (linhas: number) => Array.from({ length: linhas }, (_, i) => `    const passo${i} = ${i}\n`).join('')

describe('medidor de funções', () => {
    it('conta da abertura ao fecho, com as linhas em branco', () => {
        const fonte = `function vinte() {\n${corpoComLinhas(18)}}\nconst vinteEUma = () => {\n\n${corpoComLinhas(18)}}\n`
        expect(tamanhosDasFuncoes('a.ts', fonte)).toEqual([20, 21])
    })

    it('mede métodos sem os decoradores e os it, mas não o corpo do describe', () => {
        const metodo = `class Pedido {\n    @registrar()\n    somar() {\n${corpoComLinhas(19)}    }\n}\n`
        const testes = `describe.each([1])('x', () => {\n    it('y', () => {\n${corpoComLinhas(25)}    })\n})\n`
        expect(tamanhosDasFuncoes('a.ts', metodo)).toEqual([21])
        expect(tamanhosDasFuncoes('a.test.ts', testes)).toEqual([27])
    })

    it('resume por arquivo', () => {
        const textos = new Map([['a.ts', `function f() {\n${corpoComLinhas(25)}}\n`], ['b.ts', 'const curta = () => 1\n']])
        expect(excessoDasFuncoes(textos)).toEqual({ 'a.ts': { funcoesAcima: 1, linhasAcima: 7 } })
    })
})

testarCatraca('tamanho-de-funcao', 'divida a função por responsabilidade: até 20 linhas, uma coisa só',
    () => excessoDasFuncoes(lerDoGit(arquivosDoIndice().filter(medeAsFuncoes))),
    (caminho) => medeAsFuncoes(caminho))
