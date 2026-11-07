"""O que não pode entrar em `projetos/`, a pasta do catálogo publicado: as expressões, a lista de palavras com
maiúscula, os termos da lista negra e a escolha do conteúdo a verificar (índice, commits do intervalo ou árvore).
Usado por `test_projetos_sem_dados.py` (o que vale para o repositório) e pelos testes dos casos."""

import functools
import os
import re
import subprocess
import sys
import types
from collections import namedtuple

from carregar_modelos import PASTA_TESTES_MODELO, RAIZ, carregar

# O molde de dados pessoais importa RAIZ de carregar_por_caminho; aqui a raiz é a deste repositório.
sys.modules["carregar_por_caminho"] = types.SimpleNamespace(RAIZ=RAIZ)
molde = carregar(PASTA_TESTES_MODELO / "test_dados_pessoais.py", "test_dados_pessoais_molde")
del sys.modules["carregar_por_caminho"]

PASTA = "projetos"
PALAVRAS = "tests/palavras-com-maiuscula.txt"
SECOES = ("comuns", "nomes")
CATEGORIAS = ("tecnologia", "papel", "projeto")
EXTENSOES_DE_ARQUIVO = frozenset({"md", "py", "ts", "tsx", "js", "mjs", "cjs", "json", "txt", "sh", "yml", "yaml",
                                  "html", "css", "sql", "toml", "lock", "csv", "png", "svg", "pdf"})
EXTENSOES_QUE_SAO_PAIS = frozenset({"md", "py", "sh"})  # Moldávia, Paraguai, Santa Helena: `fulano.sh` pode ser domínio
FINAIS_DE_DOMINIO = frozenset({"com", "net", "org", "info", "biz", "edu", "gov", "mil", "int", "io", "dev", "app", "site",
                               "online", "xyz", "tech", "store", "shop", "cloud", "pro"})  # além dos de duas letras (países)
PALAVRAS_LONGAS_ACEITAS = frozenset()  # palavras de 20 letras que o catálogo usa (nenhuma até agora)
DOMINIOS_ACEITOS = frozenset({"user.name", "user.email"})  # chaves da configuração do git, que parecem domínios
Conteudo = namedtuple("Conteudo", "origem texto palavras e_lista caminho")

SEPARADOR = "[ .\u00a0\u202f\u2009-]?"  # espaço, ponto, espaço sem quebra, espaço fino estreito, espaço fino, hífen
DOCUMENTO = re.compile(r"(?<![\d.,])(?:\d{3}" + SEPARADOR + r"\d{3}" + SEPARADOR + r"\d{3}|\d{11})(?!\d|[.,]\d)")
IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:[ -]?[A-Z0-9]{4}){3,7}(?:[ -]?[A-Z0-9]{1,3})?\b", re.IGNORECASE)
UUID = re.compile(r"\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b", re.IGNORECASE)
HASH = re.compile(r"(?<![#\w])(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b", re.IGNORECASE)
SERVICO = re.compile(r"\b[a-z0-9]{20}\b")
DOMINIO = re.compile(r"\b[\w-]+(?:\.[\w-]+)*\.([a-z]{2,24})\b", re.IGNORECASE)
DINHEIRO_SIMBOLO = re.compile(r"€|\bEUR\b|\bUSD\b|R\$|US\$")
DINHEIRO_DOLAR = re.compile(r"\bd[óo]lar(?:es)?\b", re.IGNORECASE)
DINHEIRO_POR_EXTENSO = re.compile(r"\d[\d .,]*\s?(?:mil\s)?(?:euros?|reais|d[óo]lares)\b", re.IGNORECASE)
DINHEIRO_CIFRAO = re.compile(r"\$\s?\d")
CRASES = re.compile(r"`[^`]*`")
ALVO_DE_LINK = re.compile(r"\]\(([^)\s]*)\)")  # o alvo de um link: [texto](alvo)
PALAVRA = re.compile(r"(?<![^\W_])[^\W\d_][^\W_]*")  # letras e dígitos: o sublinhado separa, como a barra e o hífen
CLASSE_POSIX = re.compile(r"\[:[a-z]+:\]")
SO_DO_GREP = re.compile(r"(?<!\\)(?:\\\\)*\\[<>`']")  # \< \> \` \': o Python os compila, mas casa outra coisa


