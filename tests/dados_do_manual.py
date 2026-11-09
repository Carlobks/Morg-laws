"""O detector de dados do manual de uso (`manual/`): nada que identifique pessoas ou empresas entra nos `.md` dele.

Chama os detectores de `dados_do_catalogo.py` (caminho, e-mail, documento, IBAN, UUID, hash, ID de serviço, domínio,
dinheiro) e a lista negra local, sem mudar aquele módulo. Não usa a regra das palavras com maiúscula: aceita como
domínios os endereços do `FONTES.md`, não acusa palavra comum com maiúscula e acusa como possível nome de pessoa duas
palavras seguidas com maiúscula, fora do início de frase, que não estejam em `manual/pessoas-citaveis.txt` nem na parte
`nomes` de `tests/palavras-com-maiuscula.txt`. Um nome de uma palavra só fica com a lista negra. O alvo de um link
`[texto](endereço)` não se confere aqui: o `FONTES.md` e o lychee já o conferem. Nomes de arquivo, sempre em crases.
O CI não vê a lista negra, que vive fora do repositório: lá, a barreira do manual é só este detector."""

import os
import re
import subprocess
from collections import namedtuple
from urllib.parse import urlsplit

import dados_do_catalogo as catalogo

PASTA = "manual"
PESSOAS = "manual/pessoas-citaveis.txt"
FONTES = "FONTES.md"
Conteudo = namedtuple("Conteudo", "origem texto")
ALVO_DE_LINK = re.compile(r"\]\([^)\s]*\)")
ENDERECO = re.compile(r"https?://[^\s<>()\[\]`\"'*|]+", re.IGNORECASE)
SEQUENCIA = re.compile(r"(?<![\w-])[A-ZÀ-Ý][\wà-ÿ'’-]+(?:[  ]+[A-ZÀ-Ý][\wà-ÿ'’-]+)+")
DICA_DE_ARQUIVO = "domínio (se for nome de arquivo, ponha em crases)"


def pessoas_citaveis(texto):
    """Os nomes do arquivo da lista: um por linha; a linha em branco e o comentário (#) não contam."""
    linhas = (linha.strip() for linha in texto.lstrip("﻿").splitlines())
    return frozenset(linha for linha in linhas if linha and not linha.startswith("#"))


def dominios_do_fontes(texto):
    """Os domínios dos endereços do FONTES.md, mais os que o catálogo já aceita."""
    enderecos = (urlsplit(endereco.rstrip(".,;:!?»")).hostname for endereco in ENDERECO.findall(texto))
    return catalogo.DOMINIOS_ACEITOS | {dominio for dominio in enderecos if dominio}


def sem_o_aceito(corrida, aceitos):
    """A corrida de palavras sem cada nome aceito (o mais longo primeiro); o que sobra é o que ninguém aceitou."""
    for nome in sorted(aceitos, key=len, reverse=True):
        corrida = re.sub(r"(?<!\w)" + re.escape(nome) + r"(?!\w)", " ", corrida)
    return corrida.split()


def nomes_de_pessoas(texto, aceitos):
    """[(linha, 'nome de pessoa', trecho)]: duas ou mais palavras com maiúscula, fora do início de frase, não aceitas."""
    achados = []
    for numero, linha in enumerate(texto.splitlines(), 1):
        for corrida in SEQUENCIA.finditer(linha):
            palavras = corrida.group(0).split()
            palavras = palavras[1:] if catalogo._abre_frase(linha[:corrida.start()]) else palavras
            if len(palavras) >= 2 and sem_o_aceito(" ".join(palavras), aceitos):
                achados.append((numero, "nome de pessoa", " ".join(palavras)))
    return achados


def dados_do_manual(texto, aceitos, dominios):
    """Todos os dados do texto por linha: o que o catálogo detecta, com o domínio dos arquivos explicado, e os nomes."""
    limpo = ALVO_DE_LINK.sub("]", texto)
    fora_nomes = [(n, DICA_DE_ARQUIVO if tipo == "domínio" else tipo, t)
                  for n, tipo, t in catalogo.dados_fora_nomes(limpo, dominios)]
    return sorted(fora_nomes + nomes_de_pessoas(limpo, aceitos), key=lambda achado: achado[0])


def problemas(conteudos, situacao, termos, ambiente=os.environ):
    """As mensagens de tudo o que não pode estar no manual; vazia se estiver limpo."""
    aceitos, dominios = situacao
    mensagens = [f"lista negra: o termo n.º {n} não compila em Python (classe POSIX ou sintaxe só do grep -E); reescreva-o"
                 for n in catalogo.termos_que_nao_compilam(termos)]
    for c in conteudos:
        achados = dados_do_manual(c.texto, aceitos, dominios) + catalogo.termos_no_texto(c.texto, termos)
        mensagens += [catalogo.mensagem(c.origem, achado, ambiente) for achado in achados]
    return list(dict.fromkeys(mensagens))


def _saida_git(raiz, *argumentos):
    execucao = subprocess.run(["git", *argumentos], cwd=raiz, capture_output=True, check=False)
    return execucao.stdout.decode("utf-8", errors="replace").removeprefix("﻿")


def _nomes_dos_md(saida):
    nomes = (nome for nome in saida.split("\0") if nome)
    return [nome for nome in nomes if nome.startswith(PASTA + "/") and nome.lower().endswith(".md")]


def ler_do_indice(raiz, caminho):
    return _saida_git(raiz, "show", ":" + caminho)


def ler_do_disco(raiz, caminho):
    arquivo = raiz / caminho
    return arquivo.read_text(encoding="utf-8-sig", errors="replace") if arquivo.is_file() else ""


def md_do_indice(raiz):
    """Os `.md` preparados de `manual/`; se a lista de pessoas, o FONTES.md ou a lista pública mudou, todos."""
    mudados = _saida_git(raiz, "diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR", "--",
                         PASTA, FONTES, catalogo.PALAVRAS)
    todos = _saida_git(raiz, "ls-files", "-z", "--", PASTA)
    relido = any(c in mudados.split("\0") for c in (PESSOAS, FONTES, catalogo.PALAVRAS))
    return _nomes_dos_md(todos if relido else mudados)


def md_do_disco(raiz):
    """A árvore commitada mais os arquivos novos que o .gitignore não esconde, lidos do disco."""
    return _nomes_dos_md(_saida_git(raiz, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", PASTA))


def situacao_do_manual(raiz, ambiente=os.environ):
    """([Conteudo], (nomes aceitos, domínios aceitos)): o índice no pre-commit (MORG_LER_DO_INDICE=1), o disco no resto."""
    ler, md = (ler_do_indice, md_do_indice) if ambiente.get("MORG_LER_DO_INDICE") == "1" else (ler_do_disco, md_do_disco)
    publicos = catalogo.ler_palavras(ler(raiz, catalogo.PALAVRAS))[1]
    aceitos = pessoas_citaveis(ler(raiz, PESSOAS)) | publicos
    conteudos = [Conteudo(nome, ler(raiz, nome)) for nome in md(raiz)]
    return conteudos, (aceitos, dominios_do_fontes(ler(raiz, FONTES)))
