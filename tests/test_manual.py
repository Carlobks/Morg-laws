"""O verificador do manual de uso (`manual/`): cada verificação tem um caso que passa e um que reprova, provados numa
pasta temporária, nunca no próprio repositório. Os arquivos de `manual/` só são conferidos depois do `git add`."""

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import verificador_do_manual as verificador
from carregar_modelos import RAIZ
from leitura_do_repositorio import arquivos_do_git

FONTES_MD = ("# Fontes\n\n## Livros e autores\n\n- **Livro** (livro).\n  - pp. 30–32, 124 e 411: x.\n"
             "  - p. 165: y.\n\n## Outra\n\n- p. 999: fora da seção dos livros.\n")
BIBLIA = "- Um conselho. (pp. 118, 120–121) · **texto**\n"
PAR = "## P6 As quatro partes\n\n### Na prática\n\nEscreva o que quer.\n\n### Por quê e fonte\n\n{teoria}\n"
TEORIA_COM_LINK = "O porquê está [aqui](https://example.com/x)."
NOME = "manual/10-glossario.md"  # parte com teto e sem seções que peçam fonte
VOZES = "as vozes da cabeça de Carlobks (decisão de 2026-11-08)"


def par(teoria=TEORIA_COM_LINK):
    return "# Pedir\n\n" + PAR.format(teoria=teoria)


class ManualTemporario(unittest.TestCase):

    def setUp(self):
        self.raiz = Path(tempfile.mkdtemp(prefix="morg-manual-"))
        self.addCleanup(shutil.rmtree, self.raiz, ignore_errors=True)
        self.escrever("FONTES.md", FONTES_MD)
        self.escrever("biblia-akita/pedidos.md", BIBLIA)

    def escrever(self, nome, texto):
        caminho = self.raiz / nome
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(texto, encoding="utf-8")

    def erros(self, nome, texto):
        """Os erros do manual com um único arquivo, `nome`, com `texto`."""
        self.escrever(nome, texto)
        return verificador.erros_do_manual(self.raiz, [nome])


