"""Hook PreToolUse (Bash/PowerShell): o agente não lê segredos pela shell nem roda um download numa shell.

O `deny` do settings.json só cobre a ferramenta Read: sem este hook, um `cat .env` pelo terminal passa, e um
`curl … | sh` roda sem pergunta (medido num projeto real). Recusa:
- um comando que nomeia um segredo: `.env`, `.envrc` e `.env.*` (menos `.env.example`/`.env.sample`), `*.pem`,
  `*.key`, e as pastas de PASTAS_SECRETAS (`.ssh`, as credenciais do Claude Code, a pasta da lista negra);
- um download que vai direto para uma shell (`curl|wget|iwr|irm … | sh|bash|iex|powershell|python`,
  `sh -c "$(curl …)"`, `bash <(curl …)`, e `iex (irm …)` ou `DownloadString`).
Reconhece os comandos pelo texto: até um heredoc que só cita um segredo é recusado (escreva o script num arquivo).
Um nome partido por aspas (`cat .e""nv`) ou montado numa variável escapa: é o limite de ler o texto.
Sai com 2 e o motivo no stderr; sai com 0 nos outros casos.
Instalar: copiar para `.claude/hooks/` do projeto e ligar no `.claude/settings.json` (modelo ao lado).
"""

import json
import re
import sys

# Pastas que o agente não lê. A lista negra fica fora do repositório (git config morg.listaNegra); ajuste a pasta.
PASTAS_SECRETAS = (r"\.ssh(?:[/\\]|$)", r"\.claude[/\\]\.credentials", r"\.config[/\\]morg-laws")

_PALAVRA = re.compile(r"""[^\s"'`;|&<>()=,]+""")
_ENV = re.compile(r"\.env(?:rc|\.(?!example$|sample$)[\w.-]+)?", re.IGNORECASE)
_CHAVE = re.compile(r".+\.(?:pem|key)", re.IGNORECASE)
_PASTAS = re.compile(r"(?:^|[/\\])(?:" + "|".join(PASTAS_SECRETAS) + ")", re.IGNORECASE)
_DOWNLOAD = r"(?:curl|wget|iwr|irm|Invoke-WebRequest|Invoke-RestMethod)"
_SHELL = r"(?:sh|bash|zsh|iex|Invoke-Expression|powershell|pwsh|python3?|py)"
_PARA_SHELL = [
    re.compile(rf"\b{_DOWNLOAD}\b[^|]*\|\s*(?:sudo\s+)?{_SHELL}\b", re.IGNORECASE),
    re.compile(rf"\b(?:iex|Invoke-Expression)\b.*(?:\b{_DOWNLOAD}\b|DownloadString)", re.IGNORECASE),
    # A saída do download vira o script: sh -c "$(curl …)" e bash <(curl …) (ou source <(curl …)).
    re.compile(rf"\b{_SHELL}\s+-c\s+[\"']?\$\(\s*{_DOWNLOAD}\b", re.IGNORECASE),
    re.compile(rf"(?:\b{_SHELL}|\bsource|(?:^|[;&|]\s*)\.)\s+<\(\s*{_DOWNLOAD}\b", re.IGNORECASE),
]


def nomeia_um_segredo(palavra):
    """True se a palavra do comando for (ou apontar para) um segredo."""
    nome = re.split(r"[/\\]", palavra)[-1]
    return bool(_ENV.fullmatch(nome) or _CHAVE.fullmatch(nome) or _PASTAS.search(palavra))


def motivo_para_bloquear(comando):
    """Devolve o motivo (texto) se o comando ler um segredo ou rodar um download; None nos outros casos."""
    if any(padrao.search(comando) for padrao in _PARA_SHELL):
        return "um download rodando direto numa shell (curl | sh) executa código que ninguém leu."
    if any(nomeia_um_segredo(palavra) for palavra in _PALAVRA.findall(comando)):
        return "o comando nomeia um segredo (.env, chave, .ssh, credenciais ou a lista negra)."
    return None


def main():
    # Bytes em UTF-8: no Windows o stdin de texto usaria a página de código local e estragaria os acentos.
    pedido = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    motivo = motivo_para_bloquear((pedido.get("tool_input") or {}).get("command") or "")
    if motivo:
        sys.stderr.reconfigure(encoding="utf-8")
        sys.stderr.write(f"Bloqueado (segredos, Morg-laws): {motivo} Se for mesmo preciso, peça ao dono.\n")
        sys.exit(2)


if __name__ == "__main__":
    main()
