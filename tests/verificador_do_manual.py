"""O verificador do manual de uso (`manual/`): as verificações que os testes comuns do repositório não cobrem.

Já cobertos sem mudar nada: o link sem entrada no `FONTES.md`, o número de decisão e o link relativo partido
(`test_fontes_e_pesquisas.py`, `test_caminhos_do_morg_laws.py`) e o link externo morto (o lychee no CI).
Aqui nascem: o link solto, a página do livro sem entrada, o par e a seção sem fonte, a decisão sem porquê, a nota de
rodapé num par, o «Codex» sem link, a «página N» por extenso, os tetos por lado e por parte, o português de Portugal e a afirmação de que as
regras foram medidas. As funções recebem a raiz e a lista de arquivos (ou o nome e o texto), para os casos de erro
serem provados numa pasta temporária."""

import re

import dados_do_catalogo as catalogo
import lingua_do_brasil
import test_fontes_e_pesquisas as fontes
from leitura_do_repositorio import ler

PASTA_DO_MANUAL = "manual/"
# Palavras de cada lado do par, abaixo do que cabe numa página de 432 x 648 pt (a do molde novo). O método: encher um lado
# do P6 com prosa real do repositório (parágrafos de 30, 60, 120 e 1000 palavras), compilar com o comando do README e
# achar o maior enchimento que sai 0. A prática leva o código (9 linhas no Markdown, 14 impressas) e cabe de 243 a 280
# palavras; a teoria, sem código, de 418 a 490. Os tetos ficam no menor da prática (243) e abaixo do menor da teoria
# (410): o `panic` do molde é a rede, estes são o aviso cedo.
TETO_DA_PRATICA = 243
TETO_DA_TEORIA = 410
MOLDE = "manual/manual.typ"
PASTA_DO_MOLDE = "manual/molde/"
TETO_DO_MOLDE_EM_LINHAS = 150
FORA_DO_TETO = ("manual/fontes/", "manual/imagens/", "manual/pessoas-citaveis.txt", "manual/nomes-citaveis.txt",
                "manual/palavras-que-abrem-frase.txt")
# O livro novo (o mapa do §1 do plano): os nomes dos arquivos, sem `manual/` e sem `.md`. Um arquivo novo só vale depois de listado
# no molde (`capitulos-novos`, `pecas-novas` em manual.typ): o alcance dos testes novos é essa lista, e as partes de hoje ficam de fora.
CAPITULOS = ("cap-01-duas-empresas", "cap-02-uma-pasta-que-lembra", "cap-03-instalar-skills-e-regras", "cap-04-as-barreiras",
             "cap-05-quatro-partes-e-um-oraculo", "cap-06-pouca-cerimonia", "cap-07-compactar-parar-e-retomar",
             "cap-08-sessoes-filhas", "cap-09-uma-orquestradora", "cap-10-quem-escreveu-nao-audita", "cap-11-o-plano-e-o-sim",
             "cap-12-commits-pequenos", "cap-13-bug-traz-teste", "cap-14-as-regras-uma-por-uma", "cap-15-texto-vira-barreira")
PECAS = ("prefacio", "como-ler", "posfacio", "apendice-a", "apendice-b", "referencias", "de-onde-veio", "glossario")
PARTE_DO_CAPITULO = {1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 4, 10: 4, 11: 5, 12: 5, 13: 5, 14: 6, 15: 6}
SECOES_DO_MAPA = frozenset({f"A.{n}" for n in range(1, 8)} | {f"B.{n}" for n in (2, 3, 4, 7, 9, 12, 15, 16)})
TETOS_POR_PARTE = {  # palavras da prosa (fora de blocos de código) por parte; com pares: n × (243 + 410) + 200
    "manual/README.md": 500, "manual/00-antes-de-comecar.md": 1500, "manual/01-o-que-e-o-morg-laws.md": 1000,
    "manual/02-preparar-o-computador.md": 2650, "manual/03-instalar.md": 3465, "manual/04-pedir.md": 2812, "manual/05-sessoes.md": 5424,
    "manual/06-o-ciclo-de-uma-mudanca.md": 3465, "manual/07-as-regras.md": 2000,
    "manual/08-como-se-garante.md": 2700, "manual/09-quando-da-errado.md": 1506, "manual/10-glossario.md": 1800,
    "manual/11-pedidos-prontos.md": 1800, "manual/12-como-este-manual-foi-feito.md": 1000,
    "manual/prefacio.md": 900, "manual/como-ler.md": 1000,
    "manual/referencias.md": 1500}  # as Referências do livro novo (≈4 pp.); cada capítulo novo acrescenta o seu teto
