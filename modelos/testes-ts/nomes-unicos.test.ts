// Nomes de topo e de arquivo únicos (Morg-laws: nomes únicos e pesquisáveis; o que já viola não piora).
//
// Dois arquivos com a mesma função `calcular` ou dois `pedido.ts` dão dois resultados no grep, e o agente edita o
// errado. A regra é a do molde Python test_nomes_unicos.py, com as mesmas isenções. Por arquivo:
// - `nomesDeTopoRepetidos`: quantos nomes do topo (funções, classes, interfaces, tipos, enums e variáveis, também
//   as desestruturadas, exportados ou não) outro arquivo JS/TS também declara. Importar não é declarar;
// - `nomeDeArquivoRepetido`: 1 se outro arquivo de código, de qualquer língua, tem o mesmo nome sem a última
//   extensão (`pedido.ts` e `pedido.py` repetem; `pedido.test.ts` não repete `pedido.ts`).
// Ficam de fora o que a ferramenta impõe (ARQUIVOS_COM_NOME_IMPOSTO) e os nomes de uma interface comum de propósito
// (NOMES_DE_INTERFACE_COMUM). Um framework que exige nomes (o `page.tsx` e o `GET` do Next.js) entra nessas listas.
// Linha de base: tests/linhas-de-base/nomes-unicos.json (linha-de-base.ts).
// Instalar: copiar esta pasta para tests/catracas/ do projeto e ajustar o bloco abaixo.
import { describe, expect, it } from 'vitest'
import { arquivosDoIndice, estaFora, lerDoGit, testarCatraca, type ExcessoPorArquivo } from './linha-de-base.js'
import { eCodigoJsOuTs, lerArvore, nomesDoTopoTs } from './ler-codigo-ts.js'

// Ajuste ao projeto. Os mesmos do molde Python test_nomes_unicos.py.
const NOMES_DE_INTERFACE_COMUM = new Set(['main', 'erros', 'motivo_para_bloquear'])
const ARQUIVOS_COM_NOME_IMPOSTO = new Set(['__init__', '__main__', 'conftest'])
const EXTENSOES_COM_NOME_UNICO = ['.py', '.js', '.mjs', '.cjs', '.jsx', '.ts', '.mts', '.cts', '.tsx']
const FORA_DOS_NOMES_UNICOS = ['vendor/', 'node_modules/']

const eDunder = (nome: string) => nome.startsWith('__') && nome.endsWith('__')

function nomesDoTopoSemIsentos(caminho: string, texto: string): string[] {
    return [...nomesDoTopoTs(lerArvore(caminho, texto))].filter((nome) => !NOMES_DE_INTERFACE_COMUM.has(nome) && !eDunder(nome))
}

/** O nome sem a última extensão (`pedido.test.ts` → `pedido.test`), ou null se a ferramenta o impõe. */
function nomeDoArquivoSemExtensao(caminho: string): string | null {
    const nome = caminho.split('/').pop() ?? ''
    const semExtensao = nome.lastIndexOf('.') > 0 ? nome.slice(0, nome.lastIndexOf('.')) : nome
    return ARQUIVOS_COM_NOME_IMPOSTO.has(semExtensao) ? null : semExtensao
}

function contarAsVezes(nomes: Array<string | null>): Map<string, number> {
    const vezes = new Map<string, number>()
    for (const nome of nomes) if (nome) vezes.set(nome, (vezes.get(nome) ?? 0) + 1)
    return vezes
}

function excessoDosNomesRepetidos(textos: Map<string, string>): ExcessoPorArquivo {
    const topos = new Map([...textos].filter(([caminho]) => eCodigoJsOuTs(caminho))
        .map(([caminho, texto]) => [caminho, nomesDoTopoSemIsentos(caminho, texto)]))
    const vezesNoTopo = contarAsVezes([...topos.values()].flat())
    const vezesDoArquivo = contarAsVezes([...textos.keys()].map(nomeDoArquivoSemExtensao))
    const excessos: ExcessoPorArquivo = {}
    for (const caminho of textos.keys()) {
        const repetidos = (topos.get(caminho) ?? []).filter((nome) => (vezesNoTopo.get(nome) ?? 0) > 1).length
        const nomeDoArquivo = nomeDoArquivoSemExtensao(caminho)
        const excesso: Record<string, number> = {}
        if (repetidos > 0) excesso.nomesDeTopoRepetidos = repetidos
        if (nomeDoArquivo && (vezesDoArquivo.get(nomeDoArquivo) ?? 0) > 1) excesso.nomeDeArquivoRepetido = 1
        if (Object.keys(excesso).length > 0) excessos[caminho] = excesso
    }
    return excessos
}

const temNomeUnico = (caminho: string) => EXTENSOES_COM_NOME_UNICO.some((extensao) => caminho.toLowerCase().endsWith(extensao))
    && !estaFora(caminho, FORA_DOS_NOMES_UNICOS)

describe('detector de repetições', () => {
    it('lê o topo pela árvore', () => {
        const fonte = ['import { ler } from "x"', 'export const TAXA = 1', 'const [A, { b: B }] = [1, { b: 2 }]',
            'export default function Pagar() { const interna = 1; return interna }', 'interface Fatura {}',
            'type Linha = string', 'enum Estado { Paga }', 'export function main() {}', 'objeto.campo = 2'].join('\n')
        expect(nomesDoTopoSemIsentos('a.ts', fonte).sort()).toEqual(['A', 'B', 'Estado', 'Fatura', 'Linha', 'Pagar', 'TAXA'])
    })

    it('conta os nomes e os arquivos repetidos', () => {
        const textos = new Map([['a/pedido.ts', 'export function somar() {}\nconst soDeA = 1'],
            ['b/caixa.ts', 'function somar() {}'], ['c/pedido.py', ''], ['c/pedido.test.ts', ''],
            ['a/__init__.py', ''], ['b/__init__.py', '']])
        expect(excessoDosNomesRepetidos(textos)).toEqual({
            'a/pedido.ts': { nomesDeTopoRepetidos: 1, nomeDeArquivoRepetido: 1 },
            'b/caixa.ts': { nomesDeTopoRepetidos: 1 }, 'c/pedido.py': { nomeDeArquivoRepetido: 1 } })
    })
})

testarCatraca('nomes-unicos', 'dê um nome único que diga o quê (git grep antes de criar)',
    () => excessoDosNomesRepetidos(lerDoGit(arquivosDoIndice().filter(temNomeUnico))),
    (caminho, metrica) => temNomeUnico(caminho) && (metrica !== 'nomesDeTopoRepetidos' || eCodigoJsOuTs(caminho)))
