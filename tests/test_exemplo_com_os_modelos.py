"""Os testes-modelo (modelos/testes/) rodam num projeto montado só com os modelos, e pegam o que devem pegar.

Verde: o projeto de exemplo, como sai dos modelos, passa. Vermelho: cada estrago típico faz falhar o teste certo.
Num ensaio real, a primeira corrida deu dois vermelhos verdadeiros: arquivos gravados com CRLF pelo write_text do
Windows e uma skill instalada fora do índice.
"""

import unittest

from projeto_de_exemplo import apagar, escrever, git, montar, rodar_testes


class ProjetoDeExemplo(unittest.TestCase):

    def setUp(self):
        self.pasta = montar()
        self.addCleanup(apagar, self.pasta)

    def assertFalhaEm(self, teste):
        git(self.pasta, "add", "--", ".")
        codigo, saida = rodar_testes(self.pasta)
        self.assertNotEqual(codigo, 0, saida[-2000:])
        self.assertIn(f"FAIL: {teste}", saida)

    def test_como_sai_dos_modelos_passa(self):
        codigo, saida = rodar_testes(self.pasta)
        self.assertEqual(codigo, 0, saida[-3000:])
        self.assertIn("OK", saida)

    def test_regra_sem_linha_no_mapa(self):
        mapa = self.pasta / "docs" / "regras-e-barreiras.md"
        texto = mapa.read_text(encoding="utf-8")
        escrever(mapa, "".join(linha for linha in texto.splitlines(True) if not linha.startswith("| NÃO PIORAR")))
        self.assertFalhaEm("test_cada_regra_esta_no_mapa_e_o_mapa_nao_tem_regras_a_mais")

    def test_arquivo_em_crlf(self):
        (self.pasta / "src" / "pedido.py").write_bytes(b"x = 1\r\n")
        self.assertFalhaEm("test_no_disco_crlf_so_no_que_o_windows_roda")

    def test_nome_generico(self):
        escrever(self.pasta / "src" / "utils.py", "x = 1\n")
        self.assertFalhaEm("test_nenhum_arquivo_ou_pasta_com_nome_generico")

    def test_alarme_sem_motivo(self):
        escrever(self.pasta / "src" / "calado.py", "import os  # noqa: F401\n")
        self.assertFalhaEm("test_cada_alarme_tem_motivo")

    def test_email_pessoal(self):
        escrever(self.pasta / "docs" / "contato.md", "Fale com ana.silva@gmail.com\n")
        self.assertFalhaEm("test_sem_emails_pessoais")

    def test_permissao_perigosa_no_allow(self):
        settings = self.pasta / ".claude" / "settings.json"
        texto = settings.read_text(encoding="utf-8").replace('"Bash(git status*)"', '"Bash(git push *)"')
        escrever(settings, texto)
        self.assertFalhaEm("test_allow_so_tem_leituras_e_testes")


if __name__ == "__main__":
    unittest.main()
