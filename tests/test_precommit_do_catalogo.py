"""O que o teste de `projetos/` lê (índice, commits do intervalo, árvore) e o passo do `.githooks/pre-commit` que o
roda em todos os commits, provados em repositórios temporários com uma cópia dos hooks e do teste: nunca no próprio
repositório. As variáveis GIT_* do ambiente saem (num commit de verdade o git as define), e a configuração global
também (a identidade e o `morg.listaNegra` de quem roda não entram)."""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

import dados_do_catalogo as catalogo
from carregar_modelos import RAIZ
from projeto_de_exemplo import apagar, escrever, git

NUMERO = "123" + "456" + "789"  # conhecido como falso (ver test_dados_do_catalogo.py)
PALAVRAS = "## comuns\numa\noutra\n## nomes\nEmpresa A | papel\n"
COPIAS = (".githooks", "tests/test_projetos_sem_dados.py", "tests/dados_do_catalogo.py", "tests/carregar_modelos.py",
          "modelos/testes/carregar_por_caminho.py", "modelos/testes/test_dados_pessoais.py")
FERRAMENTAS_DO_HOOK = ("git", "sh", "grep", "mktemp", "rm", "wc", "head", "dirname", "cat")
ARQUIVO = "projetos/erp-de-servicos/sonda.md"


def ambiente_limpo(**extra):
    base = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "MORG_"))}
    return {**base, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", **extra}


class RepositorioTemporario(unittest.TestCase):

    def setUp(self):
        self.pasta = Path(tempfile.mkdtemp(prefix="morg-catalogo-"))
        self.addCleanup(apagar, self.pasta)
        self.ambiente = ambiente_limpo()
        for copia in COPIAS:
            origem, destino = RAIZ / copia, self.pasta / copia
            destino.parent.mkdir(parents=True, exist_ok=True)
            (shutil.copytree if origem.is_dir() else shutil.copy2)(origem, destino)
        escrever(self.pasta / catalogo.PALAVRAS, PALAVRAS)
        escrever(self.pasta / "projetos" / "README.md", "| projeto | o que é |\n|---|---|\n")
        self.git("init", "-q")
        for chave, valor in (("user.email", "1+ana@users.noreply.github.com"), ("user.name", "Ana"),
                             ("core.autocrlf", "false"), ("morg.lista" + "Negra", "")):
            self.git("config", "--local", chave, valor)
        self.git("add", "--", ".")
        self.git("commit", "-q", "-m", "docs(x): base")  # sem os hooks ligados ainda
        self.git("config", "--local", "core." + "hooksPath", ".githooks")

    def git(self, *argumentos, **opcoes):
        return git(self.pasta, *argumentos, env=opcoes.pop("env", self.ambiente), **opcoes)

    def commits(self):
        return int(self.git("rev-list", "--count", "HEAD").stdout)

    def preparar(self, texto, nome=ARQUIVO):
        escrever(self.pasta / nome, texto)
        self.git("add", "--", nome)

    def tentar_commitar(self, env=None):
        return self.git("commit", "-q", "-m", "docs(x): sonda", check=False, env=env or self.ambiente)

    def assertRecusado(self, resultado, tipo, antes):
        self.assertNotEqual(resultado.returncode, 0, resultado.stdout)
        self.assertIn(tipo, resultado.stdout + resultado.stderr)
        self.assertEqual(self.commits(), antes)


class PreCommitDoCatalogo(RepositorioTemporario):

    def test_dado_fictício_e_recusado_com_o_tipo(self):
        antes = self.commits()
        self.preparar(f"Uma linha com o número {NUMERO} aqui.\n")
        self.assertRecusado(self.tentar_commitar(), "documento", antes)

    def test_nome_proprio_fora_da_lista_e_recusado(self):
        antes = self.commits()
        self.preparar("Uma linha que fala do Fulano.\n")
        self.assertRecusado(self.tentar_commitar(), "nome próprio", antes)

    def test_texto_limpo_passa(self):
        self.preparar("Uma linha limpa, da Empresa A.\n")
        resultado = self.tentar_commitar()
        self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)

    def test_arquivo_que_nao_e_md_em_projetos_e_recusado_mesmo_com_texto_limpo(self):
        antes = self.commits()
        for nome in ("sonda.pdf", "sonda.png", "sonda.txt"):
            with self.subTest(nome=nome):
                self.preparar(f"número {NUMERO}\n", f"projetos/erp-de-servicos/{nome}")
                self.assertRecusado(self.tentar_commitar(), "só arquivos .md", antes)

    def test_o_teste_le_o_indice_e_nao_o_disco(self):
        antes = self.commits()
        self.preparar(f"número {NUMERO}\n")
        escrever(self.pasta / ARQUIVO, "Uma linha limpa só no disco.\n")  # o índice continua sujo
        self.assertRecusado(self.tentar_commitar(), "documento", antes)

    def test_dado_so_no_disco_nao_barra_o_que_esta_preparado(self):
        self.preparar("Uma linha limpa.\n")
        escrever(self.pasta / ARQUIVO, f"número {NUMERO}\n")  # fica fora do commit
        self.assertEqual(self.tentar_commitar().returncode, 0)

    def test_sem_python_o_commit_nao_passa_nem_com_MORG_PY_errado_nem_sem_py_no_PATH(self):
        self.preparar("Uma linha limpa.\n")
        antes = self.commits()
        self.assertRecusado(self.tentar_commitar(ambiente_limpo(MORG_PY="/nao/existe")), "sem Python", antes)

    @unittest.skipIf(os.name == "nt", "o PATH só com as ferramentas do hook usa ligações simbólicas")
    def test_sem_py_nem_python3_no_path_o_commit_nao_passa(self):
        ferramentas = Path(tempfile.mkdtemp(prefix="morg-ferramentas-"))
        self.addCleanup(apagar, ferramentas)
        for nome in FERRAMENTAS_DO_HOOK:
            (ferramentas / nome).symlink_to(shutil.which(nome))
        self.preparar("Uma linha limpa.\n")
        antes = self.commits()
        self.assertRecusado(self.tentar_commitar(ambiente_limpo(PATH=str(ferramentas))), "sem Python", antes)

    def test_termo_da_lista_negra_que_o_python_nao_compila_e_acusado(self):
        lista = self.pasta / "lista.txt"
        escrever(lista, "*" + "abc\n")
        self.git("config", "--local", "morg.lista" + "Negra", str(lista))
        self.preparar("Uma linha limpa.\n")
        antes = self.commits()
        self.assertRecusado(self.tentar_commitar(), "o termo n.º 1 não compila", antes)