PARTES_EM_TEXTO_SEGUIDO = ("00", "01", "02", "07", "08", "11", "12")  # prefixos do nome; o glossário (10) não pede fonte
EXCECOES_DE_SECAO = frozenset({("manual/07-as-regras.md", "O índice das skills")})  # (arquivo, título) sem fonte
EXCECOES_DO_CODEX = frozenset()  # (arquivo, primeiros 40 caracteres do parágrafo) que cita o Codex sem link
ORDEM_DO_PAR = ["Na prática", "Por quê e fonte"]  # o par de hoje (`## P<n>`)
ORDEM_DO_PAR_NOVO = ["Na prática", "Por quê"]  # o par marcado: a fonte é a nota numerada
MARCA_DE_PAR = re.compile(r"\s*<!--\s*raw-typst\s+#marca-de-par\(\)\s*-->\s*")
CHAMADA_DE_NOTA = re.compile(r"\[\^([^\]\s]+)\](?!:)")
DEFINICAO_DE_NOTA = re.compile(r"\[\^([^\]\s]+)\]:[ \t]*(.*)")
VOZES_DO_AUTOR = re.compile(r"vozes da minha cabeça")
ASPAS_CURVAS = re.compile(r"“[^”]*”")
ALCANCE_TOTAL = False  # a 4.8 liga-o, quando a lista do molde já não tem nenhuma parte de hoje: N1 e N5 valem para tudo

LINK_MARCADO = re.compile(r"\[[^\]]*\]\([^)\s]*\)")
LINK_COM_ENDERECO = re.compile(r"\]\(https?://")
LINK_DO_CODEX = re.compile(r"\]\(https?://[^)\s]*codex[^)\s]*\)", re.IGNORECASE)
CODEX = re.compile(r"\bCodex\b")
PAGINA_POR_EXTENSO = re.compile(r"\b(?:páginas?|págs?\.)\s*\d", re.IGNORECASE)
PAR_DE_PROCEDIMENTO = re.compile(r"P\d+\b")
CITACAO_DE_PAGINA = re.compile(r"(?<![\w.])pp?\. ?(\d+(?:\s?[–-]\s?\d+)?(?:(?:,\s?| e )\d+(?:\s?[–-]\s?\d+)?)*)")
ITEM_DE_PAGINA = re.compile(r"\d+(?:\s?[–-]\s?\d+)?")
DECISAO_DO_PO = re.compile(r"(?:vozes da cabeça de Carlobks \(decisão de |\b[Dd]ecisão de Carlobks \(|\b[Dd]ecisão do autor \()"
                           r"\d{4}-\d\d-\d\d\)")
SENTENCA = re.compile(r"(?<=[.!?])(?<!\bp\.)(?<!\bpp\.)\s+")
ABRE_BLOCO = re.compile(r"\s*(?:[-*+]\s|\d+[.)]\s|\||#)")
DE_CITACAO = re.compile(r"^\s*(?:>\s*)+")
ORACAO = re.compile(r"[:;]")
AFIRMA_MEDICAO = re.compile(r"\b(?:medid|testad|validad|comprovad|provad)[oa]s?\b", re.IGNORECASE)
SOBRE_AS_REGRAS = re.compile(r"\bregras?\b|\b[dn]?o Morg-laws\b|\bskills?\b", re.IGNORECASE)
NEGACAO = re.compile(r"\b(?:não|nunca|nenhum|nenhuma)\b", re.IGNORECASE)


def linhas_por_secao(texto, nivel):
    """[(título, [linhas])] dos títulos de `nivel` (2 → «## »), fora dos blocos de código; as linhas são as originais."""
    marca, secoes, no_codigo = "#" * nivel + " ", [], False
    for linha in texto.splitlines():
        no_codigo ^= linha.lstrip().startswith(fontes.CERCAS_DE_CODIGO)
        if linha.startswith(marca) and not no_codigo:
            secoes.append((linha[len(marca):].strip(), []))
        elif secoes:
            secoes[-1][1].append(linha)
    return secoes


def prosa(linhas):
    """As linhas fora dos blocos de código."""
    saida, no_codigo = [], False
    for linha in linhas:
        if linha.lstrip().startswith(fontes.CERCAS_DE_CODIGO):
            no_codigo = not no_codigo
        elif not no_codigo and not MARCA_DE_PAR.fullmatch(linha):
            saida.append(linha)
    return saida


