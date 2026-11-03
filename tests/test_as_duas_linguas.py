"""As duas línguas dão o mesmo veredito: a mesma pasta de casos, corrida pelo molde Python e pelo molde TypeScript
da mesma regra, aprova e reprova os mesmos casos. Isso mostra que os limites e as listas são iguais.

Um projeto misto leva os moldes das duas línguas. Cada caso entra sozinho no índice, corre o molde Python e o
TypeScript da regra, e sai. Nas regras de texto (tamanho de arquivo, nomes de arquivo e de pasta, alarmes) os dois
moldes julgam os MESMOS arquivos. Nas de código (tamanho de função, identificadores, nomes de topo, testes saltados)
cada molde lê a sua língua, e o caso leva gémeos: o arquivo .py e o .ts com o mesmo defeito, ou a mesma forma certa.
Rodar como script imprime a tabela dos vereditos: py tests/test_as_duas_linguas.py
"""

import shutil
import subprocess
import sys
import unittest

from carregar_modelos import MODELOS
from projeto_de_exemplo import escrever, git
from projeto_de_exemplo_ts import apagar_ts, montar_ts, rodar_vitest

MOLDES = {"tamanho-de-arquivo": "test_tamanho_dos_arquivos.py", "tamanho-de-funcao": "test_tamanho_das_funcoes.py",
          "nomes-genericos": "test_nomes.py", "nomes-unicos": "test_nomes_unicos.py", "alarmes": "test_alarmes.py",
          "testes-saltados": "test_testes_saltados.py"}


def corpo(linhas, recuo="    "):
    return "".join(f"{recuo}passo_{numero} = {numero}\n" for numero in range(linhas))


def corpo_ts(linhas, recuo="    "):
    return "".join(f"{recuo}const passo{numero} = {numero}\n" for numero in range(linhas))


TEXTO = [  # (regra, caso, arquivos julgados pelos dois moldes, veredito)
    ("tamanho-de-arquivo", "500 linhas", {"casos/no_limite.py": "x = 1\n" * 500}, "aprova"),
    ("tamanho-de-arquivo", "501 linhas em .py", {"casos/acima.py": "x = 1\n" * 501}, "reprova"),
    ("tamanho-de-arquivo", "501 linhas em .ts", {"casos/acima.ts": "const x = 1\n" * 501}, "reprova"),
    ("tamanho-de-arquivo", "600 linhas em .txt", {"casos/notas.txt": "nota\n" * 600}, "aprova"),
    ("nomes-genericos", "arquivo utils.py", {"casos/utils.py": "x = 1\n"}, "reprova"),
    ("nomes-genericos", "parte Comum de um nome", {"casos/instalar.Comum.ps1": "x\n"}, "reprova"),
    ("nomes-genericos", "nome composto", {"casos/bar_helper.md": "x\n"}, "aprova"),
    ("nomes-unicos", "recibo.py e recibo.ts", {"casos/a/recibo.py": "x = 1\n", "casos/b/recibo.ts": ""}, "reprova"),
    ("nomes-unicos", "recibo.ts e recibo.test.ts", {"casos/recibo.ts": "", "casos/recibo.test.ts": ""}, "aprova"),
    ("alarmes", "eslint-disable sem motivo", {"casos/calado.ts": "// eslint-disable-next-line no-console\n"}, "reprova"),
    ("alarmes", "eslint-disable com motivo", {"casos/calado.ts": "// eslint-disable-line no-console — o CLI\n"},
     "reprova"),
    ("alarmes", "noqa num .py", {"casos/calado.py": "import os  # noqa: F401 — exemplo\n"}, "reprova"),
    ("alarmes", "texto que fala do alarme", {"casos/fala.ts": "const aviso = 'nada de eslint-disable'\n"}, "aprova"),
]

