// Nomes de arquivos, pastas e identificadores que dizem a função (Morg-laws: nomes únicos e pesquisáveis).
//
// Um nome genérico solto (`utils`, `helper`, `data`…) esconde onde está a lógica e dá dezenas de resultados no
// grep. A lista e a regra dos arquivos são as do molde Python test_nomes.py, e as duas línguas dão o mesmo veredito:
// - arquivos e pastas, de qualquer língua: o nome inteiro ou uma parte separada por ponto (`instalar.Comum.ps1`);
//   um nome composto que diz o quê (`bar-helper.ts`) não é solto;
// - identificadores JS/TS, lidos pela árvore: variáveis (também as desestruturadas e as do catch), parâmetros,
//   funções, classes, métodos, propriedades, interfaces, tipos e enums. `{ data }` declara `data`;
//   `{ data: faturasDoMes }` declara `faturasDoMes`; usar um nome (`pedido.data`) não é declará-lo. A caixa não conta.
// Por arquivo: `nomesGenericos` (quantos identificadores) e `caminhoGenerico` (1 se o caminho tem um nome solto).
// Linha de base: tests/linhas-de-base/nomes-genericos.json (linha-de-base.ts).
// Instalar: copiar esta pasta para tests/catracas/ do projeto e ajustar o bloco abaixo.
import { describe, expect, it } from 'vitest'
import { arquivosDoIndice, estaFora, lerDoGit, testarCatraca, type ExcessoPorArquivo } from './linha-de-base.js'
import { eCodigoJsOuTs, lerArvore, todosOsNomesDeclarados } from './ler-codigo-ts.js'

// Ajuste ao projeto. A mesma lista do molde Python test_nomes.py.
const NOMES_GENERICOS_PROIBIDOS = new Set(['comum', 'common', 'utils', 'util', 'helper', 'helpers', 'data', 'misc',
    'tmp', 'temp', 'info', 'manager', 'handler', 'stuff', 'geral', 'props', 'foo', 'bar', 'thing', 'dados', 'coisa',
    'coisas', 'auxiliar', 'auxiliares', 'diversos', 'temporario'])
const FORA_DOS_NOMES_GENERICOS = ['vendor/', 'node_modules/']

/** Um arquivo ou pasta do caminho cujo nome (ou uma parte separada por ponto) é uma palavra genérica solta. */
function eCaminhoGenerico(caminho: string): boolean {
    return caminho.split('/').some((parte) => parte.split('.').some((pedaco) => NOMES_GENERICOS_PROIBIDOS.has(pedaco.toLowerCase())))
}

function identificadoresGenericos(caminho: string, texto: string): string[] {
    return todosOsNomesDeclarados(lerArvore(caminho, texto)).filter((nome) => NOMES_GENERICOS_PROIBIDOS.has(nome.toLowerCase()))
}

function excessoGenerico(caminho: string, texto: string): Record<string, number> {
    const excesso: Record<string, number> = {}
    const genericos = eCodigoJsOuTs(caminho) ? identificadoresGenericos(caminho, texto).length : 0
    if (genericos > 0) excesso.nomesGenericos = genericos
    if (eCaminhoGenerico(caminho)) excesso.caminhoGenerico = 1
    return excesso
}

function excessoDosNomesGenericos(textos: Map<string, string>): ExcessoPorArquivo {
    return Object.fromEntries([...textos].map(([caminho, texto]) => [caminho, excessoGenerico(caminho, texto)])
        .filter(([, excesso]) => Object.keys(excesso).length > 0))
}

/** O caminho é julgado; o texto só se lê nos arquivos JS/TS (os outros entram com o texto vazio). */
function lerParaOsNomesGenericos(): Map<string, string> {
    const caminhos = arquivosDoIndice().filter((caminho) => !estaFora(caminho, FORA_DOS_NOMES_GENERICOS))
    const textos = lerDoGit(caminhos.filter(eCodigoJsOuTs))
    return new Map(caminhos.map((caminho) => [caminho, textos.get(caminho) ?? '']))
}

describe('detector de nomes genéricos', () => {
    it('pega os soltos no caminho e deixa os compostos', () => {
        expect(['a/comum/x.mjs', 'tests/instalar.Comum.ps1', 'bar-helper.ts', 'pedido.ts'].map(eCaminhoGenerico))
            .toEqual([true, true, false, false])
    })

    it('lê as declarações pela árvore, em qualquer nível', () => {
        const fonte = ['export async function carregar(info: string, ...dados: string[]) {',
            '    const { data, erro: [, ...tmp] } = await pedir(info)', '    for (const Coisa of []) usar(Coisa)',
            '    const { data: faturasDoMes } = await pedir(info)', '    usar(pedido.data, utils[0], faturasDoMes)',
            '    try { usar(data, erro) } catch (foo) { return [1].map((bar) => bar) }', '}',
            'class Helper { props = 1; handler() {} }'].join('\n')
        expect(identificadoresGenericos('a.ts', fonte).sort()).toEqual(
            ['Coisa', 'Helper', 'bar', 'dados', 'data', 'foo', 'handler', 'info', 'props', 'tmp'])
    })

    it('resume por arquivo', () => {
        const textos = new Map([['src/a.ts', 'const { data } = obter()'], ['lib/utils/certo.ts', 'export const moeda = 1'],
            ['docs/helpers.md', ''], ['src/limpo.ts', 'const { data: faturasDoMes } = obter()']])
        expect(excessoDosNomesGenericos(textos)).toEqual({ 'src/a.ts': { nomesGenericos: 1 },
            'lib/utils/certo.ts': { caminhoGenerico: 1 }, 'docs/helpers.md': { caminhoGenerico: 1 } })
    })
})

testarCatraca('nomes-genericos', 'troque pelo nome que diz o que guarda, ex.: { data: faturasDoMes }',
    () => excessoDosNomesGenericos(lerParaOsNomesGenericos()),
    (caminho, metrica) => !estaFora(caminho, FORA_DOS_NOMES_GENERICOS) && (metrica !== 'nomesGenericos' || eCodigoJsOuTs(caminho)))
