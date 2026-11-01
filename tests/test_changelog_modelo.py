"""Changelog por fragmentos (modelos/changelog/juntar_changelog.py; Keep a Changelog 1.1.0, towncrier e SemVer).

Cada mudança que se vê de fora leva um arquivo changelog.d/AAAA-MM-DD-assunto.md: a primeira linha diz a
categoria, depois uma linha em branco e os itens começados por "- ". O script junta-os no CHANGELOG.md na hora
de lançar uma versão, calcula a versão e apaga-os; com --rascunho só mostra.
"""

import io
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from carregar_modelos import MODELOS, carregar, correr_como_script

SCRIPT = MODELOS / "changelog" / "juntar_changelog.py"
changelog = carregar(SCRIPT, "juntar_changelog")
INICIO = "# Changelog\n\nIntrodução.\n"
DIA = date(2026, 10, 31)


class Fragmento(unittest.TestCase):

    def test_le_a_categoria_e_os_itens(self):
        texto = "Categoria: Corrigido\n\n- A barra já não salta.\n  Continua aqui.\n- Outro.\n"
        self.assertEqual(changelog.ler_fragmento(texto),
                         ("Corrigido", ["- A barra já não salta.", "  Continua aqui.", "- Outro."]))

    def test_linhas_vazias_no_fim_nao_contam(self):
        self.assertEqual(changelog.ler_fragmento("Categoria: Removido\n\n- Saiu.\n\n\n"), ("Removido", ["- Saiu."]))

    def test_recusa_o_que_esta_mal(self):
        casos = {
            "": "Categoria:",
            "Corrigido\n\n- x\n": "Categoria:",
            "Categoria: Arranjado\n\n- x\n": "Arranjado",
            "Categoria: Corrigido\n- x\n": "linha em branco",
            "Categoria: Corrigido\n\n": "itens",
            "Categoria: Corrigido\n\nTexto solto.\n": "- ",
            "Categoria: Corrigido\n\n- x\n\n- y\n": "- ",
        }
        for texto, motivo in casos.items():
            with self.subTest(texto=texto), self.assertRaises(ValueError) as erro:
                changelog.ler_fragmento(texto)
            self.assertIn(motivo, str(erro.exception))

    def test_linha_incompativel_vira_o_primeiro_item(self):
        texto = "Categoria: Alterado\nIncompatível: o arquivo de configuração muda de formato\n\n- Formato novo.\n"
        self.assertEqual(changelog.ler_fragmento(texto),
                         ("Alterado", ["- **Incompatível:** o arquivo de configuração muda de formato",
                                       "- Formato novo."]))
        with self.assertRaises(ValueError):  # sem o motivo não conta, e falta a linha em branco
            changelog.ler_fragmento("Categoria: Alterado\nIncompatível: \n\n- x\n")

    def test_as_categorias_seguem_a_ordem_do_keep_a_changelog(self):
        self.assertEqual(changelog.CATEGORIAS,
                         ("Adicionado", "Alterado", "Obsoleto", "Removido", "Corrigido", "Segurança"))


class ProximaVersao(unittest.TestCase):

    def test_cada_categoria_sobe_a_parte_certa(self):
        casos = [
            ("1.4.2", ["Corrigido"], False, "1.4.3"),
            ("1.4.2", ["Segurança", "Corrigido"], False, "1.4.3"),
            ("1.4.2", ["Adicionado", "Corrigido"], False, "1.5.0"),
            ("1.4.2", ["Alterado"], False, "1.5.0"),
            ("1.4.2", ["Obsoleto"], False, "1.5.0"),
            ("1.4.2", ["Removido", "Corrigido"], False, "2.0.0"),
            ("1.4.2", ["Alterado"], True, "2.0.0"),
            ("0.3.1", ["Removido"], False, "0.4.0"),  # no 0.x o incompatível sobe só o MENOR
            ("0.3.1", ["Alterado"], True, "0.4.0"),
            ("0.3.1", ["Corrigido"], False, "0.3.2"),
            ("0.0.0", ["Adicionado", "Removido"], False, "0.1.0"),  # o 1.º lançamento
            ("9.9.9", ["Corrigido"], False, "9.9.10"),  # números, não texto
        ]
        for atual, categorias, incompativel, esperada in casos:
            with self.subTest(atual=atual, categorias=categorias, incompativel=incompativel):
                self.assertEqual(changelog.proxima_versao(atual, categorias, incompativel), esperada)


