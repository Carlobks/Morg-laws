"""Os testes do livro novo no verificador do manual: os dois gatilhos de par, a nota numerada, as decisões do autor, N1 a N7 e
o alcance. Cada verificação tem um caso que passa e um que reprova, numa pasta temporária (nunca no próprio repositório)."""

import unittest
from unittest import mock

import verificador_do_manual as verificador
from carregar_modelos import RAIZ
from leitura_do_repositorio import arquivos_do_git
from test_manual import VOZES, ManualTemporario

MARCA = "<!--raw-typst #marca-de-par() -->\n"
PAR_NOVO = MARCA + "## O par novo\n\n### Na prática\n\nEscreva.\n\n### Por quê\n\n{teoria}\n"
LINK = "O porquê está [aqui](https://example.com/x)."
CAP = "manual/cap-07-compactar-parar-e-retomar.md"
APENDICE_B = "manual/apendice-b.md"
COMO_LER = "manual/como-ler.md"
MOLDE_NOVO = '#let capitulos-novos = ("cap-07-compactar-parar-e-retomar",)\n#let pecas-novas = ("referencias",)\n'


class DoLivroNovo(ManualTemporario):

    def erros_novos(self, nome, texto):
        """Os erros do manual com um arquivo novo (no alcance), com teto à parte para o nome não reprovar por isso."""
        self.escrever(nome, texto)
        return self.erros_de([nome], nome)

    def erros_de(self, arquivos, novo):
        """Os erros de uns arquivos, sendo `novo` o único do livro novo; o molde e as artes da parte 4 (a do CAP) já estão."""
        self.escrever(verificador.MOLDE, '#image("imagens/arte-parte-4-a.svg")\n#image("imagens/arte-parte-4-b.svg")\n')
        artes = ["manual/imagens/arte-parte-4-a.svg", "manual/imagens/arte-parte-4-b.svg"]
        with mock.patch.dict(verificador.TETOS_POR_PARTE, {novo: 100000}):
            return verificador.erros_do_manual(self.raiz, [*arquivos, verificador.MOLDE, *artes], novos=[novo])

    def erros_de_hoje(self, nome, texto):
        self.escrever(nome, texto)
        with mock.patch.dict(verificador.TETOS_POR_PARTE, {nome: 100000}):
            return verificador.erros_do_manual(self.raiz, [nome], novos=[])


class DosGatilhosDoPar(DoLivroNovo):

    def test_o_par_marcado_passa_e_o_marcador_nao_conta_palavras(self):
        self.assertEqual(self.erros_de_hoje("manual/04-pedir.md", PAR_NOVO.format(teoria=LINK)), [])
        with mock.patch.object(verificador, "TETO_DA_PRATICA", 1):
            self.assertEqual(self.erros_de_hoje("manual/04-pedir.md", PAR_NOVO.format(teoria=LINK)), [])
            self.assertEqual(len(self.erros_de_hoje("manual/04-pedir.md", PAR_NOVO.format(teoria=LINK).replace("Escreva", "Escreva já"))), 1)

    def test_o_par_marcado_leva_por_que_e_o_de_hoje_leva_por_que_e_fonte(self):
        velho = PAR_NOVO.format(teoria=LINK).replace("### Por quê\n", "### Por quê e fonte\n")
        erros = self.erros_de_hoje("manual/04-pedir.md", velho)
        self.assertEqual(len(erros), 1)
        self.assertIn("«### Na prática» e depois «### Por quê»", erros[0])
        hoje = "## P6 X\n\n### Na prática\n\nTexto.\n\n### Por quê\n\n[a](https://example.com/x)\n"
        self.assertIn("«### Por quê e fonte»", self.erros_de_hoje("manual/04-pedir.md", hoje)[0])

    def test_marcador_sem_titulo_a_seguir_reprova(self):
        for texto in (MARCA + "\nTexto solto.\n", "Texto.\n\n" + MARCA):
            with self.subTest(texto=texto):
                erros = self.erros_de_hoje("manual/04-pedir.md", texto)
                self.assertEqual(len(erros), 1)
                self.assertIn("marcador de par sem «## título»", erros[0])

    def test_o_mesmo_titulo_de_par_marcado_duas_vezes_reprova_e_titulos_diferentes_passam(self):
        um = PAR_NOVO.format(teoria=LINK)
        erros = self.erros_de_hoje("manual/04-pedir.md", um + "\n" + um)
        self.assertEqual(len(erros), 1)
        self.assertIn("o par «O par novo» já existe em manual/04-pedir.md", erros[0])
        self.assertEqual(self.erros_de_hoje("manual/04-pedir.md", um + "\n" + um.replace("O par novo", "Outro")), [])
        self.assertEqual(self.erros_de_hoje("manual/04-pedir.md", um + "\n## O par novo\n\nTexto sem marcador.\n"), [])


