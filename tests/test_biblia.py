"""A bíblia (`biblia-akita/`) fica conferida pelo CI, e não só escrita:

1. cada conselho (uma linha `- ` de um arquivo de tema) cita a página impressa do livro, `(p. N)` ou `(pp. N–M)`,
   diz a barreira (`**texto**`, `**máquina**` ou as duas, `**texto + máquina**`) e termina com « · onde aplicar: », seguido de uma ou mais skills
   que existem em `skills/` (entre crases, separadas por vírgula) ou de «ainda nenhuma»;
2. cada arquivo da pasta está na tabela do README da pasta, e cada linha da tabela aponta para um arquivo que existe;
3. nenhum arquivo da pasta passa de 500 linhas, o limite de arquivo que o Morg-laws ensina.
O README e a lista de leituras (`leituras.md`, artigos com link e não conselhos) seguem só as regras 2 e 3.
As funções recebem a raiz e a lista de arquivos, para os casos de erro serem provados numa pasta temporária.
"""

import re
import tempfile
import unittest
from pathlib import Path

from carregar_modelos import RAIZ
from leitura_do_repositorio import arquivos_do_git, ler

PASTA = "biblia-akita"
SEM_CONSELHOS = ("README.md", "leituras.md")
LIMITE_DE_LINHAS = 500
PAGINA = re.compile(r"\(pp?\. \d+")
BARREIRA = re.compile(r" · \*\*(?:texto|máquina)(?: \+ (?:texto|máquina))?\*\*")
ONDE_APLICAR = re.compile(r" · onde aplicar: (.+)$")
NENHUMA = "ainda nenhuma"
SKILL_ENTRE_CRASES = re.compile(r"`([^`]+)`")
LINK_DA_TABELA = re.compile(r"^\| \[([^\]]+)\]\(([^)]+)\)", re.MULTILINE)


def erros_do_onde_aplicar(resto, skills):
    """O que está errado na lista de skills de «onde aplicar»."""
    if resto == NENHUMA:
        return []
    nomes = SKILL_ENTRE_CRASES.findall(resto)
    if not nomes or SKILL_ENTRE_CRASES.sub("", resto).replace(",", "").strip():
        return [f"«onde aplicar» tem de ser `skill`, `skill`… ou «{NENHUMA}»"]
    return [f"skill que não existe: `{nome}`" for nome in nomes if nome not in skills]


def erros_do_conselho(linha, skills):
    """Mensagens para o que falta numa linha de conselho."""
    erros = [] if PAGINA.search(linha) else ["sem página: (p. N) ou (pp. N–M)"]
    erros += [] if BARREIRA.search(linha) else ["sem barreira: · **texto** ou · **máquina**"]
    onde = ONDE_APLICAR.search(linha)
    if not onde:
        return erros + ["sem « · onde aplicar: » no fim da linha"]
    return erros + erros_do_onde_aplicar(onde.group(1).strip(), skills)


def erros_dos_conselhos(nome, texto, skills):
    if nome in SEM_CONSELHOS:
        return []
    return [f"{PASTA}/{nome}:{numero}: {erro}" for numero, linha in enumerate(texto.splitlines(), 1)
            if linha.startswith("- ") for erro in erros_do_conselho(linha, skills)]


def erros_da_tabela(readme, nomes):
    """Arquivos fora da tabela do README e linhas da tabela que apontam para nada."""
    na_tabela = {destino for _, destino in LINK_DA_TABELA.findall(readme)}
    fora = [f"{PASTA}/{nome}: falta na tabela do README da pasta" for nome in sorted(nomes - na_tabela)
            if nome != "README.md"]
    return fora + [f"{PASTA}/README.md: a tabela aponta para «{d}», que não existe" for d in sorted(na_tabela - nomes)]


def erros(raiz, arquivos, skills):
    """Todas as mensagens da pasta, para os `arquivos` (caminhos relativos à raiz) e as `skills` que existem."""
    textos = {Path(a).name: ler(raiz / a) for a in arquivos}
    achados = erros_da_tabela(textos.get("README.md", ""), set(textos))
    for nome, texto in sorted(textos.items()):
        if len(texto.splitlines()) > LIMITE_DE_LINHAS:
            achados.append(f"{PASTA}/{nome}: passa de {LIMITE_DE_LINHAS} linhas")
        achados += erros_dos_conselhos(nome, texto, skills)
    return achados


def skills_do_repositorio(raiz):
    return {Path(c).parent.name for c in arquivos_do_git(raiz, "skills/*/SKILL.md")}


