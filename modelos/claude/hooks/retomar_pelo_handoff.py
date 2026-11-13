"""Hook SessionStart (matcher `compact`): depois de compactar, manda o agente ler o handoff deste assunto.

Lista os `.context/HANDOFF-*.md` da raiz do git (ou do `cwd`, sem git), com a data do último commit de cada, ou a
hora do arquivo quando ele não tem commit (a pasta ignorada). Não escolhe o arquivo: com várias sessões na mesma
pasta, o mais recente pode ser de outra; o texto manda perguntar. Sem handoff, não diz nada.
O texto não diz «continue»: diz «leia o handoff» (depois de uma pausa longa, o certo é uma sessão nova).
Nunca bloqueia: sai com 0 e põe o texto no `additionalContext` do agente.
Instalar: copiar para `.claude/hooks/` do projeto e ligar no `.claude/settings.json` (modelo ao lado).
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

TEXTO_DA_RETOMADA = (
    "A conversa foi compactada. Antes de seguir, leia o .context/HANDOFF-<assunto>.md deste assunto (existem: "
    "{lista}); os outros são de outros assuntos e não se tocam. Rode `git status -s` e compare com o «Estado "
    "verificado». Se não souber qual é o assunto, pergunte."
)


def git_da_retomada(pasta, *argumentos):
    """Roda o git na pasta; devolve o stdout sem espaços nas pontas, ou "" se falhar ou não houver git."""
    try:
        resultado = subprocess.run(["git", "-C", str(pasta), *argumentos], capture_output=True, text=True,
                                   encoding="utf-8", check=False, timeout=10)
    except OSError:
        return ""
    return resultado.stdout.strip() if resultado.returncode == 0 else ""


def quando_mudou(caminho, raiz):
    """A data do último commit do arquivo, ou a hora do arquivo se ele não tem commit."""
    commit = git_da_retomada(raiz, "log", "-1", "--format=%cd", "--date=format-local:%Y-%m-%d %H:%M", "--", caminho.name)
    if commit:
        return f"último commit {commit}"
    return "sem commit; arquivo de " + datetime.fromtimestamp(caminho.stat().st_mtime).strftime("%Y-%m-%d %H:%M")


def texto_da_retomada(cwd):
    """O texto para o agente, ou None se não houver handoff."""
    raiz = Path(git_da_retomada(cwd, "rev-parse", "--show-toplevel") or cwd)
    pasta = raiz / ".context"
    handoffs = sorted(pasta.glob("HANDOFF-*.md"))
    if not handoffs:
        return None
    lista = "; ".join(f".context/{caminho.name} ({quando_mudou(caminho, pasta)})" for caminho in handoffs)
    return TEXTO_DA_RETOMADA.format(lista=lista)


def main():
    # Bytes em UTF-8: no Windows o stdin de texto usaria a página de código local e estragaria os acentos.
    pedido = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    if pedido.get("source") != "compact":
        return
    texto = texto_da_retomada(Path(pedido.get("cwd") or "."))
    if texto:
        saida = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": texto}}
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(json.dumps(saida, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