class DasNotasEDasDecisoes(DoLivroNovo):

    def test_a_nota_chamada_conta_como_o_link_do_codex(self):
        nota = "[^c]: [Documentação do Codex](https://example.com/codex/agents)."
        self.assertEqual(self.erros_de_hoje(CAP, f"O Codex lê o arquivo.[^c]\n\n{nota}\n"), [])
        self.assertEqual(len(self.erros_de_hoje(CAP, "O Codex lê o arquivo.[^c]\n\n[^c]: Sem link.\n")), 1)
        self.assertEqual(len(self.erros_de_hoje(CAP, "O Codex lê o arquivo.[^x]\n\n" + nota.replace("^c", "^y") + "\n")), 1)

    def test_a_decisao_do_autor_na_nota_pede_o_porque_e_as_vozes_pedem_a_nota(self):
        com = "As vozes da minha cabeça decidiram.[^d]\n\n[^d]: Decisão do autor (2026-11-08). Porquê: cabe numa tela.\n"
        self.assertEqual(self.erros_novos(CAP, com), [])
        sem_porque = com.replace(" Porquê: cabe numa tela.", "")
        erros = self.erros_novos(CAP, sem_porque)
        self.assertEqual(len(erros), 1)
        self.assertIn("decisão sem «Porquê:»", erros[0])
        sem_nota = self.erros_novos(CAP, "As vozes da minha cabeça decidiram.\n")
        self.assertEqual(len(sem_nota), 1)
        self.assertIn("«as vozes da minha cabeça» sem nota", sem_nota[0])
        nota_de_outra_coisa = self.erros_novos(CAP, "As vozes da minha cabeça decidiram.[^d]\n\n[^d]: Outra coisa.\n")
        self.assertEqual(len(nota_de_outra_coisa), 1)
        self.assertEqual(self.erros_novos(CAP, "Explico “as vozes da minha cabeça” numa linha.\n"), [])
        self.assertEqual(self.erros_de_hoje("manual/10-glossario.md", f"Foi {VOZES}. Porquê: simples.\n"), [])

    def test_as_definicoes_das_notas_juntam_as_linhas_e_a_linha_em_branco_fecha(self):
        texto = "[^a]: Começa\ncontinua.\n\nParágrafo solto.\n\n[^b]: Outra.\n```\n[^z]: no código\n```\n"
        self.assertEqual(verificador.definicoes_de_notas(texto), [("a", "Começa continua."), ("b", "Outra.")])


