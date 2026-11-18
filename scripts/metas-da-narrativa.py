"""As metas da narrativa do livro novo: só avisam, nunca reprovam (sai sempre com 0). Corre no `pre-commit`, depois dos testes.

Lê os capítulos novos (`manual/cap-NN-*.md`) e imprime um aviso por meta falhada:
A1 · 1.ª pessoa (eu, meu, meus, minha, minhas, comigo) por mil palavras abaixo de 5 (o livro de referência tem 9,6);
A2 · a 1.ª frase do capítulo sem mês ou ano e sem 1.ª pessoa (o episódio do autor);
A3 · capítulo sem nenhuma frase-síntese em destaque (uma citação `>`);
A4 · capítulo com menos de 3 páginas estimadas ou com mais de 3 vezes a média (321 palavras por página, 2 páginas por par)."""

import re
import sys
from pathlib import Path

PRIMEIRA_PESSOA = re.compile(r"\b(?:eu|meu|meus|minha|minhas|comigo)\b", re.IGNORECASE)
MES_OU_ANO = re.compile(r"\b(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\b"
                        r"|\b(?:19|20)\d\d\b", re.IGNORECASE)
MARCA_DE_PAR = re.compile(r"\s*<!--\s*raw-typst\s+#marca-de-par\(\)\s*-->\s*")
PALAVRAS_POR_PAGINA = 321
META_DE_PRIMEIRA_PESSOA = 5
MINIMO_DE_PAGINAS = 3
VEZES_A_MEDIA = 3


def prosa(texto):
    """As linhas fora dos blocos de código e fora do marcador de par."""
    saida, no_codigo = [], False
    for linha in texto.splitlines():
        if linha.lstrip().startswith(("```", "~~~")):
            no_codigo = not no_codigo
        elif not no_codigo and not MARCA_DE_PAR.fullmatch(linha):
            saida.append(linha)
    return saida


def primeira_frase(linhas):
    """A 1.ª frase do 1.º parágrafo de prosa corrida (nem título nem citação nem lista)."""
    for linha in linhas:
        if linha.strip() and not linha.lstrip().startswith(("#", ">", "-", "*", "|", "!", "<")):
            return re.split(r"(?<=[.!?])\s", linha.strip(), maxsplit=1)[0]
    return ""


def paginas_estimadas(linhas):
    """Palavras de prosa fora dos pares (321 por página) mais 2 páginas por par (cada `## ` depois do marcador)."""
    pares = sum(1 for i, linha in enumerate(linhas) if MARCA_DE_PAR.fullmatch(linha))
    palavras = len(" ".join(prosa("\n".join(linhas))).split())
    return palavras / PALAVRAS_POR_PAGINA + 2 * pares


def avisos_de_um_capitulo(nome, texto):
    """A1, A2 e A3 de um capítulo."""
    avisos, linhas = [], prosa(texto)
    palavras = len(" ".join(linhas).split())
    por_mil = len(PRIMEIRA_PESSOA.findall("\n".join(linhas))) * 1000 / palavras if palavras else 0
    if por_mil < META_DE_PRIMEIRA_PESSOA:
        avisos.append(f"A1 {nome}: {por_mil:.1f} marcas de 1.ª pessoa por mil palavras (meta {META_DE_PRIMEIRA_PESSOA})")
    frase = primeira_frase(linhas)
    if not MES_OU_ANO.search(frase) and not PRIMEIRA_PESSOA.search(frase):
        avisos.append(f"A2 {nome}: a 1.ª frase não tem mês/ano nem o episódio do autor — «{frase[:50]}»")
    if not any(linha.lstrip().startswith(">") for linha in linhas):
        avisos.append(f"A3 {nome}: nenhuma frase-síntese em destaque (uma citação `>`)")
    return avisos


def avisos_de_paginas(paginas):
    """A4: `paginas` é {nome: páginas estimadas}."""
    avisos, media = [], sum(paginas.values()) / len(paginas) if paginas else 0
    for nome, estimadas in sorted(paginas.items()):
        if estimadas < MINIMO_DE_PAGINAS:
            avisos.append(f"A4 {nome}: {estimadas:.1f} páginas estimadas (mínimo {MINIMO_DE_PAGINAS})")
        elif estimadas > VEZES_A_MEDIA * media:
            avisos.append(f"A4 {nome}: {estimadas:.1f} páginas estimadas, mais de {VEZES_A_MEDIA} vezes a média ({media:.1f})")
    return avisos


def avisos_dos_capitulos(capitulos):
    """`capitulos` é {nome: texto}; devolve a lista de avisos (vazia se nenhuma meta falha)."""
    avisos = [a for nome, texto in sorted(capitulos.items()) for a in avisos_de_um_capitulo(nome, texto)]
    return avisos + avisos_de_paginas({nome: paginas_estimadas(texto.splitlines()) for nome, texto in capitulos.items()})


def principal(raiz):
    capitulos = {c.name: c.read_text(encoding="utf-8-sig") for c in sorted((raiz / "manual").glob("cap-[0-9][0-9]-*.md"))}
    avisos = avisos_dos_capitulos(capitulos)
    print(f"metas da narrativa: {len(capitulos)} capítulos novos, {len(avisos)} avisos (só avisam, não reprovam)")
    for aviso in avisos:
        print("AVISO", aviso)
    return 0


if __name__ == "__main__":
    try:
        principal(Path(__file__).resolve().parent.parent)
    except Exception as erro:  # as metas só avisam: nem um erro delas barra o commit
        print(f"AVISO as metas da narrativa não correram: {erro}")
    sys.exit(0)
