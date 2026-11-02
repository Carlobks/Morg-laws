"""Os hooks do git modelo (modelos/git/hooks/) rodam de verdade num repositório: o git chama-os, eles chamam os
portões em Python e o commit sai ou é recusado."""

import os
import sys
import unittest

from projeto_de_exemplo import apagar, escrever, git, montar

MENSAGEM_CERTA = "docs(exemplo): primeiro commit\n"


class HooksDoGit(unittest.TestCase):

    def setUp(self):
        self.pasta = montar()
        self.addCleanup(apagar, self.pasta)
        self.ambiente = {**os.environ, "MORG_PY": sys.executable}
        self.ambiente.pop("MORG_A_TESTAR", None)

    def definir_testes(self, comando):
        pre_commit = self.pasta / ".githooks" / "pre-commit"
        texto = pre_commit.read_text(encoding="utf-8").replace("COMANDO_DOS_TESTES=''", f"COMANDO_DOS_TESTES='{comando}'")
        escrever(pre_commit, texto)

    def commit(self, mensagem=MENSAGEM_CERTA):
        escrever(self.pasta / "msg.txt", mensagem)
        return git(self.pasta, "commit", "-q", "-F", "msg.txt", "--", "CLAUDE.md", check=False, env=self.ambiente)

    def test_sem_comando_de_testes_o_commit_e_recusado(self):
        resultado = self.commit()
        self.assertNotEqual(resultado.returncode, 0)
        self.assertIn("COMANDO_DOS_TESTES", resultado.stderr)

    def test_com_testes_verdes_e_mensagem_certa_o_commit_sai(self):
        self.definir_testes("exit 0")
        resultado = self.commit()
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("primeiro commit", git(self.pasta, "log", "--oneline").stdout)

    def test_testes_vermelhos_recusam(self):
        self.definir_testes("echo falhou; exit 1")
        resultado = self.commit()
        self.assertNotEqual(resultado.returncode, 0)
        self.assertIn("os testes falharam", resultado.stderr)

    def test_dentro_de_uma_corrida_de_testes_nao_repete(self):
        self.definir_testes("exit 1")
        self.ambiente["MORG_A_TESTAR"] = "1"
        self.assertEqual(self.commit().returncode, 0)

    def test_mensagem_fora_do_formato_e_recusada(self):
        self.definir_testes("exit 0")
        resultado = self.commit("primeiro commit\n")
        self.assertNotEqual(resultado.returncode, 0)
        self.assertIn("tipo(área)", resultado.stderr)

    def test_identidade_que_nao_e_noreply_e_recusada(self):
        self.definir_testes("exit 0")
        git(self.pasta, "config", "--local", "user.email", "ana@example.com")
        resultado = self.commit()
        self.assertNotEqual(resultado.returncode, 0)
        self.assertIn("noreply", resultado.stderr)


if __name__ == "__main__":
    unittest.main()