def _achados_de(padrao, linha):
    return [achado.group(0) for achado in padrao.finditer(linha)]


def _caminhos(linha, _):
    return [m.group(0) for m in molde.CONTA_EM_CAMINHO.finditer(linha) if not molde.conta_de_exemplo(m)]


def _emails(linha, _):
    return [m.group(0) for m in molde.EMAIL.finditer(linha) if not molde.email_aceito(m)]


def _servicos(linha, _):
    return [achado for achado in _achados_de(SERVICO, linha) if achado not in PALAVRAS_LONGAS_ACEITAS]


def _e_arquivo(rotulos, em_codigo):
    """Nome de arquivo: a extensão é conhecida; as que também são país (md, py, sh) só em crases e com um ponto só."""
    if rotulos[-1] not in EXTENSOES_DE_ARQUIVO:
        return False
    return rotulos[-1] not in EXTENSOES_QUE_SAO_PAIS or (em_codigo and len(rotulos) == 2)


def _e_dominio(m, em_codigo, aceitos):
    """Fora das crases, todo nome com ponto é domínio. Dentro delas é código, e só é domínio se acabar como um."""
    rotulos = m.group(0).lower().split(".")
    if m.group(0).lower() in aceitos or rotulos[-2] == "example" or _e_arquivo(rotulos, em_codigo):
        return False
    return not em_codigo or len(rotulos[-1]) == 2 or rotulos[-1] in FINAIS_DE_DOMINIO


def _e_alvo_relativo(alvo):
    """Caminho relativo: começa por ./ ou ../, ou é um .md; nunca com :// (esse é endereço de internet)."""
    return "://" not in alvo and (alvo.startswith(("./", "../")) or alvo.endswith(".md"))


def _dominios(linha, aceitos):
    """Um alvo de link relativo é lido como código (só é domínio se acabar como um); qualquer outro, como texto."""
    em_codigo = [(m.start(), m.end()) for m in CRASES.finditer(linha)]
    em_codigo += [m.span(1) for m in ALVO_DE_LINK.finditer(linha) if _e_alvo_relativo(m.group(1))]
    return [m.group(0) for m in DOMINIO.finditer(linha)
            if _e_dominio(m, any(inicio <= m.start() < fim for inicio, fim in em_codigo), aceitos)]


def _dinheiro(linha, _):
    fora_das_crases = CRASES.sub(lambda m: " " * len(m.group(0)), linha)  # `echo $1` é comando, não dinheiro
    padroes = (DINHEIRO_SIMBOLO, DINHEIRO_DOLAR, DINHEIRO_POR_EXTENSO)
    return [a for p in padroes for a in _achados_de(p, linha)] + _achados_de(DINHEIRO_CIFRAO, fora_das_crases)


def _simples(padrao):
    return lambda linha, _: _achados_de(padrao, linha)


DETECTORES = (("caminho", _caminhos), ("e-mail", _emails), ("documento", _simples(DOCUMENTO)),
              ("IBAN", _simples(IBAN)), ("UUID", _simples(UUID)), ("hash", _simples(HASH)),
              ("ID de serviço", _servicos), ("domínio", _dominios), ("dinheiro", _dinheiro))


def dados_fora_nomes(texto, dominios_aceitos=DOMINIOS_ACEITOS):
    """[(linha, tipo, trecho)] de tudo o que o texto tem além de nomes próprios."""
    achados = []
    for numero, linha in enumerate(texto.splitlines(), 1):
        for tipo, detector in DETECTORES:
            achados += [(numero, tipo, trecho) for trecho in detector(linha, dominios_aceitos)]
    return achados


