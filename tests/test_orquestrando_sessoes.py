"""A `orquestrando-sessoes` guarda a regra do título das sessões na seção «Várias sessões na mesma pasta»,
conferida sem rede e sobre o texto:

- o item «O título diz o estado» existe nessa seção, com o formato literal `ESTADO | ÁREA · assunto` e os quatro
  estados (`ATIVO`, `ESPERA`, `OK`, `OFF`);
- o item diz que quem orquestra troca o título da filha e que o terminal renomeia com `/rename`;
- só o item não leva palavras nem construções do português de Portugal (o resto da skill ainda leva).
- a seção «Leitura independente» traz a subseção «Uma leitura longa: uma parte de cada vez», com o método (uma
  parte, a seção gravada, só então a seguinte; reler o próprio relatório; a opinião geral das seções; a segunda
  sessão pelo relatório da primeira; os números como escolha do projeto; o plano diz o método) e sem formas de
  Portugal; e a `description` fala da leitura longa.
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
    "Cada sessão troca o próprio título",
    "app de desktop",
    "CLI do Codex",
    "a página do CLI não diz como se faz",
    "Onde a ferramenta não tiver nenhuma forma",
)
SECAO_DA_LEITURA = "Leitura independente"
SUBSECAO_DA_LEITURA = "### Uma leitura longa: uma parte de cada vez"
PEDACOS_DA_LEITURA = (
    "Uma parte de cada vez",
    "escrever logo a seção dela no relatório",
    "no relatório, gravado em disco, e só então",  # só existe no item (o «Por quê» também diz «gravado em disco»)
    "só então abrir a seguinte",
    "Nunca duas partes antes de escrever",
    "reler o próprio relatório",
    "e não a parte anterior",
    "A opinião geral sai só das seções",
    "a segunda começa pelo relatório da primeira",
    "escolha do projeto, não de uma fonte",
    "O plano diz o método",
    "e não só o que se lê",
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


def subsecao_da_leitura(texto):
    """A subseção da leitura longa dentro da seção «Leitura independente»; vazia se ela não estiver lá."""
    achado = re.search(rf"^## [^\n]*{SECAO_DA_LEITURA}[^\n]*\n(.*?)(?=^## |\Z)", texto, re.MULTILINE | re.DOTALL)
    secao = achado.group(1) if achado else ""
    sub = re.search(rf"^{re.escape(SUBSECAO_DA_LEITURA)}.*?(?=^### |\Z)", secao, re.MULTILINE | re.DOTALL)
    return sub.group().strip() if sub else ""


def erros_da_leitura(texto):
    sub = subsecao_da_leitura(texto)
    if not sub:
        return [f"falta a subseção «Uma leitura longa» na seção «{SECAO_DA_LEITURA}»"]
    erros = [f"a subseção da leitura não traz {pedaco}" for pedaco in PEDACOS_DA_LEITURA if pedaco not in sub]
    return erros + erros_de_lingua("a subseção da leitura", sub)


def erros_da_descricao_da_leitura(texto):
    linha = re.search(r"^description:[^\n]*", texto, re.MULTILINE)
    if linha and "leitura longa" in linha.group():
        return []
    return ["a description não fala da leitura longa"]


class OrquestrandoSessoes(unittest.TestCase):
    def setUp(self):
        self.texto = ler(SKILL)

    def assertErro(self, texto, trecho):
        erros = erros_do_titulo(texto)
        self.assertTrue(any(trecho in erro for erro in erros), f"esperava «{trecho}» em {erros}")

    def assertErroDaLeitura(self, texto, trecho):
        erros = erros_da_leitura(texto)
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

    def test_sem_cada_sessao_troca_o_proprio_reprova(self):
        self.assertErro(self.texto.replace("Cada sessão troca o próprio título", "Alguém troca"),
                        "Cada sessão troca o próprio título")

    def test_sem_a_app_de_desktop_reprova(self):
        self.assertErro(self.texto.replace("na app de desktop do Claude Code", "no Claude Code"), "app de desktop")

    def test_o_codex_sem_dizer_que_e_o_cli_reprova(self):
        self.assertErro(self.texto.replace("no CLI do Codex", "no Codex"), "CLI do Codex")

    def test_sem_dizer_que_a_pagina_do_cli_nao_cobre_a_extensao_reprova(self):
        self.assertErro(self.texto.replace("a página do CLI não diz como se faz", "tudo funciona igual"),
                        "a página do CLI não diz como se faz")

    def test_sem_o_que_fazer_quando_nao_ha_forma_reprova(self):
        self.assertErro(self.texto.replace("Onde a ferramenta não tiver nenhuma forma", "Em qualquer caso"),
                        "Onde a ferramenta não tiver nenhuma forma")

    def test_palavra_de_portugal_no_item_reprova(self):
        self.assertErro(self.texto.replace("em poucas palavras", "em poucas palavras partilhadas"), "partilhadas")

    def test_o_item_fora_da_secao_reprova(self):
        self.assertErro(self.texto.replace(f"## 6. {SECAO}", "## 6. Outra seção"), "falta o item")

    def test_palavra_de_portugal_fora_do_item_passa(self):
        self.assertEqual([], erros_do_titulo(self.texto + "\nO ficheiro fica partilhado.\n"))

    def test_a_subsecao_da_leitura_passa(self):
        self.assertEqual([], erros_da_leitura(self.texto))

    def test_sem_o_so_entao_a_seguinte_reprova(self):
        self.assertErroDaLeitura(self.texto.replace("só então abrir a seguinte", "depois abrir as outras"),
                                 "só então abrir a seguinte")

    def test_sem_o_nunca_duas_partes_reprova(self):
        self.assertErroDaLeitura(self.texto.replace("Nunca duas partes antes de escrever.", ""),
                                 "Nunca duas partes antes de escrever")

    def test_sem_reler_o_proprio_relatorio_reprova(self):
        self.assertErroDaLeitura(self.texto.replace("reler o próprio relatório", "reler a parte"),
                                 "reler o próprio relatório")

    def test_sem_a_opiniao_geral_das_secoes_reprova(self):
        self.assertErroDaLeitura(
            self.texto.replace("A opinião geral sai só das seções", "A opinião geral sai da memória"),
            "A opinião geral sai só das seções")

    def test_a_segunda_sessao_sem_o_relatorio_da_primeira_reprova(self):
        self.assertErroDaLeitura(
            self.texto.replace("a segunda começa pelo relatório da primeira", "a segunda começa do zero"),
            "a segunda começa pelo relatório da primeira")

    def test_os_numeros_sem_dizer_que_sao_escolha_reprova(self):
        self.assertErroDaLeitura(
            self.texto.replace("escolha do projeto, não de uma fonte", "o que a pesquisa achou"),
            "escolha do projeto, não de uma fonte")

    def test_sem_o_plano_diz_o_metodo_reprova(self):
        self.assertErroDaLeitura(self.texto.replace("O plano diz o método", "O plano diz as partes"),
                                 "O plano diz o método")

    def test_a_subsecao_fora_da_leitura_independente_reprova(self):
        self.assertErroDaLeitura(self.texto.replace("## 2. Leitura independente", "## 2. Outra seção"),
                                 "falta a subseção")

    def test_palavra_de_portugal_na_subsecao_reprova(self):
        self.assertErroDaLeitura(self.texto.replace("ler a parte inteira", "ler o ficheiro inteiro"), "ficheiro")

    def test_a_description_fala_da_leitura_longa(self):
        self.assertEqual([], erros_da_descricao_da_leitura(self.texto))

    def test_a_description_sem_a_leitura_longa_reprova(self):
        self.assertEqual(["a description não fala da leitura longa"],
                         erros_da_descricao_da_leitura(self.texto.replace("uma leitura longa em partes", "uma coisa")))


if __name__ == "__main__":
    unittest.main()
