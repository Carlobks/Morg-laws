"""Arquivos de código até LIMITE_DE_LINHAS linhas (Morg-laws: arquivos pequenos; o que já viola não piora).

Um arquivo grande mistura responsabilidades, e o agente lê-o inteiro para mudar uma linha. O limite e as extensões
são os do hook limite_de_linhas.py, que recusa a edição na hora; este teste mede todos os arquivos, também os que
mudaram pela shell. As linhas contam-se como o editor as mostra: a quebra no fim não é uma linha a mais.
A regra é de texto: julga os arquivos de todas as línguas, como o molde TypeScript tamanho-de-arquivo.test.ts,
com o mesmo limite e o mesmo veredito. Linha de base: tests/linhas-de-base/tamanho-de-arquivo.json (linha_de_base.py).
Limites conhecidos: um arquivo com as linhas separadas só por `\\r` (a quebra antiga do Mac) conta como uma linha; o
hook conta com o splitlines() (que também quebra no `\\r`), e por isso os dois podem divergir nesse caso raro.
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import unittest

from linha_de_base import TresVerificacoesDaCatraca, arquivos_do_indice, ler_do_git

# Ajuste ao projeto. Os mesmos do molde TypeScript tamanho-de-arquivo.test.ts.
LIMITE_DE_LINHAS = 500
EXTENSOES_COM_LIMITE = (".py", ".ps1", ".psm1", ".sh", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".mts", ".cts", ".tsx",
                        ".html", ".css", ".sql", ".cmd", ".bat", ".yaml", ".yml", ".md")
FORA_DO_LIMITE = ("vendor/", "node_modules/")


def linhas_no_editor(texto):
    """Linhas como o editor as mostra: cada quebra fecha uma linha, e o resto sem quebra no fim também conta."""
    return texto.count("\n") + (1 if texto and not texto.endswith("\n") else 0)


def tem_limite(caminho):
    return (caminho.lower().endswith(EXTENSOES_COM_LIMITE)
            and not any(caminho.startswith(fora) or f"/{fora}" in caminho for fora in FORA_DO_LIMITE))


def excesso_de_linhas(textos):
    """{caminho: {"linhasAcima": n}} dos arquivos acima do limite."""
    return {caminho: {"linhasAcima": linhas_no_editor(texto) - LIMITE_DE_LINHAS} for caminho, texto in textos.items()
            if tem_limite(caminho) and linhas_no_editor(texto) > LIMITE_DE_LINHAS}


class MedidorDeLinhas(unittest.TestCase):

    def test_conta_como_o_editor(self):
        self.assertEqual([linhas_no_editor(t) for t in ("", "a", "a\n", "a\r\nb", "a\n\n")], [0, 1, 1, 2, 2])

    def test_pega_o_que_passa_do_limite_e_deixa_o_resto(self):
        no_limite, acima = "x\n" * LIMITE_DE_LINHAS, "x\n" * (LIMITE_DE_LINHAS + 3)
        textos = {"a.py": no_limite, "b.ts": acima, "notas.txt": acima, "vendor/c.js": acima}
        self.assertEqual(excesso_de_linhas(textos), {"b.ts": {"linhasAcima": 3}})


class TamanhoDosArquivos(TresVerificacoesDaCatraca, unittest.TestCase):
    REGRA = "tamanho-de-arquivo"
    CONSELHO = "divida o arquivo por responsabilidade"

    def medir(self):
        return excesso_de_linhas(ler_do_git([caminho for caminho in arquivos_do_indice() if tem_limite(caminho)]))

    def julga(self, caminho, metrica):
        return tem_limite(caminho)


if __name__ == "__main__":
    unittest.main()