def texto_de_prosa(texto):
    """O texto sem os blocos de código e sem o que está entre crases."""
    return catalogo.CRASES.sub(" ", "\n".join(prosa(texto.splitlines())))


def palavras_da_prosa(linhas):
    return len(" ".join(prosa(linhas)).split())


def paragrafos(texto):
    return re.split(r"\n\s*\n", texto)


def links_soltos(nome, texto):
    """Um endereço em texto corrido, fora de `[texto](url)` e fora de código."""
    limpo = LINK_MARCADO.sub(" ", texto_de_prosa(texto))
    return [f"{nome}: {url} — link solto: escreva [texto](endereço)" for url in fontes.URL.findall(limpo)]


def itens_de_pagina(texto):
    """Os itens citados («124», «30–32») em cada «p. N», «pp. N–M» ou lista («pp. 30–39, 124 e 411»)."""
    return [item for citacao in CITACAO_DE_PAGINA.findall(texto) for item in ITEM_DE_PAGINA.findall(citacao)]


def numeros_do_item(item):
    return [int(numero) for numero in re.findall(r"\d+", item)]


def paginas_conhecidas(raiz):
    """As páginas do livro com entrada: a seção «Livros e autores» do FONTES.md e os itens da `biblia-akita/`."""
    secao = ler(raiz / "FONTES.md").partition("## Livros e autores")[2].split("\n## ")[0]
    textos = [secao] + [ler(caminho) for caminho in sorted((raiz / "biblia-akita").glob("*.md"))]
    intervalos = [numeros_do_item(item) for texto in textos for item in itens_de_pagina(texto)]
    return {pagina for numeros in intervalos for pagina in range(numeros[0], numeros[-1] + 1)}


def paginas_sem_entrada(nome, texto, conhecidas):
    """Cada página citada (os dois extremos de um intervalo) tem de estar numa entrada; o manual cita a página impressa."""
    citadas = [n for item in itens_de_pagina(texto_de_prosa(texto)) for n in numeros_do_item(item)]
    return [f"{nome}: p. {n} do livro sem entrada em FONTES.md («Livros e autores») nem na biblia-akita/"
            for n in citadas if n not in conhecidas]


def tem_fonte(linhas):
    """Um link com endereço, uma página do livro, uma nota numerada chamada, ou uma decisão com «Porquê:»."""
    texto = texto_de_prosa("\n".join(linhas))
    decisao = DECISAO_DO_PO.search(texto) and "Porquê:" in texto
    return bool(LINK_COM_ENDERECO.search(texto) or itens_de_pagina(texto) or CHAMADA_DE_NOTA.search(texto) or decisao)


def definicoes_de_notas(texto):
    """[(nome, texto)] das notas `[^nome]: …`: a linha e as seguintes até uma linha em branco; o código não conta."""
    definicoes, aberta = [], False
    for linha in texto_de_prosa(texto).splitlines():
        if achado := DEFINICAO_DE_NOTA.fullmatch(linha):
            definicoes.append((achado[1], achado[2]))
            aberta = True
        elif aberta and linha.strip():
            definicoes[-1] = (definicoes[-1][0], definicoes[-1][1] + " " + linha.strip())
        else:
            aberta = False
    return definicoes


def texto_antes_do_primeiro_h3(nome, titulo, linhas):
    """O texto entre o `## P…` e o primeiro `###` não tem lado no PDF: reprova (só a prosa conta, não o código)."""
    antes = []
    for linha in linhas:
        if linha.startswith("### "):
            break
        antes.append(linha)
    return [f"{nome}: «{titulo}»: texto antes de «### Na prática» — ponha-o dentro de um dos dois lados"] \
        * bool(" ".join(prosa(antes)).strip())


def lados_do_par(nome, titulo, linhas, marcado=False):
    """A ordem «Na prática» → «Por quê» (o par marcado) ou «Por quê e fonte» (o de hoje), o teto de cada lado e a fonte."""
    lados, ordem = linhas_por_secao("\n".join(linhas), 3), ORDEM_DO_PAR_NOVO if marcado else ORDEM_DO_PAR
    if [lado for lado, _ in lados] != ordem:
        return [f"{nome}: «{titulo}»: precisa de «### Na prática» e depois «### {ordem[1]}»"]
    tetos = (TETO_DA_PRATICA, TETO_DA_TEORIA)
    erros = [f"{nome}: «{titulo}»: «{lado}» tem {n} palavras (teto {teto})"
             for (lado, corpo), teto in zip(lados, tetos) if (n := palavras_da_prosa(corpo)) > teto]
    return erros + [f"{nome}: «{titulo}»: a teoria está sem fonte"] * (not tem_fonte(lados[1][1]))


