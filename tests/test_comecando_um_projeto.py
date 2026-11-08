"""O molde do documento do projeto (`modelos/documentos/projeto.md`) guarda o que a primeira conversa com um projeto
precisa, conferido sem rede e sobre o texto:

- tem as oito seções, na ordem: O que é, Para quem, O que faz, O que não faz, Restrições, Arquitetura, Palavras do
  dono e Perguntas em aberto;
- não leva palavras nem construções do português de Portugal.
As funções recebem o texto, para os casos de erro serem provados sem tocar no molde.
"""

import re
import unittest

from carregar_modelos import MODELOS
from leitura_do_repositorio import ler
from lingua_do_brasil import erros_de_lingua

MOLDE_DO_PROJETO = MODELOS / "documentos" / "projeto.md"
SECOES_DO_PROJETO = ("O que é", "Para quem", "O que faz", "O que não faz", "Restrições", "Arquitetura",
                     "Palavras do dono", "Perguntas em aberto")


def secoes_do_molde(texto):
    """Os títulos `## …` do texto, na ordem em que aparecem."""
    return re.findall(r"^## (.+?)\s*$", texto, re.MULTILINE)


def erros_do_molde(texto):
    achadas = secoes_do_molde(texto)
    erros = [f"falta a seção «{titulo}»" for titulo in SECOES_DO_PROJETO if titulo not in achadas]
    ordem = [titulo for titulo in achadas if titulo in SECOES_DO_PROJETO]
    if not erros and ordem != list(SECOES_DO_PROJETO):
        erros.append(f"as seções estão fora da ordem: {ordem}")
    return erros


class MoldeDoProjeto(unittest.TestCase):
    def setUp(self):
        self.texto = ler(MOLDE_DO_PROJETO)

    def assertErro(self, texto, trecho):
        erros = erros_do_molde(texto)
        self.assertTrue(any(trecho in erro for erro in erros), f"esperava «{trecho}» em {erros}")

    def test_o_molde_passa(self):
        self.assertEqual([], erros_do_molde(self.texto))

    def test_sem_o_que_nao_faz_reprova(self):
        self.assertErro(self.texto.replace("## O que não faz", "## Outra coisa"), "falta a seção «O que não faz»")

    def test_secoes_trocadas_de_ordem_reprovam(self):
        trocado = self.texto.replace("## O que faz\n", "## @@\n").replace("## O que não faz\n", "## O que faz\n")
        self.assertErro(trocado.replace("## @@\n", "## O que não faz\n"), "fora da ordem")

    def test_palavra_de_portugal_no_molde_reprova(self):
        erros = erros_de_lingua("projeto.md", self.texto + "\nO ficheiro do projeto.\n")
        self.assertIn("ficheiro", erros[0])

    def test_o_molde_esta_em_portugues_do_brasil(self):
        self.assertEqual([], erros_de_lingua("projeto.md", self.texto))


if __name__ == "__main__":
    unittest.main()
