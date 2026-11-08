"""A `pondo-o-plano-a-prova` alargada às mudanças guarda o que a faz funcionar, conferido sem rede e sobre o texto:

- tem as seções «Quando o pedido é uma mudança» e «O oráculo», e o resumo final tem a linha `Oráculo`;
- a seção do oráculo diz que ele julga o resultado e não o mecanismo, tem a linha «Continua igual» e as duas regras
  opostas do passo 2: a linha do «depois» falha antes, a «Continua igual» passa antes e depois;
- o `SKILL.md` e o `evals/` não levam palavras nem construções do português de Portugal.
As funções recebem o texto, para os casos de erro serem provados sem tocar na skill.
"""

import re
import tempfile
import unittest
from pathlib import Path

from carregar_modelos import RAIZ
from leitura_do_repositorio import ler
from lingua_do_brasil import erros_de_lingua

SKILL = RAIZ / "skills" / "pondo-o-plano-a-prova"
TITULOS = ("Quando o pedido é uma mudança", "O oráculo")
FRASES_DO_ORACULO = (
    "Julga o resultado, não o mecanismo",
    "Continua igual",
    "tem de falhar antes",
    "tem de passar antes e depois",
)


def secao(texto, titulo):
    """O texto da seção `## … titulo` até a seção seguinte; vazio se ela não existir."""
    achado = re.search(rf"^## [^\n]*{re.escape(titulo)}\n(.*?)(?=^## |\Z)", texto, re.MULTILINE | re.DOTALL)
    return achado.group(1) if achado else ""


def erros_do_oraculo(texto):
    erros = [f"falta a seção «{titulo}»" for titulo in TITULOS if not secao(texto, titulo)]
    if not re.search(r"^Oráculo\b", secao(texto, "O que entregar no fim"), re.MULTILINE):
        erros.append("o resumo final não tem a linha «Oráculo»")
    oraculo = secao(texto, "O oráculo")
    erros += [f"a seção do oráculo não traz «{frase}»" for frase in FRASES_DO_ORACULO if frase not in oraculo]
    return erros


def erros_de_lingua_da_skill(raiz):
    arquivos = [raiz / "SKILL.md", raiz / "evals" / "trigger-eval.json"]
    return [erro for arquivo in arquivos for erro in erros_de_lingua(arquivo.name, ler(arquivo))]


class PondoOPlanoAProva(unittest.TestCase):
    def setUp(self):
        self.texto = ler(SKILL / "SKILL.md")

    def assertErro(self, texto, trecho):
        erros = erros_do_oraculo(texto)
        self.assertTrue(any(trecho in erro for erro in erros), f"esperava «{trecho}» em {erros}")

    def test_o_texto_da_skill_passa(self):
        self.assertEqual([], erros_do_oraculo(self.texto))

    def test_sem_a_linha_oraculo_no_resumo_reprova(self):
        self.assertErro(self.texto.replace("\nOráculo (obrigatório", "\nOutra (obrigatório"), "linha «Oráculo»")

    def test_sem_o_resultado_reprova(self):
        self.assertErro(self.texto.replace("Julga o resultado,", "Julga o código,"), "Julga o resultado, não o mecanismo")

    def test_sem_a_regra_do_depois_reprova(self):
        self.assertErro(self.texto.replace("tem de falhar antes", "pode falhar"), "tem de falhar antes")

    def test_sem_a_regra_do_continua_igual_reprova(self):
        self.assertErro(self.texto.replace("tem de passar antes e depois", "passa"), "tem de passar antes e depois")

    def test_sem_a_secao_da_mudanca_reprova(self):
        self.assertErro(self.texto.replace("Quando o pedido é uma mudança", "Outra coisa"), "falta a seção «Quando")

    def test_a_secao_vazia_vem_vazia(self):
        self.assertEqual("", secao("# só um título", "O oráculo"))

    def test_a_skill_e_o_eval_estao_em_portugues_do_brasil(self):
        self.assertEqual([], erros_de_lingua_da_skill(SKILL))

    def test_ficheiro_no_skill_reprova(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "evals").mkdir()
            (raiz / "SKILL.md").write_text(self.texto.replace("o arquivo.", "o ficheiro.", 1), encoding="utf-8")
            (raiz / "evals" / "trigger-eval.json").write_text("[]", encoding="utf-8")
            self.assertIn("ficheiro", erros_de_lingua_da_skill(raiz)[0])


if __name__ == "__main__":
    unittest.main()