@functools.cache
def _padrao_dos_nomes(nomes):
    alternativas = "|".join(re.escape(nome) for nome in sorted(nomes, key=len, reverse=True))
    return re.compile(r"(?<!\w)(?:" + alternativas + r")(?!\w)") if nomes else None


def _sem_nomes_aceitos(linha, nomes):
    """A linha com cada nome aceito trocado por letras minúsculas do mesmo tamanho (o resto fica na mesma posição)."""
    padrao = _padrao_dos_nomes(nomes)
    return padrao.sub(lambda m: "x" * len(m.group(0)), linha) if padrao else linha


def _abre_frase(antes):
    """True se o que vem antes é o começo da linha, de uma frase, de uma célula de tabela ou de um item de lista."""
    resto = re.sub(r"[\s*_`\"“«(]+$", "", antes)
    return resto == "" or resto[-1] in ".!?:|" or bool(re.fullmatch(r"[\s#>\-+*\d.)]*", resto))


def _e_opcao_de_comando(linha, palavra, inicio):
    """O `-` seguido de uma letra só, dentro de crases (`-S`): opção de comando, não nome."""
    em_crases = any(m.start() < inicio < m.end() for m in CRASES.finditer(linha))
    return len(palavra) == 1 and em_crases and linha[inicio - 1:inicio] == "-"


def nomes_no_texto(texto, palavras_aceitas):
    """[(linha, 'nome próprio', palavra)]: maiúscula (Unicode) que não é palavra comum de início de frase nem nome aceito."""
    comuns, nomes = palavras_aceitas
    achados = []
    for numero, linha in enumerate(texto.splitlines(), 1):
        limpa = _sem_nomes_aceitos(linha, nomes)  # as crases não isentam nada: cada pedaço de um caminho é conferido
        for m in PALAVRA.finditer(limpa):
            palavra = m.group(0)
            if palavra[0].isupper() and not (palavra.lower() in comuns and _abre_frase(limpa[:m.start()])) \
                    and not _e_opcao_de_comando(linha, palavra, m.start()):
                achados.append((numero, "nome próprio", palavra))
    return achados


def dados_no_texto(texto, palavras_aceitas, dominios_aceitos=DOMINIOS_ACEITOS):
    """Todos os dados do texto, por linha: `palavras_aceitas` é (comuns em minúsculas, nomes aceitos)."""
    achados = dados_fora_nomes(texto, dominios_aceitos) + nomes_no_texto(texto, palavras_aceitas)
    return sorted(achados, key=lambda achado: achado[0])


def _guardar_palavra(linha, secao, comuns, nomes):
    """Guarda a linha na parte certa; devolve o erro, ou None."""
    nome, _, categoria = (parte.strip() for parte in linha.partition("|"))
    if secao == "comuns" and categoria == "" and " " not in nome and "|" not in linha:
        comuns.add(nome.lower())
    elif secao == "nomes" and nome and categoria in CATEGORIAS:
        nomes.add(nome)
    elif secao is None:
        return f"«{linha}» está fora de uma parte (## comuns ou ## nomes)"
    else:
        return f"«{linha}» é inválida (comuns: uma palavra; nomes: «nome | {'/'.join(CATEGORIAS)}»)"
    return None


@functools.cache
def ler_palavras(texto):
    """(comuns em minúsculas, nomes, erros) do arquivo de palavras com maiúscula, em duas partes (## comuns, ## nomes)."""
    comuns, nomes, erros, secao = set(), set(), [], None
    for numero, bruta in enumerate(texto.lstrip("﻿").splitlines(), 1):
        linha = bruta.strip()
        if linha.startswith("## "):
            secao = linha[3:].strip()
            erros += [f"linha {numero}: a parte «{secao}» não existe (use comuns ou nomes)"] * (secao not in SECOES)
        elif linha and not linha.startswith("#"):
            erro = _guardar_palavra(linha, secao, comuns, nomes)
            erros += [f"linha {numero}: {erro}"] * bool(erro)
    return frozenset(comuns), frozenset(nomes), tuple(erros)