def secoes_de_par(texto):
    """[(título, linhas, marcado)] dos `##`: `marcado` quando a linha de antes é o marcador invisível do par novo."""
    saida, no_codigo, anterior = [], False, ""
    for linha in texto.splitlines():
        no_codigo ^= linha.lstrip().startswith(fontes.CERCAS_DE_CODIGO)
        if linha.startswith("## ") and not no_codigo:
            saida.append((linha[3:].strip(), [], bool(MARCA_DE_PAR.fullmatch(anterior))))
        elif saida:
            saida[-1][1].append(linha)
        anterior = linha if linha.strip() else anterior
    return saida


def marcas_soltas(nome, texto):
    """O marcador de par sem um `## título` logo a seguir: não abre par nenhum."""
    linhas = [linha for linha in texto.splitlines() if linha.strip()]
    return [f"{nome}: marcador de par sem «## título» logo a seguir" for i, linha in enumerate(linhas)
            if MARCA_DE_PAR.fullmatch(linha) and not (i + 1 < len(linhas) and linhas[i + 1].startswith("## "))]


def pares_do_texto(nome, texto):
    """Cada `## P…` (o gatilho de hoje) e cada `##` depois do marcador (o gatilho novo) é um par: ordem, tetos e fonte."""
    erros = marcas_soltas(nome, texto)
    for titulo, linhas, marcado in secoes_de_par(texto):
        if marcado or PAR_DE_PROCEDIMENTO.match(titulo):
            erros += texto_antes_do_primeiro_h3(nome, titulo, linhas) + lados_do_par(nome, titulo, linhas, marcado)
    return erros


def secoes_sem_fonte(nome, texto):
    """Nas partes em texto seguido, cada `##` leva fonte; as exceções estão em EXCECOES_DE_SECAO, à vista."""
    if not nome.removeprefix(PASTA_DO_MANUAL).startswith(PARTES_EM_TEXTO_SEGUIDO):
        return []
    return [f"{nome}: «{titulo}»: a seção está sem fonte" for titulo, linhas in linhas_por_secao(texto, 2)
            if (nome, titulo) not in EXCECOES_DE_SECAO and not tem_fonte(linhas)]


def decisoes_sem_porque(nome, texto):
    """«as vozes da cabeça de Carlobks (decisão de AAAA-MM-DD)» ou «Decisão de Carlobks (AAAA-MM-DD)», seguida de
    «Porquê:» no mesmo parágrafo."""
    achados = [(p, DECISAO_DO_PO.search(p)) for p in paragrafos(texto)]
    return [f"{nome}: decisão sem «Porquê:» no mesmo parágrafo — «{p.strip()[:40]}…»"
            for p, achado in achados if achado and "Porquê:" not in p[achado.end():]]


def codex_sem_link(nome, texto):
    """Todo parágrafo de prosa com «Codex» leva um link para a documentação dele (só a presença; a fonte entra no
    FONTES.md). A nota numerada chamada no parágrafo conta como o link dele, se a nota o tiver. As exceções,
    (arquivo, início do parágrafo), estão em EXCECOES_DO_CODEX."""
    notas = dict(definicoes_de_notas(texto))

    def com_link(p):
        return LINK_DO_CODEX.search(p) or any(LINK_DO_CODEX.search(notas.get(n, "")) for n in CHAMADA_DE_NOTA.findall(p))
    return [f"{nome}: «Codex» sem link para a documentação do Codex no mesmo parágrafo — «{p.strip()[:40]}…»"
            for p in paragrafos(texto_de_prosa(texto))
            if CODEX.search(p) and not com_link(p) and (nome, p.strip()[:40]) not in EXCECOES_DO_CODEX]


def vozes_sem_decisao_na_nota(nome, texto):
    """«as vozes da minha cabeça» na prosa (fora de aspas) leva uma nota «Decisão do autor (AAAA-MM-DD). Porquê: …»."""
    notas = dict(definicoes_de_notas(texto))
    return [f"{nome}: «as vozes da minha cabeça» sem nota «Decisão do autor (AAAA-MM-DD). Porquê: …» — «{p.strip()[:40]}…»"
            for p in paragrafos(texto_de_prosa(texto)) if VOZES_DO_AUTOR.search(ASPAS_CURVAS.sub(" ", p))
            and not any(DECISAO_DO_PO.search(notas.get(n, "")) for n in CHAMADA_DE_NOTA.findall(p))]


