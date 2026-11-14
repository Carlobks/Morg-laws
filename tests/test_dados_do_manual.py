"""O detector de dados do manual (`dados_do_manual.py`): os casos puros, a leitura do índice e do disco em repositórios
temporários e o passo do `.githooks/pre-commit` que o roda em todos os commits. Nunca no próprio repositório."""

import unittest

import dados_do_catalogo as catalogo
import dados_do_manual as manual
import test_precommit_do_catalogo as base
import verificador_do_manual as verificador

NUMERO = "123" + "456" + "789"  # conhecido como falso
CITAVEIS = frozenset({"Fabio Akita", "Matt Pocock", "Carlobks", "Claude Code", "Bia"})
ABREM = frozenset({"veja", "leia", "depois", "disse"})
ACEITOS = CITAVEIS | {"GitHub", "Markdown", "RH", "Financeiro"}
DOMINIOS = catalogo.DOMINIOS_ACEITOS | {"docs.github.com"}
ARQUIVO = "manual/04-pedir.md"


def tipos(texto, aceitos=ACEITOS, dominios=DOMINIOS):
    return [tipo for _, tipo, _ in manual.dados_do_manual(texto, aceitos, dominios, ABREM, CITAVEIS)]


class NomesDoManual(unittest.TestCase):

    def test_os_nomes_sao_proprios_e_as_regras_vem_do_catalogo_e_do_fontes(self):
        for novo in ("ConteudoDoManual", "problemas_do_manual", "PASTA_DO_MANUAL"):
            self.assertTrue(hasattr(manual, novo), novo)
        self.assertTrue(hasattr(verificador, "PASTA_DO_MANUAL"))
        for modulo, copiado in ((manual, ("Conteudo", "problemas", "PASTA", "ENDERECO", "ALVO_DE_LINK")),
                                (verificador, ("PASTA", "CRASES"))):
            for nome in copiado:
                self.assertFalse(hasattr(modulo, nome), f"{modulo.__name__}.{nome} devia vir de outro módulo")


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

    def test_nome_no_inicio_de_linha_de_lista_de_tabela_de_titulo_ou_com_particula_reprova(self):
        for texto in ("Maria Souza esteve aqui.\n", "- Maria Souza pediu o relatório.\n", "| Maria Souza | gerente |\n",
                      "## Maria Souza\n", "Resumo: Maria Souza pediu.\n", "Falei com João da Silva ontem.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(tipos(texto), ["nome de pessoa"])

    def test_imperativo_antes_de_nome_titulo_em_maiusculas_e_lista_de_nomes_passam(self):
        for texto in ("Veja Fabio Akita.\n", "Depois Maria foi.\n", "Leia AGENTS antes.\n", "Fabio Akita e Matt Pocock.\n",
                      "Então o Claude Code lê.\n", "Use **SEM DADOS REAIS:** sempre.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(tipos(texto), [])

    def test_tres_palavras_no_inicio_perdem_so_a_primeira(self):
        self.assertEqual(tipos("Maria Souza Costa foi.\n"), ["nome de pessoa"])

    def test_assunto_com_particula_e_um_citavel_no_inicio_da_frase_nao_e_nome(self):
        for texto in ("Escolha de Carlobks (2026-11-10): ficou assim.\n", "- Escolha de Carlobks: a curta.\n",
                      "| Escolha de Carlobks | sim |\n", "Pergunta de Carlobks: e agora?\n", "Nota da Bia: ler antes.\n",
                      "Nota de Fabio Akita: ler antes.\n", "Ana de Carlobks revisou.\n"):  # o último é o custo aceito
            with self.subTest(texto=texto):
                self.assertEqual(tipos(texto), [])

    def test_so_o_citavel_depois_da_particula_e_o_inicio_da_frase_isentam_a_corrida(self):
        for texto in ("Ana de Souza revisou.\n", "Pedro de Alcântara revisou.\n", "Rosa de Souza revisou.\n",
                      "Ana do RH revisou o contrato.\n", "Maria do Financeiro pagou.\n", "- Paulo do Financeiro: aprovou.\n",
                      "| Rita do RH | sim |\n", "e a Escolha de Carlobks no meio.\n", "Ana Souza Carlobks revisou.\n",
                      "Maria Souza revisou.\n", "Ontem, Maria de Souza revisou.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(tipos(texto), ["nome de pessoa"])

    def test_nome_de_arquivo_e_comando_dentro_de_um_bloco_de_codigo_passam_como_entre_crases(self):
        for texto in ("```text\nfix: o teste\n\nSem tests/test_x.py: motivo.\n```\n", "```sh\nrode scripts/testar.sh antes\n```\n",
                      "```sh\necho $1\n```\n", "~~~text\nSem tests/c.py\n~~~\n", "````text\nfix: `a.py` e tests/b.py\n````\n",
                      "```text\nabra empresa.digital\n```\n", "```text\nCusto: $1500 por mês\n```\n"):  # os dois últimos: o custo
            with self.subTest(texto=texto):
                self.assertEqual(tipos(texto), [])

    def test_dado_de_verdade_num_bloco_continua_acusado_e_a_prosa_perto_dele_tambem(self):
        for texto, quantos in (("```text\nabra empresa-real.pt no navegador\n```\n", 1), ("~~~\nabra empresa-real.com\n~~~\n", 1),
                               ("```text\nescreva a fulano@empresa-real.pt\n```\n", 2), ("O arquivo test_x.py roda.\n", 1),
                               ("```\nabra a\n\nDepois empresa.digital aqui.\n", 1),
                               ("````text\n```\nx\n```\nDepois empresa.digital aqui.\n", 1),
                               ("```text\nFalei com Maria Souza ontem.\n```\n", 1),
                               ("```text\nabra empresa.digital\n````\nDepois empresa.digital aqui.\n", 1),
                               ("```text\nabra empresa.digital\n```  \nDepois empresa.digital aqui.\n", 1),
                               ("```text\nabra empresa.digital\n``` x\nDepois empresa.digital aqui.\n", 2),
                               ("``` `x`\nabra empresa.digital\n```\n", 1),
                               ("    ```\n    abra empresa.digital\n    ```\n", 1)):
            with self.subTest(texto=texto):
                self.assertEqual(len(tipos(texto)), quantos)
        achados = manual.dados_do_manual(f"limpo\n```text\nSem tests/a.py\n```\nnúmero {NUMERO}\n", ACEITOS, DOMINIOS)
        self.assertEqual([linha for linha, _, _ in achados], [5])

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
        conteudos = [manual.ConteudoDoManual("manual/a.md", f"número {NUMERO}\nFalei do zeca.\n")]
        mensagens = manual.problemas_do_manual(conteudos, (ACEITOS, DOMINIOS, ABREM, CITAVEIS), ["zeca", "*" + "abc"], {"CI": "true"})
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
        self.preparar("Outro texto.\n", "manual/05-sessoes.md")
        self.assertEqual(self.nomes(indice), ["manual/05-sessoes.md"])

    def test_a_lista_de_pessoas_ou_o_fontes_mudados_releem_o_manual_todo(self):
        indice = {"MORG_LER_DO_INDICE": "1"}
        self.preparar("Fabio Akita\nBia\n", manual.PESSOAS)
        self.assertEqual(self.nomes(indice), [ARQUIVO])
        self.preparar("# Fontes\n", "FONTES.md")
        self.assertEqual(self.nomes(indice), [ARQUIVO])

    def test_a_lista_publica_de_palavras_mudada_rele_o_manual_todo(self):
        self.preparar("# lista\n", catalogo.PALAVRAS)
        self.assertEqual(self.nomes({"MORG_LER_DO_INDICE": "1"}), [ARQUIVO])

    def test_os_nomes_citaveis_e_as_palavras_que_abrem_frase_mudados_releem_o_manual_todo(self):
        for lista in (manual.NOMES_CITAVEIS, manual.PALAVRAS_QUE_ABREM):
            with self.subTest(lista=lista):
                self.preparar("x\n", lista)
                self.assertEqual(self.nomes({"MORG_LER_DO_INDICE": "1"}), [ARQUIVO])
                self.git("commit", "-q", "-m", "docs(x): lista", "--no-verify")

    def test_a_situacao_junta_as_quatro_listas_e_as_comuns(self):
        self.preparar("Claude Code\n", manual.NOMES_CITAVEIS)
        self.preparar("# nota\nLeia\n", manual.PALAVRAS_QUE_ABREM)
        _, (aceitos, _, abrem, citaveis) = manual.situacao_do_manual(self.pasta, {})
        self.assertLessEqual({"Fabio Akita", "Claude Code"}, aceitos)
        self.assertLessEqual({"leia"}, abrem)
        self.assertEqual(citaveis, {"Fabio Akita"})

    def test_o_citavel_da_lista_isenta_o_assunto_no_manual_lido_do_disco(self):
        """«Escolha de Carlobks» tem duas palavras contadas: sem os citáveis, é acusada (com três, a primeira já sai)."""
        self.preparar("Fabio Akita\nCarlobks\n", manual.PESSOAS)
        base.escrever(self.pasta / "manual" / "nova.md", "Escolha de Carlobks: a curta.\nNota de Maria Souza.\n")
        conteudos, situacao = manual.situacao_do_manual(self.pasta, {})
        self.assertEqual(manual.problemas_do_manual(conteudos, situacao, [], {"CI": "true"}),
                         ["manual/nova.md:2: nome de pessoa"])

    def test_o_disco_le_a_arvore_com_os_arquivos_novos_e_so_os_md(self):
        self.preparar("x\n", "manual/fontes/licenca.txt")
        base.escrever(self.pasta / "manual" / "nova.md", f"número {NUMERO}\n")
        self.assertEqual(self.nomes({}), [ARQUIVO, "manual/nova.md"])
        conteudos, (aceitos, _, _, _) = manual.situacao_do_manual(self.pasta, {})
        self.assertIn("Fabio Akita", aceitos)
        self.assertEqual(len(manual.problemas_do_manual(conteudos, (aceitos, DOMINIOS, ABREM, CITAVEIS), [])), 1)

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
