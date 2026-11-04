// Nenhum teste desligado para sempre nem isolado (Morg-laws: não piorar; um teste saltado deixa de proteger).
//
// Um teste saltado sem condição nunca mais corre, e um `.only` esconde todos os outros. Nos arquivos de teste, lidos
// pela árvore, olhando a cadeia toda (`it.skip.each`, `test.only.each`, `test.concurrent.only`), é recusado:
// - `.only` e `xit`, `xdescribe`, `xtest`, `fit`, `fdescribe`;
// - `it.skip`, `test.skip` e `describe.skip`, com qualquer argumento: no vitest o 1.º argumento é o NOME do teste,
//   e `test.skip(semRede, 'motivo')` regista um teste saltado chamado `false` (é a assinatura do Playwright, não a
//   do vitest);
// - `contexto.skip()` sem condição nem `if`/`catch` à volta, ou sem a nota escrita (um texto que não está vazio);
// - as opções do teste: `it('a', { skip: true }, …)` e `{ only: true }` (também `it['only']`); um
//   `{ skip: condição }` não leva nota e recusa-se como o `contexto.skip(condição)` sem ela.
// A forma certa diz quando e porquê: `it.skipIf(semRede)(…)`, `contexto.skip(semRede, 'precisa da rede')`, ou
// `if (semRede) contexto.skip('precisa da rede')` (também num `catch`). É a regra do molde Python
// test_testes_saltados.py (`@unittest.skip`, `skipIf(condição, motivo)`, `skipTest` num `if` ou num `except`).
// Limites conhecidos: uma condição constante (`it.skipIf(true)`) passa; um `.skip(…)` de outra coisa num arquivo de
// teste (`leitor.skip(3)`) é recusado; não serve o Playwright, cujo `test.skip(condição, motivo)` é a forma certa lá.
// Linha de base: tests/linhas-de-base/testes-saltados.json (linha-de-base.ts).
// Instalar: copiar esta pasta para tests/catracas/ do projeto e ajustar o bloco abaixo.
import ts from 'typescript'
import { describe, expect, it } from 'vitest'
import { arquivosDoIndice, estaFora, lerDoGit, testarCatraca, type ExcessoPorArquivo } from './linha-de-base.js'
import { eCodigoJsOuTs, lerArvore, linhaDaPosicao } from './ler-codigo-ts.js'

// Ajuste ao projeto. Arquivo de teste: numa pasta tests/, test/ ou __tests__/, ou com .test. ou .spec. no nome.
const ARQUIVO_DE_TESTE_JS_OU_TS = /(?:^|\/)(?:tests?|__tests__)\/|\.(?:test|spec)\.[^/]+$/
const FORA_DOS_TESTES_SALTADOS_TS = ['vendor/', 'node_modules/']
const CHAMADAS_QUE_SEMPRE_DESLIGAM = new Set(['xit', 'xdescribe', 'xtest', 'fit', 'fdescribe'])
const APIS_DE_TESTES = new Set(['it', 'test', 'describe', 'suite', 'bench'])

const SALTA_SEMPRE = 'salta sempre: use it.skipIf(condição) ou contexto.skip(condição, "nota"), ou apague o teste'
const SEM_MOTIVO_ESCRITO = 'falta o motivo escrito'

type SaltoProibido = { linha: number, motivo: string }

function eMotivoEscrito(no: ts.Node | undefined): boolean {
    if (!no) return false
    if (ts.isStringLiteral(no) || ts.isNoSubstitutionTemplateLiteral(no)) return no.text.trim() !== ''
    return ts.isTemplateExpression(no)
}

const eTextoLiteral = (no: ts.Node) => ts.isStringLiteralLike(no) || ts.isTemplateExpression(no)

/** Os nomes da cadeia chamada: `it.skip.each` → ['it', 'skip', 'each'], também `it['only']`; null se não for uma
 *  cadeia de nomes. */