def aspas_francesas(nome, texto):
    """O manual usa as aspas curvas “ ” (e ‘ ’ dentro delas), como no Brasil; as «» são do resto do repositório."""
    return [f"{nome}: aspas «» na prosa — no manual use aspas curvas “ ”"] * bool(re.search(r"[«»]", texto_de_prosa(texto)))


def pagina_por_extenso(nome, texto):
    """«página 31» e «pág. 9» não se leem como página do livro: o manual escreve «p. N»."""
    return [f"{nome}: «{achado.group()}» — escreva p. N" for achado in PAGINA_POR_EXTENSO.finditer(texto_de_prosa(texto))]


def blocos_do_paragrafo(paragrafo):
    """As linhas de um parágrafo juntas em blocos: só uma linha de continuação se junta à anterior; um item de lista,
    uma linha de tabela, um título ou uma citação nova abrem bloco novo."""
    blocos, citacao_antes = [], False
    for linha in paragrafo.splitlines():
        limpa, e_citacao = DE_CITACAO.sub("", linha), linha.lstrip().startswith(">")
        if not blocos or ABRE_BLOCO.match(limpa) or blocos[-1].startswith("#") or (e_citacao and not citacao_antes):
            blocos.append(limpa.strip())
        else:
            blocos[-1] += " " + limpa.strip()
        citacao_antes = e_citacao
    return blocos


def frases_do_texto(texto):
    """As frases da prosa: a quebra de linha não parte a frase; o ponto de «p.» e «pp.» também não."""
    return [frase for paragrafo in paragrafos(texto_de_prosa(texto)) for bloco in blocos_do_paragrafo(paragrafo)
            for frase in SENTENCA.split(bloco)]


def medido_sem_negacao(nome, texto):
    """Nenhum texto diz que as regras foram medidas: «regra(s)», «skills» ou «o/do/no Morg-laws» com um verbo de
    medição na mesma frase reprova, a menos que haja não, nunca ou nenhum antes do verbo, na mesma oração (sem «:» nem
    «;» no meio). O resto fica com a leitura do Davi: a negação que não nega o verbo («as regras que não mudam foram
    medidas») e o verbo em outra forma («nós medimos as regras») passam."""
    erros = []
    for frase in frases_do_texto(texto):
        verbo = AFIRMA_MEDICAO.search(frase)
        oracao = ORACAO.split(frase[:verbo.start()])[-1] if verbo else ""
        if verbo and SOBRE_AS_REGRAS.search(frase) and not NEGACAO.search(oracao):
            erros.append(f"{nome}: afirma que as regras foram medidas, testadas ou provadas — «{frase.strip()[:60]}»")
    return erros


def teto_de_um_arquivo(raiz, nome):
    """O arquivo dentro do teto: o molde em linhas, cada parte em palavras; o que não tem teto reprova, sem ser lido
    (só o `.md` e o `.typ` com teto se leem; uma imagem acusa-se pela extensão)."""
    if nome == MOLDE or (nome.startswith(PASTA_DO_MOLDE) and nome.endswith(".typ")):
        medida, teto, unidade = len(ler(raiz / nome).splitlines()), TETO_DO_MOLDE_EM_LINHAS, "linhas"
    elif nome in TETOS_POR_PARTE:
        medida, teto, unidade = palavras_da_prosa(ler(raiz / nome).splitlines()), TETOS_POR_PARTE[nome], "palavras"
    else:
        return [f"{nome}: arquivo fora de qualquer teto — ponha-o em TETOS_POR_PARTE ou em FORA_DO_TETO"]
    return [f"{nome}: {medida} {unidade} (teto {teto})"] * (medida > teto)


def erros_de_teto_por_parte(raiz, arquivos):
    erros = []
    for nome in sorted(a for a in arquivos if not a.startswith(FORA_DO_TETO)):
        erros += teto_de_um_arquivo(raiz, nome)
    return erros


def lista_do_molde(texto, nome):
    """Os nomes da tupla `#let <nome> = (...)` do molde, lidos como texto (sem o Typst e sem rede)."""
    tupla = re.search(r"#let " + nome + r" = \((.*?)\)\s*(?:\n|$)", texto, re.DOTALL)
    return re.findall(r'"([^"]+)"', tupla.group(1)) if tupla else []


