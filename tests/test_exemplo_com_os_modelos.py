"""Os testes-modelo (modelos/testes/) rodam num projeto montado só com os modelos, e pegam o que devem pegar.

Verde: o projeto de exemplo, como sai dos modelos, passa. Vermelho: cada estrago típico faz falhar o teste certo.
Num ensaio real, a primeira corrida deu dois vermelhos verdadeiros: arquivos gravados com CRLF pelo write_text do
Windows e uma skill instalada fora do índice.
"""

import subprocess
import sys
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
        escrever(self.pasta / "docs" / "contato.md", "Fale com ana@correio-ficticio.net\n")
        self.assertFalhaEm("test_sem_emails_pessoais")

    def test_action_sem_sha(self):
        ci = self.pasta / ".github" / "workflows" / "ci.yml"
        texto = ci.read_text(encoding="utf-8")
        escrever(ci, texto.replace("actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1",
                                   "actions/checkout@v7", 1))
        self.assertFalhaEm("test_cada_action_fixada_por_sha_com_a_versao")

    def test_download_sem_sha256(self):
        ci = self.pasta / ".github" / "workflows" / "ci.yml"
        linhas = ci.read_text(encoding="utf-8").splitlines(True)
        escrever(ci, "".join(linha for linha in linhas if "sha256sum -c" not in linha))
        self.assertFalhaEm("test_nada_baixado_direto_para_uma_shell")

    def test_juntar_changelog_em_rascunho_mostra_a_secao(self):
        escrever(self.pasta / "CHANGELOG.md", "# Changelog\n")
        escrever(self.pasta / "changelog.d" / "2026-11-01-primeira.md", "Categoria: Adicionado\n\n- Tudo novo.\n")
        resultado = subprocess.run([sys.executable, "-I", "scripts/changelog/juntar_changelog.py", "--rascunho"],
                                   cwd=self.pasta, capture_output=True, check=False, timeout=60)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn(b"## [0.1.0]", resultado.stdout)
        self.assertIn(b"### Adicionado\n\n- Tudo novo.", resultado.stdout.replace(b"\r\n", b"\n"))
        self.assertFalse((self.pasta / "VERSION").exists(), "o rascunho não grava")

    def test_permissao_perigosa_no_allow(self):
        settings = self.pasta / ".claude" / "settings.json"
        texto = settings.read_text(encoding="utf-8").replace('"Bash(git status*)"', '"Bash(git push *)"')
        escrever(settings, texto)
        self.assertFalhaEm("test_allow_so_tem_leituras_e_testes")


if __name__ == "__main__":
    unittest.main()