function nomesDaCadeia(expressao: ts.Expression): string[] | null {
    if (ts.isIdentifier(expressao)) return [expressao.text]
    const porIndice = ts.isElementAccessExpression(expressao) && ts.isStringLiteralLike(expressao.argumentExpression)
    if (!ts.isPropertyAccessExpression(expressao) && !porIndice) return null
    const antes = nomesDaCadeia(expressao.expression)
    const nome = ts.isPropertyAccessExpression(expressao) ? expressao.name.text
        : ((expressao as ts.ElementAccessExpression).argumentExpression as ts.StringLiteralLike).text
    return antes && [...antes, nome]
}

/** `it('a', { skip: true }, …)`, `test('a', { only: true }, …)`: as opções do teste (o 2.º argumento no vitest). */
function erroDasOpcoes(chamada: ts.CallExpression): string | null {
    const propriedades = chamada.arguments.filter(ts.isObjectLiteralExpression).flatMap((opcoes) => [...opcoes.properties])
    for (const propriedade of propriedades.filter(ts.isPropertyAssignment)) {
        const nome = ts.isIdentifier(propriedade.name) || ts.isStringLiteral(propriedade.name) ? propriedade.name.text : ''
        const desligada = propriedade.initializer.kind === ts.SyntaxKind.FalseKeyword
        if (nome === 'only' && !desligada) return '{ only } esconde todos os outros testes'
        // Uma condição nas opções não leva nota: no vitest, diga-a com it.skipIf(condição) ou contexto.skip.
        if (nome === 'skip' && !desligada) return propriedade.initializer.kind === ts.SyntaxKind.TrueKeyword ? SALTA_SEMPRE : SEM_MOTIVO_ESCRITO
    }
    return null
}

function dentroDeUmIfOuCatch(no: ts.Node): boolean {
    for (let pai = no.parent; pai; pai = pai.parent) if (ts.isIfStatement(pai) || ts.isCatchClause(pai)) return true
    return false
}

/** `contexto.skip(condição, 'nota')`, ou `contexto.skip('nota')` num if ou num catch: a forma dinâmica do vitest. */
function erroDoSkipDoContexto(chamada: ts.CallExpression): string | null {
    const [condicao, nota] = chamada.arguments
    if (condicao && !eTextoLiteral(condicao)) return eMotivoEscrito(nota) ? null : SEM_MOTIVO_ESCRITO
    if (!dentroDeUmIfOuCatch(chamada)) return SALTA_SEMPRE
    return eMotivoEscrito(condicao) ? null : SEM_MOTIVO_ESCRITO
}

/** Porque esta chamada desliga ou isola um teste; null se não o fizer. */
function erroDaChamada(chamada: ts.CallExpression): string | null {
    const cadeia = nomesDaCadeia(chamada.expression)
    if (!cadeia) return null
    if (CHAMADAS_QUE_SEMPRE_DESLIGAM.has(cadeia[0])) return `${cadeia[0]} desliga ou isola o teste`
    const daApiDeTestes = APIS_DE_TESTES.has(cadeia[0])
    if (daApiDeTestes && cadeia.includes('only')) return '.only esconde todos os outros testes'
    // No vitest o 1.º argumento de test.skip é o NOME do teste: `test.skip(condição, …)` salta sempre.
    if (daApiDeTestes && cadeia.includes('skip')) return SALTA_SEMPRE
    if (daApiDeTestes) return erroDasOpcoes(chamada)
    return cadeia.length > 1 && cadeia[cadeia.length - 1] === 'skip' ? erroDoSkipDoContexto(chamada) : null
}

function saltosProibidos(caminho: string, texto: string): SaltoProibido[] {
    const arvore = lerArvore(caminho, texto)
    const proibidos: SaltoProibido[] = []
    const visitar = (no: ts.Node): void => {
        const motivo = ts.isCallExpression(no) ? erroDaChamada(no) : null
        if (motivo) proibidos.push({ linha: linhaDaPosicao(arvore, no.getStart(arvore)), motivo })
        ts.forEachChild(no, visitar)
    }
    visitar(arvore)
    return proibidos
}

const eTesteJsOuTs = (caminho: string) => eCodigoJsOuTs(caminho) && ARQUIVO_DE_TESTE_JS_OU_TS.test(caminho)
    && !estaFora(caminho, FORA_DOS_TESTES_SALTADOS_TS)

