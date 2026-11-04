"""Os moldes TypeScript (modelos/testes-ts/) rodam num projeto de exemplo com o package-lock.json fixado, e pegam o
que devem pegar.

Verde: o projeto, como sai dos moldes, passa no vitest e no tsc estrito. Vermelho: cada estrago faz falhar o teste
certo, numa pasta temporária; os estragos independentes juntam-se numa só corrida do vitest, e cada um é conferido
pelo teste que falha e pelo caminho que a falha cita. A linha de base: deixa passar o que já violava, recusa a folga
e a entrada nova (também no CI, contra a base do ramo de destino), deixa o alarme mudar de arquivo e subir só com a
linha `Alarme-novo:`, e cria-se uma vez, com MORG_CRIAR_LINHA_DE_BASE=1.
"""

import json
import os
import unittest
from unittest import mock

from projeto_de_exemplo import escrever, git
from projeto_de_exemplo_ts import apagar_ts, montar_ts, rodar_tsc, rodar_vitest

FUNCAO_DE_21_LINHAS = "export function longa() {\n" + "    const passo = 1\n" * 19 + "}\n"
ALARME_COM_MOTIVO = "// eslint-disable-next-line no-console — o CLI escreve no terminal\nconsole.log(1)\n"
# Os estragos que se juntam numa corrida: (arquivo, texto, teste que falha, trecho que a falha cita).
ESTRAGOS = [
    ("src/grande.ts", "const linha = 1\n" * 501, "catraca tamanho-de-arquivo > não piora", "src/grande.ts: linhasAcima 1"),
    ("src/longa.ts", FUNCAO_DE_21_LINHAS, "catraca tamanho-de-funcao > não piora", "src/longa.ts: funcoesAcima 1"),
    ("src/carregar.ts", "const { data } = obter()\n", "catraca nomes-genericos > não piora",
     "src/carregar.ts: nomesGenericos 1"),
    ("src/campos.ts", "export interface Pedido { info: string }\n", "catraca nomes-genericos > não piora",
     "src/campos.ts: nomesGenericos 1"),
    ("src/utils.ts", "export const moeda = 1\n", "catraca nomes-genericos > não piora", "src/utils.ts: caminhoGenerico 1"),
    ("src/caixa.ts", "export function totalDoPedido() {\n    return 0\n}\n", "catraca nomes-unicos > não piora",
     "src/caixa.ts: nomesDeTopoRepetidos 1"),
    ("src/calado.ts", "// eslint-disable-next-line no-console\nconsole.log(1)\n",
     "alarmes com motivo > cada alarme tem o motivo na mesma linha, depois de —", "src/calado.ts:1 eslint-disable"),
    ("src/tela.ts", "// @ts-expect-error — o tipo da lib está errado\nconst a: number = 'x'\n",
     "catraca alarmes > não piora", "src/tela.ts:1"),
    ("src/pedido.test.ts", "import { it } from 'vitest'\nit.skip('soma', () => {})\n",
     "catraca testes-saltados > não piora", "src/pedido.test.ts: testesSaltados 1"),
]


