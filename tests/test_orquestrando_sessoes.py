"""A `orquestrando-sessoes` guarda a regra do título das sessões na seção «Várias sessões na mesma pasta»,
conferida sem rede e sobre o texto:

- o item «O título diz o estado» existe nessa seção, com o formato literal `ESTADO | ÁREA · assunto` e os quatro
  estados (`ATIVO`, `ESPERA`, `OK`, `OFF`);
- o item diz que quem orquestra troca o título da filha e que o terminal renomeia com `/rename`;
- só o item não leva palavras nem construções do português de Portugal (o resto da skill ainda leva).
As funções recebem o texto, para os casos de erro serem provados sem tocar na skill.
"""

import re
import unittest

from carregar_modelos import RAIZ
from leitura_do_repositorio import ler
from lingua_do_brasil import erros_de_lingua

SKILL = RAIZ / "skills" / "orquestrando-sessoes" / "SKILL.md"
SECAO = "Várias sessões na mesma pasta"
INICIO_DO_ITEM = "- **O título diz o estado:**"
PEDACOS = (
    "`ESTADO | ÁREA · assunto`",
    "`ATIVO`",
    "`ESPERA`",
    "`OK`",
    "`OFF`",
    "quem orquestra troca o da filha",
    "`/rename",
)


def item_do_titulo(texto):
    """O item do título dentro da seção 6, com a linha de continuação; vazio se ele não estiver lá."""
    achado = re.search(rf"^## [^\n]*{SECAO}\n(.*?)(?=^## |\Z)", texto, re.MULTILINE | re.DOTALL)
    secao = achado.group(1) if achado else ""
    item = re.search(rf"^{re.escape(INICIO_DO_ITEM)}.*?(?=^- \*\*|\Z)", secao, re.MULTILINE | re.DOTALL)
    return item.group().strip() if item else ""


def erros_do_titulo(texto):
    item = item_do_titulo(texto)
    if not item:
        return [f"falta o item «O título diz o estado» na seção «{SECAO}»"]
    erros = [f"o item do título não traz {pedaco}" for pedaco in PEDACOS if pedaco not in item]
    return erros + erros_de_lingua("o item do título", item)


class OrquestrandoSessoes(unittest.TestCase):
    def setUp(self):
        self.texto = ler(SKILL)

    def assertErro(self, texto, trecho):
        erros = erros_do_titulo(texto)
        self.assertTrue(any(trecho in erro for erro in erros), f"esperava «{trecho}» em {erros}")

    def test_o_texto_da_skill_passa(self):
        self.assertEqual([], erros_do_titulo(self.texto))

    def test_sem_o_estado_off_reprova(self):
        self.assertErro(self.texto.replace("`OFF` (parada de propósito)", "(parada de propósito)"), "`OFF`")

    def test_o_ponto_do_meio_trocado_reprova(self):
        self.assertErro(self.texto.replace("ÁREA · assunto", "ÁREA - assunto"), "ÁREA · assunto")

    def test_sem_a_frase_da_filha_reprova(self):
        self.assertErro(self.texto.replace("quem orquestra troca o da filha", "outra pessoa troca"), "da filha")

    def test_sem_o_rename_reprova(self):
        self.assertErro(self.texto.replace("`/rename <título>`", "um comando"), "/rename")

    def test_palavra_de_portugal_no_item_reprova(self):
        self.assertErro(self.texto.replace("em poucas palavras", "em poucas palavras partilhadas"), "partilhadas")

    def test_o_item_fora_da_secao_reprova(self):
        self.assertErro(self.texto.replace(f"## 6. {SECAO}", "## 6. Outra seção"), "falta o item")

    def test_palavra_de_portugal_fora_do_item_passa(self):
        self.assertEqual([], erros_do_titulo(self.texto + "\nO ficheiro fica partilhado.\n"))


if __name__ == "__main__":
    unittest.main()
