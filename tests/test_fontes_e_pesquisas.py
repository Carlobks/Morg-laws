"""As fontes e as pesquisas do próprio Morg-laws ficam conferidas pelo CI, e não só escritas (D27, D28, D30, D33):

1. cada endereço http(s) de um `.md` do git (fora o FONTES.md) está no FONTES.md, ignorando a âncora e a barra
   final; isentos só os links para o próprio repositório e os domínios de exemplo (example.com, .org, .net);
2. cada entrada do FONTES.md com link tem uma data AAAA-MM-DD (na entrada ou no parágrafo «Lidas em …» da seção) e
   «Sustenta» ou «(secundária»; o que já falhava fica na linha de base, que só encolhe;
3. cada pesquisa (`pesquisas/*.md`, fora o README) está no índice com a data na última coluna e tem as cinco seções.
As funções recebem a raiz e a lista de arquivos, para os casos de erro serem provados numa pasta temporária.
"""

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from carregar_modelos import RAIZ

LINHA_DE_BASE = RAIZ / "tests" / "linhas-de-base" / "fontes.json"
URL = re.compile(r"https?://[^\s<>()\[\]`\"'*]+")
DATA = re.compile(r"\b20\d\d-\d\d-\d\d\b")
DATA_NA_ULTIMA_COLUNA = re.compile(r"\|\s*20\d\d-\d\d-\d\d\s*\|\s*$")
PROPRIO_REPOSITORIO = re.compile(r"https?://github\.com/Carlobks/Morg-laws(?:[/.]|$)", re.IGNORECASE)
DOMINIOS_DE_EXEMPLO = ("example.com", "example.org", "example.net")
SECOES_DA_PESQUISA = ("Pergunta", "Fontes", "O que se mediu", "O que não se verificou", "Conclusão")


def normalizar(url):
    """O endereço sem a pontuação colada, sem a âncora e sem a barra final."""
    return url.rstrip(".,;:!?»").split("#")[0].rstrip("/")


def isento(url):
    dominio = url.split("/")[2].lower()
    exemplo = any(dominio == d or dominio.endswith("." + d) for d in DOMINIOS_DE_EXEMPLO)
    return exemplo or bool(PROPRIO_REPOSITORIO.match(url))


def links(texto):
    return {normalizar(url) for url in URL.findall(texto)}


def ler(caminho):
    return caminho.read_text(encoding="utf-8-sig")


def links_sem_fonte(raiz, arquivos):
    """Mensagens para cada link de um .md que falta no FONTES.md."""
    fontes = links(ler(raiz / "FONTES.md"))
    erros = []
    for nome in sorted(arquivos):
        if nome == "FONTES.md":
            continue
        for url in sorted(links(ler(raiz / nome)) - fontes):
            if not isento(url):
                erros.append(f"{nome}: {url} — link novo → entrada no FONTES.md com a data e o que sustenta")
    return erros


def entradas_do_fontes(texto):
    """[(primeiro link, texto da entrada, a seção tem «Lidas em AAAA-MM-DD»)] das entradas com link."""
    entradas, data_da_secao, atual = [], False, None
    for linha in texto.splitlines():
        if linha.startswith("## "):
            data_da_secao, atual = False, None
        elif linha.startswith("Lidas em"):
            data_da_secao = bool(DATA.search(linha))
        elif linha.startswith("- "):
            atual = [linha, data_da_secao]
            entradas.append(atual)
        elif linha.startswith("  ") and atual:
            atual[0] += " " + linha.strip()
        else:
            atual = None
    return [(normalizar(URL.search(t).group()), t, d) for t, d in entradas if URL.search(t)]


def falta_na_entrada(texto, data_da_secao):
    """O que falta no formato de uma entrada: "data", "Sustenta" ou nada."""
    falta = []
    if not (data_da_secao or DATA.search(texto)):
        falta.append("data")
    if "Sustenta" not in texto and "(secundária" not in texto:
        falta.append("Sustenta")
    return falta


