"""O detector de dados do manual (`dados_do_manual.py`): os casos puros, a leitura do índice e do disco em repositórios
temporários e o passo do `.githooks/pre-commit` que o roda em todos os commits. Nunca no próprio repositório."""

import unittest

import dados_do_catalogo as catalogo
import dados_do_manual as manual
import test_precommit_do_catalogo as base

NUMERO = "123" + "456" + "789"  # conhecido como falso
CITAVEIS = frozenset({"Fabio Akita", "Carlobks"})
ACEITOS = CITAVEIS | {"GitHub", "Markdown"}
DOMINIOS = catalogo.DOMINIOS_ACEITOS | {"docs.github.com"}
ARQUIVO = "manual/03-pedir.md"


def tipos(texto, aceitos=ACEITOS, dominios=DOMINIOS):
    return [tipo for _, tipo, _ in manual.dados_do_manual(texto, aceitos, dominios)]


class DadosDoTexto(unittest.TestCase):

    def test_nome_de_arquivo_fora_das_crases_reprova_e_com_crases_passa(self):
        achados = tipos("Leia o AGENTS.md antes.\n")
        self.assertEqual(len(achados), 1)
        self.assertIn("ponha em crases", achados[0])
        self.assertEqual(tipos("Leia o `AGENTS.md` antes.\n"), [])

    def test_o_que_o_catalogo_detecta_continua_detectado(self):
        for texto, tipo in ((f"número {NUMERO}\n", "documento"), ("escreva a fulano@exemplo.com.br\n", "e-mail"),
                            ("pagou 10 euros\n", "dinheiro"), ("o caminho /home/fulano/x\n", "caminho")):
            with self.subTest(tipo=tipo):
                self.assertIn(tipo, tipos(texto))

    def test_o_alvo_de_um_link_nao_conta_e_o_dominio_solto_so_se_for_do_fontes(self):
        self.assertEqual(tipos("Veja [o guia](https://exemplo.dev/a/README.md).\n"), [])
        self.assertEqual(tipos("Veja docs.github.com.\n"), [])
        self.assertEqual(tipos("Veja exemplo.dev.\n"), ["domínio (se for nome de arquivo, ponha em crases)"])

    def test_duas_palavras_com_maiuscula_fora_do_inicio_de_frase_e_nao_aceitas_reprovam(self):
        for texto in ("Falei com Maria Souza ontem.\n", "Ontem Maria Souza falou.\n", "Foi Fabio Akita Souza.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(tipos(texto), ["nome de pessoa"])

    def test_nomes_citaveis_publicos_e_inicio_de_frase_passam(self):
        for texto in ("Leu Fabio Akita no GitHub Markdown.\n", "Depois Maria foi embora.\n", "Fabio Akita e Carlobks.\n",
                      "Disse Bia.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(tipos(texto), [])

    def test_os_achados_saem_por_linha(self):
        achados = manual.dados_do_manual(f"limpo\nnúmero {NUMERO}\nOntem Maria Souza.\n", ACEITOS, DOMINIOS)
        self.assertEqual([linha for linha, _, _ in achados], [2, 3])

    def test_a_lista_de_pessoas_ignora_comentarios_e_linhas_em_branco(self):
        self.assertEqual(manual.pessoas_citaveis("# nota\n\nFabio Akita\n  Bia  \n"), {"Fabio Akita", "Bia"})

    def test_os_dominios_vem_dos_enderecos_do_fontes(self):
        fontes = "- **A** — https://code.claude.com/docs/en/memory, e [b](https://Docs.GitHub.com/x).\n"
        dominios = manual.dominios_do_fontes(fontes)
        self.assertLessEqual({"code.claude.com", "docs.github.com", "user.name"}, dominios)

    def test_problemas_diz_onde_e_nunca_mostra_o_termo_da_lista_negra(self):
        conteudos = [manual.Conteudo("manual/a.md", f"número {NUMERO}\nFalei do zeca.\n")]
        mensagens = manual.problemas(conteudos, (ACEITOS, DOMINIOS), ["zeca", "*" + "abc"], {"CI": "true"})
        nao_compila = "lista negra: o termo n.º 2 não compila em Python (classe POSIX ou sintaxe só do grep -E); reescreva-o"
        self.assertEqual(sorted(mensagens), [nao_compila, "manual/a.md:1: documento",
                                             "manual/a.md:2: lista negra — termo n.º 1"])


class SituacaoDoManual(base.RepositorioTemporario):

    def setUp(self):
        super().setUp()
        self.preparar("Fabio Akita\n", manual.PESSOAS)
        self.preparar("Um texto limpo.\n", ARQUIVO)
        self.git("commit", "-q", "-m", "docs(x): manual", "--no-verify")

    def nomes(self, ambiente):
        return sorted(c.origem for c in manual.situacao_do_manual(self.pasta, ambiente)[0])

    def test_o_indice_le_so_o_preparado(self):
        indice = {"MORG_LER_DO_INDICE": "1"}
        self.assertEqual(self.nomes(indice), [])
        self.preparar("Outro texto.\n", "manual/04-sessoes.md")
        self.assertEqual(self.nomes(indice), ["manual/04-sessoes.md"])

    def test_a_lista_de_pessoas_ou_o_fontes_mudados_releem_o_manual_todo(self):
        indice = {"MORG_LER_DO_INDICE": "1"}
        self.preparar("Fabio Akita\nBia\n", manual.PESSOAS)
        self.assertEqual(self.nomes(indice), [ARQUIVO])
        self.preparar("# Fontes\n", "FONTES.md")
        self.assertEqual(self.nomes(indice), [ARQUIVO])

    def test_o_disco_le_a_arvore_com_os_arquivos_novos_e_so_os_md(self):
        self.preparar("x\n", "manual/fontes/licenca.txt")
        base.escrever(self.pasta / "manual" / "nova.md", f"número {NUMERO}\n")
        self.assertEqual(self.nomes({}), [ARQUIVO, "manual/nova.md"])
        conteudos, (aceitos, _) = manual.situacao_do_manual(self.pasta, {})
        self.assertIn("Fabio Akita", aceitos)
        self.assertEqual(len(manual.problemas(conteudos, (aceitos, DOMINIOS), [])), 1)

    def test_o_disco_sem_o_arquivo_le_vazio(self):
        self.assertEqual(manual.ler_do_disco(self.pasta, "nao/existe.md"), "")


class PreCommitDoManual(base.RepositorioTemporario):

    def test_dado_no_manual_e_recusado_com_o_tipo(self):
        antes = self.commits()
        self.preparar(f"Uma linha com o número {NUMERO} aqui.\n", ARQUIVO)
        self.assertRecusado(self.tentar_commitar(), "documento", antes)

    def test_nome_de_arquivo_sem_crases_e_recusado(self):
        antes = self.commits()
        self.preparar("Leia o AGENTS.md primeiro.\n", ARQUIVO)
        self.assertRecusado(self.tentar_commitar(), "ponha em crases", antes)

    def test_texto_limpo_e_arquivo_que_nao_e_md_passam(self):
        self.preparar("Leia o `AGENTS.md` primeiro.\n", ARQUIVO)
        self.preparar(f"número {NUMERO}\n", "manual/fontes/licenca.txt")
        resultado = self.tentar_commitar()
        self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)

    def test_sem_o_teste_do_manual_no_disco_o_commit_nao_passa(self):
        (self.pasta / "tests" / "test_manual_sem_dados.py").unlink()
        self.preparar("Um texto limpo.\n", ARQUIVO)
        antes = self.commits()
        self.assertRecusado(self.tentar_commitar(), "falta tests/test_manual_sem_dados.py", antes)


if __name__ == "__main__":
    unittest.main()
