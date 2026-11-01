"""Carrega pelo caminho os modelos em Python do Morg-laws (hooks do agente e portões do git) para os testes.

Usa o próprio modelo `modelos/testes/carregar_por_caminho.py`, que assim também fica provado.
"""

import importlib.util
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELOS = RAIZ / "modelos"
PASTA_HOOKS = MODELOS / "claude" / "hooks"
PASTA_PORTOES = MODELOS / "git" / "portoes"
PASTA_HOOKS_DO_GIT = MODELOS / "git" / "hooks"
PASTA_TESTES_MODELO = MODELOS / "testes"

_especificacao = importlib.util.spec_from_file_location("carregar_por_caminho_modelo",
                                                        PASTA_TESTES_MODELO / "carregar_por_caminho.py")
_ajudante = importlib.util.module_from_spec(_especificacao)
_especificacao.loader.exec_module(_ajudante)
carregar = _ajudante.carregar
correr_como_script = _ajudante.correr_como_script


def carregar_hook(nome):
    """Importa modelos/claude/hooks/<nome>.py como módulo."""
    return carregar(PASTA_HOOKS / f"{nome}.py", f"hook_{nome}")


def carregar_portao(nome):
    """Importa modelos/git/portoes/<nome>.py como módulo."""
    return carregar(PASTA_PORTOES / f"{nome}.py", f"portao_{nome}")
