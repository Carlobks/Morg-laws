"""A lista curta de palavras e construções do português de Portugal, uma só para os testes do Morg-laws."""

import re

PALAVRAS_DE_PORTUGAL = re.compile(
    r"\b(?:ficheiro|registo|ecrã|utilizador|equipa|telemóvel|facto|artefacto|contacto|omissão|salta)s?\b",
    re.IGNORECASE)
PREFIXOS_DE_PORTUGAL = re.compile(r"\bpartilh\w*", re.IGNORECASE)
CONSTRUCOES_DE_PORTUGAL = re.compile(
    r"\b(?:continua|continuam|está|estão|fica|ficam|anda|andam)\s+a\s+(?:ver|fazer|falhar|correr|esperar)\b"
    r"|\w+-(?:lo|la|los|las|se|lhe|lhes|me|te|nos|vos)-(?:ei|ás|á|emos|ão|ia|ias|íamos|iam)\b", re.IGNORECASE)


def erros_de_lingua(nome, texto):
    """Palavras e construções do português de Portugal num arquivo, uma mensagem por achado."""
    erros = []
    for padrao in (PALAVRAS_DE_PORTUGAL, PREFIXOS_DE_PORTUGAL, CONSTRUCOES_DE_PORTUGAL):
        erros += [f"{nome}: «{achado.group()}» é do português de Portugal; escreva em português do Brasil"
                  for achado in padrao.finditer(texto)]
    return erros