class DosNovos(DoLivroNovo):

    def test_n1_codigos_internos_reprovam_so_nos_arquivos_novos(self):
        for texto in ("Veja o P3 aqui.\n", "Segundo a L-12 do autor.\n", "O procedimento P1 manda.\n", "Na parte 05 está.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(len(self.erros_novos(CAP, texto)), 1)
                self.assertEqual(self.erros_de_hoje(CAP, texto), [])
        self.assertEqual(self.erros_novos(CAP, "O P2P não é código; veja `P3` e a skill P.\n```pedido\nP9\n```\n"), [])

    def test_n2_as_notas_fecham(self):
        ok = "Uma frase.[^a] Outra.[^a]\n\n[^a]: Fonte.\n"
        self.assertEqual(self.erros_novos(CAP, ok), [])
        casos = {"Frase.[^a]\n": "chamada sem definição", "Frase.\n\n[^a]: Fonte.\n": "definida e nunca chamada",
                 "Frase.[^a]\n\n[^a]: Um.\n\n[^a]: Dois.\n": "definida duas vezes", "Frase.[^a]\n\n[^a]:\n": "vazia"}
        for texto, esperado in casos.items():
            with self.subTest(esperado=esperado):
                erros = self.erros_novos(CAP, texto)
                self.assertEqual(len(erros), 1)
                self.assertIn(esperado, erros[0])
        self.assertEqual(self.erros_de_hoje(CAP, "Frase.[^a]\n"), [])

    def test_n3_notas_e_referencias(self):
        self.escrever("FONTES.md", FONTES_COM_AKITA)
        nota = "Frase.[^a]\n\n[^a]: AKITA, 2026, pp. 30–32.\n"
        entrada = "# Referências\n\nAKITA, Fabio. Título. São Paulo: Editora, 2026. Disponível em: x. Acesso em: 3 nov. 2030.\n"
        self.escrever(CAP, nota)
        self.escrever(verificador.REFERENCIAS, entrada)
        todos = [CAP, verificador.REFERENCIAS]
        self.assertEqual(self.erros_de(todos, CAP), [])
        self.assertEqual(self.erros_de([CAP], CAP)[0][:27], "nota «AKITA, 2026» sem entr")
        self.escrever(verificador.REFERENCIAS, entrada.replace("Editora, 2026", "Editora, 2025"))
        erros = self.erros_de(todos, CAP)
        self.assertEqual(len(erros), 2)
        self.assertIn("sem entrada", erros[0])
        self.assertIn("«AKITA, 2025» sem nota que a cite", erros[1])
        self.escrever(verificador.REFERENCIAS, "ZZZ, Fulano. Sem ano.\n- ZZZ, Fulano. Sem ano.\n")
        erros = self.erros_de(todos, CAP)
        self.assertEqual([e for e in erros if "FONTES.md" in e], [f"{verificador.REFERENCIAS}: «ZZZ» sem linha no FONTES.md"])
        self.assertEqual(len([e for e in erros if "None" in e]), 2)

    def test_n4_remissoes_existem_contra_o_mapa(self):
        ok = "Veja o Capítulo 12, os Capítulos 3 e 4, o Apêndice B, a Seção B.15, o Ap. A.7 e o capítulo 1.\n"
        self.assertEqual(self.erros_novos(CAP, ok), [])
        for texto in ("Veja o Capítulo 16.\n", "Veja os Capítulos 3 e 0.\n", "Veja o Apêndice C.\n", "Veja a Seção B.5.\n"):
            with self.subTest(texto=texto):
                self.assertEqual(len(self.erros_novos(CAP, texto)), 1)
        self.assertEqual(self.erros_de_hoje(CAP, "Veja o Capítulo 16.\n"), [])

    def test_n5_comandos_so_no_apendice_b(self):
        self.assertEqual(self.erros_novos(CAP, "```pedido\nFaça isto.\n```\n"), [])
        for bloco in ("```\nls\n```\n", "```bash\nls\n```\n", "~~~\nls\n~~~\n"):
            with self.subTest(bloco=bloco):
                erros = self.erros_novos(CAP, bloco)
                self.assertEqual(len(erros), 1)
                self.assertIn("fora do Apêndice B", erros[0])
        self.assertEqual(self.erros_novos(APENDICE_B, "```bash\nls\n```\n\nNo terminal, assim. Não testado pelo autor.\n"), [])
        self.assertEqual(self.erros_novos(COMO_LER, "O terminal não foi testado.\n"), [])
        self.assertEqual(self.erros_novos("manual/glossario.md", "O terminal é do Apêndice B.\n"), [])
        erros = self.erros_novos(CAP, "Abra o Terminal e escreva `ls` no terminal.\n")
        self.assertEqual(len(erros), 1)
        self.assertIn("«terminal»", erros[0])
        self.assertEqual(self.erros_novos(CAP, "O `terminal` entre crases passa.\n"), [])

    def test_n6_nao_testado_a_vista(self):
        sem = "## B.2 A pasta\n\nNo Windows faça assim.\n\n## B.3 Outra\n\nTexto sem sistema.\n"
        erros = self.erros_novos(APENDICE_B, sem)
        self.assertEqual(len(erros), 1)
        self.assertIn("«B.2 A pasta»", erros[0])
        for ok in (sem.replace("assim.", "assim (não testado pelo autor)."), sem.replace("Windows", "app")):
            with self.subTest(ok=ok):
                self.assertEqual(self.erros_novos(APENDICE_B, ok), [])
        with mock.patch.object(verificador, "FUNCOES_DO_APP", frozenset({(APENDICE_B, "B.2 A pasta")})):
            self.assertEqual(self.erros_novos(APENDICE_B, sem), [])
        self.assertEqual(self.erros_novos(CAP, sem.replace("## B.", "## C.")), [])
        self.assertEqual(verificador.nao_testado_a_vista(CAP, sem), [])

    def test_n7_cada_figura_tem_a_legenda_figura_n_m(self):
        self.assertEqual(self.erros_novos(CAP, "![Figura 7.1 A janela que enche.](imagens/figura-7-1.svg)\n"), [])
        self.assertEqual(len(self.erros_novos(CAP, "![A janela](imagens/figura-7-1.svg)\n")), 1)
        self.assertEqual(len(self.erros_novos(CAP, "![Figura 7.2 A janela](imagens/figura-7-1.svg)\n")), 1)
        erros = self.erros_novos(CAP, "![Figura 7.1 Foto](imagens/foto.png)\n")
        self.assertEqual(len(erros), 1)
        self.assertIn("as artes são do molde", erros[0])

    def test_n7_as_12_artes_e_o_molde_que_as_chama(self):
        cap, arte = [CAP], "manual/imagens/arte-parte-4-{}.svg"
        todos = [CAP, "manual/manual.typ", arte.format("a"), arte.format("b")]
        self.escrever("manual/manual.typ", '#image("imagens/arte-parte-4-a.svg")\n#image("imagens/arte-parte-4-b.svg")\n')
        self.assertEqual(verificador.artes_das_partes(self.raiz, todos, cap), [])
        self.assertEqual(verificador.artes_das_partes(self.raiz, todos[:2] + todos[3:], cap),
                         ["manual/imagens/arte-parte-4-a.svg: falta — a parte 4 já tem capítulo novo"])
        self.escrever("manual/manual.typ", '#image("imagens/arte-parte-4-a.svg")\n')
        self.assertEqual(verificador.artes_das_partes(self.raiz, todos, cap),
                         ["manual/imagens/arte-parte-4-b.svg: o molde não a chama"])
        fora = todos + ["manual/imagens/arte-parte-7-a.svg"]
        self.assertEqual(len(verificador.artes_das_partes(self.raiz, fora, cap)), 2)
        self.assertEqual(verificador.artes_das_partes(self.raiz, todos[1:], []), [])


FONTES_COM_AKITA = "# Fontes\n\n## Livros e autores\n\n- **Akita**, Fabio (livro).\n  - pp. 30–32: x.\n"


class DaListaDoMolde(ManualTemporario):

    def test_novos_do_molde_le_as_duas_listas_e_sem_molde_ninguem_e_novo(self):
        self.assertEqual(verificador.novos_do_molde(self.raiz), [])
        self.escrever(verificador.MOLDE, MOLDE_NOVO)
        self.assertEqual(verificador.novos_do_molde(self.raiz), [CAP, verificador.REFERENCIAS])

    def test_a_lista_nova_bate_com_o_git_e_com_a_ordem_do_mapa(self):
        self.escrever(verificador.MOLDE, MOLDE_NOVO)
        com_tudo = [CAP, verificador.REFERENCIAS]
        with mock.patch.object(verificador, "TETOS_POR_PARTE", {"manual/README.md": 1}):
            self.assertEqual(verificador.erros_da_lista_do_molde(self.raiz, com_tudo), [])
            for arquivos in ([CAP], [verificador.REFERENCIAS], com_tudo + ["manual/prefacio.md"]):
                with self.subTest(arquivos=arquivos):
                    erros = verificador.erros_da_lista_do_molde(self.raiz, arquivos)
                    self.assertEqual(len(erros), 1)
                    self.assertIn("na ordem do mapa", erros[0])
            outra = '#let capitulos-novos = ("cap-07-compactar-parar-e-retomar", "cap-01-duas-empresas")\n'
            self.escrever(verificador.MOLDE, outra)
            self.assertEqual(len(verificador.erros_da_lista_do_molde(self.raiz, [CAP, "manual/cap-01-duas-empresas.md"])), 1)


class DoAlcanceTotal(DoLivroNovo):

    def test_o_alcance_total_acha_o_par_de_hoje_e_aplica_n1_e_n5_a_tudo(self):
        hoje = "## P6 X\n\nVeja o P3 e o terminal.\n\n```\nls\n```\n"
        self.escrever("manual/04-pedir.md", hoje)
        erros = verificador.erros_do_alcance_total(self.raiz, ["manual/04-pedir.md", CAP], [CAP])
        self.assertEqual(len(erros), 5)  # o gatilho, «P6» no título, «P3», «terminal» e o bloco sem «pedido»
        self.assertIn("o gatilho de hoje já devia ter saído", erros[0])
        self.assertEqual(verificador.erros_do_alcance_total(self.raiz, [CAP], [CAP]), [])
        with mock.patch.dict(verificador.TETOS_POR_PARTE, {"manual/04-pedir.md": 99999}):
            desligado = verificador.erros_do_manual(self.raiz, ["manual/04-pedir.md"], novos=[])
            with mock.patch.object(verificador, "ALCANCE_TOTAL", True):
                ligado = verificador.erros_do_manual(self.raiz, ["manual/04-pedir.md"], novos=[])
        self.assertEqual(len(ligado) - len(desligado), 5)


class DoRepositorio(unittest.TestCase):

    def test_o_alcance_total_nasce_desligado_e_so_se_liga_sem_partes_de_hoje(self):
        arquivos = arquivos_do_git(RAIZ, "manual/*")
        erros = verificador.erros_do_alcance_total(RAIZ, arquivos, verificador.novos_do_molde(RAIZ))
        if verificador.ALCANCE_TOTAL:
            self.assertEqual(erros, [])
        else:
            self.assertTrue(erros, "já não sobra parte de hoje: ligue ALCANCE_TOTAL em verificador_do_manual.py")


if __name__ == "__main__":
    unittest.main()