class BibliaDoRepositorio(unittest.TestCase):

    def test_a_pasta_do_repositorio_esta_certa(self):
        arquivos = arquivos_do_git(RAIZ, f"{PASTA}/*.md")
        self.assertIn(f"{PASTA}/README.md", arquivos)
        self.assertEqual(erros(RAIZ, arquivos, skills_do_repositorio(RAIZ)), [])


README_CERTO = "| Arquivo | O que tem |\n|---|---|\n| [tema.md](tema.md) | um tema |\n"
CONSELHO_CERTO = "- Faça algo útil. (p. 12) · **texto** · onde aplicar: `testes-e-provas`"


class CasosDeErro(unittest.TestCase):
    """Cada regra provada numa pasta temporária, com um caso certo de controlo."""

    def correr(self, tema, readme=README_CERTO, extras=None):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / PASTA).mkdir()
            conteudos = {"README.md": readme, "tema.md": tema, **(extras or {})}
            for nome, texto in conteudos.items():
                (raiz / PASTA / nome).write_text(texto, encoding="utf-8")
            return erros(raiz, [f"{PASTA}/{n}" for n in conteudos], {"testes-e-provas", "sql-postgres"})

    def test_conselho_certo_passa(self):
        self.assertEqual(self.correr(CONSELHO_CERTO + "\n"), [])

    def test_varias_skills_e_paginas_e_barreira_com_detalhe_passam(self):
        linha = "- Algo. (pp. 3–4, 9) · **máquina** (hook em `DROP`) · onde aplicar: `testes-e-provas`, `sql-postgres`"
        self.assertEqual(self.correr(linha + "\n"), [])

    def test_as_duas_barreiras_passam_e_outra_palavra_falha(self):
        self.assertEqual(self.correr("- Algo. (p. 1) · **texto + máquina** · onde aplicar: ainda nenhuma\n"), [])
        self.assertIn("sem barreira", self.correr("- Algo. (p. 1) · **lei** · onde aplicar: ainda nenhuma\n")[0])

    def test_ainda_nenhuma_passa(self):
        self.assertEqual(self.correr("- Algo. (p. 1) · **texto** · onde aplicar: ainda nenhuma\n"), [])

    def test_sem_pagina_falha(self):
        self.assertIn("sem página", self.correr("- Algo. · **texto** · onde aplicar: ainda nenhuma\n")[0])

    def test_sem_barreira_falha(self):
        self.assertIn("sem barreira", self.correr("- Algo. (p. 1) · onde aplicar: ainda nenhuma\n")[0])

    def test_sem_onde_aplicar_falha(self):
        self.assertIn("onde aplicar", self.correr("- Algo. (p. 1) · **texto**\n")[0])

    def test_skill_que_nao_existe_falha(self):
        achado = self.correr("- Algo. (p. 1) · **texto** · onde aplicar: `inventada`\n")
        self.assertEqual(achado, [f"{PASTA}/tema.md:1: skill que não existe: `inventada`"])

    def test_texto_solto_no_onde_aplicar_falha(self):
        achado = self.correr("- Algo. (p. 1) · **texto** · onde aplicar: a skill de testes\n")
        self.assertIn("tem de ser", achado[0])

    def test_skill_com_texto_solto_ao_lado_falha(self):
        achado = self.correr("- Algo. (p. 1) · **texto** · onde aplicar: `sql-postgres` e mais\n")
        self.assertIn("tem de ser", achado[0])

    def test_arquivo_fora_da_tabela_falha(self):
        achado = self.correr(CONSELHO_CERTO + "\n", extras={"outro.md": CONSELHO_CERTO + "\n"})
        self.assertEqual(achado, [f"{PASTA}/outro.md: falta na tabela do README da pasta"])

    def test_tabela_que_aponta_para_nada_falha(self):
        readme = README_CERTO + "| [sumido.md](sumido.md) | nada |\n"
        self.assertIn("«sumido.md», que não existe", self.correr(CONSELHO_CERTO + "\n", readme=readme)[0])

    def test_arquivo_longo_falha(self):
        longo = (CONSELHO_CERTO + "\n") * (LIMITE_DE_LINHAS + 1)
        self.assertEqual(self.correr(longo), [f"{PASTA}/tema.md: passa de {LIMITE_DE_LINHAS} linhas"])

    def test_leituras_nao_segue_o_formato_dos_conselhos(self):
        readme = README_CERTO + "| [leituras.md](leituras.md) | artigos |\n"
        leituras = {"leituras.md": "- [Um artigo](https://example.com) (2026-01-01): para quê.\n"}
        self.assertEqual(self.correr(CONSELHO_CERTO + "\n", readme=readme, extras=leituras), [])


if __name__ == "__main__":
    unittest.main()
