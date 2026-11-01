"""Hook limite_de_linhas (modelos/claude/hooks/limite_de_linhas.py): arquivo de código acima do limite só encolhe."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from carregar_modelos import PASTA_HOOKS, carregar_hook, correr_como_script

linhas = carregar_hook("limite_de_linhas")
DENTRO = PASTA_HOOKS.parent.parent / "tests" / "nao_existe.py"  # dentro da RAIZ do modelo (modelos/)


def correr(ferramenta, **entrada):
    pedido = json.dumps({"tool_name": ferramenta, "tool_input": entrada}).encode("utf-8")
    return correr_como_script(PASTA_HOOKS / "limite_de_linhas.py", pedido)


class Decisao(unittest.TestCase):

    def test_conta_linhas_como_o_editor(self):
        self.assertEqual(linhas.contar_linhas("a\nb\n"), 2)
        self.assertEqual(linhas.contar_linhas("a\nb"), 2)
        self.assertEqual(linhas.contar_linhas(""), 0)

    def test_texto_depois_do_write_e_do_edit(self):
        self.assertEqual(linhas.texto_depois("Write", {"content": "novo"}, "velho"), "novo")
        self.assertEqual(linhas.texto_depois("Edit", {"old_string": "a", "new_string": "b"}, "a a"), "b a")
        self.assertEqual(linhas.texto_depois("Edit", {"old_string": "a", "new_string": "b", "replace_all": True},
                                             "a a"), "b b")
        self.assertIsNone(linhas.texto_depois("Edit", {"old_string": "z", "new_string": "b"}, "a"))

    def test_recusa_crescer_acima_do_limite(self):
        self.assertIsNotNone(linhas.motivo_para_bloquear(Path("x.py"), 10, 501))
        self.assertIsNotNone(linhas.motivo_para_bloquear(Path("x.tsx"), 600, 601))

    def test_deixa_encolher_e_ficar_no_limite(self):
        self.assertIsNone(linhas.motivo_para_bloquear(Path("x.py"), 1982, 1900))  # refatoração
        self.assertIsNone(linhas.motivo_para_bloquear(Path("x.py"), 10, 500))
        self.assertIsNone(linhas.motivo_para_bloquear(Path("x.json"), 10, 9000))  # não é código


class ComoHook(unittest.TestCase):

    def test_recusa_um_write_grande_no_projeto(self):
        codigo, _, erro = correr("Write", file_path=str(DENTRO), content="x\n" * 501)
        self.assertEqual(codigo, 2)
        self.assertIn("501 linhas", erro)

    def test_conta_o_arquivo_que_ja_existe(self):
        este_hook = PASTA_HOOKS / "limite_de_linhas.py"
        self.assertEqual(correr("Edit", file_path=str(este_hook), old_string="LIMITE = 500",
                                new_string="LIMITE = 500  "), (0, "", ""))

    def test_deixa_passar_o_que_nao_da_para_saber_ou_nao_e_do_projeto(self):
        with tempfile.TemporaryDirectory() as pasta:
            fora = correr("Write", file_path=str(Path(pasta) / "a.py"), content="x\n" * 900)
        casos = {
            "fora do projeto": fora,
            "sem caminho": correr("Write", content="x\n" * 900),
            "edit que não encaixa": correr("Edit", file_path=str(DENTRO), old_string="z", new_string="x\n" * 900),
        }
        for caso, resultado in casos.items():
            with self.subTest(caso=caso):
                self.assertEqual(resultado, (0, "", ""))

    def test_no_python_isolado_de_verdade(self):
        pedido = {"tool_name": "Write", "tool_input": {"file_path": str(DENTRO), "content": "x\n" * 501}}
        resultado = subprocess.run([sys.executable, "-I", str(PASTA_HOOKS / "limite_de_linhas.py")],
                                   input=json.dumps(pedido), capture_output=True, text=True, encoding="utf-8",
                                   check=False, timeout=30)
        self.assertEqual(resultado.returncode, 2)


if __name__ == "__main__":
    unittest.main()