def compilar_termo(termo):
    """O termo da lista negra como expressão do Python, ou None se o hook (grep -E) o entende e o Python não."""
    if CLASSE_POSIX.search(termo) or SO_DO_GREP.search(termo):
        return None
    try:
        return re.compile(termo, re.IGNORECASE)
    except re.error:
        return None


def termos_que_nao_compilam(termos):
    """Os números (a partir de 1) dos termos que o teste não consegue casar: nunca se saltam em silêncio."""
    return [numero for numero, termo in enumerate(termos, 1) if compilar_termo(termo) is None]


def termos_no_texto(texto, termos):
    """[(linha, 'lista negra', 'termo n.º N')] com a semântica do hook: cada termo é uma expressão, sem fronteira."""
    achados = []
    for numero, termo in enumerate(termos, 1):
        padrao = compilar_termo(termo)
        if padrao:
            achados += [(n, "lista negra", f"termo n.º {numero}") for n, l in enumerate(texto.splitlines(), 1)
                        if padrao.search(l)]
    return achados


def mensagem(origem, achado, ambiente=os.environ):
    """«arquivo:linha: tipo»; fora do CI, com o trecho para quem corrige. O termo da lista negra nunca se mostra."""
    linha, tipo, trecho = achado
    com_trecho = ambiente.get("CI") != "true" or tipo == "lista negra"
    return f"{origem}:{linha}: {tipo}" + (f" — {trecho}" if com_trecho else "")


def _git(raiz, *argumentos):
    execucao = subprocess.run(["git", *argumentos], cwd=raiz, capture_output=True, check=False)
    return execucao.returncode, execucao.stdout.decode("utf-8", errors="replace").removeprefix("﻿")


def _nomes_da_saida(saida):
    return [caminho for caminho in saida.split("\0") if caminho]


def _do_indice(raiz):
    """O que está preparado (git add), lido do índice e não do disco: apagar só do disco não esconde nada."""
    mudados = _nomes_da_saida(_git(raiz, "diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR", "--", PASTA, PALAVRAS)[1])
    if PALAVRAS in mudados:  # a lista mudou: o catálogo todo é relido com ela
        mudados += [c for c in _nomes_da_saida(_git(raiz, "ls-files", "-z", "--", PASTA)[1]) if c not in mudados]
    palavras = _git(raiz, "show", ":" + PALAVRAS)[1]
    return [Conteudo(f"{c} (preparado)", _git(raiz, "show", ":" + c)[1], palavras, c == PALAVRAS, c)
            for c in mudados]


def _commits_do_intervalo(raiz, base):
    """Os commits do intervalo `base..HEAD` que mexem na pasta ou na lista; sem base utilizável, todos os da história."""
    alvo = ["HEAD"] if re.fullmatch("0*", base) else [f"{base}..HEAD"]
    codigo, saida = _git(raiz, "rev-list", *alvo, "--", PASTA, PALAVRAS)
    if codigo != 0:
        saida = _git(raiz, "rev-list", "HEAD", "--", PASTA, PALAVRAS)[1]
    return saida.split()


def _de_um_commit(raiz, commit, palavras_da_ponta):
    """Os arquivos do commit, julgados com a lista de palavras da ponta (a que vale hoje): a lista que o commit tinha
    pode ser mais velha que a barreira. Sem lista na ponta, vale a do próprio commit."""
    palavras = palavras_da_ponta or _git(raiz, "show", f"{commit}:{PALAVRAS}")[1]
    nomes = _nomes_da_saida(_git(raiz, "ls-tree", "-r", "-z", "--name-only", commit, "--", PASTA, PALAVRAS)[1])
    return [Conteudo(f"{n} (commit {commit[:7]})", _git(raiz, "show", f"{commit}:{n}")[1], palavras, n == PALAVRAS, n)
            for n in nomes]


