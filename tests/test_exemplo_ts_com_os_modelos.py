"""Os moldes TypeScript (modelos/testes-ts/) rodam num projeto de exemplo com o package-lock.json fixado, e pegam o
que devem pegar.

Verde: o projeto, como sai dos moldes, passa no vitest e no tsc estrito. Vermelho: cada estrago faz falhar o teste
certo, numa pasta temporária. A linha de base: deixa passar o que já violava, recusa a folga e a entrada nova, e só
se cria uma vez, com MORG_CRIAR_LINHA_DE_BASE=1.
"""

import json
import os
import unittest
from unittest import mock

from projeto_de_exemplo import escrever, git
from projeto_de_exemplo_ts import apagar_ts, montar_ts, rodar_tsc, rodar_vitest

FUNCAO_DE_21_LINHAS = "export function longa() {\n" + "    const passo = 1\n" * 19 + "}\n"


class ProjetoDeExemploTs(unittest.TestCase):

    def setUp(self):
        self.pasta = montar_ts()
        self.addCleanup(apagar_ts, self.pasta)

    def assertFalhaEm(self, molde, teste):
        git(self.pasta, "add", "--", ".")
        codigo, saida = rodar_vitest(self.pasta, molde)
        self.assertNotEqual(codigo, 0, saida[-3000:])
        self.assertIn(f"> {teste}", saida, saida[-3000:])

    def assertPassa(self, molde):
        git(self.pasta, "add", "--", ".")
        codigo, saida = rodar_vitest(self.pasta, molde)
        self.assertEqual(codigo, 0, saida[-3000:])

    def gravar_base(self, regra, valores):
        escrever(self.pasta / "tests" / "linhas-de-base" / f"{regra}.json",
                 json.dumps({"regra": regra, "valores": valores}, indent=2) + "\n")

    def test_como_sai_dos_moldes_passa_no_vitest_e_no_tsc(self):
        codigo, saida = rodar_vitest(self.pasta)
        self.assertEqual(codigo, 0, saida[-3000:])
        self.assertIn("6 passed", saida)
        self.assertEqual(rodar_tsc(self.pasta), (0, ""))

    def test_arquivo_acima_de_500_linhas(self):
        escrever(self.pasta / "src" / "grande.ts", "const linha = 1\n" * 501)
        self.assertFalhaEm("tamanho-de-arquivo", "catraca tamanho-de-arquivo > não piora")

    def test_funcao_de_21_linhas(self):
        escrever(self.pasta / "src" / "longa.ts", FUNCAO_DE_21_LINHAS)
        self.assertFalhaEm("tamanho-de-funcao", "catraca tamanho-de-funcao > não piora")

    def test_identificador_e_caminho_genericos(self):
        for caminho, texto in (("src/carregar.ts", "const { data } = obter()\n"), ("src/utils.ts", "export const a = 1\n")):
            with self.subTest(caminho=caminho):
                escrever(self.pasta / caminho, texto)
                self.assertFalhaEm("nomes-genericos", "catraca nomes-genericos > não piora")
                git(self.pasta, "rm", "-q", "--cached", "--", caminho)
                (self.pasta / caminho).unlink()

    def test_nome_de_topo_repetido(self):
        escrever(self.pasta / "src" / "caixa.ts", "export function totalDoPedido() {\n    return 0\n}\n")
        self.assertFalhaEm("nomes-unicos", "catraca nomes-unicos > não piora")

    def test_alarme_sem_motivo_e_alarme_a_mais(self):
        escrever(self.pasta / "src" / "calado.ts", "// eslint-disable-next-line no-console\nconsole.log(1)\n")
        self.assertFalhaEm("alarmes", "alarmes com motivo > cada alarme tem o motivo na mesma linha, depois de —")
        escrever(self.pasta / "src" / "calado.ts", "// eslint-disable-next-line no-console — o CLI escreve\nconsole.log(1)\n")
        self.assertFalhaEm("alarmes", "catraca alarmes > não piora")

    def test_teste_saltado_sem_condicao(self):
        escrever(self.pasta / "src" / "pedido.test.ts", "import { it } from 'vitest'\nit.skip('soma', () => {})\n")
        self.assertFalhaEm("testes-saltados", "catraca testes-saltados > não piora")

    def test_a_base_deixa_passar_o_que_ja_violava(self):
        escrever(self.pasta / "src" / "longa.ts", FUNCAO_DE_21_LINHAS)
        self.gravar_base("tamanho-de-funcao", {"src/longa.ts": {"funcoesAcima": 1, "linhasAcima": 1}})
        self.assertPassa("tamanho-de-funcao")

    def test_a_base_com_folga(self):
        escrever(self.pasta / "src" / "longa.ts", FUNCAO_DE_21_LINHAS)
        self.gravar_base("tamanho-de-funcao", {"src/longa.ts": {"funcoesAcima": 1, "linhasAcima": 5}})
        self.assertFalhaEm("tamanho-de-funcao", "catraca tamanho-de-funcao > a linha de base não tem folga")

    def test_entrada_nova_na_base_ja_commitada(self):
        self.gravar_base("tamanho-de-funcao", {})
        git(self.pasta, "add", "--", ".")
        git(self.pasta, "commit", "-q", "-m", "base")
        escrever(self.pasta / "src" / "longa.ts", FUNCAO_DE_21_LINHAS)
        self.gravar_base("tamanho-de-funcao", {"src/longa.ts": {"funcoesAcima": 1, "linhasAcima": 1}})
        self.assertFalhaEm("tamanho-de-funcao", "catraca tamanho-de-funcao > a linha de base só encolhe")

    def test_criar_a_base_num_projeto_que_ja_viola(self):
        escrever(self.pasta / "src" / "longa.ts", FUNCAO_DE_21_LINHAS)
        with mock.patch.dict(os.environ, {"MORG_CRIAR_LINHA_DE_BASE": "1"}):
            self.assertFalhaEm("tamanho-de-funcao", "catraca tamanho-de-funcao > não piora")
        base = json.loads((self.pasta / "tests" / "linhas-de-base" / "tamanho-de-funcao.json").read_text("utf-8"))
        self.assertEqual(base, {"regra": "tamanho-de-funcao",
                                "valores": {"src/longa.ts": {"funcoesAcima": 1, "linhasAcima": 1}}})
        self.assertPassa("tamanho-de-funcao")


if __name__ == "__main__":
    unittest.main()
