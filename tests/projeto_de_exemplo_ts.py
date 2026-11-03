"""Monta, numa pasta temporária, o projeto de exemplo TypeScript (tests/exemplo-ts/) com os moldes de
modelos/testes-ts/ em tests/catracas/, num repositório git com identidade fictícia, e roda o vitest e o tsc.

As dependências instalam-se uma vez em tests/exemplo-ts/ (`npm ci`, que o scripts/testar.sh roda). A pasta temporária
liga-se ao node_modules de lá (junção no Windows, link simbólico no resto); `apagar_ts` desfaz a ligação antes de
apagar a pasta, para nunca apagar o que está do outro lado.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from carregar_modelos import MODELOS, RAIZ
from projeto_de_exemplo import apagar, escrever, git

EXEMPLO_TS = RAIZ / "tests" / "exemplo-ts"
MOLDES_TS = MODELOS / "testes-ts"
TOTAL_DO_PEDIDO_TS = ("export function totalDoPedido(itens: number[]): number {\n"
                      "    return itens.reduce((soma, item) => soma + item, 0)\n}\n")


def ligar_node_modules(pasta):
    alvo, ligacao = EXEMPLO_TS / "node_modules", pasta / "node_modules"
    if not (alvo / "vitest").is_dir():
        raise RuntimeError("falta o node_modules do exemplo: rode `npm ci` em tests/exemplo-ts")
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "mklink", "/J", str(ligacao), str(alvo)], check=True, capture_output=True)
    else:
        ligacao.symlink_to(alvo, target_is_directory=True)


def apagar_ts(pasta):
    """Tira a ligação ao node_modules (só a ligação) e apaga a pasta temporária."""
    ligacao = pasta / "node_modules"
    if os.path.lexists(ligacao):
        os.rmdir(ligacao) if os.name == "nt" else ligacao.unlink()
    if os.path.lexists(ligacao):
        raise RuntimeError(f"a ligação {ligacao} não saiu: a pasta fica por apagar, à mão")
    apagar(pasta)


def iniciar_git(pasta):
    git(pasta, "init", "-q")
    for chave, valor in (("user.email", "1+ana@users.noreply.github.com"), ("user.name", "Ana"),
                         ("core.autocrlf", "false"), ("morg.listaNegra", "")):
        git(pasta, "config", "--local", chave, valor)
    git(pasta, "add", "--", ".")


def montar_ts():
    """Cria o projeto de exemplo TypeScript e devolve a pasta (apague-a com `apagar_ts`)."""
    pasta = Path(tempfile.mkdtemp(prefix="morg-exemplo-ts-"))
    for nome in ("package.json", "package-lock.json", "tsconfig.json"):
        shutil.copy2(EXEMPLO_TS / nome, pasta / nome)
    shutil.copytree(MOLDES_TS, pasta / "tests" / "catracas")
    ligar_node_modules(pasta)
    escrever(pasta / ".gitignore", "node_modules\n")
    escrever(pasta / "src" / "total-do-pedido.ts", TOTAL_DO_PEDIDO_TS)
    iniciar_git(pasta)
    return pasta


def rodar_node(pasta, *argumentos):
    """Roda o node com `argumentos` na pasta; devolve (código de saída, stdout e stderr juntos)."""
    ambiente = {**os.environ, "NO_COLOR": "1", "FORCE_COLOR": "0"}
    resultado = subprocess.run([shutil.which("node"), *argumentos], cwd=pasta, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", check=False, timeout=300, env=ambiente)
    return resultado.returncode, resultado.stdout + resultado.stderr


def rodar_vitest(pasta, *filtros):
    """Roda os moldes TypeScript (ou só os arquivos que `filtros` pedirem) com o vitest do exemplo."""
    return rodar_node(pasta, "node_modules/vitest/vitest.mjs", "run", *filtros)


def rodar_tsc(pasta):
    """Confere os tipos dos moldes com o tsconfig estrito do exemplo."""
    return rodar_node(pasta, "node_modules/typescript/bin/tsc", "--noEmit", "-p", ".")
