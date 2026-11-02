"""Portão da mensagem do commit (modelos/git/portoes/mensagem_commit.py): formato da skill git-e-commits.

Título `tipo(área): …` com até 72 caracteres e sem ponto final; linha em branco; corpo com o porquê em
fix/feat/refactor; um fix sem arquivo de teste leva `Sem-teste: <motivo>`; um feat ou fix no que se publica leva
um fragmento em changelog.d/ ou `Sem-changelog: <motivo>`; tirar linhas de um teste pede `Teste-mudado:`.
"""

import io
import runpy
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from carregar_modelos import PASTA_PORTOES, carregar_portao

mensagem = carregar_portao("mensagem_commit")
CORPO = "\n\nO que mudou e porquê.\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n"
COM_TESTE = ["src/a.py", "tests/test_a.py"]


class Titulo(unittest.TestCase):

    def test_formatos_aceitos(self):
        for titulo in ("docs(regras): plano 01", "fix: sem área", "chore(ci): versões fixas"):
            with self.subTest(titulo=titulo):
                self.assertEqual(mensagem.erros(titulo + CORPO, COM_TESTE), [])

    def test_merge_e_revert_passam_como_o_git_os_escreve(self):
        self.assertEqual(mensagem.erros("Merge branch 'main' into x\n", []), [])
        self.assertEqual(mensagem.erros('Revert "feat: x"\n\nThis reverts commit abc.\n', []), [])

    def test_sem_tipo_e_recusado(self):
        erros = mensagem.erros("Instalador: só reinicia" + CORPO, [])
        self.assertEqual(len(erros), 1)
        self.assertIn("tipo(área)", erros[0])

    def test_tipo_desconhecido_e_recusado(self):
        self.assertIn("tipo(área)", mensagem.erros("coisa(x): y" + CORPO, [])[0])

    def test_titulo_longo_e_recusado(self):
        erros = mensagem.erros("docs: " + "a" * 67 + CORPO, [])
        self.assertEqual(len(erros), 1)
        self.assertIn("73 caracteres", erros[0])

    def test_ponto_final_e_recusado(self):
        self.assertIn("ponto final", mensagem.erros("docs: frase." + CORPO, [])[0])

    def test_mensagem_vazia_ou_so_comentarios(self):
        self.assertIn("vazia", mensagem.erros("# Please enter the commit message\n\n", [])[0])


class Corpo(unittest.TestCase):

    def test_fix_feat_refactor_exigem_corpo(self):
        for tipo in ("fix", "feat", "refactor"):
            with self.subTest(tipo=tipo):
                erros = mensagem.erros(f"{tipo}(x): y\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n", COM_TESTE)
                self.assertEqual(len(erros), 1)
                self.assertIn("corpo", erros[0])

    def test_docs_pode_ir_sem_corpo(self):
        self.assertEqual(mensagem.erros("docs: só o título\n", []), [])

    def test_falta_a_linha_em_branco_depois_do_titulo(self):
        self.assertIn("linha em branco", mensagem.erros("docs: x\ncorpo colado\n", [])[0])

    def test_comentarios_do_git_nao_contam(self):
        self.assertEqual(mensagem.erros("docs: x\n# Changes to be committed:\n#\tmodified: a\n", []), [])


class SemTeste(unittest.TestCase):

    def test_fix_sem_arquivo_de_teste_e_recusado(self):
        erros = mensagem.erros("fix(x): y" + CORPO, ["src/a.ts", "docs/testes.md"])
        self.assertEqual(len(erros), 1)
        self.assertIn("Sem-teste:", erros[0])

    def test_reconhece_os_testes_de_varias_linguagens(self):
        for teste in ("tests/test_a.py", "test/a.js", "src/a.test.ts", "src/a.spec.tsx", "pkg/test_b.py"):
            with self.subTest(teste=teste):
                self.assertEqual(mensagem.erros("fix(x): y" + CORPO, ["src/a.ts", teste]), [])

    def test_fix_sem_teste_com_motivo_passa(self):
        texto = "fix(x): y\n\nPorquê.\n\nSem-teste: só muda os fins de linha\n"
        self.assertEqual(mensagem.erros(texto, ["a.py"]), [])

    def test_sem_teste_sem_motivo_nao_conta(self):
        self.assertIn("Sem-teste:", mensagem.erros("fix(x): y\n\nPorquê.\n\nSem-teste:\n", ["a.py"])[0])

    def test_outros_tipos_nao_precisam_de_teste(self):
        self.assertEqual(mensagem.erros("feat(x): y" + CORPO, ["a.py"]), [])


