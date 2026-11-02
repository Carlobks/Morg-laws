"""Carrega e roda pelo caminho os scripts que não estão num pacote (portões do git, hooks do Claude Code).

`correr_como_script` roda o script como `__main__` dentro do processo de teste: conta na cobertura, o que um
subprocesso não faz. Rode os dois: o subprocesso prova o `python -I` real; este, as linhas.
Instalar: copiar para `tests/` do projeto.
"""

import importlib.util
import io
import runpy
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

RAIZ = Path(__file__).resolve().parent.parent


def carregar(caminho, nome):
    """Importa o arquivo `caminho` como um módulo chamado `nome`."""
    especificacao = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(especificacao)
    especificacao.loader.exec_module(modulo)
    return modulo


def correr_como_script(caminho, entrada, argv=None):
    """Roda o script como __main__ neste processo, com `entrada` (bytes) no stdin e `argv` opcional.

    Devolve (código de saída, stdout, stderr); o código é 0 se o script acabar sem sys.exit. Cuidado: o que o
    script instala no processo (um gancho global de exceções, por exemplo) fica; desfaça-o no fim do teste.
    """
    saida = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
    erro = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
    codigo = 0
    with mock.patch("sys.stdin", SimpleNamespace(buffer=io.BytesIO(entrada))), \
            mock.patch("sys.stdout", saida), mock.patch("sys.stderr", erro), \
            mock.patch("sys.argv", [str(caminho), *(argv or [])]):
        try:
            runpy.run_path(str(caminho), run_name="__main__")
        except SystemExit as fim:
            codigo = fim.code
        saida.flush()
        erro.flush()
    return codigo, saida.buffer.getvalue().decode("utf-8"), erro.buffer.getvalue().decode("utf-8")
