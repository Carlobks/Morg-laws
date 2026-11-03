"""A documentação continua achável e coerente (Morg-laws: índice dos docs, ADR, armadilhas, pesquisa, planos e
handoffs). Num projeto real, estas regras eram só texto e falharam: um relatório nunca entrou no índice e um plano
não dizia o que ficava fora do escopo.

- cada `.md` e pasta de `docs/` tem uma linha no índice `docs/README.md`;
- as ADRs (`docs/decisoes/NNNN-titulo.md`) têm números seguidos e estão no índice;
- cada pesquisa (`docs/pesquisa/*.md`) está no índice dela, com a data na última coluna;
- as armadilhas (`| A1 | … |`) seguem A1, A2, … sem saltos, cada uma com a regra para a evitar;
- cada plano diz o que fica "Fora do escopo" e a "Prova";
- cada handoff é um arquivo por assunto, com as seções e só hashes de commits que existem.
Uma parte cuja pasta ou arquivo não existe no projeto é pulada. Instalar: copiar para `tests/` e ajustar abaixo.
"""

import re
import subprocess
import unittest

from carregar_por_caminho import RAIZ

# Ajuste ao projeto.
DOCS = RAIZ / "docs"
ARMADILHAS = DOCS / "armadilhas.md"
PLANOS = ("docs/planos/*.md",)
HANDOFFS = RAIZ / ".context"

DATA_NA_ULTIMA_COLUNA = re.compile(r"\|\s*20\d\d-\d\d-\d\d(?:/\d\d)?\s*\|\s*$")  # aceita um intervalo: 2026-10-22/23
SECOES_DO_HANDOFF = ("Objetivo", "Estado verificado", "Decisões", "Descartado", "Próximos passos")
HASH = re.compile(r"`([0-9a-f]{7,40})`")


def texto_do_doc(caminho):
    return caminho.read_text(encoding="utf-8-sig")


def titulos(caminho):
    """Títulos (# …) de um arquivo Markdown."""
    return [linha.lstrip("#").strip() for linha in texto_do_doc(caminho).splitlines() if linha.startswith("#")]


def exigir(teste, caminho):
    if not caminho.exists():
        teste.skipTest(f"{caminho.relative_to(RAIZ)} não existe neste projeto")


class IndiceDosDocs(unittest.TestCase):

    def test_cada_arquivo_e_pasta_de_docs_estao_no_indice(self):
        exigir(self, DOCS / "README.md")
        indice = texto_do_doc(DOCS / "README.md")
        for caminho in sorted(DOCS.iterdir()):
            if caminho.name == "README.md" or caminho.suffix not in ("", ".md"):
                continue
            alvo = f"]({caminho.name}/" if caminho.is_dir() else f"]({caminho.name})"
            with self.subTest(caminho=caminho.name):
                self.assertIn(alvo, indice, "arquivo .md novo → linha em docs/README.md")

    def test_cada_adr_esta_na_tabela_com_numeros_seguidos(self):
        exigir(self, DOCS / "decisoes")
        indice = texto_do_doc(DOCS / "README.md")
        adrs = sorted(caminho.name for caminho in (DOCS / "decisoes").glob("*.md"))
        self.assertEqual([nome[:4] for nome in adrs], [f"{n:04d}" for n in range(1, len(adrs) + 1)])
        for nome in adrs:
            with self.subTest(adr=nome):
                self.assertIn(f"](decisoes/{nome})", indice)


class Pesquisa(unittest.TestCase):

    def test_cada_pesquisa_esta_no_indice_com_data(self):
        exigir(self, DOCS / "pesquisa" / "README.md")
        linhas = texto_do_doc(DOCS / "pesquisa" / "README.md").splitlines()
        for caminho in sorted((DOCS / "pesquisa").glob("*.md")):
            if caminho.name == "README.md":
                continue
            with self.subTest(pesquisa=caminho.name):
                linha = next((linha for linha in linhas if f"]({caminho.name})" in linha), "")
                self.assertRegex(linha, DATA_NA_ULTIMA_COLUNA, "linha no índice da pesquisa com a data na última coluna")


class Armadilhas(unittest.TestCase):

    def test_numeracao_seguida_e_cada_uma_com_a_regra(self):
        exigir(self, ARMADILHAS)
        linhas = [linha for linha in texto_do_doc(ARMADILHAS).splitlines() if re.match(r"\| A\d+ \|", linha)]
        numeros = [int(re.match(r"\| A(\d+)", linha).group(1)) for linha in linhas]
        self.assertEqual(numeros, list(range(1, len(numeros) + 1)), "A1, A2, … sem saltos nem repetidos")
        for linha in linhas:
            colunas = [coluna.strip() for coluna in linha.strip().strip("|").split("|")]
            with self.subTest(armadilha=colunas[0]):
                self.assertGreaterEqual(len(colunas), 4)
                self.assertTrue(colunas[-1], "falta a regra para a evitar")


class Planos(unittest.TestCase):

    def test_planos_dizem_o_fora_do_escopo_e_a_prova(self):
        planos = [plano for padrao in PLANOS for plano in RAIZ.glob(padrao)]
        if not planos:
            self.skipTest("nenhum plano no projeto")
        for plano in planos:
            secoes = " | ".join(titulos(plano))
            with self.subTest(plano=plano.name):
                self.assertIn("Fora do escopo", secoes)
                self.assertRegex(secoes, r"Prova|Verificação")


class Handoffs(unittest.TestCase):

    def test_um_arquivo_por_assunto_com_as_secoes_e_hashes_que_existem(self):
        exigir(self, HANDOFFS)
        self.assertFalse((HANDOFFS / "HANDOFF.md").exists(), "um arquivo por assunto: HANDOFF-<assunto>.md")
        for handoff in sorted(HANDOFFS.glob("HANDOFF-*.md")):
            with self.subTest(handoff=handoff.name):
                secoes = titulos(handoff)
                for secao in SECOES_DO_HANDOFF:
                    self.assertTrue(any(s.startswith(secao) for s in secoes), f"falta a seção {secao}")
                for sha in HASH.findall(texto_do_doc(handoff)):
                    existe = subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=RAIZ,
                                            capture_output=True, check=False).returncode == 0
                    self.assertTrue(existe, f"o commit {sha} não existe: o estado não foi verificado")


if __name__ == "__main__":
    unittest.main()