def erros_da_lista_do_molde(raiz, arquivos):
    """As `escritas` do molde são os `manual/NN-*.md` do git, e as `partes` são as chaves de TETOS_POR_PARTE (sem o
    README), pela mesma ordem: uma parte fora da lista fica fora do PDF sem aviso."""
    molde = ler(raiz / MOLDE)
    no_git = sorted(a.removeprefix(PASTA_DO_MANUAL).removesuffix(".md") for a in arquivos
                    if re.fullmatch(r"manual/\d\d-[^/]*\.md", a))
    dos_tetos = [c.removeprefix(PASTA_DO_MANUAL).removesuffix(".md") for c in TETOS_POR_PARTE
               if re.fullmatch(r"manual/\d\d-[^/]*\.md", c)]
    erros = []
    for nome, esperado, origem in (("escritas", no_git, "os manual/NN-*.md do git"), ("partes", dos_tetos, "as chaves de TETOS_POR_PARTE")):
        lista = lista_do_molde(molde, nome)
        if lista != esperado:
            erros.append(f"{MOLDE}: `{nome}` {lista} diferem de {origem} {esperado}")
    for nome, mapa in (("capitulos-novos", CAPITULOS), ("pecas-novas", PECAS)):
        esperado, lista = [n for n in mapa if f"{PASTA_DO_MANUAL}{n}.md" in arquivos], lista_do_molde(molde, nome)
        if lista != esperado:
            erros.append(f"{MOLDE}: `{nome}` {lista} diferem dos arquivos novos do git {esperado}, na ordem do mapa")
    return erros


def novos_do_molde(raiz):
    """Os arquivos novos que o molde já lista: o alcance dos testes do livro novo (sem molde, nenhum)."""
    molde = ler(raiz / MOLDE) if (raiz / MOLDE).exists() else ""
    return [f"{PASTA_DO_MANUAL}{n}.md" for lista in ("capitulos-novos", "pecas-novas") for n in lista_do_molde(molde, lista)]


def pares_repetidos(vistos, nome, texto):
    """O mesmo `P<n>` (par de hoje) ou o mesmo título (par marcado) duas vezes, no mesmo arquivo ou noutro, reprova;
    `vistos` guarda onde cada um nasceu."""
    erros = []
    for titulo, _, marcado in secoes_de_par(texto):
        achado = PAR_DE_PROCEDIMENTO.match(titulo)
        chave = f"par «{titulo}»" if marcado else achado and achado.group()
        if chave in vistos:
            erros.append(f"{nome}: «{titulo}»: o {chave} já existe em {vistos[chave]}")
        elif chave:
            vistos[chave] = nome
    return erros


CODIGOS_INTERNOS = re.compile(r"\bP\d+\b|\bL-\d+\b|\b[Pp]rocedimentos? P\b|\b[Nn]a parte \d+\b")
REMISSAO_DE_CAPITULO = re.compile(r"\b[Cc]apítulos? (\d+(?:(?:,\s?| e )\d+)*)")
REMISSAO_DE_APENDICE = re.compile(r"\b(?:[Aa]pêndice|Ap\.|[Ss]eção) ([A-Z])(?:\.(\d+))?\b")
IMAGEM = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
FIGURA = re.compile(r"(?:.*/)?figura-(\d+)-(\d+)\.svg")
ARTE_DE_PARTE = re.compile(r"manual/imagens/arte-parte-([1-6])-([ab])\.svg")
FALA_DO_SISTEMA = re.compile(r"\b(?:Windows|macOS|terminal)\b", re.IGNORECASE)
NOTA_DE_AUTOR = re.compile(r"[A-ZÀ-Ý][A-ZÀ-Ý' -]*[A-ZÀ-Ý], \d{4}\b")
ENTRADA_DE_REFERENCIA = re.compile(r"[ \t]*(?:[-*+][ \t]+)?([A-ZÀ-Ý][A-ZÀ-Ý' -]*[A-ZÀ-Ý]),\s")
APENDICE_B, COMO_LER, GLOSSARIO, REFERENCIAS = ("manual/apendice-b.md", "manual/como-ler.md", "manual/glossario.md",
                                                "manual/referencias.md")
FUNCOES_DO_APP = frozenset()  # (arquivo, título) das seções do Ap. B que o autor marcou como usadas no app (a folha da 4.0)


def codigos_internos(nome, texto):
    """N1 · nenhum `P<n>`, `L-<n>`, «procedimento P» nem «na parte N» na prosa (o `D<n>` já o recusa test_fontes_e_pesquisas)."""
    return [f"{nome}: código interno «{a.group()}» na prosa — conte a ideia, sem o código"
            for a in CODIGOS_INTERNOS.finditer(texto_de_prosa(texto))]