def erros_das_fontes(texto, linha_de_base):
    """Entradas fora do formato e fora da linha de base, e entradas da linha de base que já estão certas."""
    erros, vistas = [], set()
    for url, entrada, data_da_secao in entradas_do_fontes(texto):
        vistas.add(url)
        falta = falta_na_entrada(entrada, data_da_secao)
        if falta and url not in linha_de_base:
            erros.append(f"{url}: sem {' e sem '.join(falta)} — a entrada do FONTES.md leva a data em que a fonte "
                         "foi lida e «Sustenta: …» ou «(secundária: …)»")
        elif not falta and url in linha_de_base:
            erros.append(f"{url}: já está certa — tire-a de tests/linhas-de-base/fontes.json no mesmo commit")
    for url in sorted(set(linha_de_base) - vistas):
        erros.append(f"{url}: não está mais no FONTES.md — tire-a de tests/linhas-de-base/fontes.json")
    return erros


def titulos(texto):
    return [linha.lstrip("#").strip() for linha in texto.splitlines() if linha.startswith("#")]


def erros_das_pesquisas(pasta):
    """Pesquisas fora do índice, sem data na última coluna ou sem uma das cinco seções."""
    if not pasta.is_dir():
        return []
    indice = ler(pasta / "README.md").splitlines() if (pasta / "README.md").exists() else []
    erros = []
    for caminho in sorted(pasta.glob("*.md")):
        if caminho.name == "README.md":
            continue
        linha = next((linha for linha in indice if f"]({caminho.name})" in linha), "")
        if not DATA_NA_ULTIMA_COLUNA.search(linha):
            erros.append(f"{caminho.name}: fora do índice — linha em pesquisas/README.md com a data na última coluna")
        secoes = titulos(ler(caminho))
        for secao in SECOES_DA_PESQUISA:
            if secao not in secoes:
                erros.append(f"{caminho.name}: falta a seção «{secao}»")
    return erros


