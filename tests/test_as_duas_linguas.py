"""As duas línguas dão o mesmo veredito: a mesma pasta de casos, corrida pelo molde Python e pelo molde TypeScript
da mesma regra, aprova e reprova os mesmos casos. Isso mostra que os limites, as listas e as linhas de base são iguais.

Um projeto misto leva os moldes das duas línguas. Os casos de uma regra entram juntos, cada um na sua pasta
(`casos/<n>/`), e cada molde corre UMA vez por regra: um caso é reprovado quando a falha cita a pasta dele. Nas regras
de texto (tamanho de arquivo, nomes de arquivo e de pasta, alarmes) os dois moldes julgam os MESMOS arquivos. Nas de
código (tamanho de função, identificadores, nomes de topo, testes saltados) cada molde lê a sua língua, e o caso leva
gémeos: o arquivo .py e o .ts com o mesmo defeito, ou a mesma forma certa. Um caso com «fora do índice» fica no disco
sem `git add`. Os cenários de linha de base (o alarme que muda de arquivo, a base partilhada criada pelas duas
línguas) correm à parte, com commits.
Rodar como script imprime a tabela dos vereditos: py tests/test_as_duas_linguas.py
"""

import json
import os
import shutil
import subprocess
import sys
import unittest
from unittest import mock

from carregar_modelos import MODELOS
from projeto_de_exemplo import escrever, git
from projeto_de_exemplo_ts import apagar_ts, montar_ts, rodar_vitest

MOLDES = {"tamanho-de-arquivo": "test_tamanho_dos_arquivos.py", "tamanho-de-funcao": "test_tamanho_das_funcoes.py",
          "nomes-genericos": "test_nomes.py", "nomes-unicos": "test_nomes_unicos.py", "alarmes": "test_alarmes.py",
          "testes-saltados": "test_testes_saltados.py"}
FORA_DO_INDICE = "fora do índice"


def corpo(linhas, recuo="    "):
    return "".join(f"{recuo}passo_{numero} = {numero}\n" for numero in range(linhas))


def corpo_ts(linhas, recuo="    "):
    return "".join(f"{recuo}const passo{numero} = {numero}\n" for numero in range(linhas))


TEXTO = [  # (regra, caso, arquivos julgados pelos dois moldes, veredito)
    ("tamanho-de-arquivo", "500 linhas", {"no_limite.py": "x = 1\n" * 500}, "aprova"),
    ("tamanho-de-arquivo", "501 linhas em .py", {"acima.py": "x = 1\n" * 501}, "reprova"),
    ("tamanho-de-arquivo", "501 linhas em .ts", {"acima.ts": "const x = 1\n" * 501}, "reprova"),
    ("tamanho-de-arquivo", "600 linhas em .txt", {"notas.txt": "nota\n" * 600}, "aprova"),
    ("nomes-genericos", "arquivo utils.py", {"utils.py": "x = 1\n"}, "reprova"),
    ("nomes-genericos", "parte Comum de um nome", {"instalar.Comum.ps1": "x\n"}, "reprova"),
    ("nomes-genericos", "nome composto", {"bar_helper.md": "x\n"}, "aprova"),
    ("nomes-genericos", "utils.py e utils.ts fora do índice", {"utils.py": "x = 1\n", "utils.ts": "", FORA_DO_INDICE: ""},
     "aprova"),
    ("nomes-unicos", "recibo.py e recibo.ts", {"a/recibo.py": "x = 1\n", "b/recibo.ts": ""}, "reprova"),
    ("nomes-unicos", "boleto.ts e boleto.test.ts", {"boleto.ts": "", "boleto.test.ts": ""}, "aprova"),
    ("alarmes", "eslint-disable sem motivo", {"calado.ts": "// eslint-disable-next-line no-console\n"}, "reprova"),
    ("alarmes", "eslint-disable com motivo, sem base", {"motivado.ts": "// eslint-disable-line no-console — o CLI\n"},
     "reprova"),
    ("alarmes", "noqa num .py", {"calado.py": "import os  # noqa: F401 — exemplo\n"}, "reprova"),
    ("alarmes", "texto que fala do alarme", {"fala.ts": "const aviso = 'nada de eslint-disable'\n"}, "aprova"),
]