class Pasta(unittest.TestCase):

    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.raiz = Path(pasta.name)
        self.fragmentos = self.raiz / "changelog.d"
        self.fragmentos.mkdir()
        (self.raiz / "CHANGELOG.md").write_bytes(INICIO.encode())

    def escrever(self, nome, texto):
        (self.fragmentos / nome).write_bytes(texto.encode("utf-8"))

    def changelog_escrito(self):
        return (self.raiz / "CHANGELOG.md").read_bytes().decode()

    def test_nomes_e_conteudos_errados_sao_apontados(self):
        self.escrever("README.md", "Explicação, ignorada.\n")
        self.escrever("2026-10-31-barra.md", "Categoria: Alterado\n\n- x\n")
        self.escrever("barra.md", "Categoria: Alterado\n\n- x\n")
        self.escrever("2026-10-31-Barra_Nova.md", "Categoria: Alterado\n\n- x\n")
        self.escrever("2026-10-31-mau.md", "Categoria: Nada\n\n- x\n")
        erros = changelog.erros_da_pasta(self.fragmentos)
        self.assertEqual(len(erros), 3)
        self.assertTrue(erros[0].startswith("2026-10-31-Barra_Nova.md: o nome"))
        self.assertTrue(erros[1].startswith("2026-10-31-mau.md: "))
        self.assertTrue(erros[2].startswith("barra.md: o nome"))

    def test_juntar_escreve_a_versao_por_categoria_e_apaga_os_fragmentos(self):
        (self.raiz / "CHANGELOG.md").write_bytes((INICIO + "\n## [0.1.0] - 2026-10-01\n\n- Antigo.\n").encode())
        self.escrever("README.md", "Fica.\n")
        self.escrever("2026-10-30-b.md", "Categoria: Corrigido\n\n- Correção.\n")
        self.escrever("2026-10-29-a.md", "Categoria: Adicionado\n\n- Novo A.\n")
        self.escrever("2026-10-31-c.md", "Categoria: Adicionado\n\n- Novo C.\n")
        codigo, texto = changelog.juntar(self.raiz, "0.2.0", DIA)
        secao = "## [0.2.0] - 2026-10-31\n\n### Adicionado\n\n- Novo A.\n- Novo C.\n\n### Corrigido\n\n- Correção.\n"
        self.assertEqual((codigo, texto), (0, secao))
        self.assertEqual(self.changelog_escrito(), INICIO + "\n" + secao + "\n## [0.1.0] - 2026-10-01\n\n- Antigo.\n")
        self.assertEqual([p.name for p in self.fragmentos.iterdir()], ["README.md"])

    def test_a_primeira_versao_vai_para_o_fim(self):
        self.escrever("2026-10-31-a.md", "Categoria: Removido\n\n- Saiu.\n")
        changelog.juntar(self.raiz, "0.1.0", DIA)
        self.assertEqual(self.changelog_escrito(), INICIO + "\n## [0.1.0] - 2026-10-31\n\n### Removido\n\n- Saiu.\n")

    def test_rascunho_so_mostra(self):
        self.escrever("2026-10-31-a.md", "Categoria: Removido\n\n- Saiu.\n")
        codigo, texto = changelog.juntar(self.raiz, "0.1.0", DIA, rascunho=True)
        self.assertEqual(codigo, 0)
        self.assertIn("- Saiu.", texto)
        self.assertEqual(self.changelog_escrito(), INICIO)
        self.assertTrue((self.fragmentos / "2026-10-31-a.md").exists())

    def test_sem_fragmentos_ou_com_erros_nao_mexe_em_nada(self):
        self.assertEqual(changelog.juntar(self.raiz, "0.1.0", DIA), (1, "Não há fragmentos em changelog.d/ para juntar."))
        self.escrever("2026-10-31-a.md", "Categoria: Nada\n\n- x\n")
        codigo, texto = changelog.juntar(self.raiz, "0.1.0", DIA)
        self.assertEqual(codigo, 1)
        self.assertIn("2026-10-31-a.md", texto)
        self.assertEqual(self.changelog_escrito(), INICIO)

    def test_sem_numero_calcula_a_versao_e_escreve_o_version(self):
        (self.raiz / "VERSION").write_bytes(b"0.3.1\n")
        self.escrever("2026-10-31-a.md", "Categoria: Corrigido\n\n- Correção.\n")
        self.escrever("2026-10-31-b.md", "Categoria: Alterado\nIncompatível: o atalho X muda\n\n- Muda.\n")
        codigo, texto = changelog.juntar(self.raiz, None, DIA, rascunho=True)
        self.assertEqual((codigo, texto.splitlines()[0]), (0, "## [0.4.0] - 2026-10-31"))
        self.assertEqual((self.raiz / "VERSION").read_bytes(), b"0.3.1\n")  # o rascunho não grava
        self.assertEqual(changelog.juntar(self.raiz, None, DIA)[0], 0)
        self.assertEqual((self.raiz / "VERSION").read_bytes(), b"0.4.0\n")
        self.assertIn("### Alterado\n\n- **Incompatível:** o atalho X muda\n- Muda.\n", self.changelog_escrito())

    def test_sem_version_e_o_primeiro_lancamento(self):
        self.escrever("2026-10-31-a.md", "Categoria: Adicionado\n\n- Novo.\n")
        self.assertTrue(changelog.juntar(self.raiz, None, DIA)[1].startswith("## [0.1.0]"))
        self.assertEqual((self.raiz / "VERSION").read_bytes(), b"0.1.0\n")

    def test_numero_a_mao_tem_de_subir_e_version_mal_escrito_para(self):
        (self.raiz / "VERSION").write_bytes(b"0.4.0\n")
        self.escrever("2026-10-31-a.md", "Categoria: Corrigido\n\n- Correção.\n")
        for versao in ("0.4.0", "0.3.9", "1.0", "01.0.0", "v1.0.0"):
            with self.subTest(versao=versao):
                codigo, texto = changelog.juntar(self.raiz, versao, DIA)
                self.assertEqual(codigo, 1)
                self.assertIn("maior do que a atual (0.4.0)", texto)
        self.assertEqual(changelog.juntar(self.raiz, "1.0.0", DIA, rascunho=True)[0], 0)
        (self.raiz / "VERSION").write_bytes(b"quatro\n")
        self.assertEqual(changelog.juntar(self.raiz, None, DIA),
                         (1, "VERSION mal escrito: 'quatro' (tem de ser MAIOR.MENOR.CORREÇÃO)"))
        self.assertEqual(self.changelog_escrito(), INICIO)

    def correr_main(self, argv):
        """(código, stdout, stderr) com os canais num terminal cp1252, como o do Windows por um pipe."""
        saida = io.TextIOWrapper(io.BytesIO(), encoding="cp1252")
        erro = io.TextIOWrapper(io.BytesIO(), encoding="cp1252")
        with mock.patch("sys.stdout", saida), mock.patch("sys.stderr", erro):
            codigo = changelog.main(argv, self.raiz, lambda: DIA)
        saida.flush()
        erro.flush()
        return codigo, saida.buffer.getvalue().decode("utf-8"), erro.buffer.getvalue().decode("utf-8")

    def test_main_mostra_o_uso_e_escreve_nos_canais_certos(self):
        self.escrever("2026-10-31-a.md", "Categoria: Removido\n\n- Saiu.\n")
        for argv, esperado in ((["j.py", "0.1.0", "--outra"], 2), (["j.py", "--rascunho", "0.1.0"], 2),
                               (["j.py", "0.1.0", "0.2.0"], 2), (["j.py", "--rascunho"], 0),
                               (["j.py", "0.1.0", "--rascunho"], 0), (["j.py"], 0), (["j.py", "0.2.0"], 1)):
            with self.subTest(argv=argv):
                codigo, _, erro = self.correr_main(argv)
                self.assertEqual(codigo, esperado)
                self.assertEqual(bool(erro), esperado != 0)

    def test_caracteres_fora_do_cp1252_saem_em_utf8(self):
        self.escrever("2026-10-31-a.md", "Categoria: Adicionado\n\n- O ✻ da barra.\n")
        self.assertIn("- O ✻ da barra.", self.correr_main(["j.py", "0.1.0", "--rascunho"])[1])
        self.escrever("2026-10-31-b.md", "Categoria: ✻\n\n- x\n")
        self.assertIn("categoria desconhecida: ✻", self.correr_main(["j.py", "0.1.0"])[2])


class ComoScript(unittest.TestCase):

    def test_roda_como_script_e_so_mostra_o_uso(self):
        # Um argumento que não grava nada: num projeto real, um "--rascunho" lido pelo código antigo como número da
        # versão juntou os fragmentos a sério no repositório verdadeiro.
        codigo, saida, erro = correr_como_script(SCRIPT, b"", ["--ajuda"])
        self.assertEqual((codigo, saida), (2, ""))
        self.assertIn("juntar_changelog.py [<versão>] [--rascunho]", erro)


if __name__ == "__main__":
    unittest.main()
