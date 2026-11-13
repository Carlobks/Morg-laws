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
# Palavras de cada lado do par, abaixo do que cabe numa página de 6 x 9,6 pol. O método: encher um lado do P6 com prosa
# real do repositório (parágrafos de 60, 120 e 1000 palavras), compilar com o comando do README e achar o maior
# enchimento que sai 0. A prática leva o código (9 linhas no Markdown, 14 impressas) e cabe de 251 a 334 palavras; a
# teoria, sem código, de 431 a 603. Os tetos ficam abaixo do menor: o `panic` do molde é a rede, estes são o aviso cedo.
TETO_DA_PRATICA = 250
TETO_DA_TEORIA = 400
MOLDE = "manual/manual.typ"
TETO_DO_MOLDE_EM_LINHAS = 150
FORA_DO_TETO = ("manual/fontes/", "manual/imagens/", "manual/pessoas-citaveis.txt", "manual/nomes-citaveis.txt",
                "manual/palavras-que-abrem-frase.txt")
TETOS_POR_PARTE = {  # palavras da prosa (fora de blocos de código) por parte; com pares: n × (250 + 400) + 200
    "manual/README.md": 500, "manual/00-antes-de-comecar.md": 1500, "manual/01-o-que-e-o-morg-laws.md": 1000,
    "manual/02-preparar-o-computador.md": 2650, "manual/03-instalar.md": 3450, "manual/04-pedir.md": 2800, "manual/05-sessoes.md": 5400,
    "manual/06-o-ciclo-de-uma-mudanca.md": 3450, "manual/07-as-regras.md": 2000,
    "manual/08-como-se-garante.md": 2700, "manual/09-quando-da-errado.md": 1500, "manual/10-glossario.md": 1800,
    "manual/11-pedidos-prontos.md": 1800, "manual/12-como-este-manual-foi-feito.md": 1000}
PARTES_EM_TEXTO_SEGUIDO = ("00", "01", "02", "07", "08", "11", "12")  # prefixos do nome; o glossário (10) não pede fonte
EXCECOES_DE_SECAO = frozenset({("manual/07-as-regras.md", "O índice das skills")})  # (arquivo, título) sem fonte
EXCECOES_DO_CODEX = frozenset()  # (arquivo, primeiros 40 caracteres do parágrafo) que cita o Codex sem link
ORDEM_DO_PAR =["Na prática", "Por quê e fonte"]

LINK_MARCADO = re.compile(r"\[[^\]]*\]\([^)\s]*\)")
LINK_COM_ENDERECO = re.compile(r"\]\(https?://")
LINK_DO_CODEX = re.compile(r"\]\(https?://[^)\s]*codex[^)\s]*\)", re.IGNORECASE)
CODEX = re.compile(r"\bCodex\b")
PAGINA_POR_EXTENSO = re.compile(r"\b(?:páginas?|págs?\.)\s*\d", re.IGNORECASE)
PAR_DE_PROCEDIMENTO = re.compile(r"P\d+\b")
CITACAO_DE_PAGINA = re.compile(r"(?<![\w.])pp?\. ?(\d+(?:\s?[–-]\s?\d+)?(?:(?:,\s?| e )\d+(?:\s?[–-]\s?\d+)?)*)")
ITEM_DE_PAGINA = re.compile(r"\d+(?:\s?[–-]\s?\d+)?")
DECISAO_DO_PO = re.compile(r"(?:vozes da cabeça de Carlobks \(decisão de |\b[Dd]ecisão de Carlobks \()\d{4}-\d\d-\d\d\)")
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
        elif not no_codigo:
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
    """Um link com endereço, uma página do livro, ou uma decisão de Carlobks com «Porquê:»."""
    texto = texto_de_prosa("\n".join(linhas))
    decisao = DECISAO_DO_PO.search(texto) and "Porquê:" in texto
    return bool(LINK_COM_ENDERECO.search(texto) or itens_de_pagina(texto) or decisao)


def notas_de_rodape_num_par(nome, titulo, linhas):
    return [f"{nome}: «{titulo}»: nota de rodapé num par — ponha a fonte em link"] * any("[^" in l for l in linhas)


