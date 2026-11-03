// Arquivos de código até 500 linhas (Morg-laws: arquivos pequenos; o que já viola não piora).
//
// Um arquivo grande mistura responsabilidades, e o agente lê-o inteiro para mudar uma linha. O limite e as
// extensões são os do hook limite_de_linhas.py e do molde Python test_tamanho_dos_arquivos.py: a regra é de texto,
// julga os arquivos de todas as línguas e dá o mesmo veredito nas duas. As linhas contam-se como o editor as
// mostra: a quebra no fim não é uma linha a mais.
// Linha de base: tests/linhas-de-base/tamanho-de-arquivo.json (linha-de-base.ts).
// Instalar: copiar esta pasta para tests/catracas/ do projeto e ajustar o bloco abaixo.
import { describe, expect, it } from 'vitest'
import { arquivosDoIndice, estaFora, lerDoGit, testarCatraca, type ExcessoPorArquivo } from './linha-de-base.js'

// Ajuste ao projeto. Os mesmos do molde Python test_tamanho_dos_arquivos.py.
const LIMITE_DE_LINHAS_POR_ARQUIVO = 500
const EXTENSOES_COM_LIMITE_DE_LINHAS = ['.py', '.ps1', '.psm1', '.sh', '.js', '.mjs', '.cjs', '.jsx', '.ts', '.mts',
    '.cts', '.tsx', '.html', '.css', '.sql', '.cmd', '.bat', '.yaml', '.yml', '.md']
const FORA_DO_LIMITE_DE_LINHAS = ['vendor/', 'node_modules/']

/** Linhas como o editor as mostra: cada quebra fecha uma linha, e o resto sem quebra no fim também conta. */
function linhasComoNoEditor(texto: string): number {
    return texto.split('\n').length - 1 + (texto !== '' && !texto.endsWith('\n') ? 1 : 0)
}

function temLimiteDeLinhas(caminho: string): boolean {
    return EXTENSOES_COM_LIMITE_DE_LINHAS.some((extensao) => caminho.toLowerCase().endsWith(extensao))
        && !estaFora(caminho, FORA_DO_LIMITE_DE_LINHAS)
}

/** { caminho: { linhasAcima } } dos arquivos acima do limite. */
function excessoDeLinhas(textos: Map<string, string>): ExcessoPorArquivo {
    return Object.fromEntries([...textos]
        .filter(([caminho, texto]) => temLimiteDeLinhas(caminho) && linhasComoNoEditor(texto) > LIMITE_DE_LINHAS_POR_ARQUIVO)
        .map(([caminho, texto]) => [caminho, { linhasAcima: linhasComoNoEditor(texto) - LIMITE_DE_LINHAS_POR_ARQUIVO }]))
}

describe('medidor de linhas', () => {
    it('conta como o editor', () => {
        expect(['', 'a', 'a\n', 'a\r\nb', 'a\n\n'].map(linhasComoNoEditor)).toEqual([0, 1, 1, 2, 2])
    })

    it('pega o que passa do limite e deixa o resto', () => {
        const noLimite = 'x\n'.repeat(LIMITE_DE_LINHAS_POR_ARQUIVO)
        const acima = 'x\n'.repeat(LIMITE_DE_LINHAS_POR_ARQUIVO + 3)
        const textos = new Map([['a.py', noLimite], ['b.ts', acima], ['notas.txt', acima], ['vendor/c.js', acima]])
        expect(excessoDeLinhas(textos)).toEqual({ 'b.ts': { linhasAcima: 3 } })
    })
})

testarCatraca('tamanho-de-arquivo', 'divida o arquivo por responsabilidade',
    () => excessoDeLinhas(lerDoGit(arquivosDoIndice().filter(temLimiteDeLinhas))),
    (caminho) => temLimiteDeLinhas(caminho))
