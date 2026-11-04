"""Nomes de arquivos, pastas e identificadores que dizem a função (Morg-laws: nomes únicos e pesquisáveis).

Um nome genérico solto (`utils`, `helper`, `data`…) esconde onde está a lógica e dá dezenas de resultados no grep.
- Arquivos e pastas, de qualquer língua: conta o nome inteiro ou uma parte separada por ponto (`instalar.Comum.ps1`);
  um nome composto que diz o quê (`bar_helper.py`, o ajudante da barra) não é solto.
- Identificadores do Python, lidos pela árvore (`ast`), e não por expressões regulares: funções, classes, métodos,
  parâmetros, os campos de uma classe (`data: str` num TypedDict) e tudo o que nasce numa atribuição, num `for`, num
  `with … as`, num `except … as` ou numa compreensão (`data, erro = ler()` declara `data`). Usar um nome
  (`pedido.data`) não é declará-lo. A caixa não conta.
Por arquivo: `nomesGenericos` (quantos identificadores) e `caminhoGenerico` (1 se o caminho tem um nome solto). Lê
do índice do git, como o molde TypeScript nomes-genericos.test.ts, que lê os identificadores JS/TS com a mesma lista
e julga os mesmos caminhos: as duas línguas dão o mesmo veredito sobre os mesmos casos.
Linha de base: tests/linhas-de-base/nomes-genericos.json (linha_de_base.py).
Limites conhecidos: `import … as data` não conta (importar não é declarar).
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import ast
import unittest
from pathlib import PurePosixPath

from linha_de_base import TresVerificacoesDaCatraca, arquivos_do_indice, ler_do_git

# Ajuste ao projeto. A mesma lista do molde TypeScript nomes-genericos.test.ts.
PROIBIDOS = {"comum", "common", "utils", "util", "helper", "helpers", "data", "misc", "tmp", "temp", "info",
             "manager", "handler", "stuff", "geral", "props", "foo", "bar", "thing", "dados", "coisa", "coisas",
             "auxiliar", "auxiliares", "diversos", "temporario"}
FORA_DOS_NOMES = ("vendor/", "node_modules/")


def caminho_generico(caminho):
    """True se um arquivo ou pasta do caminho tem por nome (ou parte separada por ponto) uma palavra genérica solta."""
    return any(PROIBIDOS & {pedaco.lower() for pedaco in parte.split(".")} for parte in PurePosixPath(caminho).parts)


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


def julga_o_nome(caminho):
    return not any(caminho.startswith(fora) or f"/{fora}" in caminho for fora in FORA_DOS_NOMES)


def excesso_dos_nomes_genericos(caminhos, textos):
    """{caminho: {"nomesGenericos": n, "caminhoGenerico": 1}}: o caminho de todos, os identificadores dos `.py`."""
    excessos = {}
    for caminho in caminhos:
        excesso = {"nomesGenericos": len(identificadores_genericos(textos[caminho])) if caminho in textos else 0,
                   "caminhoGenerico": int(caminho_generico(caminho))}
        if any(excesso.values()):
            excessos[caminho] = {metrica: valor for metrica, valor in excesso.items() if valor}
    return excessos


class DetectorDeNomes(unittest.TestCase):

    def test_o_detector_pega_os_soltos_e_deixa_os_compostos(self):
        caminhos = ["a/comum/x.mjs", "tests/instalar.Comum.ps1", "bar_helper.py", "pedido.py"]
        self.assertEqual([caminho_generico(caminho) for caminho in caminhos], [True, True, False, False])

    def test_o_detector_le_as_declaracoes_pela_arvore(self):
        fonte = ("def carregar(info, *dados):\n    data, (erro, *tmp) = ler()\n    for Coisa in []:\n        pass\n"
                 "    with abrir() as helper:\n        usar(pedido.data, utils[0])\n    try:\n        pass\n"
                 "    except Exception as foo:\n        return [bar for bar in ()]\n"
                 "class Pedido(TypedDict):\n    props: str\n")
        self.assertEqual(sorted(identificadores_genericos(fonte)),
                         ["Coisa", "bar", "dados", "data", "foo", "helper", "info", "props", "tmp"])

    def test_resume_por_arquivo(self):
        textos = {"src/a.py": "data = 1\n", "src/limpo.py": "faturas = 1\n"}
        caminhos = ["src/a.py", "lib/utils/certo.py", "docs/helpers.md", "src/limpo.py"]
        self.assertEqual(excesso_dos_nomes_genericos(caminhos, {**textos, "lib/utils/certo.py": "moeda = 1\n"}),
                         {"src/a.py": {"nomesGenericos": 1}, "lib/utils/certo.py": {"caminhoGenerico": 1},
                          "docs/helpers.md": {"caminhoGenerico": 1}})


class NomesGenericos(TresVerificacoesDaCatraca, unittest.TestCase):
    REGRA = "nomes-genericos"
    CONSELHO = "dê um nome que diga o que guarda (menos de 5 resultados no grep)"

    def medir(self):
        caminhos = [caminho for caminho in arquivos_do_indice() if julga_o_nome(caminho)]
        return excesso_dos_nomes_genericos(caminhos, ler_do_git([c for c in caminhos if c.endswith(".py")]))

    def julga(self, caminho, metrica):
        return julga_o_nome(caminho) and (metrica != "nomesGenericos" or caminho.endswith(".py"))


if __name__ == "__main__":
    unittest.main()
