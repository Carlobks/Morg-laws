"""A lista curta de palavras e construções do português de Portugal, uma só para os testes do Morg-laws.

Seis formas têm fronteira própria (`FORMAS_DE_PORTUGAL_COM_FRONTEIRA`): «noutro», «píxel», «secção», «arrastar e
largar», «a meio» e «na consola». Cada uma deixa passar o que existe no Brasil («meio a meio», «a meio mastro», «a meio
caminho», «ela consola o amigo»). Custo conhecido: o pronome antes do verbo consolar («a mãe a consola») também é
acusado; é raro num texto técnico. `estagiar` e `arrancar` ficaram de fora porque existem no Brasil, e `corre`,
`correm` e `correr` também («para correr» passa)."""

import re

PALAVRAS_DE_PORTUGAL = re.compile(
    r"\b(?:ficheiro|registo|ecrã|utilizador|equipa|telemóvel|facto|artefacto|contacto|omissão|salta)s?\b",
    re.IGNORECASE)
PREFIXOS_DE_PORTUGAL = re.compile(r"\bpartilh\w*", re.IGNORECASE)
CONSTRUCOES_DE_PORTUGAL = re.compile(
    r"\b(?:continua|continuam|está|estão|fica|ficam|anda|andam)\s+a\s+(?:ver|fazer|falhar|correr|esperar)\b"
    r"|\w+-(?:lo|la|los|las|se|lhe|lhes|me|te|nos|vos)-(?:ei|ás|á|emos|ão|ia|ias|íamos|iam)\b", re.IGNORECASE)
FORMAS_DE_PORTUGAL_COM_FRONTEIRA = re.compile(
    r"\bnoutr[ao]s?\b"
    r"|\bpíxe(?:l|is)\b"
    r"|\bsecç(?:ão|ões)\b"
    r"|\barrastar e largar\b"
    r"|(?<!meio )\ba meio\b(?! caminho| mastro| pau|-)"
    r"|\b(?:a|à|na|nas|da|das|numa|pela|uma)\s+consolas?\b", re.IGNORECASE)


def erros_de_lingua(nome, texto):
    """Palavras e construções do português de Portugal num arquivo, uma mensagem por achado."""
    erros = []
    for padrao in (PALAVRAS_DE_PORTUGAL, PREFIXOS_DE_PORTUGAL, CONSTRUCOES_DE_PORTUGAL, FORMAS_DE_PORTUGAL_COM_FRONTEIRA):
        erros += [f"{nome}: «{achado.group()}» é do português de Portugal; escreva em português do Brasil"
                  for achado in padrao.finditer(texto)]
    return erros