class PorTexto(ManualTemporario):

    def test_link_solto_reprova_e_link_marcado_ou_em_codigo_passa(self):
        self.assertEqual(len(self.erros(NOME, "Veja https://example.com/x agora.\n")), 1)
        for texto in ("Veja [o site](https://example.com/x).\n", "Veja `https://example.com/x`.\n",
                      "```\nhttps://example.com/x\n```\n"):
            with self.subTest(texto=texto):
                self.assertEqual(self.erros(NOME, texto), [])

    def test_pagina_do_livro_sem_entrada_reprova(self):
        for texto in ("O livro diz (p. 999).\n", "O livro diz (pp. 30–39).\n", "Veja p. 5 e p. 31.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(len(self.erros(NOME, texto)), 1)

    def test_pagina_do_livro_com_entrada_passa_no_fontes_ou_na_biblia(self):
        for texto in ("O livro diz (pp. 30–32, 124 e 411).\n", "Veja p. 165 e pp. 118, 120–121.\n", "Veja `p. 999`.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(self.erros(NOME, texto), [])

    def test_decisao_sem_porque_reprova_e_com_porque_passa(self):
        sem = f"Foi assim porque {VOZES} quis.\n"
        com = f"Foi assim porque {VOZES} quis. Porquê: para ser simples.\n"
        self.assertEqual(len(self.erros(NOME, sem)), 1)
        self.assertEqual(self.erros(NOME, com), [])
        self.assertEqual(self.erros(NOME, "Explica “as vozes da cabeça de Carlobks” numa linha.\n"), [])
        self.assertEqual(len(self.erros(NOME, f"Porquê: antes.\n\n{sem}")), 1)

    def test_decisao_na_forma_curta_sem_porque_reprova(self):
        curta = "Decisão de Carlobks (2026-11-06): o número é cinco.\n"
        self.assertEqual(len(self.erros(NOME, curta)), 1)
        self.assertEqual(self.erros(NOME, curta.replace("\n", " Porquê: cabe numa tela.\n")), [])

    def test_no_codex_sem_link_reprova_e_com_link_passa(self):
        self.assertEqual(len(self.erros(NOME, "No Codex o arquivo se chama AGENTS.\n")), 1)
        com = "No Codex vale o mesmo ([documentação](https://example.com/codex/agents)).\n"
        self.assertEqual(self.erros(NOME, com), [])
        self.assertEqual(self.erros(NOME, "O autor ainda não usou o Claude.\n"), [])

    def test_todo_paragrafo_com_codex_pede_o_link_e_a_excecao_esta_a_vista(self):
        for texto in ("O Codex lê o `AGENTS.md` sozinho.\n", "O Codex lê o arquivo.\n\nOutro.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(len(self.erros(NOME, texto)), 1)
        self.assertEqual(self.erros(NOME, "O Codex lê o [guia](https://example.com/codex/agents).\n"), [])
        self.assertEqual(len(self.erros(NOME, "O que vale: `no Codex [x](https://example.com/codex)`.\n")), 0)
        self.assertEqual(len(self.erros(NOME, "Veja `https://example.com/codex` no Codex.\n")), 1)
        self.assertEqual(self.erros(NOME, "```\nno Codex\n```\n"), [])
        frase = "O autor ainda não usou o Codex."
        with mock.patch.object(verificador, "EXCECOES_DO_CODEX", frozenset({(NOME, frase)})):
            self.assertEqual(self.erros(NOME, frase + "\n"), [])
        self.assertEqual(len(self.erros(NOME, frase + "\n")), 1)

    def test_pagina_ou_pag_por_extenso_reprova_e_pede_p_n(self):
        for texto in ("Veja a página 31.\n", "Veja pág. 9.\n", "Veja as págs. 9 e 10.\n", "Veja páginas 3–5.\n"):
            with self.subTest(texto=texto):
                erros = self.erros(NOME, texto)
                self.assertEqual(len(erros), 1)
                self.assertIn("escreva p. N", erros[0])
        self.assertEqual(self.erros(NOME, "A página inicial do site e a `página 3`.\n"), [])

    def test_no_codex_com_link_que_nao_e_do_codex_reprova(self):
        self.assertEqual(len(self.erros(NOME, "No Codex vale o mesmo ([doc](https://example.com/x)).\n")), 1)

    def test_porque_antes_da_decisao_no_mesmo_paragrafo_reprova(self):
        self.assertEqual(len(self.erros(NOME, f"Porquê: antes. Foi {VOZES}.\n")), 1)

    def test_so_pt_br(self):
        erros = self.erros(NOME, "Abra o ficheiro.\n")
        self.assertEqual(len(erros), 1)
        self.assertIn("português de Portugal", erros[0])


class AfirmacaoDeMedicao(ManualTemporario):

    def test_nenhum_texto_diz_que_as_regras_foram_medidas_passa(self):
        self.assertEqual(self.erros(NOME, "Nenhum texto diz que as regras foram medidas.\n"), [])
        self.assertEqual(self.erros(NOME, "As regras nunca foram medidas.\n"), [])

    def test_as_regras_foram_medidas_reprova(self):
        for texto in ("As regras foram medidas.\n", "O Morg-laws foi testado em 12 casos.\n",
                      "A regra está comprovada. Nada mais.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(len(self.erros(NOME, texto)), 1)

    def test_a_medida_que_passa_porque_nao_ha_regra(self):
        self.assertEqual(self.erros(NOME, "À medida que o contexto enche, a atenção cai.\n"), [])
        self.assertEqual(self.erros(NOME, "A regra é curta e as skills são claras.\n"), [])
        self.assertEqual(len(self.erros(NOME, "Não é um número. As regras foram medidas.\n")), 1)

    def test_a_ressalva_quebrada_em_linhas_passa_e_a_afirmacao_quebrada_reprova(self):
        ressalva = ("> **A medição paga não foi feita.** As tentativas nunca correram, por decisão do dono: a validação\n"
                    "> das regras passa a ser pelo uso real. Nenhum resultado\n"
                    "> deste banco pode ser apresentado como medido, e nenhum documento pode dizer que as regras\n"
                    "> foram medidas.\n")
        self.assertEqual(self.erros(NOME, ressalva), [])
        self.assertEqual(len(self.erros(NOME, "As regras do Morg-laws foram\nmedidas em 12 casos.\n")), 1)
        self.assertEqual(len(verificador.medido_sem_negacao(NOME, "A regra (veja p. 3) foi medida.\n")), 1)

    def test_item_de_lista_linha_de_tabela_e_titulo_abrem_frase_nova(self):
        for texto in ("- Nunca rode o hook sem ler\n- As regras foram testadas em 12 casos\n",
                      "1. Nunca rode o hook\n2. As regras foram testadas\n",
                      "| Não se mediu | x |\n| As regras foram medidas | y |\n",
                      "# Nunca\nAs regras foram medidas.\n", "> Nunca isto.\n\n> As regras foram medidas.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(len(self.erros(NOME, texto)), 1)

    def test_a_negacao_so_vale_na_mesma_oracao_e_o_morg_laws_e_as_skills_contam(self):
        for texto in ("Nunca se esqueça: as regras foram medidas.\n", "Cada regra tem o seu teste; o código testado passa.\n",
                      "As skills do Morg-laws foram testadas.\n", "No Morg-laws, a skill foi validada.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(len(self.erros(NOME, texto)), 1)
        self.assertEqual(self.erros(NOME, "As skills nunca foram medidas.\n"), [])

    def test_a_negacao_depois_do_verbo_nao_salva(self):
        self.assertEqual(len(self.erros(NOME, "As regras foram medidas, não só lidas.\n")), 1)


class PorPar(ManualTemporario):

    def test_par_completo_passa(self):
        self.assertEqual(self.erros("manual/04-pedir.md", par()), [])

    def test_par_sem_fonte_reprova(self):
        erros = self.erros("manual/04-pedir.md", par("Só uma opinião."))
        self.assertEqual(len(erros), 1)
        self.assertIn("sem fonte", erros[0])

    def test_texto_antes_do_primeiro_h3_do_par_reprova_e_sem_texto_passa(self):
        solto = "## P6 X\n\n" + "palavra " * 50 + "\n\n### Na prática\n\nTexto.\n\n### Por quê e fonte\n\n[a](https://example.com)\n"
        erros = self.erros("manual/04-pedir.md", solto)
        self.assertEqual(len(erros), 1)
        self.assertIn("texto antes de «### Na prática»", erros[0])
        em_codigo = solto.replace("palavra " * 50, "```\nx\n```")
        self.assertEqual(len(self.erros("manual/04-pedir.md", em_codigo)), 0)
        self.assertEqual(verificador.texto_antes_do_primeiro_h3("a.md", "Q", ["", "", "### A"]), [])
        self.assertEqual(len(verificador.texto_antes_do_primeiro_h3("a.md", "Q", ["Só texto, sem lados."])), 1)

    def test_par_com_pagina_do_livro_ou_decisao_com_porque_tem_fonte(self):
        self.assertEqual(self.erros("manual/04-pedir.md", par("Veja o livro (p. 165).")), [])
        self.assertEqual(self.erros("manual/04-pedir.md", par(f"Foi {VOZES}. Porquê: simples.")), [])
        self.assertEqual(len(self.erros("manual/04-pedir.md", par(f"Foi {VOZES}."))), 2)

    def test_par_fora_de_ordem_ou_incompleto_reprova(self):
        trocado = "## P6 X\n\n### Por quê e fonte\n\n[a](https://example.com)\n\n### Na prática\n\nTexto.\n"
        for texto in (trocado, "## P6 X\n\n### Na prática\n\nTexto.\n"):
            with self.subTest(texto=texto):
                erros = self.erros("manual/04-pedir.md", texto)
                self.assertEqual(len(erros), 1)
                self.assertIn("«### Na prática» e depois «### Por quê e fonte»", erros[0])

    def test_o_mesmo_numero_de_par_duas_vezes_reprova_no_mesmo_arquivo_e_entre_arquivos(self):
        dois = par() + "\n" + PAR.format(teoria=TEORIA_COM_LINK).replace("As quatro partes", "Outra cópia")
        erros = self.erros("manual/04-pedir.md", dois)
        self.assertEqual(len(erros), 1)
        self.assertIn("o P6 já existe em manual/04-pedir.md", erros[0])
        self.escrever("manual/03-instalar.md", par())
        self.escrever("manual/04-pedir.md", par())
        erros = verificador.erros_do_manual(self.raiz, ["manual/03-instalar.md", "manual/04-pedir.md"])
        self.assertEqual(len(erros), 1)
        self.assertIn("manual/04-pedir.md", erros[0])
        self.assertIn("o P6 já existe em manual/03-instalar.md", erros[0])

    def test_numeros_de_par_diferentes_e_titulos_que_nao_sao_par_passam(self):
        texto = par() + "\n" + PAR.format(teoria=TEORIA_COM_LINK).replace("P6", "P7") + "\n## P2P não é par\n"
        self.assertEqual(self.erros("manual/04-pedir.md", texto), [])

    def test_aspas_francesas_na_prosa_reprovam_e_as_curvas_e_o_codigo_passam(self):
        for texto in ("Diz «fica bom» aqui.\n", "Fecha» sozinha.\n"):
            with self.subTest(texto=texto):
                erros = self.erros(NOME, texto)
                self.assertEqual(len(erros), 1)
                self.assertIn("aspas curvas", erros[0])
        for texto in ("Diz “fica ‘bom’ ou não” aqui.\n", "```\n«no código»\n```\n", "Veja `«x»`.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(self.erros(NOME, texto), [])

    def test_nota_de_rodape_num_par_reprova(self):
        erros = self.erros("manual/04-pedir.md", par(TEORIA_COM_LINK + "[^1]\n\n[^1]: nota"))
        self.assertEqual(len(erros), 1)
        self.assertIn("nota de rodapé", erros[0])
        self.assertEqual(verificador.notas_de_rodape_num_par("a.md", "Q", ["Texto sem nota."]), [])

    def test_teto_da_teoria(self):
        com_cinco = par("um dois três quatro [cinco](https://example.com/x)")
        with mock.patch.object(verificador, "TETO_DA_TEORIA", 4):
            erros = self.erros("manual/04-pedir.md", com_cinco)
        self.assertEqual(len(erros), 1)
        self.assertIn("«Por quê e fonte» tem 5 palavras (teto 4)", erros[0])
        self.assertEqual(self.erros("manual/04-pedir.md", com_cinco), [])

    def test_teto_da_pratica(self):
        longa = "## P6 X\n\n### Na prática\n\num dois três quatro cinco\n\n### Por quê e fonte\n\n[a](https://example.com/x)\n"
        with mock.patch.object(verificador, "TETO_DA_PRATICA", 4):
            erros = self.erros("manual/04-pedir.md", longa)
        self.assertEqual(len(erros), 1)
        self.assertIn("«Na prática» tem 5 palavras (teto 4)", erros[0])
        self.assertEqual(self.erros("manual/04-pedir.md", longa), [])

    def test_cada_lado_tem_o_seu_teto(self):
        longa = "## P6 X\n\n### Na prática\n\num dois três quatro cinco\n\n### Por quê e fonte\n\n[a](https://example.com/x)\n"
        with mock.patch.object(verificador, "TETO_DA_TEORIA", 4):
            self.assertEqual(self.erros("manual/04-pedir.md", longa), [])
        com_cinco = par("um dois três quatro [cinco](https://example.com/x)")
        with mock.patch.object(verificador, "TETO_DA_PRATICA", 4):
            self.assertEqual(self.erros("manual/04-pedir.md", com_cinco), [])

    def test_os_tetos_por_lado_sao_243_e_410(self):
        self.assertEqual((verificador.TETO_DA_PRATICA, verificador.TETO_DA_TEORIA), (243, 410))

    def test_os_tetos_dos_procedimentos_seguem_a_conta_de_n_pares(self):
        pares = {"03-instalar": 5, "04-pedir": 4, "05-sessoes": 8, "06-o-ciclo-de-uma-mudanca": 5,
                 "09-quando-da-errado": 2}
        for parte, n in pares.items():
            with self.subTest(parte=parte):
                esperado = n * (verificador.TETO_DA_PRATICA + verificador.TETO_DA_TEORIA) + 200
                self.assertEqual(verificador.TETOS_POR_PARTE[f"manual/{parte}.md"], esperado)

    def test_o_molde_dentro_de_um_bloco_de_codigo_nao_conta_nas_palavras(self):
        molde = "```\n" + "palavra " * 400 + "\n```\n"
        pratica = "## P6 X\n\n### Na prática\n\n" + molde + "\n### Por quê e fonte\n\n[a](https://example.com)\n"
        self.assertEqual(self.erros("manual/04-pedir.md", pratica), [])


class PorSecao(ManualTemporario):

    def test_secao_de_texto_seguido_sem_fonte_reprova_e_com_fonte_passa(self):
        sem = "# Regras\n\n## O núcleo\n\nUm texto sem fonte.\n"
        com = "# Regras\n\n## O núcleo\n\nUm texto [com fonte](https://example.com/x).\n"
        self.assertEqual(len(self.erros("manual/07-as-regras.md", sem)), 1)
        self.assertEqual(self.erros("manual/07-as-regras.md", com), [])

    def test_partes_fora_da_lista_e_excecoes_nao_pedem_fonte(self):
        sem = "# X\n\n## O núcleo\n\nUm texto sem fonte.\n"
        self.assertEqual(self.erros("manual/10-glossario.md", sem), [])
        self.assertEqual(self.erros("manual/09-quando-da-errado.md", sem), [])
        excecao = "# X\n\n## " + next(iter(verificador.EXCECOES_DE_SECAO))[1] + "\n\nUm índice.\n"
        self.assertEqual(self.erros("manual/07-as-regras.md", excecao), [])


class PorTeto(ManualTemporario):

    def test_parte_acima_do_teto_em_palavras_reprova(self):
        with mock.patch.dict(verificador.TETOS_POR_PARTE, {"manual/00-antes-de-comecar.md": 3}):
            erros = self.erros("manual/00-antes-de-comecar.md", "um dois três quatro [a](https://example.com)\n")
        self.assertEqual(len(erros), 1)
        self.assertIn("5 palavras (teto 3)", erros[0])

    def test_parte_dentro_do_teto_passa(self):
        self.assertEqual(self.erros("manual/00-antes-de-comecar.md", "um dois três\n"), [])

    def test_o_molde_tem_teto_em_linhas(self):
        self.escrever("manual/manual.typ", "\n" * verificador.TETO_DO_MOLDE_EM_LINHAS)
        self.assertEqual(verificador.erros_do_manual(self.raiz, ["manual/manual.typ"]), [])
        self.escrever("manual/manual.typ", "\n" * (verificador.TETO_DO_MOLDE_EM_LINHAS + 1))
        erros = verificador.erros_do_manual(self.raiz, ["manual/manual.typ"])
        self.assertEqual(len(erros), 1)
        self.assertIn("151 linhas (teto 150)", erros[0])

    def test_arquivo_fora_de_tudo_reprova_e_os_caminhos_fora_do_teto_passam(self):
        for nome in ("manual/zzz.md", "manual/solto.txt"):
            with self.subTest(nome=nome):
                self.assertEqual(len(self.erros(nome, "x\n")), 1)
        for nome in ("manual/fontes/licenca.txt", "manual/pessoas-citaveis.txt", "manual/nomes-citaveis.txt",
                     "manual/palavras-que-abrem-frase.txt"):
            with self.subTest(nome=nome):
                self.assertEqual(self.erros(nome, "x\n" * 5000), [])

    def test_imagem_so_se_acusa_pela_extensao_e_so_passa_em_imagens(self):
        png = b"\x89PNG\r\n\x1a\n\x00\xff"
        for nome in ("manual/outra/fluxo.png", "manual/imagens/fluxo.png"):
            caminho = self.raiz / nome
            caminho.parent.mkdir(parents=True, exist_ok=True)
            caminho.write_bytes(png)
        self.assertEqual(len(verificador.erros_do_manual(self.raiz, ["manual/outra/fluxo.png"])), 1)
        self.assertEqual(verificador.erros_do_manual(self.raiz, ["manual/imagens/fluxo.png"]), [])


MOLDE_COM_LISTAS = ('#let partes = ("00-a", "04-pedir",\n  "04-b")\n#let escritas = ("04-pedir",)\n')


class ListaDasPartesDoMolde(ManualTemporario):

    def erros_da_lista(self, molde, *arquivos, tetos=None):
        self.escrever(verificador.MOLDE, molde)
        tetos = tetos or {"manual/README.md": 1, "manual/00-a.md": 1, "manual/04-pedir.md": 1, "manual/04-b.md": 1}
        with mock.patch.object(verificador, "TETOS_POR_PARTE", tetos):
            return verificador.erros_da_lista_do_molde(self.raiz, list(arquivos))

    def test_lista_conforme_passa_com_uma_so_escrita_e_a_virgula_final(self):
        self.assertEqual(self.erros_da_lista(MOLDE_COM_LISTAS, "manual/04-pedir.md", "manual/README.md"), [])

    def test_parte_escrita_fora_das_escritas_reprova(self):
        erros = self.erros_da_lista(MOLDE_COM_LISTAS, "manual/04-pedir.md", "manual/04-b.md")
        self.assertEqual(len(erros), 1)
        self.assertIn("escritas", erros[0])
        self.assertIn("04-b", erros[0])

    def test_escrita_sem_arquivo_no_git_reprova(self):
        self.assertEqual(len(self.erros_da_lista(MOLDE_COM_LISTAS, "manual/README.md")), 1)

    def test_partes_diferentes_dos_tetos_ou_noutra_ordem_reprovam(self):
        trocadas = {"manual/README.md": 1, "manual/04-b.md": 1, "manual/04-pedir.md": 1, "manual/00-a.md": 1}
        for tetos in (trocadas, {"manual/README.md": 1, "manual/00-a.md": 1, "manual/04-pedir.md": 1}):
            with self.subTest(tetos=tetos):
                erros = self.erros_da_lista(MOLDE_COM_LISTAS, "manual/04-pedir.md", tetos=tetos)
                self.assertEqual(len(erros), 1)
                self.assertIn("partes", erros[0])


class ManualDoRepositorio(unittest.TestCase):
    maxDiff = None

    def test_o_manual_do_git_esta_conforme(self):
        self.assertEqual(verificador.erros_do_manual(RAIZ, arquivos_do_git(RAIZ, "manual/*")), [])

    def test_as_listas_do_molde_batem_com_o_git_e_com_os_tetos(self):
        self.assertEqual(verificador.erros_da_lista_do_molde(RAIZ, arquivos_do_git(RAIZ, "manual/*")), [])


if __name__ == "__main__":
    unittest.main()