def arquivos_md(raiz):
    # Só os arquivos que o git conhece: um .md novo é conferido depois do `git add`.
    return subprocess.run(["git", "ls-files", "*.md"], cwd=raiz, capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout.splitlines()


def carregar_linha_de_base(caminho):
    return set(json.loads(ler(caminho))["entradas"]) if caminho.exists() else set()


class FontesEPesquisasDoMorgLaws(unittest.TestCase):
    maxDiff = None  # a falha mostra todas as mensagens, cada uma com o que fazer

    def test_cada_link_dos_md_esta_no_fontes(self):
        self.assertEqual(links_sem_fonte(RAIZ, arquivos_md(RAIZ)), [])

    def test_cada_entrada_do_fontes_tem_data_e_o_que_sustenta(self):
        self.assertEqual(erros_das_fontes(ler(RAIZ / "FONTES.md"), carregar_linha_de_base(LINHA_DE_BASE)), [])

    def test_cada_pesquisa_esta_no_indice_com_as_secoes(self):
        self.assertEqual(erros_das_pesquisas(RAIZ / "pesquisas"), [])


PESQUISA_CERTA = "# P\n\n## Pergunta\n\n## Fontes\n\n## O que se mediu\n\n## O que não se verificou\n\n## Conclusão\n"


class ReprovaQuandoDeve(unittest.TestCase):
    """Cada caso de erro numa pasta temporária, nunca nos arquivos do repositório."""

    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.raiz = Path(self.pasta.name)
        self.escrever("FONTES.md", "## A\n\n- **Fonte** — https://fonte.test/a — lido em 2026-11-02. Sustenta: x.\n")

    def escrever(self, nome, texto):
        (self.raiz / nome).parent.mkdir(parents=True, exist_ok=True)
        (self.raiz / nome).write_text(texto, encoding="utf-8")

    def test_link_novo_sem_entrada(self):
        self.escrever("doc.md", "Ver https://fonte.test/a/#x e https://nova.test/b.\n")
        self.assertEqual(links_sem_fonte(self.raiz, ["doc.md", "FONTES.md"]),
                         ["doc.md: https://nova.test/b — link novo → entrada no FONTES.md com a data e o que sustenta"])

    def test_links_isentos_passam(self):
        self.escrever("doc.md", "https://github.com/Carlobks/Morg-laws/tree/main/x https://example.com/r.git "
                                "https://www.example.org https://example.net/ https://github.com/Carlobks/Morg-laws\n")
        self.assertEqual(links_sem_fonte(self.raiz, ["doc.md"]), [])

    def test_o_proprio_repositorio_nao_isenta_um_nome_parecido(self):
        self.assertFalse(isento("https://github.com/Carlobks/Morg-laws-copia"))
        self.assertFalse(isento("https://example.com.test/x"))

    def test_entrada_sem_data(self):
        erros = erros_das_fontes("## A\n\n- **F** — https://f.test — Sustenta: x.\n", set())
        self.assertEqual(len(erros), 1)
        self.assertIn("https://f.test: sem data —", erros[0])

    def test_entrada_sem_sustenta_e_sem_data(self):
        erros = erros_das_fontes("## A\n\n- **F** — https://f.test\n  continua sem nada.\n", set())
        self.assertIn("https://f.test: sem data e sem Sustenta —", erros[0])

    def test_data_da_secao_e_secundaria_contam(self):
        texto = "## A\n\nLidas em 2026-10-31.\n\n- **F** — https://f.test — *(secundária: não relida)*\n"
        self.assertEqual(erros_das_fontes(texto, set()), [])
        self.assertEqual(erros_das_fontes("## B\n\n- **Livro**, sem link.\n", set()), [])

    def test_entrada_da_linha_de_base_que_ja_esta_certa(self):
        texto = "## A\n\n- **F** — https://f.test — lido em 2026-11-02. Sustenta: x.\n"
        self.assertEqual(erros_das_fontes(texto, {"https://f.test"}),
                         ["https://f.test: já está certa — tire-a de tests/linhas-de-base/fontes.json no mesmo commit"])

    def test_linha_de_base_cobre_a_que_falha_e_some_quando_a_entrada_sai(self):
        self.assertEqual(erros_das_fontes("## A\n\n- **F** — https://f.test\n", {"https://f.test"}), [])
        self.assertIn("não está mais no FONTES.md", erros_das_fontes("", {"https://f.test"})[0])

    def test_pesquisa_fora_do_indice(self):
        self.escrever("pesquisas/README.md", "| Arquivo | Pergunta | Data |\n|---|---|---|\n")
        self.escrever("pesquisas/2026-11-02-x.md", PESQUISA_CERTA)
        esperado = "2026-11-02-x.md: fora do índice — linha em pesquisas/README.md com a data na última coluna"
        self.assertEqual(erros_das_pesquisas(self.raiz / "pesquisas"), [esperado])

    def test_pesquisa_sem_uma_das_secoes(self):
        self.escrever("pesquisas/README.md", "| [x](2026-11-02-x.md) | Pergunta? | 2026-11-02 |\n")
        self.escrever("pesquisas/2026-11-02-x.md", PESQUISA_CERTA.replace("## Conclusão\n", ""))
        self.assertEqual(erros_das_pesquisas(self.raiz / "pesquisas"), ["2026-11-02-x.md: falta a seção «Conclusão»"])

    def test_pesquisa_certa_e_pasta_ausente_passam(self):
        self.escrever("pesquisas/README.md", "| [x](2026-11-02-x.md) | Pergunta? | 2026-11-02 |\n")
        self.escrever("pesquisas/2026-11-02-x.md", PESQUISA_CERTA)
        self.assertEqual(erros_das_pesquisas(self.raiz / "pesquisas"), [])
        self.assertEqual(erros_das_pesquisas(self.raiz / "nao-existe"), [])
        self.assertEqual(carregar_linha_de_base(self.raiz / "nao-existe.json"), set())


if __name__ == "__main__":
    unittest.main()