GEMEOS = [  # (regra, caso, arquivos para o molde Python, arquivos para o molde TypeScript, veredito)
    ("tamanho-de-funcao", "função de 20 linhas", {"vinte.py": "def vinte():\n" + corpo(19)},
     {"vinte.ts": "export function vinte() {\n" + corpo_ts(18) + "}\n"}, "aprova"),
    ("tamanho-de-funcao", "função de 21 linhas", {"longa.py": "def longa():\n" + corpo(20)},
     {"longa.ts": "export function longa() {\n" + corpo_ts(19) + "}\n"}, "reprova"),
    ("tamanho-de-funcao", "decorador fora da conta", {"metodo.py": "class Pedido:\n    @property\n"
                                                      "    def somar(self):\n" + corpo(19, " " * 8)},
     {"metodo.ts": "class Pedido {\n    @registrar()\n    somar() {\n" + corpo_ts(18, " " * 8) + "    }\n}\n"},
     "aprova"),
    ("tamanho-de-funcao", "20 de código e 3 comentários no fim", {"notas.py": "def notas():\n" + corpo(19)
                                                                  + "    # a\n    # b\n    # c\n"},
     {"notas.ts": "export function notas() {\n" + corpo_ts(18) + "    // a\n    // b\n    // c\n}\n"}, "reprova"),
    ("tamanho-de-funcao", "dois métodos com o mesmo nome, o 1.º longo",
     {"correr.py": "class A:\n    def correr(self):\n" + corpo(26, " " * 8) + "class B:\n    def correr(self):\n        pass\n"},
     {"correr.ts": "class A {\n    correr() {\n" + corpo_ts(25, " " * 8) + "    }\n}\nclass B {\n    correr() {}\n}\n"},
     "reprova"),
    ("tamanho-de-funcao", "teste longo", {"test_pedido.py": "class Pedido:\n    def test_soma(self):\n" + corpo(20, " " * 8)},
     {"pedido.test.ts": "describe('pedido', () => {\n    it('soma', () => {\n" + corpo_ts(20, " " * 8)
      + "    })\n})\n"}, "reprova"),
    ("tamanho-de-funcao", "agrupador longo, testes curtos", {"test_caixa.py": "class Caixa:\n"
                                                             + "    def test_a(self):\n        pass\n" * 12},
     {"caixa.test.ts": "describe('caixa', () => {\n" + "    it('a', () => {\n        usar()\n    })\n" * 12
      + "})\n"}, "aprova"),
    ("nomes-genericos", "identificador desempacotado", {"carregar.py": "data, erro = ler()\n"},
     {"carregar.ts": "const { data } = ler()\n"}, "reprova"),
    ("nomes-genericos", "parâmetro genérico", {"pagar.py": "def pagar(info):\n    return info\n"},
     {"pagar.ts": "export function pagar(info: string) {\n    return info\n}\n"}, "reprova"),
    ("nomes-genericos", "campo genérico de um tipo", {"pedido.py": "class Pedido(TypedDict):\n    data: str\n"},
     {"pedido.ts": "interface Pedido { data: string }\n"}, "reprova"),
    ("nomes-genericos", "membro genérico de um enum", {"cor.py": "class Cor(Enum):\n    data = 1\n"},
     {"cor.ts": "export enum Cor { data = 1 }\n"}, "reprova"),
    ("nomes-genericos", "uso não é declaração", {"mostrar.py": "print(pedido.data)\n"},
     {"mostrar.ts": "usar(pedido.data)\n"}, "aprova"),
    ("nomes-genericos", "nome composto", {"somar.py": "dados_do_pedido = 1\n"},
     {"somar.ts": "const dadosDoPedido = 1\n"}, "aprova"),
    ("nomes-unicos", "função de topo repetida", {"frete_a.py": "def calcular_frete():\n    pass\n",
                                                 "frete_b.py": "def calcular_frete():\n    pass\n"},
     {"frete-a.ts": "export function calcularFrete() {}\n", "frete-b.ts": "function calcularFrete() {}\n"},
     "reprova"),
    ("nomes-unicos", "main repetido e nomes locais", {"x_a.py": "def main():\n    total = 1\n",
                                                      "x_b.py": "def main():\n    total = 2\n"},
     {"x-a.ts": "export function main() { const total = 1 }\n",
      "x-b.ts": "export function main() { const total = 2 }\n"}, "aprova"),
    ("testes-saltados", "salta sempre", {"test_salto.py": "@unittest.skip('lento')\ndef test_a(): pass\n"},
     {"salto.test.ts": "it.skip('a', () => {})\n"}, "reprova"),
    ("testes-saltados", "condição sem motivo", {"test_salto.py": "@unittest.skipIf(x, '')\ndef test_a(): pass\n"},
     {"salto.test.ts": "it('a', (contexto) => { contexto.skip(semRede) })\n"}, "reprova"),
    ("testes-saltados", "condição com motivo", {"test_salto.py": "@unittest.skipIf(x, 'rede')\ndef test_a(): pass\n"},
     {"salto.test.ts": "it.skipIf(semRede)('a', () => {})\n"}, "aprova"),
    ("testes-saltados", "o test.skip do Playwright (no vitest salta sempre)", None,
     {"salto.test.ts": "test.skip(semRede, 'precisa da rede')\n"}, "reprova"),
    ("testes-saltados", "salto no corpo, sem condição", {"test_salto.py": "def test_a(self):\n    self.skipTest('x')\n"},
     {"salto.test.ts": "it('a', (contexto) => { contexto.skip('x') })\n"}, "reprova"),
    ("testes-saltados", "salto com motivo num if", {"test_salto.py": "def test_a(self):\n    if x:\n"
                                                    "        self.skipTest('sem rede')\n"},
     {"salto.test.ts": "it('a', (contexto) => { if (semRede) contexto.skip('sem rede') })\n"}, "aprova"),
    ("testes-saltados", "salto com motivo num except/catch", {"test_salto.py": "def test_a(self):\n    try:\n"
                                                              "        import numpy\n    except ImportError:\n"
                                                              "        self.skipTest('sem numpy')\n"},
     {"salto.test.ts": "it('a', async (contexto) => { try { await abrir() } catch { contexto.skip('sem o serviço') } })\n"},
     "aprova"),
    ("testes-saltados", ".only.each (só TypeScript)", None, {"so.test.ts": "test.only.each([1])('a', () => {})\n"},
     "reprova"),
    ("testes-saltados", "as opções { skip: true } do vitest (só TypeScript)", None,
     {"opcoes.test.ts": "it('a', { skip: true }, () => {})\n"}, "reprova"),
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
    return resultado.returncode, resultado.stderr


def rodar_molde_ts(pasta, regra):
    return rodar_vitest(pasta, f"tests/catracas/{regra}.test.ts")


def casos_da_regra(regra):
    """[(caso, arquivos para o Python, arquivos para o TypeScript, veredito)] de uma regra, os de texto e os gémeos."""
    return ([(caso, arquivos, arquivos, veredito) for r, caso, arquivos, veredito in TEXTO if r == regra]
            + [(caso, de_py, de_ts, veredito) for r, caso, de_py, de_ts, veredito in GEMEOS if r == regra])


def veredito_de_cada_caso(pasta, regra, casos, lado, correr):
    """{número do caso: 'aprova' | 'reprova' | '—'} numa só corrida do molde com todos os casos de um lado."""
    postos = []
    for numero, caso in enumerate(casos):
        arquivos = caso[lado] or {}
        for nome, texto in arquivos.items():
            if nome != FORA_DO_INDICE:
                escrever(pasta / f"casos/{numero}/{nome}", texto)
        if arquivos and FORA_DO_INDICE not in arquivos:
            postos.append(f"casos/{numero}")
    if postos:
        git(pasta, "add", "--", *postos)
    _, saida = correr(pasta, regra)
    vereditos = {numero: ("—" if not caso[lado] else "reprova" if f"casos/{numero}/" in saida else "aprova")
                 for numero, caso in enumerate(casos)}
    git(pasta, "rm", "-r", "-q", "--cached", "--ignore-unmatch", "--", "casos")
    shutil.rmtree(pasta / "casos", ignore_errors=True)
    return vereditos


def veredictos(pasta):
    """[(regra, caso, veredito do Python, veredito do TypeScript, esperado)] de todos os casos."""
    linhas = []
    for regra in MOLDES:
        casos = casos_da_regra(regra)
        do_python = veredito_de_cada_caso(pasta, regra, casos, 1, rodar_molde_python)
        do_ts = veredito_de_cada_caso(pasta, regra, casos, 2, rodar_molde_ts)
        linhas += [(regra, caso[0], do_python[numero], do_ts[numero], caso[3]) for numero, caso in enumerate(casos)]
    return linhas


def de_acordo(linha):
    """Os dois vereditos que existem são iguais entre si e ao esperado."""
    return all(veredito in ("—", linha[4]) for veredito in linha[2:4])


def gravar_base(pasta, regra, valores):
    escrever(pasta / "tests" / "linhas-de-base" / f"{regra}.json", json.dumps({"regra": regra, "valores": valores}) + "\n")


def commitar(pasta):
    git(pasta, "add", "--", ".")
    git(pasta, "commit", "-q", "-m", "chore: base")


def cenario_do_alarme_que_muda_de_arquivo(pasta):
    """Achado 3: a base guarda a contagem por tipo; o mesmo alarme noutro arquivo não a sobe, nas duas línguas."""
    escrever(pasta / "src/a.ts", "// eslint-disable-next-line no-console — o CLI\n")
    gravar_base(pasta, "alarmes", {"*": {"eslint-disable": 1}})
    commitar(pasta)
    git(pasta, "rm", "-q", "--", "src/a.ts")
    escrever(pasta / "src/b.ts", "// eslint-disable-next-line no-console — o CLI\n")
    git(pasta, "add", "--", ".")
    return rodar_molde_python(pasta, "alarmes")[0], rodar_molde_ts(pasta, "alarmes")[0]


def cenario_da_base_partilhada(pasta):
    """Achado 4: com a variável, o Python cria a base de nomes únicos e o TypeScript junta-lhe as suas métricas."""
    for nome, texto in (("src/pedido_a.py", "def calcular():\n    pass\n"), ("src/pedido_b.py", "def calcular():\n    pass\n"),
                        ("src/soma-a.ts", "export function somar() {}\n"), ("src/soma-b.ts", "export function somar() {}\n")):
        escrever(pasta / nome, texto)
    with mock.patch.dict(os.environ, {"MORG_CRIAR_LINHA_DE_BASE": "1"}):
        git(pasta, "add", "--", ".")
        criou = rodar_molde_python(pasta, "nomes-unicos")[0]
        git(pasta, "add", "--", ".")
        juntou = rodar_molde_ts(pasta, "nomes-unicos")[0]
    git(pasta, "add", "--", ".")
    return criou, juntou, rodar_molde_python(pasta, "nomes-unicos")[0], rodar_molde_ts(pasta, "nomes-unicos")[0]


class AsDuasLinguas(unittest.TestCase):

    def setUp(self):
        # A variável do CI do próprio Morg-laws aponta para um commit deste repositório, não do projeto misto.
        self.enterContext(mock.patch.dict(os.environ))
        os.environ.pop("MORG_BASE_DE_COMPARACAO", None)
        self.pasta = montar_projeto_misto()
        self.addCleanup(apagar_ts, self.pasta)

    def test_o_projeto_misto_passa_sem_casos_nas_duas_linguas(self):
        self.assertEqual([(regra, rodar_molde_python(self.pasta, regra)[0], rodar_molde_ts(self.pasta, regra)[0])
                          for regra in MOLDES], [(regra, 0, 0) for regra in MOLDES])

    def test_o_mesmo_veredito_e_o_esperado(self):
        self.assertEqual([linha for linha in veredictos(self.pasta) if not de_acordo(linha)], [])

    def test_o_alarme_que_muda_de_arquivo_passa_nas_duas(self):
        self.assertEqual(cenario_do_alarme_que_muda_de_arquivo(self.pasta), (0, 0))

    def test_a_base_partilhada_serve_as_duas_linguas(self):
        # Cada uma falha até ao git add da base que gravou; depois, as duas passam com a mesma base.
        self.assertEqual(cenario_da_base_partilhada(self.pasta), (1, 1, 0, 0))
        base = json.loads((self.pasta / "tests" / "linhas-de-base" / "nomes-unicos.json").read_text("utf-8"))
        self.assertEqual(sorted(base["valores"]), ["src/pedido_a.py", "src/pedido_b.py", "src/soma-a.ts", "src/soma-b.ts"])


def imprimir_a_tabela():
    pasta = montar_projeto_misto()
    try:
        print("| Regra | Caso | Python | TypeScript | Esperado |\n|---|---|---|---|---|")
        for linha in veredictos(pasta):
            print("| " + " | ".join(linha) + " |")
    finally:
        apagar_ts(pasta)


if __name__ == "__main__":
    imprimir_a_tabela()
