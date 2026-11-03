// Nenhum teste desligado para sempre nem isolado (Morg-laws: não piorar; um teste saltado deixa de proteger).
//
// Um teste saltado sem condição nunca mais corre, e um `.only` esconde todos os outros. Nos arquivos de teste, lidos
// pela árvore, é recusado:
// - `.only` (`it.only`, `describe.only`, `test.describe.only`) e `xit`, `xdescribe`, `xtest`, `fit`, `fdescribe`;
// - `.skip` sem condição: `it.skip('nome', …)`, `test.skip()`, `contexto.skip('nota')`;
// - `.skip` com condição sem o motivo escrito (um texto literal que não está vazio): `test.skip(semRede)`.
// A forma certa diz quando e porquê: `test.skip(semRede, 'precisa da rede')`, ou `it.skipIf(semRede)(…)`. É a regra
// do molde Python test_testes_saltados.py (`@unittest.skip`, `skipIf(condição, motivo)`, `skipTest` num `if`).
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

type SaltoProibido = { linha: number, motivo: string }

function eMotivoEscrito(no: ts.Node | undefined): boolean {
    if (!no) return false
    if (ts.isStringLiteral(no) || ts.isNoSubstitutionTemplateLiteral(no)) return no.text.trim() !== ''
    return ts.isTemplateExpression(no)
}

function erroDoSkip(argumentos: ts.NodeArray<ts.Expression>): string | null {
    const primeiro = argumentos[0]
    if (!primeiro || ts.isStringLiteralLike(primeiro) || ts.isTemplateExpression(primeiro)) {
        return 'salta sempre: diga a condição (skipIf) ou apague o teste'
    }
    return eMotivoEscrito(argumentos[1]) ? null : 'falta o motivo escrito'
}

/** Porque esta chamada desliga ou isola um teste; null se não o fizer. */
function erroDaChamada(chamada: ts.CallExpression): string | null {
    const alvo = chamada.expression
    if (ts.isIdentifier(alvo) && CHAMADAS_QUE_SEMPRE_DESLIGAM.has(alvo.text)) return `${alvo.text} desliga ou isola o teste`
    if (!ts.isPropertyAccessExpression(alvo)) return null
    if (alvo.name.text === 'only') return '.only esconde todos os outros testes'
    return alvo.name.text === 'skip' ? erroDoSkip(chamada.arguments) : null
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
            'test.skip(!temAviso)', "test.skip(semRede, '')"].join('\n')
        expect(linhasProibidas(fonte)).toEqual([1, 2, 3, 4, 5, 6, 7, 8])
    })

    it('deixa o que tem condição e motivo', () => {
        const fonte = ["test.skip(semRede, 'precisa da rede')", 'test.skip(!id, `defina ${nome}`)',
            "it.skipIf(semRede)('a', () => {})", "it.todo('por construir')", "const aviso = 'não use it.only'"].join('\n')
        expect(linhasProibidas(fonte)).toEqual([])
    })

    it('só julga os arquivos de teste', () => {
        expect(['tests/x.ts', 'src/a.test.ts', '__tests__/b.tsx', 'src/c.spec.mjs', 'src/d.ts'].map(eTesteJsOuTs))
            .toEqual([true, true, true, true, false])
    })
})

testarCatraca('testes-saltados', 'diga a condição e o motivo (test.skip(condição, "motivo")) ou apague o teste',
    () => excessoDosSaltos(lerDoGit(arquivosDoIndice().filter(eTesteJsOuTs))),
    (caminho) => eTesteJsOuTs(caminho))