class LeituraDoIntervaloEDaArvore(RepositorioTemporario):

    def commitar(self, texto, nome=ARQUIVO):
        self.preparar(texto, nome)
        self.git("commit", "-q", "-m", "docs(x): c", "--no-verify")  # o passo do hook já tem os testes acima
        return self.git("rev-parse", "HEAD").stdout.strip()

    def textos(self, ambiente):
        return [c.texto for c in catalogo.conteudos_a_verificar(self.pasta, ambiente)]

    def test_o_intervalo_apanha_o_commit_do_meio_mesmo_limpo_no_seguinte(self):
        base = self.git("rev-parse", "HEAD").stdout.strip()
        self.commitar(f"número {NUMERO}\n")
        self.commitar("Uma linha limpa.\n")
        sujo = catalogo.problemas(catalogo.conteudos_a_verificar(self.pasta, {"MORG_BASE_DE_COMPARACAO": base}), [])
        self.assertEqual(len(sujo), 1)
        self.assertIn("documento", sujo[0])

    def test_base_so_de_zeros_ou_desconhecida_cai_para_toda_a_historia(self):
        self.commitar(f"número {NUMERO}\n")
        self.commitar("Uma linha limpa.\n")
        for base in ("0" * 40, "f" * 40):
            with self.subTest(base=base):
                achados = catalogo.problemas(catalogo.conteudos_a_verificar(self.pasta, {"MORG_BASE_DE_COMPARACAO": base}), [])
                self.assertEqual(len(achados), 1)

    def test_o_intervalo_so_le_o_que_o_intervalo_traz(self):
        self.commitar(f"número {NUMERO}\n")
        base = self.commitar("Uma linha limpa.\n")
        self.commitar("Outra linha limpa.\n", "projetos/erp-de-servicos/outra.md")
        achados = catalogo.problemas(catalogo.conteudos_a_verificar(self.pasta, {"MORG_BASE_DE_COMPARACAO": base}), [])
        self.assertEqual(achados, [])

    def test_arquivo_que_nao_e_md_e_acusado_no_intervalo_e_na_arvore_sem_ler_o_conteudo(self):
        base = self.git("rev-parse", "HEAD").stdout.strip()
        self.commitar(f"número {NUMERO}\n", "projetos/erp-de-servicos/sonda.pdf")
        for ambiente in ({"MORG_BASE_DE_COMPARACAO": base}, {}):
            with self.subTest(ambiente=ambiente):
                achados = catalogo.problemas(catalogo.conteudos_a_verificar(self.pasta, ambiente), [])
                self.assertEqual(len(achados), 1)
                self.assertIn("só arquivos .md", achados[0])
                self.assertNotIn("documento", achados[0])

    def test_a_arvore_le_o_disco_com_os_arquivos_novos(self):
        escrever(self.pasta / "projetos" / "nova.md", f"número {NUMERO}\n")  # nem preparado
        self.assertIn(f"número {NUMERO}\n", self.textos({}))

    def test_o_indice_le_so_o_preparado_e_a_lista_mudada_rele_o_catalogo_todo(self):
        self.commitar("Uma linha limpa.\n")
        self.assertEqual(self.textos({"MORG_LER_DO_INDICE": "1"}), [])
        escrever(self.pasta / catalogo.PALAVRAS, PALAVRAS + "Outra | papel\n")
        self.git("add", "--", catalogo.PALAVRAS)
        origens = [c.origem for c in catalogo.conteudos_a_verificar(self.pasta, {"MORG_LER_DO_INDICE": "1"})]
        self.assertEqual(sorted(origens), ["projetos/README.md (preparado)", f"{ARQUIVO} (preparado)",
                                           f"{catalogo.PALAVRAS} (preparado)"])


if __name__ == "__main__":
    unittest.main()
