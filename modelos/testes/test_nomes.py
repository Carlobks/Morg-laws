"""Nomes de arquivos, pastas e identificadores que dizem a função (Morg-laws: nomes únicos e pesquisáveis).

Um nome genérico solto (`utils`, `helper`, `data`…) esconde onde está a lógica e dá dezenas de resultados no grep.
Conta o nome inteiro ou uma parte separada por ponto (`instalar.Comum.ps1`); um nome composto que diz o quê
(`bar_helper.py`, o ajudante da barra) não é solto.
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import re
import subprocess
import unittest
from pathlib import PurePosixPath

from carregar_por_caminho import RAIZ

# Ajuste ao projeto.
PROIBIDOS = {"comum", "common", "utils", "util", "helper", "helpers", "data", "misc", "tmp", "info", "manager",
             "handler", "stuff", "geral", "props"}
EXTENSOES_DE_CODIGO = (".py", ".js", ".mjs", ".jsx", ".ts", ".tsx")
FORA = ("vendor/", "node_modules/")

DECLARACAO = re.compile(r"\b(?:const|let|var|function|def|class|interface|type)\s+(\w+)\b")


def nomes_proibidos(caminhos):
    """Arquivos ou pastas cujo nome (ou uma parte separada por ponto) é uma palavra genérica solta."""
    achados = set()
    for caminho in caminhos:
        for parte in PurePosixPath(caminho).parts:
            if PROIBIDOS & {pedaco.lower() for pedaco in parte.split(".")}:
                achados.add(parte)
    return sorted(achados)


def arquivos_do_repositorio():
    caminhos = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=RAIZ,
                              capture_output=True, text=True, encoding="utf-8", check=True).stdout.splitlines()
    return [caminho for caminho in caminhos if (RAIZ / caminho).exists()
            and not any(caminho.startswith(fora) or f"/{fora}" in caminho for fora in FORA)]


class NomesPesquisaveis(unittest.TestCase):

    def test_o_detector_pega_os_soltos_e_deixa_os_compostos(self):
        self.assertEqual(nomes_proibidos(["a/comum/x.mjs", "tests/instalar.Comum.ps1", "bar_helper.py", "dados.py"]),
                         ["comum", "instalar.Comum.ps1"])

    def test_nenhum_arquivo_ou_pasta_com_nome_generico(self):
        self.assertEqual(nomes_proibidos(arquivos_do_repositorio()), [],
                         "dê um nome que diga a função (menos de 5 resultados no grep)")

    def test_nenhum_identificador_generico_solto(self):
        for caminho in arquivos_do_repositorio():
            if not caminho.endswith(EXTENSOES_DE_CODIGO):
                continue
            nomes = DECLARACAO.findall((RAIZ / caminho).read_text(encoding="utf-8-sig", errors="replace"))
            soltos = [nome for nome in nomes if nome.lower() in PROIBIDOS]
            with self.subTest(arquivo=caminho):
                self.assertEqual(soltos, [], "dê um nome que diga a função")


if __name__ == "__main__":
    unittest.main()
