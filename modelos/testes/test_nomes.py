"""Nomes de arquivos, pastas e identificadores que dizem a função (Morg-laws: nomes únicos e pesquisáveis).

Um nome genérico solto (`utils`, `helper`, `data`…) esconde onde está a lógica e dá dezenas de resultados no grep.
- Arquivos e pastas, de qualquer língua: conta o nome inteiro ou uma parte separada por ponto (`instalar.Comum.ps1`);
  um nome composto que diz o quê (`bar_helper.py`, o ajudante da barra) não é solto.
- Identificadores do Python, lidos pela árvore (`ast`), e não por expressões regulares: funções, classes,
  parâmetros e tudo o que nasce numa atribuição, num `for`, num `with … as`, num `except … as` ou numa compreensão
  (`data, erro = ler()` declara `data`). Usar um nome (`pedido.data`) não é declará-lo. A caixa não conta.
Os identificadores JS/TS são do molde TypeScript `nomes-genericos.test.ts`, com a mesma lista e a mesma regra dos
arquivos: as duas línguas dão o mesmo veredito sobre os mesmos casos.
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import ast
import subprocess
import unittest
from pathlib import PurePosixPath

from carregar_por_caminho import RAIZ

# Ajuste ao projeto. A mesma lista do molde TypeScript nomes-genericos.test.ts.
PROIBIDOS = {"comum", "common", "utils", "util", "helper", "helpers", "data", "misc", "tmp", "temp", "info",
             "manager", "handler", "stuff", "geral", "props", "foo", "bar", "thing", "dados", "coisa", "coisas",
             "auxiliar", "auxiliares", "diversos", "temporario"}
FORA_DOS_NOMES = ("vendor/", "node_modules/")


def nomes_proibidos(caminhos):
    """Arquivos ou pastas cujo nome (ou uma parte separada por ponto) é uma palavra genérica solta."""
    achados = set()
    for caminho in caminhos:
        for parte in PurePosixPath(caminho).parts:
            if PROIBIDOS & {pedaco.lower() for pedaco in parte.split(".")}:
                achados.add(parte)
    return sorted(achados)


def nomes_do_alvo(alvo):
    """Os nomes que um alvo de atribuição declara: `a`, `a, (b, *c)`; `x.a` e `x[0]` são usos, não declarações."""
    if isinstance(alvo, ast.Name):
        return [alvo.id]
    if isinstance(alvo, ast.Starred):
        return nomes_do_alvo(alvo.value)
    if isinstance(alvo, (ast.Tuple, ast.List)):
        return [nome for elemento in alvo.elts for nome in nomes_do_alvo(elemento)]
    return []


def nomes_declarados_pelo_no(no):
    """Os nomes que este nó da árvore declara (nenhum, se não for uma declaração)."""
    if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return [no.name]
    if isinstance(no, ast.arg):
        return [no.arg]
    if isinstance(no, ast.ExceptHandler):
        return [no.name] if no.name else []
    if isinstance(no, ast.Assign):
        return [nome for alvo in no.targets for nome in nomes_do_alvo(alvo)]
    if isinstance(no, ast.withitem):
        return nomes_do_alvo(no.optional_vars)
    if isinstance(no, (ast.AnnAssign, ast.For, ast.AsyncFor, ast.comprehension, ast.NamedExpr)):
        return nomes_do_alvo(no.target)
    return []


def identificadores_genericos(fonte):
    """Os identificadores genéricos que um código Python declara, um por declaração."""
    return [nome for no in ast.walk(ast.parse(fonte)) for nome in nomes_declarados_pelo_no(no)
            if nome.lower() in PROIBIDOS]


def arquivos_com_nome():
    caminhos = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=RAIZ,
                              capture_output=True, text=True, encoding="utf-8", check=True).stdout.splitlines()
    return [caminho for caminho in caminhos if (RAIZ / caminho).exists()
            and not any(caminho.startswith(fora) or f"/{fora}" in caminho for fora in FORA_DOS_NOMES)]


class NomesPesquisaveis(unittest.TestCase):

    def test_o_detector_pega_os_soltos_e_deixa_os_compostos(self):
        self.assertEqual(nomes_proibidos(["a/comum/x.mjs", "tests/instalar.Comum.ps1", "bar_helper.py", "pedido.py"]),
                         ["comum", "instalar.Comum.ps1"])

    def test_o_detector_le_as_declaracoes_pela_arvore(self):
        fonte = ("def carregar(info, *dados):\n    data, (erro, *tmp) = ler()\n    for Coisa in []:\n        pass\n"
                 "    with abrir() as helper:\n        usar(pedido.data, utils[0])\n    try:\n        pass\n"
                 "    except Exception as foo:\n        return [bar for bar in ()]\n")
        self.assertEqual(sorted(identificadores_genericos(fonte)),
                         ["Coisa", "bar", "dados", "data", "foo", "helper", "info", "tmp"])

    def test_nenhum_arquivo_ou_pasta_com_nome_generico(self):
        self.assertEqual(nomes_proibidos(arquivos_com_nome()), [],
                         "dê um nome que diga a função (menos de 5 resultados no grep)")

    def test_nenhum_identificador_generico_solto(self):
        for caminho in arquivos_com_nome():
            if caminho.endswith(".py"):
                with self.subTest(arquivo=caminho):
                    self.assertEqual(identificadores_genericos((RAIZ / caminho).read_text(encoding="utf-8-sig")), [],
                                     "dê um nome que diga a função")


if __name__ == "__main__":
    unittest.main()