class ProjetoDeExemploTs(unittest.TestCase):

    def setUp(self):
        # A variável do CI do próprio Morg-laws aponta para um commit deste repositório, não do exemplo.
        self.enterContext(mock.patch.dict(os.environ))
        os.environ.pop("MORG_BASE_DE_COMPARACAO", None)
        self.pasta = montar_ts()
        self.addCleanup(apagar_ts, self.pasta)

    def assertFalhaEm(self, molde, teste):
        git(self.pasta, "add", "--", ".")
        codigo, saida = rodar_vitest(self.pasta, f"tests/catracas/{molde}")
        self.assertNotEqual(codigo, 0, saida[-3000:])
        self.assertIn(f"> {teste}", saida, saida[-3000:])
        return saida

    def assertPassa(self, molde):
        git(self.pasta, "add", "--", ".")
        codigo, saida = rodar_vitest(self.pasta, f"tests/catracas/{molde}")
        self.assertEqual(codigo, 0, saida[-3000:])

    def gravar_base(self, regra, valores):
        escrever(self.pasta / "tests" / "linhas-de-base" / f"{regra}.json",
                 json.dumps({"regra": regra, "valores": valores}, indent=2) + "\n")

    def commitar(self, mensagem="chore: base"):
        git(self.pasta, "add", "--", ".")
        git(self.pasta, "commit", "-q", "-m", mensagem)
        return git(self.pasta, "rev-parse", "HEAD").stdout.strip()

    def test_como_sai_dos_moldes_passa_no_vitest_e_no_tsc(self):
        codigo, saida = rodar_vitest(self.pasta)
        self.assertEqual(codigo, 0, saida[-3000:])
        self.assertIn("6 passed", saida)
        self.assertEqual(rodar_tsc(self.pasta), (0, ""))

    def test_cada_estrago_cai_no_seu_teste(self):
        for caminho, texto, _, _ in ESTRAGOS:
            escrever(self.pasta / caminho, texto)
        git(self.pasta, "add", "--", ".")
        codigo, saida = rodar_vitest(self.pasta, "tests/catracas")
        self.assertNotEqual(codigo, 0, saida[-3000:])
        for caminho, _, teste, trecho in ESTRAGOS:
            with self.subTest(estrago=caminho):
                self.assertIn(f"> {teste}", saida)
                self.assertIn(trecho, saida)

    def test_a_base_deixa_passar_o_que_ja_violava_mas_sem_folga(self):
        escrever(self.pasta / "src" / "longa.ts", FUNCAO_DE_21_LINHAS)
        self.gravar_base("tamanho-de-funcao", {"src/longa.ts": {"funcoesAcima": 1, "linhasAcima": 1}})
        self.assertPassa("tamanho-de-funcao")
        self.gravar_base("tamanho-de-funcao", {"src/longa.ts": {"funcoesAcima": 1, "linhasAcima": 5}})
        self.assertFalhaEm("tamanho-de-funcao", "catraca tamanho-de-funcao > a linha de base não tem folga")

    def test_entrada_nova_na_base_ja_commitada(self):
        self.gravar_base("tamanho-de-funcao", {})
        self.commitar()
        escrever(self.pasta / "src" / "longa.ts", FUNCAO_DE_21_LINHAS)
        self.gravar_base("tamanho-de-funcao", {"src/longa.ts": {"funcoesAcima": 1, "linhasAcima": 1}})
        self.assertFalhaEm("tamanho-de-funcao", "catraca tamanho-de-funcao > a linha de base só encolhe")

    def test_no_ci_a_entrada_nova_ja_commitada_tambem_e_recusada(self):
        self.gravar_base("tamanho-de-funcao", {})
        anterior = self.commitar()
        escrever(self.pasta / "src" / "longa.ts", FUNCAO_DE_21_LINHAS)
        self.gravar_base("tamanho-de-funcao", {"src/longa.ts": {"funcoesAcima": 1, "linhasAcima": 1}})
        self.commitar("feat: entrada nova")
        os.environ["MORG_BASE_DE_COMPARACAO"] = anterior
        self.assertFalhaEm("tamanho-de-funcao", "catraca tamanho-de-funcao > a linha de base só encolhe")

    def test_o_alarme_que_muda_de_arquivo_passa(self):
        escrever(self.pasta / "src" / "a.ts", ALARME_COM_MOTIVO)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 1}})
        self.commitar()
        git(self.pasta, "rm", "-q", "--", "src/a.ts")
        escrever(self.pasta / "src" / "b.ts", ALARME_COM_MOTIVO)
        self.assertPassa("alarmes")

    def test_alarme_novo_so_com_a_linha_alarme_novo(self):
        self.gravar_base("alarmes", {})
        anterior = self.commitar()
        escrever(self.pasta / "src" / "a.ts", ALARME_COM_MOTIVO)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 1}})
        self.assertPassa("alarmes")  # no índice, a subida fica para o commit-msg
        self.commitar("feat: alarme novo")
        os.environ["MORG_BASE_DE_COMPARACAO"] = anterior
        self.assertFalhaEm("alarmes", "catraca alarmes > a linha de base só encolhe")  # no CI, sem a linha
        git(self.pasta, "commit", "-q", "--amend", "-m", "feat: alarme novo\n\nAlarme-novo: o CLI escreve no terminal")
        self.assertPassa("alarmes")

    def test_no_ci_cada_subida_dos_alarmes_pede_a_sua_linha(self):
        # Uma linha Alarme-novo: num commit não cobre a subida de outro commit do mesmo push.
        escrever(self.pasta / "src" / "a.ts", ALARME_COM_MOTIVO)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 1}})
        anterior = self.commitar()
        for numero, mensagem in ((2, "feat: b\n\nAlarme-novo: o CLI escreve no terminal"), (3, "feat: c sem a linha")):
            escrever(self.pasta / "src" / f"{numero}.ts", ALARME_COM_MOTIVO)
            self.gravar_base("alarmes", {"*": {"eslint-disable": numero}})
            self.commitar(mensagem)
        os.environ["MORG_BASE_DE_COMPARACAO"] = anterior
        saida = self.assertFalhaEm("alarmes", "catraca alarmes > a linha de base só encolhe")
        self.assertIn("feat: c sem a linha", saida)

    def test_a_base_de_comparacao_que_o_git_nao_conhece_salta_com_o_motivo(self):
        self.gravar_base("tamanho-de-funcao", {})
        self.commitar()
        escrever(self.pasta / "src" / "longa.ts", FUNCAO_DE_21_LINHAS)
        self.gravar_base("tamanho-de-funcao", {"src/longa.ts": {"funcoesAcima": 1, "linhasAcima": 1}})
        self.commitar("feat: entrada nova")
        for desconhecida in ("0" * 40, "nao-existe"):
            with self.subTest(base=desconhecida):
                os.environ["MORG_BASE_DE_COMPARACAO"] = desconhecida
                git(self.pasta, "add", "--", ".")
                codigo, saida = rodar_vitest(self.pasta, "tests/catracas/tamanho-de-funcao", "--reporter=verbose")
                self.assertEqual(codigo, 0, saida[-3000:])
                self.assertIn("↓ tests/catracas/tamanho-de-funcao.test.ts > catraca tamanho-de-funcao > a linha de base só encolhe", saida)
                self.assertIn(f"a base de comparação {desconhecida}", saida)

    def test_criar_a_base_num_projeto_que_ja_viola(self):
        escrever(self.pasta / "src" / "longa.ts", FUNCAO_DE_21_LINHAS)
        os.environ["MORG_CRIAR_LINHA_DE_BASE"] = "1"
        self.assertFalhaEm("tamanho-de-funcao", "catraca tamanho-de-funcao > não piora")
        base = json.loads((self.pasta / "tests" / "linhas-de-base" / "tamanho-de-funcao.json").read_text("utf-8"))
        self.assertEqual(base, {"regra": "tamanho-de-funcao",
                                "valores": {"src/longa.ts": {"funcoesAcima": 1, "linhasAcima": 1}}})
        self.assertPassa("tamanho-de-funcao")


if __name__ == "__main__":
    unittest.main()