function excessoDosSaltos(textos: Map<string, string>): ExcessoPorArquivo {
    const excessos: ExcessoPorArquivo = {}
    for (const [caminho, texto] of textos) {
        const saltos = saltosProibidos(caminho, texto).length
        if (saltos > 0) excessos[caminho] = { testesSaltados: saltos }
    }
    return excessos
}

const linhasProibidas = (fonte: string) => saltosProibidos('a.test.ts', fonte).map(({ linha }) => linha)

describe('detector de saltos', () => {
    it('recusa o .only, o skip sem condição e o skip sem motivo', () => {
        const fonte = ["it.only('a', () => {})", "test.describe.only('a', () => {})", "it.skip('a', () => {})",
            'test.skip()', "xit('a', () => {})", "it('a', (contexto) => { contexto.skip('nota') })",
            "it('a', (contexto) => { contexto.skip(semRede) })", "it('a', (contexto) => { contexto.skip(semRede, '') })"]
            .join('\n')
        expect(linhasProibidas(fonte)).toEqual([1, 2, 3, 4, 5, 6, 7, 8])
    })

    it('no vitest, test.skip salta sempre, com qualquer 1.º argumento (é o nome do teste)', () => {
        const fonte = ["test.skip(semRede, 'precisa da rede')", 'it.skip(!id, `defina ${nome}`)',
            "describe.skip(semRede, () => {})"].join('\n')
        expect(linhasProibidas(fonte)).toEqual([1, 2, 3])
    })

    it('olha a cadeia toda: .skip.each e .only.each', () => {
        const fonte = ["it.skip.each([1])('a', () => {})", "describe.skip.each([1])('b', () => {})",
            "test.only.each([1])('c', () => {})", "test.concurrent.only('d', () => {})"].join('\n')
        expect(linhasProibidas(fonte)).toEqual([1, 2, 3, 4])
    })

    it('lê também as opções do teste: { skip }, { only } e o acesso por índice', () => {
        const fonte = ["it('a', { skip: true }, () => {})", "test('b', { only: true }, () => {})",
            "describe('c', { skip: true }, () => {})", "it('d', { skip: semRede }, () => {})", "it['only']('e', () => {})",
            "it('f', { timeout: 10 }, () => {})", "it('g', { skip: false }, () => {})"].join('\n')
        expect(linhasProibidas(fonte)).toEqual([1, 2, 3, 4, 5])
    })

    it('deixa o que tem condição e motivo', () => {
        const fonte = ["it.skipIf(semRede)('a', () => {})", "it.runIf(comRede)('a', () => {})",
            "it('a', (contexto) => { contexto.skip(semRede, 'precisa da rede') })", "it.todo('por construir')",
            "const aviso = 'não use it.only'", "it.skipIf(semRede).each([1])('a', () => {})"].join('\n')
        expect(linhasProibidas(fonte)).toEqual([])
    })

    it('o salto com nota dentro de um if ou de um catch vale, como no Python', () => {
        const fonte = ["it('a', (contexto) => { if (semRede) contexto.skip('sem rede') })",
            "it('b', async (contexto) => { try { await abrir() } catch { contexto.skip('sem o serviço') } })",
            "it('c', (contexto) => { if (semRede) contexto.skip() })"].join('\n')
        expect(linhasProibidas(fonte)).toEqual([3])
    })

    it('só julga os arquivos de teste', () => {
        expect(['tests/x.ts', 'src/a.test.ts', '__tests__/b.tsx', 'src/c.spec.mjs', 'src/d.ts'].map(eTesteJsOuTs))
            .toEqual([true, true, true, true, false])
    })
})

testarCatraca('testes-saltados', 'diga a condição e o motivo (it.skipIf(condição) ou contexto.skip(condição, "nota")) ou apague o teste',
    () => excessoDosSaltos(lerDoGit(arquivosDoIndice().filter(eTesteJsOuTs))),
    (caminho) => eTesteJsOuTs(caminho))
