"""Nomes de topo e de arquivo únicos (Morg-laws: nomes únicos e pesquisáveis; o que já viola não piora).

Dois arquivos com a mesma função `calcular` ou dois `pedido.py` dão dois resultados no grep, e o agente edita o
errado. Por arquivo, conta:
- `nomesDeTopoRepetidos`: quantos nomes do topo do arquivo (funções, classes, constantes e variáveis do corpo do
  módulo, lidos pela árvore) outro arquivo Python também declara. Importar um nome não é declará-lo;
- `nomeDeArquivoRepetido`: 1 se outro arquivo de código, de qualquer língua, tem o mesmo nome sem a última extensão
  (`pedido.py` e `pedido.ts` repetem; `pedido.test.ts` não repete `pedido.ts`).
Ficam de fora o que a língua impõe (`__init__`, `main`, os nomes `__x__`) e os nomes de uma interface comum de
propósito (NOMES_DE_INTERFACE). O molde TypeScript nomes-unicos.test.ts lê o topo do TS com as mesmas isenções.
Linha de base: tests/linhas-de-base/nomes-unicos.json (linha_de_base.py).
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import ast
import unittest
from collections import Counter
from pathlib import PurePosixPath

from linha_de_base import TresVerificacoesDaCatraca, arquivos_do_indice, ler_do_git

# Ajuste ao projeto. Os mesmos do molde TypeScript nomes-unicos.test.ts.
# A interface comum dos portões (erros) e dos hooks (motivo_para_bloquear) do Morg-laws repete-se de propósito.
NOMES_DE_INTERFACE = {"main", "erros", "motivo_para_bloquear"}
ARQUIVOS_COM_NOME_IMPOSTO = {"__init__", "__main__", "conftest"}
EXTENSOES_COM_NOME_UNICO = (".py", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".mts", ".cts", ".tsx")
FORA_DOS_NOMES_UNICOS = ("vendor/", "node_modules/")


def alvos_do_topo(alvo):
    """Os nomes que um alvo de atribuição do topo declara: `A`, `A, (B, *C)`; `x.a` e `x[0]` não."""
    if isinstance(alvo, ast.Name):
        return {alvo.id}
    if isinstance(alvo, ast.Starred):
        return alvos_do_topo(alvo.value)
    if isinstance(alvo, (ast.Tuple, ast.List)):
        return {nome for elemento in alvo.elts for nome in alvos_do_topo(elemento)}
    return set()


def nomes_do_topo(fonte):
    """Os nomes declarados no corpo do módulo, sem repetir e sem os isentos."""
    nomes = set()
    for no in ast.parse(fonte).body:
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            nomes.add(no.name)
        elif isinstance(no, ast.Assign):
            nomes.update(nome for alvo in no.targets for nome in alvos_do_topo(alvo))
        elif isinstance(no, ast.AnnAssign):
            nomes.update(alvos_do_topo(no.target))
    return {nome for nome in nomes if nome not in NOMES_DE_INTERFACE
            and not (nome.startswith("__") and nome.endswith("__"))}


def nome_do_arquivo(caminho):
    """O nome sem a última extensão, ou None se for um nome que a língua impõe."""
    nome = PurePosixPath(caminho).stem
    return None if nome in ARQUIVOS_COM_NOME_IMPOSTO else nome


def tem_nome_unico(caminho):
    return (caminho.lower().endswith(EXTENSOES_COM_NOME_UNICO)
            and not any(caminho.startswith(fora) or f"/{fora}" in caminho for fora in FORA_DOS_NOMES_UNICOS))


def nomes_repetidos(textos):
    """{caminho: {"nomesDeTopoRepetidos": n, "nomeDeArquivoRepetido": 1}} dos arquivos com repetições."""
    topos = {caminho: nomes_do_topo(texto) for caminho, texto in textos.items() if caminho.endswith(".py")}
    vezes_no_topo = Counter(nome for nomes in topos.values() for nome in nomes)
    vezes_do_arquivo = Counter(nome_do_arquivo(caminho) for caminho in textos)
    resultado = {}
    for caminho in textos:
        excesso = {"nomesDeTopoRepetidos": sum(vezes_no_topo[nome] > 1 for nome in topos.get(caminho, ())),
                   "nomeDeArquivoRepetido": int(bool(nome_do_arquivo(caminho)) and
                                                vezes_do_arquivo[nome_do_arquivo(caminho)] > 1)}
        if any(excesso.values()):
            resultado[caminho] = {metrica: valor for metrica, valor in excesso.items() if valor}
    return resultado


class DetectorDeRepeticoes(unittest.TestCase):

    def test_le_o_topo_pela_arvore(self):
        fonte = ("import os\nfrom x import ler\nTAXA = 1\nA, (B, *C) = 1, (2, 3)\nnumero: int = 0\nobj.campo = 2\n"
                 "def pagar():\n    interna = 1\nclass Fatura:\n    total = 0\n__all__ = []\ndef main():\n    pass\n")
        self.assertEqual(nomes_do_topo(fonte), {"TAXA", "A", "B", "C", "numero", "pagar", "Fatura"})

    def test_conta_os_nomes_e_os_arquivos_repetidos(self):
        textos = {"a/pedido.py": "def somar():\n    pass\nSO_DE_A = 1\n", "b/caixa.py": "def somar():\n    pass\n",
                  "c/pedido.ts": "", "c/pedido.test.ts": "", "a/__init__.py": "", "b/__init__.py": ""}
        self.assertEqual(nomes_repetidos(textos), {"a/pedido.py": {"nomesDeTopoRepetidos": 1, "nomeDeArquivoRepetido": 1},
                                                   "b/caixa.py": {"nomesDeTopoRepetidos": 1},
                                                   "c/pedido.ts": {"nomeDeArquivoRepetido": 1}})


class NomesUnicos(TresVerificacoesDaCatraca, unittest.TestCase):
    REGRA = "nomes-unicos"
    CONSELHO = "dê um nome único que diga o quê (git grep antes de criar)"

    def medir(self):
        return nomes_repetidos(ler_do_git([caminho for caminho in arquivos_do_indice() if tem_nome_unico(caminho)]))

    def julga(self, caminho, metrica):
        return tem_nome_unico(caminho) and (metrica != "nomesDeTopoRepetidos" or caminho.endswith(".py"))


if __name__ == "__main__":
    unittest.main()