GEMEOS = [  # (regra, caso, arquivos para o molde Python, arquivos para o molde TypeScript, veredito)
    ("tamanho-de-funcao", "função de 20 linhas", {"casos/vinte.py": "def vinte():\n" + corpo(19)},
     {"casos/vinte.ts": "export function vinte() {\n" + corpo_ts(18) + "}\n"}, "aprova"),
    ("tamanho-de-funcao", "função de 21 linhas", {"casos/longa.py": "def longa():\n" + corpo(20)},
     {"casos/longa.ts": "export function longa() {\n" + corpo_ts(19) + "}\n"}, "reprova"),
    ("tamanho-de-funcao", "decorador fora da conta", {"casos/metodo.py": "class Pedido:\n    @property\n"
                                                      "    def somar(self):\n" + corpo(19, " " * 8)},
     {"casos/metodo.ts": "class Pedido {\n    @registrar()\n    somar() {\n" + corpo_ts(18, " " * 8) + "    }\n}\n"},
     "aprova"),
    ("tamanho-de-funcao", "teste longo", {"casos/test_pedido.py": "class Pedido:\n    def test_soma(self):\n"
                                          + corpo(20, " " * 8)},
     {"casos/pedido.test.ts": "describe('pedido', () => {\n    it('soma', () => {\n" + corpo_ts(20, " " * 8)
      + "    })\n})\n"}, "reprova"),
    ("tamanho-de-funcao", "agrupador longo, testes curtos", {"casos/test_caixa.py": "class Caixa:\n"
                                                             + "    def test_a(self):\n        pass\n" * 12},
     {"casos/caixa.test.ts": "describe('caixa', () => {\n" + "    it('a', () => {\n        usar()\n    })\n" * 12
      + "})\n"}, "aprova"),
    ("nomes-genericos", "identificador desempacotado", {"casos/carregar.py": "data, erro = ler()\n"},
     {"casos/carregar.ts": "const { data } = ler()\n"}, "reprova"),
    ("nomes-genericos", "parâmetro genérico", {"casos/pagar.py": "def pagar(info):\n    return info\n"},
     {"casos/pagar.ts": "export function pagar(info: string) {\n    return info\n}\n"}, "reprova"),
    ("nomes-genericos", "uso não é declaração", {"casos/mostrar.py": "print(pedido.data)\n"},
     {"casos/mostrar.ts": "usar(pedido.data)\n"}, "aprova"),
    ("nomes-genericos", "nome composto", {"casos/somar.py": "dados_do_pedido = 1\n"},
     {"casos/somar.ts": "const dadosDoPedido = 1\n"}, "aprova"),
    ("nomes-unicos", "função de topo repetida", {"casos/frete_a.py": "def calcular_frete():\n    pass\n",
                                                 "casos/frete_b.py": "def calcular_frete():\n    pass\n"},
     {"casos/frete-a.ts": "export function calcularFrete() {}\n", "casos/frete-b.ts": "function calcularFrete() {}\n"},
     "reprova"),
    ("nomes-unicos", "main repetido e nomes locais", {"casos/x_a.py": "def main():\n    total = 1\n",
                                                      "casos/x_b.py": "def main():\n    total = 2\n"},
     {"casos/x-a.ts": "export function main() { const total = 1 }\n",
      "casos/x-b.ts": "export function main() { const total = 2 }\n"}, "aprova"),
    ("testes-saltados", "salta sempre", {"casos/test_salto.py": "@unittest.skip('lento')\ndef test_a(): pass\n"},
     {"casos/salto.test.ts": "it.skip('a', () => {})\n"}, "reprova"),
    ("testes-saltados", "condição sem motivo", {"casos/test_salto.py": "@unittest.skipIf(x, '')\ndef test_a(): pass\n"},
     {"casos/salto.test.ts": "test.skip(semRede)\n"}, "reprova"),
    ("testes-saltados", "condição com motivo", {"casos/test_salto.py": "@unittest.skipIf(x, 'rede')\ndef test_a(): pass\n"},
     {"casos/salto.test.ts": "test.skip(semRede, 'rede')\n"}, "aprova"),
    ("testes-saltados", "salto no corpo, sem condição", {"casos/test_salto.py": "def test_a(self):\n    self.skipTest('x')\n"},
     {"casos/salto.test.ts": "it('a', (contexto) => { contexto.skip('x') })\n"}, "reprova"),
    ("testes-saltados", "salto no corpo, com condição", {"casos/test_salto.py": "def test_a(self):\n    if x:\n"
                                                         "        self.skipTest('x')\n"},
     {"casos/salto.test.ts": "it('a', (contexto) => { contexto.skip(x, 'x') })\n"}, "aprova"),
]


