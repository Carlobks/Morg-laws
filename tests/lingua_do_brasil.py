"""A lista curta de palavras e construções do português de Portugal, uma só para os testes do Morg-laws.

Seis formas têm fronteira própria (`FORMAS_DE_PORTUGAL_COM_FRONTEIRA`): «noutro», «píxel», «secção», «arrastar e
largar», «a meio» e «na consola». Cada uma deixa passar o que existe no Brasil («meio a meio», «a meio mastro», «a meio
caminho», «ela consola o amigo»). Custo conhecido: o pronome antes do verbo consolar («a mãe a consola») também é
acusado; é raro num texto técnico. `estagiar` e `arrancar` ficaram de fora porque existem no Brasil, e `corre`,
`correm` e `correr` também («para correr» passa).

`SALTAR_E_REGISTAR` pega «saltar» e «registar» em todas as formas do verbo («saltou», «saltando», «saltá-lo»,
«registado»…), menos «salta» e «saltas», que já estão em `PALAVRAS_DE_PORTUGAL`. Custo conhecido: "saltar" no
sentido de pulo físico ("saltar do ônibus") também é acusado; num texto técnico, escreva "pular" ou "descer"; uma
citação entra em `EXCECOES_DE_LINGUA`."""

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

# «saltar» e «registar» em todas as formas do verbo; «salta» e «saltas» já estão em PALAVRAS_DE_PORTUGAL. O
# sublinhado não é fronteira (`SALTA_SEMPRE` e `saltar_teste` passam: os nomes com sublinhado ficam com a
# revisão), e depois de um hífen também passa: é o nome velho da regra,
# `testes-saltados`, que o passo de migração cita (OsNomesVelhosDaRegraNaoVoltam o prende ao passo). «Salto» e
# «saltos» existem no Brasil e ficam de fora. Custo conhecido: "saltar" no sentido de pulo físico ("saltar do
# ônibus") também é acusado; num texto técnico, escreva "pular" ou "descer"; uma citação entra em EXCECOES_DE_LINGUA.
SALTAR_E_REGISTAR = re.compile(
    r"(?<!-)\bsalt(?:a(?!s?\b)[^\W_]*|á[^\W_]*|e|es|em|ei|emos|eis|ou)\b"
    r"|\bregist(?:a[^\W_]*|á[^\W_]*|e|es|em|ei|emos|eis|ou)\b", re.IGNORECASE)


def erros_de_lingua(nome, texto):
    """Palavras e construções do português de Portugal num arquivo, uma mensagem por achado."""
    erros = []
    for padrao in (PALAVRAS_DE_PORTUGAL, PREFIXOS_DE_PORTUGAL, CONSTRUCOES_DE_PORTUGAL, FORMAS_DE_PORTUGAL_COM_FRONTEIRA,
                   SALTAR_E_REGISTAR):
        erros += [f"{nome}: «{achado.group()}» é do português de Portugal; escreva em português do Brasil"
                  for achado in padrao.finditer(texto)]
    return erros