class SemChangelog(unittest.TestCase):

    def setUp(self):
        publicado = mock.patch.object(mensagem, "PUBLICADO", ("src/", "instalador/"))
        publicado.start()
        self.addCleanup(publicado.stop)

    def test_feat_ou_fix_no_que_se_publica_sem_fragmento_e_recusado(self):
        for arquivo in ("src/a.py", "instalador/b.ps1"):
            for tipo in ("feat", "fix"):
                with self.subTest(arquivo=arquivo, tipo=tipo):
                    erros = mensagem.erros(f"{tipo}(x): y" + CORPO, [arquivo, "tests/test_a.py"])
                    self.assertEqual(len(erros), 1)
                    self.assertIn("Sem-changelog:", erros[0])

    def test_com_fragmento_passa(self):
        arquivos = ["src/a.py", "tests/test_a.py", "changelog.d/2026-10-31-barra.md"]
        self.assertEqual(mensagem.erros("feat(barra): y" + CORPO, arquivos), [])

    def test_fragmento_tem_de_ser_md_na_pasta(self):
        arquivos = ["src/a.py", "tests/test_a.py", "changelog.d/README.txt", "docs/changelog.d/x.md"]
        self.assertEqual(len(mensagem.erros("feat(barra): y" + CORPO, arquivos)), 1)

    def test_sem_changelog_com_motivo_passa_e_sem_motivo_nao_conta(self):
        self.assertEqual(mensagem.erros("fix(x): y\n\nPorquê.\n\nSem-changelog: só um comentário\n",
                                        ["src/a.py", "tests/test_a.py"]), [])
        self.assertIn("Sem-changelog:", mensagem.erros("feat(x): y\n\nPorquê.\n\nSem-changelog:\n", ["src/a.py"])[0])

    def test_outros_tipos_e_outras_pastas_nao_precisam(self):
        self.assertEqual(mensagem.erros("refactor(x): y" + CORPO, ["src/a.py"]), [])
        self.assertEqual(mensagem.erros("feat(x): y" + CORPO, ["scripts/a.py"]), [])

    def test_sem_publicado_o_changelog_nao_e_exigido(self):
        with mock.patch.object(mensagem, "PUBLICADO", ()):
            self.assertEqual(mensagem.erros("feat(x): y" + CORPO, ["src/a.py"]), [])


class TesteMudado(unittest.TestCase):

    def test_tirar_linhas_de_um_teste_sem_motivo_e_recusado(self):
        erros = mensagem.erros("test(x): y\n", ["tests/a.py"], ["tests/a.py"])
        self.assertEqual(len(erros), 1)
        self.assertIn("Teste-mudado:", erros[0])
        self.assertIn("tests/a.py", erros[0])

    def test_com_motivo_passa_e_sem_motivo_nao_conta(self):
        self.assertEqual(mensagem.erros("test(x): y\n\nTeste-mudado: o nome da função mudou\n", ["tests/a.py"],
                                        ["tests/a.py"]), [])
        self.assertEqual(len(mensagem.erros("test(x): y\n\nTeste-mudado:\n", ["tests/a.py"], ["tests/a.py"])), 1)

    def test_acrescentar_casos_nao_pede_nada(self):
        self.assertEqual(mensagem.erros("test(x): y\n", ["tests/a.py"], []), [])
        self.assertEqual(mensagem.erros("test(x): y\n", ["tests/a.py"]), [])

    def test_le_do_indice_so_os_testes_com_linhas_tiradas(self):
        saida = "3\t1\ttests/a.py\n2\t0\ttests/b.py\n-\t-\ttests/c.png\n0\t4\tsrc/d.test.ts\n5\t5\tsrc/e.py\n"
        correr = mock.Mock(return_value=SimpleNamespace(stdout=saida))
        self.assertEqual(mensagem.testes_com_linhas_tiradas(correr), ["tests/a.py", "tests/c.png", "src/d.test.ts"])
        self.assertEqual(correr.call_args.args[0], ["git", "diff", "--cached", "--numstat", "--diff-filter=M"])


class PontoDeEntrada(unittest.TestCase):

    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.arquivo = Path(pasta.name) / "COMMIT_EDITMSG"

    def test_arquivos_do_commit_vem_do_indice(self):
        correr = mock.Mock(return_value=SimpleNamespace(stdout="a.py\ntests/b.py\n"))
        self.assertEqual(mensagem.arquivos_do_commit(correr), ["a.py", "tests/b.py"])
        self.assertEqual(correr.call_args.args[0], ["git", "diff", "--cached", "--name-only"])

    def correr_main(self, texto):
        self.arquivo.write_bytes(texto.encode("utf-8"))
        falso = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
        with mock.patch.object(mensagem, "arquivos_do_commit", return_value=["a.py"]), mock.patch("sys.stderr", falso), \
                mock.patch.object(mensagem, "testes_com_linhas_tiradas", return_value=[]):
            codigo = mensagem.main(["mensagem_commit.py", str(self.arquivo)])
        falso.flush()
        return codigo, falso.buffer.getvalue().decode("utf-8")

    def test_recusa_e_mostra_como_corrigir(self):
        codigo, erro = self.correr_main("Instalador: título à moda antiga\n")
        self.assertEqual(codigo, 1)
        self.assertIn("tipo(área)", erro)
        self.assertIn("Commit recusado", erro)

    def test_aceita_calado(self):
        self.assertEqual(self.correr_main("docs: título\n"), (0, ""))

    def test_roda_como_script(self):
        self.arquivo.write_bytes(b"docs: x\n")
        correr = mock.Mock(return_value=SimpleNamespace(stdout=""))
        with mock.patch("subprocess.run", correr), mock.patch("sys.argv", ["m.py", str(self.arquivo)]), \
                self.assertRaises(SystemExit) as saida:
            runpy.run_path(str(PASTA_PORTOES / "mensagem_commit.py"), run_name="__main__")
        self.assertEqual(saida.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