def _da_arvore(raiz):
    """A árvore commitada mais os arquivos novos que o .gitignore não esconde, lidos do disco."""
    saida = _git(raiz, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", PASTA, PALAVRAS)[1]
    arquivos = [c for c in _nomes_da_saida(saida) if (raiz / c).is_file()]
    palavras = (raiz / PALAVRAS).read_text(encoding="utf-8-sig") if (raiz / PALAVRAS).is_file() else ""
    return [Conteudo(c, (raiz / c).read_text(encoding="utf-8-sig", errors="replace"), palavras, c == PALAVRAS, c)
            for c in arquivos]


def conteudos_a_verificar(raiz, ambiente=os.environ):
    """O que o teste lê: o índice no pre-commit (MORG_LER_DO_INDICE=1), os commits do intervalo no CI
    (MORG_BASE_DE_COMPARACAO) e a árvore quando se roda à mão."""
    if ambiente.get("MORG_LER_DO_INDICE") == "1":
        return _do_indice(raiz)
    if ambiente.get("MORG_BASE_DE_COMPARACAO"):
        da_ponta = _git(raiz, "show", f"HEAD:{PALAVRAS}")[1]  # vazia se a ponta não tem a lista
        return [c for commit in _commits_do_intervalo(raiz, ambiente["MORG_BASE_DE_COMPARACAO"])
                for c in _de_um_commit(raiz, commit, da_ponta)]
    return _da_arvore(raiz)


def problemas(conteudos, termos, ambiente=os.environ):
    """As mensagens de tudo o que não pode estar no catálogo; vazia se estiver limpo."""
    mensagens = [f"lista negra: o termo n.º {n} não compila em Python (classe POSIX ou sintaxe só do grep -E); reescreva-o"
                 for n in termos_que_nao_compilam(termos)]
    for c in conteudos:
        if not (c.e_lista or c.caminho.lower().endswith(".md")):  # um pdf ou png não se lê: não entra
            mensagens.append(f"{c.origem}: só arquivos .md entram em {PASTA}/")
            continue
        comuns, nomes, erros = ler_palavras(c.palavras)
        mensagens += [f"{PALAVRAS}: {erro}" for erro in erros]
        achados = dados_fora_nomes(c.texto) if c.e_lista else dados_no_texto(c.texto, (comuns, nomes))
        mensagens += [mensagem(c.origem, achado, ambiente) for achado in achados + termos_no_texto(c.texto, termos)]
    return list(dict.fromkeys(mensagens))


ARQUIVOS_DE_CADA_PROJETO = ("README.md", "modulos-e-fluxos.md", "regras-e-incidentes.md", "o-que-se-mediu.md")
LIMITE_DE_LINHAS = 500
LINHA_DA_TABELA = re.compile(r"^\|\s*\[([\w-]+)\]\(", re.MULTILINE)


def erros_da_estrutura(raiz):
    """A tabela do `projetos/README.md` e as pastas batem; cada pasta tem os quatro arquivos, de até 500 linhas."""
    pasta = raiz / PASTA
    if not (pasta / "README.md").is_file():
        return [f"falta {PASTA}/README.md"]
    tabela = sorted(LINHA_DA_TABELA.findall((pasta / "README.md").read_text(encoding="utf-8-sig")))
    projetos = sorted(p.name for p in pasta.iterdir() if p.is_dir())
    erros = [] if tabela == projetos else [f"a tabela do README lista {tabela} e as pastas são {projetos}"]
    for projeto in projetos:
        for nome in ARQUIVOS_DE_CADA_PROJETO:
            arquivo = pasta / projeto / nome
            linhas = len(arquivo.read_text(encoding="utf-8-sig").splitlines()) if arquivo.is_file() else None
            erros += [f"falta {PASTA}/{projeto}/{nome}"] * (linhas is None)
            erros += [f"{PASTA}/{projeto}/{nome} tem {linhas} linhas (máximo {LIMITE_DE_LINHAS})"] * bool(
                linhas and linhas > LIMITE_DE_LINHAS)
    return erros