def notas_fecham(nome, texto):
    """N2 · cada `[^nome]` chamado tem a sua definição, cada definição é chamada, uma vez só, e nenhuma é vazia."""
    definicoes = definicoes_de_notas(texto)
    definidas, chamadas = [n for n, _ in definicoes], set(CHAMADA_DE_NOTA.findall(texto_de_prosa(texto)))
    return ([f"{nome}: nota [^{n}] chamada sem definição" for n in sorted(chamadas - set(definidas))]
            + [f"{nome}: nota [^{n}] definida e nunca chamada" for n in sorted(set(definidas) - chamadas)]
            + [f"{nome}: nota [^{n}] definida duas vezes" for n in sorted({n for n in definidas if definidas.count(n) > 1})]
            + [f"{nome}: nota [^{n}] vazia" for n, corpo in definicoes if not corpo.strip()])


def remissoes_existem(nome, texto):
    """N4 · cada «Capítulo N», «Apêndice X» e «Seção B.N» aponta para uma peça do mapa do §1 (não para os arquivos que existem)."""
    prosa_do_texto, erros = texto_de_prosa(texto), []
    for achado in REMISSAO_DE_CAPITULO.finditer(prosa_do_texto):
        erros += [f"{nome}: «Capítulo {n}» não existe no mapa (1 a {len(CAPITULOS)})" for n in re.findall(r"\d+", achado[1])
                  if not 1 <= int(n) <= len(CAPITULOS)]
    for achado in REMISSAO_DE_APENDICE.finditer(prosa_do_texto):
        letra, numero = achado.groups()
        if letra not in "AB" or (numero and f"{letra}.{numero}" not in SECOES_DO_MAPA):
            erros.append(f"{nome}: «{achado.group()}» não existe no mapa (Apêndices A e B, seções {sorted(SECOES_DO_MAPA)})")
    return erros


def comandos_so_no_apendice_b(nome, texto):
    """N5 · fora do Ap. B só blocos ```pedido; a palavra «terminal» só no Ap. B e no «Como ler» (e no glossário, que a define)."""
    erros, aberto = [], False
    for linha in texto.splitlines():
        if linha.lstrip().startswith(fontes.CERCAS_DE_CODIGO):
            info = linha.lstrip().lstrip("`~").strip()
            erros += [f"{nome}: bloco de código «{info}» fora do Apêndice B — só os blocos ```pedido"] * (
                not aberto and info != "pedido" and nome != APENDICE_B)
            aberto = not aberto
    if nome not in (APENDICE_B, COMO_LER, GLOSSARIO) and re.search(r"\bterminal\b", texto_de_prosa(texto), re.IGNORECASE):
        erros.append(f"{nome}: a palavra «terminal» só aparece no Apêndice B e no «Como ler»")
    return erros


def nao_testado_a_vista(nome, texto):
    """N6 · cada seção do Ap. B que fala de Windows, macOS ou terminal diz «não testado pelo autor», salvo as do app."""
    if nome != APENDICE_B:
        return []
    return [f"{nome}: «{titulo}»: fala de Windows, macOS ou terminal sem «não testado pelo autor»"
            for titulo, linhas in linhas_por_secao(texto, 2) if (nome, titulo) not in FUNCOES_DO_APP
            and FALA_DO_SISTEMA.search(titulo + " " + " ".join(prosa(linhas)))
            and "não testado pelo autor" not in " ".join(prosa(linhas)).lower()]


def figuras_dos_capitulos(nome, texto):
    """N7 · cada imagem de um arquivo é `figura-<capítulo>-<n>.svg` e a legenda abre com «Figura <capítulo>.<n>»."""
    erros = []
    for legenda, caminho in IMAGEM.findall(texto_de_prosa(texto)):
        achado = FIGURA.fullmatch(caminho)
        if not achado:
            erros.append(f"{nome}: imagem «{caminho}» — as figuras são figura-<capítulo>-<n>.svg (as artes são do molde)")
        elif not re.match(rf"Figura {int(achado[1])}\.{int(achado[2])}\b", legenda):
            erros.append(f"{nome}: a figura «{caminho}» precisa da legenda «Figura {int(achado[1])}.{int(achado[2])}»")
    return erros


