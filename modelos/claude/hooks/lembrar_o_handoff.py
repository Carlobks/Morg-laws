"""Hook PreCompact (matcher `manual`): para o /compact manual que não aponta para um handoff gravado.

Passa se o texto do /compact cita um `.context/HANDOFF-<assunto>.md` que existe e está commitado, ou se traz a marca
de saída «sem handoff» (a compactação de uma conversa curta, de propósito). A compactação automática passa sempre.
Sem git, ou com a pasta ignorada, basta o arquivo existir; um handoff já rastreado conta como rastreado mesmo numa
pasta ignorada, logo tem de estar commitado. O caminho relativo resolve contra a raiz do git, não contra o `cwd`.
Sai com 2 para parar (o motivo no stderr, para o usuário); com 0 nos outros casos. Um hook quebrado sai com 1, e o
`"onFailure": "continue"` deixa compactar: só o bloqueio de propósito para.
Instalar: copiar para `.claude/hooks/` do projeto e ligar no `.claude/settings.json` (modelo ao lado).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

MARCA_DE_SAIDA = "sem handoff"
CITACAO_DE_HANDOFF = re.compile(r"[^\s`'\"«»()<>\[\]]*HANDOFF-[^\s`'\"«»()<>/]+\.md")
TEXTO_DA_PARADA = (
    "Compactação parada (Morg-laws): o /compact não aponta para um .context/HANDOFF-<assunto>.md gravado e "
    "commitado.\nGrave o handoff com a skill passando-o-trabalho e use o /compact que ela entrega. Se vai parar (fim "
    "do dia ou pausa de mais de uma hora), não compacte: grave o handoff e pare. Para compactar mesmo assim, ponha "
    "«sem handoff».\n"
)


def git_do_lembrete(pasta, *argumentos):
    """Roda o git na pasta; devolve o resultado, ou None se o git não existir."""
    try:
        return subprocess.run(["git", "-C", str(pasta), *argumentos], capture_output=True, text=True,
                              encoding="utf-8", check=False, timeout=10)
    except OSError:
        return None


def raiz_do_git(pasta):
    """A raiz do repositório que contém a pasta; None fora de um repositório ou sem git."""
    resultado = git_do_lembrete(pasta, "rev-parse", "--show-toplevel")
    if resultado is None or resultado.returncode != 0:
        return None
    return Path(resultado.stdout.strip())


def handoffs_citados(texto, base):
    """Os caminhos `HANDOFF-*.md` citados no texto, resolvidos contra a base."""
    return [base / citacao for citacao in CITACAO_DE_HANDOFF.findall(texto)]


def handoff_gravado(caminho, raiz):
    """True se o handoff existe e, quando o git o acompanha, não tem mudanças por commitar."""
    if not caminho.is_file():
        return False
    if raiz is None:
        return True
    rastreado = git_do_lembrete(raiz, "ls-files", "--error-unmatch", "--", str(caminho)).returncode == 0
    if not rastreado:
        return git_do_lembrete(raiz, "check-ignore", "-q", "--", str(caminho)).returncode == 0
    return git_do_lembrete(raiz, "status", "--porcelain", "--", str(caminho)).stdout.strip() == ""


def deve_parar(pedido):
    """True se o /compact deve parar por falta de um handoff gravado."""
    texto = pedido.get("custom_instructions") or ""
    if pedido.get("trigger") != "manual" or MARCA_DE_SAIDA in texto.lower():
        return False
    pasta = Path(pedido.get("cwd") or ".")
    raiz = raiz_do_git(pasta)
    citados = handoffs_citados(texto, raiz or pasta)
    return not any(handoff_gravado(caminho, raiz) for caminho in citados)


def main():
    # Bytes em UTF-8: no Windows o stdin de texto usaria a página de código local e estragaria os acentos.
    pedido = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    if deve_parar(pedido):
        sys.stderr.reconfigure(encoding="utf-8")
        sys.stderr.write(TEXTO_DA_PARADA)
        sys.exit(2)


if __name__ == "__main__":
    main()
