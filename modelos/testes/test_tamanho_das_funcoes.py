"""Funções Python até LIMITE_POR_FUNCAO linhas (Morg-laws: decisão do dono; o que já viola não piora).

Uma função curta faz uma coisa só, e o agente acerta a mudança à primeira. Conta-se como no molde TypeScript
tamanho-de-funcao.test.ts: da linha do `def` (os decoradores não) à última linha do corpo, com as linhas em branco
e os comentários do meio e do fim (os que estão mais à direita do que o `def`). Entram as funções, os métodos e as
funções dentro de funções, também nos testes; as classes não se medem.
Por arquivo: `funcoesAcima` (quantas passam) e `linhasAcima` (quantas linhas passam, somadas). A medida é por
arquivo e não por função: uma base por nome de função deixaria escapar quem a renomeasse, e dois métodos com o
mesmo nome em classes diferentes contariam como um só.
Linha de base: tests/linhas-de-base/tamanho-de-funcao.json (linha_de_base.py).
Limites conhecidos: um comentário mais à direita do que o `def`, depois da função e antes da seguinte, conta na
função de cima.
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import ast
import unittest

from linha_de_base import TresVerificacoesDaCatraca, arquivos_do_indice, ler_do_git

# Ajuste ao projeto. O limite é o do molde TypeScript tamanho-de-funcao.test.ts.
LIMITE_POR_FUNCAO = 20
FORA_DO_TAMANHO_DE_FUNCAO = ("vendor/", "node_modules/")


def ultima_linha_da_funcao(funcao, linhas):
    """A última linha da função: a da última instrução, ou a do último comentário do corpo que vem depois dela."""
    fim = funcao.end_lineno
    for numero in range(funcao.end_lineno, len(linhas)):
        linha = linhas[numero]
        recuo = len(linha) - len(linha.lstrip())
        if linha.strip() and not (linha.lstrip().startswith("#") and recuo > funcao.col_offset):
            break
        fim = numero + 1 if linha.strip() else fim
    return fim


def tamanhos_das_funcoes(fonte):
    """As linhas de cada função de um código Python, da linha do `def` à última do corpo."""
    linhas = fonte.splitlines()
    return [ultima_linha_da_funcao(no, linhas) - no.lineno + 1 for no in ast.walk(ast.parse(fonte))
            if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef))]


def excesso_das_funcoes(textos):
    """{caminho: {"funcoesAcima": n, "linhasAcima": soma}} dos arquivos com funções acima do limite."""
    excessos = {}
    for caminho, texto in textos.items():
        acima = [linhas for linhas in tamanhos_das_funcoes(texto) if linhas > LIMITE_POR_FUNCAO]
        if acima:
            excessos[caminho] = {"funcoesAcima": len(acima), "linhasAcima": sum(acima) - LIMITE_POR_FUNCAO * len(acima)}
    return excessos


def mede_as_funcoes(caminho):
    return (caminho.endswith(".py")
            and not any(caminho.startswith(fora) or f"/{fora}" in caminho for fora in FORA_DO_TAMANHO_DE_FUNCAO))


class MedidorDeFuncoes(unittest.TestCase):

    def test_conta_da_linha_do_def_a_do_fim_com_os_comentarios(self):
        vinte = "def vinte():\n" + "    x = 1\n" * 19
        com_notas = ("def com_notas():\n" + "    x = 1\n" * 18
                     + "    # uma nota\n\n    # outra\n\ndef seguinte():\n    pass\n")
        decorada = "@registrar\ndef decorada():\n" + "    x = 1\n" * 19
        self.assertEqual([tamanhos_das_funcoes(f) for f in (vinte, com_notas, decorada)], [[20], [22, 2], [20]])

    def test_dois_metodos_com_o_mesmo_nome_contam_os_dois(self):
        fonte = ("class A:\n    def correr(self):\n" + "        x = 1\n" * 26
                 + "class B:\n    def correr(self):\n        pass\n")
        self.assertEqual(excesso_das_funcoes({"a.py": fonte}), {"a.py": {"funcoesAcima": 1, "linhasAcima": 7}})


class TamanhoDasFuncoes(TresVerificacoesDaCatraca, unittest.TestCase):
    REGRA = "tamanho-de-funcao"
    CONSELHO = "divida a função por responsabilidade: até 20 linhas, uma coisa só"

    def medir(self):
        return excesso_das_funcoes(ler_do_git([caminho for caminho in arquivos_do_indice() if mede_as_funcoes(caminho)]))

    def julga(self, caminho, metrica):
        return mede_as_funcoes(caminho)


if __name__ == "__main__":
    unittest.main()
