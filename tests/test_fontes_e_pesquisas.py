"""As fontes e as pesquisas do próprio Morg-laws ficam conferidas pelo CI, e não só escritas:

1. cada endereço http(s) de um `.md` do git (fora o FONTES.md) abre uma entrada do FONTES.md (é o primeiro link
   dela), ignorando a âncora e a barra final; isentos só os links para o próprio repositório (no GitHub e no
   raw.githubusercontent.com) e os domínios de exemplo (example.com, .org e .net, com subdomínio ou porta);
2. cada entrada do FONTES.md com link (marcador `-`, `*`, `+` ou `1.`) tem uma data AAAA-MM-DD fora do endereço (na
   entrada ou no parágrafo «Lidas em …» da seção) e «Sustenta» ou «(secundária»; o que já falhava fica na linha de
   base, que só encolhe: não passa de LINHA_DE_BASE_INICIAL e não guarda uma entrada que já está certa;
3. cada pesquisa fica direto em `pesquisas/`, está no índice com a data na última coluna e tem as cinco seções
   `## `, na ordem (um título dentro de um bloco de código não conta);
4. nenhum arquivo do git cita uma decisão pelo número (a letra D seguida de algarismos): o número só existe num
   registro privado, e quem lê o repositório não o consegue seguir. A decisão escreve-se em palavras.
As funções recebem a raiz e a lista de arquivos, para os casos de erro serem provados numa pasta temporária.
"""

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlsplit

from carregar_modelos import RAIZ

LINHA_DE_BASE = RAIZ / "tests" / "linhas-de-base" / "fontes.json"
# As entradas que já falhavam quando o teste entrou. Só encolhe: quem corrige uma tira-a daqui e do JSON.
LINHA_DE_BASE_INICIAL = frozenset({
    "https://code.claude.com/docs/en/plugin-marketplaces",
    "https://agentskills.io",
    "https://pester.dev/docs/usage/code-coverage",
    "https://github.com/mattpocock/skills",
    "https://cheatsheetseries.owasp.org",
    "https://akitaonrails.com",
})
URL = re.compile(r"https?://[^\s<>()\[\]`\"'*|]+")
DATA = re.compile(r"\b20\d\d-\d\d-\d\d\b")
DATA_NA_ULTIMA_COLUNA = re.compile(r"\|\s*20\d\d-\d\d-\d\d\s*\|\s*$")
MARCADOR_DE_LISTA = re.compile(r"(?:[-*+]|\d+\.) ")
PROPRIO_REPOSITORIO = re.compile(r"https?://(?:github\.com|raw\.githubusercontent\.com)/Carlobks/Morg-laws(?:[/.]|$)",
                                 re.IGNORECASE)
DOMINIOS_DE_EXEMPLO = ("example.com", "example.org", "example.net")
SECOES_DA_PESQUISA = ("Pergunta", "Fontes", "O que se mediu", "O que não se verificou", "Conclusão")
CERCAS_DE_CODIGO = ("```", "~~~")
NUMERO_DE_DECISAO = re.compile(r"\bD\d+\b")


def normalizar(url):
    """O endereço sem a pontuação colada, sem a âncora e sem a barra final."""
    return url.rstrip(".,;:!?»").split("#")[0].rstrip("/")


def isento(url):
    dominio = urlsplit(url).hostname or ""  # sem a porta e em minúsculas
    exemplo = any(dominio == d or dominio.endswith("." + d) for d in DOMINIOS_DE_EXEMPLO)
    return exemplo or bool(PROPRIO_REPOSITORIO.match(url))


def links(texto):
    return {normalizar(url) for url in URL.findall(texto)}


def ler(caminho):
    return caminho.read_text(encoding="utf-8-sig")


def links_sem_fonte(raiz, arquivos):
    """Mensagens para cada link de um .md que não abre uma entrada do FONTES.md."""
    fontes = {url for url, _, _ in entradas_do_fontes(ler(raiz / "FONTES.md"))}
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
        elif MARCADOR_DE_LISTA.match(linha):
            atual = [linha, data_da_secao]
            entradas.append(atual)
        elif linha[:1].isspace() and atual:  # continuação recuada, com espaços ou TAB
            atual[0] += " " + linha.strip()
        else:
            atual = None
    return [(normalizar(URL.search(t).group()), t, d) for t, d in entradas if URL.search(t)]


