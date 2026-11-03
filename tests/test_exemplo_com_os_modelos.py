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

    def estragar_o_claude_md(self, texto):
        escrever(self.pasta / "CLAUDE.md", texto)

    def test_claude_md_sem_importar_o_agents_md(self):
        self.estragar_o_claude_md("## Só no Claude Code\n\nNada.\n")
        self.assertFalhaEm("test_o_claude_md_importa_o_arquivo_de_regras")

    def test_claude_md_com_caminho_que_nao_existe(self):
        self.estragar_o_claude_md("@AGENTS.md\n\nVer `docs/nao-existe.md`.\n")
        self.assertFalhaEm("test_caminhos_citados_existem")

    def test_claude_md_que_passa_o_limite_somado(self):
        # Sozinhos, os dois ficam abaixo de 100 linhas; o Claude Code carrega-os juntos.
        self.estragar_o_claude_md("@AGENTS.md\n" + "- nota\n" * 60)
        self.assertFalhaEm("test_tamanho")

    def test_arquivo_em_crlf(self):
        (self.pasta / "src" / "pedido.py").write_bytes(b"x = 1\r\n")
        self.assertFalhaEm("test_no_disco_crlf_so_no_que_o_windows_roda")

    def test_nome_generico(self):
        escrever(self.pasta / "src" / "utils.py", "x = 1\n")
        self.assertFalhaEm("test_nenhum_arquivo_ou_pasta_com_nome_generico")

    def test_alarme_sem_motivo(self):
        escrever(self.pasta / "src" / "calado.py", "import os  # noqa: F401\n")
        self.assertFalhaEm("test_cada_alarme_tem_motivo")

    def test_alarme_com_comentario_qualquer_em_cima(self):
        # A regra do alarme: o motivo vai na mesma linha; um TODO ou outro alarme em cima não é motivo.
        escrever(self.pasta / "src" / "calado.py", "# TODO ver depois\nimport os  # noqa: F401\n")
        self.assertFalhaEm("test_cada_alarme_tem_motivo")

    def test_alarme_em_comentario_de_bloco_conta(self):
        # No JSX o @ts-expect-error vai em /* */; tem de entrar na contagem como o de //.
        escrever(self.pasta / "src" / "tela.tsx", "const a = <div>{/* @ts-expect-error — tipo da lib */}</div>;\n")
        self.assertFalhaEm("test_a_contagem_nao_sobe")

    def test_linha_de_base_dos_alarmes_que_nao_desceu(self):
        # Quem tira um alarme baixa o máximo no mesmo commit; senão a folga deixa o próximo entrar calado.
        teste = self.pasta / "tests" / "test_alarmes.py"
        escrever(teste, teste.read_text(encoding="utf-8").replace("MAXIMO_POR_TIPO = {}", 'MAXIMO_POR_TIPO = {"noqa": 1}'))
        self.assertFalhaEm("test_a_linha_de_base_desce_com_a_contagem")

    def test_email_pessoal(self):
        escrever(self.pasta / "docs" / "contato.md", "Fale com ana@correio-ficticio.net\n")
        self.assertFalhaEm("test_sem_emails_pessoais")

    def test_numero_de_documento_com_o_padrao_ligado(self):
        teste = self.pasta / "tests" / "test_dados_pessoais.py"
        escrever(teste, teste.read_text(encoding="utf-8").replace(
            "DOCUMENTOS = {}", r'DOCUMENTOS = {"CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"}'))
        escrever(self.pasta / "docs" / "cliente.md", "CPF do cliente: 000.000.000-00\n")
        self.assertFalhaEm("test_sem_numeros_de_documentos")

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

    def estragar_o_ci(self, antes, depois):
        ci = self.pasta / ".github" / "workflows" / "ci.yml"
        texto = ci.read_text(encoding="utf-8")
        self.assertIn(antes, texto)
        escrever(ci, texto.replace(antes, depois, 1))

    def test_permissao_de_escrita_num_job(self):
        # O bloco do topo continua só de leitura; o job ganha escrita por baixo dele.
        self.estragar_o_ci("    timeout-minutes: 10\n", "    timeout-minutes: 10\n    permissions:\n      contents: write\n")
        self.assertFalhaEm("test_o_token_so_le_e_o_checkout_nao_guarda_a_credencial")

    def test_permissao_write_all(self):
        self.estragar_o_ci("  segredos:\n", "  segredos:\n    permissions: write-all\n")
        self.assertFalhaEm("test_o_token_so_le_e_o_checkout_nao_guarda_a_credencial")

    def test_download_dentro_de_sh_c(self):
        self.estragar_o_ci("          tar -xzf", '          sh -c "$(curl -sSfL https://exemplo.com/x)"\n          tar -xzf')
        self.assertFalhaEm("test_nada_baixado_direto_para_uma_shell")

    def test_download_com_redirecionamento_ou_output_sem_sha256(self):
        for baixar in ("curl -sSfL https://exemplo.com/f.tar.gz > f.tar.gz",
                       "curl -sSfL --output f.tar.gz https://exemplo.com/f.tar.gz"):
            with self.subTest(baixar=baixar):
                self.estragar_o_ci("          tar -xzf", f"          {baixar}\n          tar -xzf")
                self.assertFalhaEm("test_nada_baixado_direto_para_uma_shell")
                self.estragar_o_ci(f"          {baixar}\n", "")

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
