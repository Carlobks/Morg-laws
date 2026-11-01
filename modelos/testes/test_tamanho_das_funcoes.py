"""Funções Python até LIMITE linhas (Morg-laws: arquivos pequenos; o que já viola não piora).

As funções que já passavam quando o teste entrou ficam em LONGAS_ANTIGAS com o tamanho de então: só podem encolher,
e saem da lista quando cabem no limite. Uma função nova acima do limite falha. No JS/TS, a mesma regra vem do lint
(ex.: `noExcessiveLinesPerFunction` do Biome ou `max-lines-per-function` do ESLint).
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import ast
import subprocess
import unittest

from carregar_por_caminho import RAIZ

# Ajuste ao projeto. "arquivo:função" -> linhas no dia em que o teste entrou. Só desce.
LIMITE = 35
LONGAS_ANTIGAS = {}


def tamanhos(fonte, caminho):
    """{"arquivo:função": linhas} de todas as funções de um código Python."""
    return {f"{caminho}:{no.name}": no.end_lineno - no.lineno + 1 for no in ast.walk(ast.parse(fonte))
            if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef))}


def funcoes_do_repositorio():
    # Só vê os arquivos que o git conhece: um arquivo novo é medido depois do `git add`.
    caminhos = subprocess.run(["git", "ls-files", "*.py"], cwd=RAIZ, capture_output=True, text=True,
                              encoding="utf-8", check=True).stdout.splitlines()
    resultado = {}
    for caminho in caminhos:
        resultado.update(tamanhos((RAIZ / caminho).read_text(encoding="utf-8-sig"), caminho))
    return resultado


class TamanhoDasFuncoes(unittest.TestCase):

    def test_o_medidor_pega_uma_funcao_acima_do_limite(self):
        fonte = "def longa():\n" + "    x = 1\n" * LIMITE
        self.assertEqual(tamanhos(fonte, "a.py"), {"a.py:longa": LIMITE + 1})

    def test_nenhuma_funcao_nova_passa_o_limite_e_as_antigas_nao_crescem(self):
        for nome, linhas in funcoes_do_repositorio().items():
            if linhas > LIMITE:
                with self.subTest(funcao=nome):
                    self.assertLessEqual(linhas, LONGAS_ANTIGAS.get(nome, LIMITE), "divida-a por responsabilidade")

    def test_lista_das_antigas_esta_atualizada(self):
        atuais = funcoes_do_repositorio()
        for nome, linhas in LONGAS_ANTIGAS.items():
            with self.subTest(funcao=nome):
                self.assertGreater(atuais.get(nome, 0), LIMITE, "já cabe no limite (ou mudou de nome): tire-a da lista")
                self.assertLessEqual(atuais[nome], linhas)


if __name__ == "__main__":
    unittest.main()