def falta_na_entrada(texto, data_da_secao):
    """O que falta no formato de uma entrada: "data", "Sustenta" ou nada."""
    falta = []
    if not (data_da_secao or DATA.search(URL.sub(" ", texto))):  # uma data dentro do endereço não conta
        falta.append("data")
    if "Sustenta" not in texto and "(secundária" not in texto.lower():
        falta.append("Sustenta")
    return falta


def erros_das_fontes(texto, linha_de_base, inicial=LINHA_DE_BASE_INICIAL):
    """Entradas fora do formato e fora da linha de base, entradas da linha de base que já estão certas ou que saíram
    do FONTES.md, e a linha de base que cresceu além da inicial."""
    erros, vistas = [], set()
    for url, entrada, data_da_secao in entradas_do_fontes(texto):
        vistas.add(url)
        falta = falta_na_entrada(entrada, data_da_secao)
        if falta and url not in linha_de_base:
            erros.append(f"{url}: sem {' e sem '.join(falta)} — a entrada do FONTES.md leva a data em que a fonte "
                         "foi lida e «Sustenta: …» ou «(secundária: …)»")
        elif not falta and url in linha_de_base:
            erros.append(f"{url}: já está certa — tire-a de tests/linhas-de-base/fontes.json e de "
                         "LINHA_DE_BASE_INICIAL no mesmo commit")
    for url in sorted(set(linha_de_base) - vistas):
        erros.append(f"{url}: não está mais no FONTES.md — tire-a de tests/linhas-de-base/fontes.json e de "
                     "LINHA_DE_BASE_INICIAL")
    for url in sorted(set(linha_de_base) - inicial):
        erros.append(f"{url}: entrada nova no FONTES.md nasce no formato — a linha de base não cresce")
    return erros


def secoes(texto):
    """Os títulos `## ` de um Markdown, fora dos blocos de código."""
    achadas, no_codigo = [], False
    for linha in texto.splitlines():
        if linha.lstrip().startswith(CERCAS_DE_CODIGO):
            no_codigo = not no_codigo
        elif linha.startswith("## ") and not no_codigo:
            achadas.append(linha[3:].strip())
    return achadas


def erros_de_uma_pesquisa(caminho, indice):
    """Fora do índice, sem data na última coluna, sem uma das cinco seções ou com elas fora da ordem."""
    erros = []
    linha = next((linha for linha in indice if f"]({caminho.name})" in linha), "")
    if not DATA_NA_ULTIMA_COLUNA.search(linha):
        erros.append(f"{caminho.name}: fora do índice — linha em pesquisas/README.md com a data na última coluna")
    achadas = secoes(ler(caminho))
    faltam = [secao for secao in SECOES_DA_PESQUISA if secao not in achadas]
    erros += [f"{caminho.name}: falta a seção «{secao}»" for secao in faltam]
    if not faltam and [secao for secao in achadas if secao in SECOES_DA_PESQUISA] != list(SECOES_DA_PESQUISA):
        erros.append(f"{caminho.name}: seções fora da ordem — {', '.join(SECOES_DA_PESQUISA)}")
    return erros


def erros_das_pesquisas(pasta):
    """Os erros de cada pesquisa da pasta, e as pesquisas guardadas numa subpasta."""
    if not pasta.is_dir():
        return []
    indice = ler(pasta / "README.md").splitlines() if (pasta / "README.md").exists() else []
    erros = []
    for caminho in sorted(pasta.rglob("*.md")):
        if caminho.parent != pasta:
            erros.append(f"{caminho.relative_to(pasta).as_posix()}: está numa subpasta — as pesquisas ficam direto "
                         "em pesquisas/")
        elif caminho.name != "README.md":
            erros += erros_de_uma_pesquisa(caminho, indice)
    return erros


def numeros_de_decisoes(raiz, arquivos):
    """Mensagens para cada número de decisão (a letra D seguida de algarismos) num arquivo de texto."""
    erros = []
    for nome in sorted(arquivos):
        dados = (raiz / nome).read_bytes()
        if b"\0" in dados:  # binário
            continue
        for numero, linha in enumerate(dados.decode("utf-8", "replace").splitlines(), start=1):
            erros += [f"{nome}:{numero}: {achado} — escreva a decisão em palavras; o número só existe num registro "
                      "privado" for achado in NUMERO_DE_DECISAO.findall(linha)]
    return erros