def texto_antes_do_primeiro_h3(nome, titulo, linhas):
    """O texto entre o `## P…` e o primeiro `###` não tem lado no PDF: reprova (só a prosa conta, não o código)."""
    antes = []
    for linha in linhas:
        if linha.startswith("### "):
            break
        antes.append(linha)
    return [f"{nome}: «{titulo}»: texto antes de «### Na prática» — ponha-o dentro de um dos dois lados"] \
        * bool(" ".join(prosa(antes)).strip())


def lados_do_par(nome, titulo, linhas):
    """A ordem «Na prática» → «Por quê e fonte», o teto de palavras de cada lado e a fonte da teoria."""
    lados = linhas_por_secao("\n".join(linhas), 3)
    if [lado for lado, _ in lados] != ORDEM_DO_PAR:
        return [f"{nome}: «{titulo}»: precisa de «### Na prática» e depois «### Por quê e fonte»"]
    tetos = (TETO_DA_PRATICA, TETO_DA_TEORIA)
    erros = [f"{nome}: «{titulo}»: «{lado}» tem {n} palavras (teto {teto})"
             for (lado, corpo), teto in zip(lados, tetos) if (n := palavras_da_prosa(corpo)) > teto]
    return erros + [f"{nome}: «{titulo}»: a teoria está sem fonte"] * (not tem_fonte(lados[1][1]))


def pares_do_texto(nome, texto):
    """Cada `## P…` é um par: notas de rodapé, ordem, tetos por lado e fonte."""
    erros = []
    for titulo, linhas in linhas_por_secao(texto, 2):
        if PAR_DE_PROCEDIMENTO.match(titulo):
            erros += (notas_de_rodape_num_par(nome, titulo, linhas) + texto_antes_do_primeiro_h3(nome, titulo, linhas)
                      + lados_do_par(nome, titulo, linhas))
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
    FONTES.md). As exceções, (arquivo, início do parágrafo), estão em EXCECOES_DO_CODEX."""
    return [f"{nome}: «Codex» sem link para a documentação do Codex no mesmo parágrafo — «{p.strip()[:40]}…»"
            for p in paragrafos(texto_de_prosa(texto))
            if CODEX.search(p) and not LINK_DO_CODEX.search(p) and (nome, p.strip()[:40]) not in EXCECOES_DO_CODEX]


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
    if nome == MOLDE:
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
    dos_tetos = [c.removeprefix(PASTA_DO_MANUAL).removesuffix(".md") for c in TETOS_POR_PARTE if c != "manual/README.md"]
    erros = []
    for nome, esperado, origem in (("escritas", no_git, "os manual/NN-*.md do git"), ("partes", dos_tetos, "as chaves de TETOS_POR_PARTE")):
        lista = lista_do_molde(molde, nome)
        if lista != esperado:
            erros.append(f"{MOLDE}: `{nome}` {lista} diferem de {origem} {esperado}")
    return erros


def pares_repetidos(vistos, nome, texto):
    """O mesmo `P<n>` em dois títulos, do mesmo arquivo ou de outro, reprova; `vistos` guarda onde cada um nasceu."""
    erros = []
    for titulo, _ in linhas_por_secao(texto, 2):
        achado = PAR_DE_PROCEDIMENTO.match(titulo)
        if achado and achado.group() in vistos:
            erros.append(f"{nome}: «{titulo}»: o {achado.group()} já existe em {vistos[achado.group()]}")
        elif achado:
            vistos[achado.group()] = nome
    return erros


VERIFICACOES_DO_TEXTO = (links_soltos, pares_do_texto, secoes_sem_fonte, decisoes_sem_porque, codex_sem_link,
                         pagina_por_extenso, aspas_francesas, medido_sem_negacao, lingua_do_brasil.erros_de_lingua)


def erros_do_manual(raiz, arquivos):
    """Todos os erros do manual: `arquivos` são os caminhos relativos à raiz (os de `manual/` do git)."""
    conhecidas, erros, vistos = paginas_conhecidas(raiz), erros_de_teto_por_parte(raiz, arquivos), {}
    for nome in sorted(a for a in arquivos if a.endswith(".md")):
        texto = ler(raiz / nome)
        erros += pares_repetidos(vistos, nome, texto)
        erros += [erro for verificacao in VERIFICACOES_DO_TEXTO for erro in verificacao(nome, texto)]
        erros += paginas_sem_entrada(nome, texto, conhecidas)
    return erros
