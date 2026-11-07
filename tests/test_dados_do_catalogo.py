"""Os casos de cada tipo de dado que a barreira de `projetos/` procura (`dados_do_catalogo.py`): o que casa e o que não
casa. Todos os valores são fictícios, de forma impossível ou conhecida como falsa, e montados aos pedaços (assim
nenhum arquivo daqui parece um dado, e este teste não é lido pela barreira)."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import dados_do_catalogo as catalogo

ACEITAS = (frozenset({"cada", "uma", "depois"}), frozenset({"Next.js", "Empresa A", "CI", "README"}))
FINO = "\u2009"  # espaço fino
NUMERO = "123" + "456" + "789"  # passa a validação de um número fiscal (dígito de controlo 9): conhecido como falso
IBAN = "PT50" + " 0000" * 5 + " 0"
UUID = "-".join(["0" * 8, "0" * 4, "0" * 4, "0" * 4, "0" * 12])
FULANO = "fulano"
CASA = (
    ("documento", NUMERO), ("documento", "123 456 789"), ("documento", f"123{FINO}456{FINO}789"),
    ("documento", "123-456-789"), ("documento", "1234" + "5678901"), ("documento", f"o número {NUMERO}."),
    ("IBAN", IBAN), ("IBAN", IBAN.lower()), ("IBAN", IBAN.replace(" ", "-")),
    ("UUID", UUID), ("UUID", UUID.upper()),
    ("hash", "1781" + "BBB"), ("hash", "dead" + "beef1"),
    ("ID de serviço", "abcdefghij" + "klmnopqrst"),
    ("domínio", FULANO + ".es"), ("domínio", FULANO + ".site"), ("domínio", "www." + FULANO + ".es"),
    ("domínio", "o github" + ".com/x"),
    ("dinheiro", "10 " + "€"), ("dinheiro", "30 " + "USD"), ("dinheiro", "um dólar"), ("dinheiro", "1,5 mil euros"),
    ("dinheiro", "R" + "$ 5"), ("dinheiro", "US" + "$ 5"), ("dinheiro", "custa $" + "5"),
    ("caminho", "/home/" + FULANO + "/x"), ("caminho", "C:\\Users\\" + FULANO + "\\x"),
    ("e-mail", FULANO + "@gmail" + ".com"),
)
NAO_CASA = (
    "2771 commits", "2.771 commits", "`README.md` e `sonda_expressoes.py`", "a pilha é Next.js", "`echo $1` roda",
    "a cor #ff5733aa", "/home/ana/x", "ana@example.com", "o domínio example.com", "Cada item. Uma coisa.",
    "- Depois disso", "| Uma | Empresa A |", "`git config user.name`", "versão 1.2.3 e v18", "e.g. isto",
)
SO_DOS_TIPOS = (("domínio", "README.md e sonda_expressoes.py"), ("dinheiro", "a EUROPA"))  # o nome em maiúsculas é outro tipo


def tipos_de(texto):
    return {tipo for _, tipo, _ in catalogo.dados_no_texto(texto, ACEITAS)}


class TiposDeDado(unittest.TestCase):

    def test_cada_tipo_e_acusado(self):
        for tipo, texto in CASA:
            with self.subTest(tipo=tipo, texto=texto):
                self.assertIn(tipo, tipos_de(texto))

    def test_o_que_nao_e_dado_passa(self):
        for texto in NAO_CASA:
            with self.subTest(texto=texto):
                self.assertEqual(catalogo.dados_no_texto(texto, ACEITAS), [])

    def test_extensao_de_arquivo_e_europa_nao_sao_dominio_nem_dinheiro(self):
        for tipo, texto in SO_DOS_TIPOS:
            with self.subTest(texto=texto):
                self.assertNotIn(tipo, tipos_de(texto))

    def test_a_linha_e_o_trecho_vem_no_achado(self):
        achados = catalogo.dados_no_texto(f"limpo\nnúmero {NUMERO} aqui\n", ACEITAS)
        self.assertEqual(achados, [(2, "documento", NUMERO)])

    def test_numero_no_fim_da_frase_e_acusado_mas_o_decimal_nao(self):
        self.assertIn("documento", tipos_de(f"era {NUMERO}. Depois"))
        self.assertEqual(tipos_de("pesa 1.234.567.890 kg"), set())

    def test_um_dominio_aceito_passa(self):
        self.assertEqual(catalogo.dados_no_texto("em fulano.es", ACEITAS, frozenset({"fulano.es"})), [])


class NomesProprios(unittest.TestCase):

    def test_maiuscula_acentuada_e_acusada(self):
        for nome in ("Ângela", "Élio", "Ílton"):
            with self.subTest(nome=nome):
                self.assertEqual(tipos_de(f"falou com o {nome} ontem"), {"nome próprio"})

    def test_palavra_comum_so_no_inicio_de_frase_celula_ou_item(self):
        self.assertEqual(tipos_de("Cada item. Depois, outro. Uma coisa"), set())
        self.assertEqual(tipos_de("| Cada | x |\n1. Depois\n- **Uma** linha"), set())
        self.assertEqual(tipos_de("isto é Cada coisa"), {"nome próprio"})

    def test_nome_aceito_vale_em_qualquer_posicao_e_o_nao_aceito_nao(self):
        self.assertEqual(tipos_de("usa Next.js e a Empresa A com CI"), set())
        self.assertEqual(tipos_de("usa Remix e a Empresa B"), {"nome próprio"})

    def test_as_crases_nao_isentam_o_conteudo(self):
        self.assertEqual(tipos_de("usa `Fulano` sempre"), {"nome próprio"})
        self.assertEqual(tipos_de('rode `git config user.name "Fulano"`'), {"nome próprio"})
        self.assertEqual(tipos_de("rode `git config user.name`"), set())

    def test_dentro_de_crases_o_token_com_cara_de_caminho_tambem_e_conferido(self):
        for texto in ("`git commit --author=" + "Fulano`", "`Ana" + "-Paula`", "`~/Projetos/" + "Fulano_ERP/`",
                      "`/srv/" + "Fulano/x`", "`sonda_" + "Fulano`"):
            with self.subTest(texto=texto):
                self.assertEqual(tipos_de(texto), {"nome próprio"})

    def test_crase_solta_nao_isenta_o_resto_da_linha(self):
        self.assertEqual(tipos_de("um ` solto e depois Fulano" + "_ERP/x"), {"nome próprio"})

    def test_pedaco_so_de_minusculas_extensao_e_nome_aceito_passam_dentro_de_crases(self):
        for texto in ("`sonda_expressoes.py`", "`git commit --amend`", "`Next.js/app`", "`README.md`"):
            with self.subTest(texto=texto):
                self.assertEqual(tipos_de(texto), set())

    def test_sigla_e_acusada_e_o_nome_depois_de_hifen_tambem(self):
        self.assertEqual(tipos_de("o RLS e o pré-Fulano"), {"nome próprio"})
        self.assertEqual([t for _, _, t in catalogo.dados_no_texto("o RLS e o pré-Fulano", ACEITAS)], ["RLS", "Fulano"])


class ListaDePalavras(unittest.TestCase):

    def test_duas_partes_com_comentarios_e_categorias(self):
        texto = "# c\n## comuns\nCada\n\n## nomes\nNext.js | tecnologia\nEmpresa A | papel\n"
        self.assertEqual(catalogo.ler_palavras(texto), (frozenset({"cada"}), frozenset({"Next.js", "Empresa A"}), ()))

    def test_o_que_esta_mal_formado_e_acusado(self):
        erros = catalogo.ler_palavras("Solta\n## outra\n## nomes\nSem Categoria\nX | pessoa\n## comuns\nduas palavras\n")[2]
        self.assertEqual(len(erros), 5)
        self.assertIn("fora de uma parte", erros[0])
        self.assertIn("a parte «outra» não existe", erros[1])


class ListaNegra(unittest.TestCase):
    TERMO = FULANO + "zz"

    def lista(self, *termos):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        arquivo = Path(pasta.name) / "lista.txt"
        arquivo.write_text("# comentário\n\n" + "\n".join(termos) + "\n", encoding="utf-8")
        return arquivo

    def test_o_termo_casa_sem_fronteira_de_palavra_e_sem_ser_impresso(self):
        achados = catalogo.termos_no_texto(f"limpo\numa {self.TERMO.upper()}s aqui\n", [self.TERMO])
        self.assertEqual(achados, [(2, "lista negra", "termo n.º 1")])
        self.assertNotIn(self.TERMO, catalogo.mensagem("x.md", achados[0], {}))

    def test_o_termo_e_uma_expressao_como_no_hook(self):
        self.assertEqual(len(catalogo.termos_no_texto("ab12", ["b[0-9]+"])), 1)

    def test_termo_que_o_python_nao_compila_e_acusado_e_nunca_saltado(self):
        termos = [self.TERMO, "*" + "abc", "[[:" + "alpha:]]x"]
        self.assertEqual(catalogo.termos_que_nao_compilam(termos), [2, 3])
        mensagens = catalogo.problemas([], termos)
        self.assertEqual([m.split(" não compila")[0] for m in mensagens], ["lista negra: o termo n.º 2", "lista negra: o termo n.º 3"])

    def test_os_termos_vem_do_arquivo_da_configuracao_do_git(self):
        configuracao = {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "morg.lista" + "Negra",
                        "GIT_CONFIG_VALUE_0": str(self.lista(self.TERMO, "  outro "))}
        with mock.patch.dict(os.environ, configuracao):
            self.assertEqual(catalogo.molde.termos_da_lista_negra(), [self.TERMO, "outro"])


class Mensagens(unittest.TestCase):

    def test_fora_do_ci_o_trecho_vem_e_no_ci_so_arquivo_linha_e_tipo(self):
        achado = (3, "documento", NUMERO)
        self.assertEqual(catalogo.mensagem("a.md", achado, {}), f"a.md:3: documento — {NUMERO}")
        self.assertEqual(catalogo.mensagem("a.md", achado, {"CI": "true"}), "a.md:3: documento")

    def test_o_trecho_de_um_termo_da_lista_negra_e_o_numero_em_qualquer_lugar(self):
        achado = (1, "lista negra", "termo n.º 4")
        for ambiente in ({}, {"CI": "true"}):
            self.assertEqual(catalogo.mensagem("a.md", achado, ambiente), "a.md:1: lista negra — termo n.º 4")


class Estrutura(unittest.TestCase):

    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.raiz = Path(pasta.name)

    def escrever(self, nome, texto="# x\n"):
        (self.raiz / nome).parent.mkdir(parents=True, exist_ok=True)
        (self.raiz / nome).write_text(texto, encoding="utf-8")

    def projeto(self, nome, faltam=(), linhas=1):
        for arquivo in catalogo.ARQUIVOS_DE_CADA_PROJETO:
            if arquivo not in faltam:
                self.escrever(f"projetos/{nome}/{arquivo}", "x\n" * linhas)

    def test_sem_readme_do_catalogo(self):
        self.assertEqual(catalogo.erros_da_estrutura(self.raiz), ["falta projetos/README.md"])

    def test_catalogo_sem_projetos_e_projeto_completo_passam(self):
        self.escrever("projetos/README.md", "| Projeto | O que é |\n|---|---|\n")
        self.assertEqual(catalogo.erros_da_estrutura(self.raiz), [])
        self.escrever("projetos/README.md", "| Projeto |\n|---|\n| [erp](erp/README.md) | x |\n")
        self.projeto("erp")
        self.assertEqual(catalogo.erros_da_estrutura(self.raiz), [])

    def test_tabela_e_pastas_que_nao_batem_arquivo_que_falta_e_arquivo_longo(self):
        self.escrever("projetos/README.md", "| [fantasma](fantasma/README.md) | x |\n")
        self.projeto("erp", faltam=("o-que-se-mediu.md",))
        self.escrever("projetos/erp/README.md", "x\n" * 501)
        erros = catalogo.erros_da_estrutura(self.raiz)
        self.assertEqual(len(erros), 3)
        self.assertIn("lista ['fantasma']", erros[0])
        self.assertIn("falta projetos/erp/o-que-se-mediu.md", erros)
        self.assertIn("projetos/erp/README.md tem 501 linhas (máximo 500)", erros)


if __name__ == "__main__":
    unittest.main()