def arquivos_do_git(raiz, *padroes):
    # Só os arquivos que o git conhece: um arquivo novo é conferido depois do `git add`.
    return subprocess.run(["git", "ls-files", *padroes], cwd=raiz, capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout.splitlines()


def carregar_linha_de_base(caminho):
    return set(json.loads(ler(caminho))["entradas"]) if caminho.exists() else set()


class FontesEPesquisasDoMorgLaws(unittest.TestCase):
    maxDiff = None  # a falha mostra todas as mensagens, cada uma com o que fazer

    def test_cada_link_dos_md_esta_no_fontes(self):
        self.assertEqual(links_sem_fonte(RAIZ, arquivos_do_git(RAIZ, "*.md")), [])

    def test_cada_entrada_do_fontes_tem_data_e_o_que_sustenta(self):
        self.assertEqual(erros_das_fontes(ler(RAIZ / "FONTES.md"), carregar_linha_de_base(LINHA_DE_BASE)), [])

    def test_a_linha_de_base_do_json_e_a_do_teste_sao_iguais(self):
        self.assertEqual(carregar_linha_de_base(LINHA_DE_BASE), LINHA_DE_BASE_INICIAL,
                         "tirou uma entrada de tests/linhas-de-base/fontes.json? tire-a também de "
                         "LINHA_DE_BASE_INICIAL; o contrário não: a linha de base não cresce")

    def test_cada_pesquisa_esta_no_indice_com_as_secoes(self):
        self.assertEqual(erros_das_pesquisas(RAIZ / "pesquisas"), [])

    def test_nenhum_arquivo_cita_uma_decisao_pelo_numero(self):
        self.assertEqual(numeros_de_decisoes(RAIZ, arquivos_do_git(RAIZ)), [])


PESQUISA_CERTA = "# P\n\n## Pergunta\n\n## Fontes\n\n## O que se mediu\n\n## O que não se verificou\n\n## Conclusão\n"


class PastaTemporaria(unittest.TestCase):
    """Base dos casos de erro: uma pasta temporária, nunca os arquivos do repositório."""

    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.raiz = Path(self.pasta.name)
        self.escrever("FONTES.md", "## A\n\n- **Fonte** — https://fonte.test/a — lido em 2026-11-02. Sustenta: x.\n")

    def escrever(self, nome, texto):
        (self.raiz / nome).parent.mkdir(parents=True, exist_ok=True)
        (self.raiz / nome).write_text(texto, encoding="utf-8")


class ReprovaQuandoDeve(PastaTemporaria):
    """Os casos da prova do plano."""

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
        esperado = ("https://f.test: já está certa — tire-a de tests/linhas-de-base/fontes.json e de "
                    "LINHA_DE_BASE_INICIAL no mesmo commit")
        self.assertEqual(erros_das_fontes(texto, {"https://f.test"}, inicial={"https://f.test"}), [esperado])

    def test_linha_de_base_cobre_a_que_falha_e_some_quando_a_entrada_sai(self):
        base = {"https://f.test"}
        self.assertEqual(erros_das_fontes("## A\n\n- **F** — https://f.test\n", base, inicial=base), [])
        self.assertIn("não está mais no FONTES.md", erros_das_fontes("", base, inicial=base)[0])

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


class RegressoesDaAuditoria(PastaTemporaria):
    """Os casos de borda achados na auditoria da fase, cada um numa pasta temporária."""

    def test_a1_a_linha_de_base_nao_cresce(self):
        texto = "## A\n\n- **Velha** — https://agentskills.io\n- **Nova** — https://nova.test\n"
        self.assertEqual(erros_das_fontes(texto, {"https://agentskills.io", "https://nova.test"}),
                         ["https://nova.test: entrada nova no FONTES.md nasce no formato — a linha de base não cresce"])

    def test_a3_link_so_na_prosa_de_outra_entrada_nao_e_fonte(self):
        self.escrever("FONTES.md", "## A\n\n- **A** — https://a.test — lido em 2026-11-02. Sustenta: x; ver também "
                                   "https://b.test.\n")
        self.escrever("doc.md", "Ver https://b.test.\n")
        self.assertEqual(links_sem_fonte(self.raiz, ["doc.md"]),
                         ["doc.md: https://b.test — link novo → entrada no FONTES.md com a data e o que sustenta"])

    def test_a4_data_dentro_do_endereco_nao_e_data_de_leitura(self):
        erros = erros_das_fontes("## A\n\n- **Post** — https://blog.test/2024-01-15-post — Sustenta: y.\n", set())
        self.assertEqual(len(erros), 1)
        self.assertIn("https://blog.test/2024-01-15-post: sem data —", erros[0])

    def test_a5_entradas_com_outros_marcadores_de_lista(self):
        for marcador in ("*", "+", "1."):
            with self.subTest(marcador=marcador):
                erros = erros_das_fontes(f"## A\n\n{marcador} **X** — https://x.test\n", set())
                self.assertEqual(len(erros), 1)
                self.assertIn("https://x.test: sem data e sem Sustenta —", erros[0])

    def test_a6_continuacao_com_tab_e_secundaria_maiuscula(self):
        self.assertEqual(erros_das_fontes("## A\n\n- **X** — https://x.test — lido em 2026-11-02.\n\tSustenta: y.\n",
                                          set()), [])
        self.assertEqual(erros_das_fontes("## A\n\n- **X** — https://x.test — 2026-11-02 *(Secundária: não relida)*\n",
                                          set()), [])

    def test_a7_titulo_dentro_de_bloco_de_codigo_nao_e_secao(self):
        self.escrever("pesquisas/README.md", "| [x](2026-11-02-x.md) | Pergunta? | 2026-11-02 |\n")
        self.escrever("pesquisas/2026-11-02-x.md", PESQUISA_CERTA.replace("## Conclusão\n", "```sh\n# Conclusão\n```\n"))
        self.assertEqual(erros_das_pesquisas(self.raiz / "pesquisas"), ["2026-11-02-x.md: falta a seção «Conclusão»"])

    def test_a8_secoes_fora_da_ordem(self):
        invertida = "# P\n\n" + "".join(f"## {secao}\n\n" for secao in reversed(SECOES_DA_PESQUISA))
        self.escrever("pesquisas/README.md", "| [x](2026-11-02-x.md) | Pergunta? | 2026-11-02 |\n")
        self.escrever("pesquisas/2026-11-02-x.md", invertida)
        esperado = ("2026-11-02-x.md: seções fora da ordem — Pergunta, Fontes, O que se mediu, O que não se verificou, "
                    "Conclusão")
        self.assertEqual(erros_das_pesquisas(self.raiz / "pesquisas"), [esperado])

    def test_a9_pesquisa_numa_subpasta(self):
        self.escrever("pesquisas/README.md", "| Arquivo | Pergunta | Data |\n|---|---|---|\n")
        self.escrever("pesquisas/sub/2026-11-03-y.md", "# Y\n")
        self.assertEqual(erros_das_pesquisas(self.raiz / "pesquisas"),
                         ["sub/2026-11-03-y.md: está numa subpasta — as pesquisas ficam direto em pesquisas/"])

    def test_a10_porta_e_raw_do_proprio_repositorio_sao_isentos(self):
        self.assertTrue(isento("https://example.com:8080/x"))
        self.assertTrue(isento("https://raw.githubusercontent.com/Carlobks/Morg-laws/main/x"))
        self.assertFalse(isento("https://raw.githubusercontent.com/Carlobks/Morg-laws-copia/main/x"))
        self.assertFalse(isento("https://raw.githubusercontent.com/outra/Morg-laws/main/x"))

    def test_a11_link_colado_a_barra_de_tabela(self):
        self.escrever("FONTES.md", "## A\n\n- **A** — https://a.test — lido em 2026-11-02. Sustenta: x.\n")
        self.escrever("doc.md", "| a |https://a.test|\n")
        self.assertEqual(links_sem_fonte(self.raiz, ["doc.md"]), [])

    def test_a14_numero_de_decisao_num_arquivo_publico(self):
        decisao = "D" + "16"  # montado aqui, para este arquivo não se acusar a si mesmo
        self.escrever("doc.md", f"Fica para a fase seguinte ({decisao}).\nSem número: ID 16, AD9, D16x.\n")
        (self.raiz / "imagem.png").write_bytes(b"\x89PNG\0" + decisao.encode())
        esperado = f"doc.md:1: {decisao} — escreva a decisão em palavras; o número só existe num registro privado"
        self.assertEqual(numeros_de_decisoes(self.raiz, ["doc.md", "imagem.png"]), [esperado])


if __name__ == "__main__":
    unittest.main()