def montar_projeto_misto():
    """O projeto de exemplo TypeScript com os moldes Python em tests/, como num projeto que usa as duas línguas."""
    pasta = montar_ts()
    for molde in (MODELOS / "testes").glob("*.py"):
        shutil.copy2(molde, pasta / "tests" / molde.name)
    git(pasta, "add", "--", ".")
    return pasta


def rodar_molde_python(pasta, regra):
    resultado = subprocess.run([sys.executable, "-I", "-m", "unittest", "discover", "-s", "tests", "-p", MOLDES[regra]],
                               cwd=pasta, capture_output=True, text=True, encoding="utf-8", errors="replace",
                               check=False, timeout=300)
    return resultado.returncode


def veredito_do_caso(pasta, regra, arquivos, correr):
    """'aprova' ou 'reprova' do molde `correr` com só `arquivos` acrescentados ao projeto."""
    for caminho, texto in arquivos.items():
        escrever(pasta / caminho, texto)
    git(pasta, "add", "--", *arquivos)
    try:
        return "aprova" if correr(pasta, regra) == 0 else "reprova"
    finally:
        git(pasta, "rm", "-q", "--cached", "--", *arquivos)
        for caminho in arquivos:
            (pasta / caminho).unlink()


def rodar_molde_ts(pasta, regra):
    return rodar_vitest(pasta, f"tests/catracas/{regra}.test.ts")[0]


def veredictos(pasta):
    """[(regra, caso, arquivos, veredito do Python, veredito do TypeScript, esperado)] de todos os casos."""
    linhas = []
    for regra, caso, arquivos, esperado in TEXTO:
        linhas.append((regra, caso, ", ".join(arquivos), veredito_do_caso(pasta, regra, arquivos, rodar_molde_python),
                       veredito_do_caso(pasta, regra, arquivos, rodar_molde_ts), esperado))
    for regra, caso, de_python, de_ts, esperado in GEMEOS:
        linhas.append((regra, caso, ", ".join([*de_python, *de_ts]), veredito_do_caso(pasta, regra, de_python,
                       rodar_molde_python), veredito_do_caso(pasta, regra, de_ts, rodar_molde_ts), esperado))
    return linhas


class AsDuasLinguas(unittest.TestCase):

    def test_o_projeto_misto_passa_sem_casos_nas_duas_linguas(self):
        pasta = montar_projeto_misto()
        self.addCleanup(apagar_ts, pasta)
        self.assertEqual([(regra, rodar_molde_python(pasta, regra), rodar_molde_ts(pasta, regra)) for regra in MOLDES],
                         [(regra, 0, 0) for regra in MOLDES])

    def test_o_mesmo_veredito_e_o_esperado(self):
        pasta = montar_projeto_misto()
        self.addCleanup(apagar_ts, pasta)
        divergentes = [linha for linha in veredictos(pasta) if not linha[3] == linha[4] == linha[5]]
        self.assertEqual(divergentes, [])


def imprimir_a_tabela():
    pasta = montar_projeto_misto()
    try:
        print("| Regra | Caso | Arquivos | Python | TypeScript | Esperado |\n|---|---|---|---|---|---|")
        for linha in veredictos(pasta):
            print("| " + " | ".join(linha) + " |")
    finally:
        apagar_ts(pasta)


if __name__ == "__main__":
    imprimir_a_tabela()