def artes_das_partes(raiz, arquivos, novos):
    """N7 · só há as 12 `arte-parte-<n>-{a,b}.svg`; as partes que já têm capítulo novo têm as duas e o molde chama-as."""
    molde = "\n".join(ler(raiz / a) for a in arquivos if a.endswith(".typ"))
    com_capitulo = {PARTE_DO_CAPITULO[int(n[len(PASTA_DO_MANUAL) + 4:][:2])] for n in novos
                    if n.startswith(PASTA_DO_MANUAL + "cap-")}
    erros = [f"{a}: fora das 12 artes arte-parte-<1 a 6>-<a ou b>.svg" for a in sorted(arquivos)
             if a.startswith(PASTA_DO_MANUAL + "imagens/arte-parte-") and not ARTE_DE_PARTE.fullmatch(a)]
    for parte in sorted(com_capitulo):
        for lado in "ab":
            arte = f"arte-parte-{parte}-{lado}.svg"
            if f"{PASTA_DO_MANUAL}imagens/{arte}" not in arquivos:
                erros.append(f"manual/imagens/{arte}: falta — a parte {parte} já tem capítulo novo")
            elif arte not in molde:
                erros.append(f"manual/imagens/{arte}: o molde não a chama")
    return erros


def notas_e_referencias(raiz, arquivos, novos):
    """N3 · cada nota «SOBRENOME, ano» tem a entrada nas Referências; cada entrada tem uma nota e uma linha no FONTES.md."""
    notas = {tuple(a.group().split(", ")) for n in novos if n in arquivos for _, corpo in definicoes_de_notas(ler(raiz / n))
             if (a := NOTA_DE_AUTOR.match(corpo))}
    entradas, erros = [], []
    for linha in (ler(raiz / REFERENCIAS).splitlines() if REFERENCIAS in arquivos else []):
        if achado := ENTRADA_DE_REFERENCIA.match(linha):
            ano = re.search(r"\b(?:19|20)\d\d\b", linha.split("Acesso em")[0])
            entradas.append((achado[1], ano.group() if ano else None))
    fontes_md = ler(raiz / "FONTES.md").lower()
    erros += [f"nota «{s}, {a}» sem entrada em {REFERENCIAS}" for s, a in sorted(notas - set(entradas))]
    erros += [f"{REFERENCIAS}: «{s}, {a}» sem nota que a cite" for s, a in entradas if (s, a) not in notas]
    return erros + [f"{REFERENCIAS}: «{s}» sem linha no FONTES.md" for s in sorted({s for s, _ in entradas})
                    if s.lower() not in fontes_md]


VERIFICACOES_DOS_NOVOS = (codigos_internos, notas_fecham, remissoes_existem, comandos_so_no_apendice_b, nao_testado_a_vista,
                          figuras_dos_capitulos, vozes_sem_decisao_na_nota)


def erros_do_alcance_total(raiz, arquivos, novos):
    """O que a 4.8 liga (ALCANCE_TOTAL): nenhum `## P<n>` sobra e N1 e N5 valem também para as partes de hoje."""
    erros = []
    for nome in sorted(a for a in arquivos if a.endswith(".md") and a not in novos):
        texto = ler(raiz / nome)
        erros += [f"{nome}: «## {t}» — o gatilho de hoje já devia ter saído" for t, _, _ in secoes_de_par(texto)
                  if PAR_DE_PROCEDIMENTO.match(t)]
        erros += codigos_internos(nome, texto) + comandos_so_no_apendice_b(nome, texto)
    return erros


VERIFICACOES_DO_TEXTO = (links_soltos, pares_do_texto, secoes_sem_fonte, decisoes_sem_porque, codex_sem_link,
                         pagina_por_extenso, aspas_francesas, medido_sem_negacao, lingua_do_brasil.erros_de_lingua)


def erros_do_manual(raiz, arquivos, novos=None):
    """Todos os erros do manual: `arquivos` são os caminhos relativos à raiz (os de `manual/` do git); `novos` são os
    arquivos do livro novo (por defeito, os que o molde lista): só neles valem os testes novos."""
    novos = novos_do_molde(raiz) if novos is None else novos
    conhecidas, erros, vistos = paginas_conhecidas(raiz), erros_de_teto_por_parte(raiz, arquivos), {}
    for nome in sorted(a for a in arquivos if a.endswith(".md")):
        texto = ler(raiz / nome)
        erros += pares_repetidos(vistos, nome, texto)
        erros += [erro for verificacao in VERIFICACOES_DO_TEXTO for erro in verificacao(nome, texto)]
        erros += paginas_sem_entrada(nome, texto, conhecidas)
        erros += [erro for verificacao in VERIFICACOES_DOS_NOVOS * (nome in novos) for erro in verificacao(nome, texto)]
    erros += notas_e_referencias(raiz, arquivos, novos) + artes_das_partes(raiz, arquivos, novos)
    return erros + erros_do_alcance_total(raiz, arquivos, novos) * ALCANCE_TOTAL
