"""Hook UserPromptSubmit: se passou mais de uma hora desde a última resposta, avisa o agente (sem parar a mensagem).

A hora vem do próprio registro da conversa (`transcript_path`): o `timestamp` da última entrada do assistente, lido
no fim do arquivo. A hora do arquivo não serve: a ferramenta escreve nele a cada mensagem e anexo. Nada se grava.
O formato do registro não é documentado: se mudar, o aviso some calado (nunca avisa, nunca quebra a mensagem).
Limite conhecido: o evento também roda em turnos que o dono não escreveu (um `/loop`, uma tarefa agendada, a
mensagem de outra sessão); num `/loop` de intervalo longo o aviso se repete.
Nunca bloqueia: sai com 0 e põe o texto no `additionalContext` do agente, que o repete ao usuário.
Instalar: copiar para `.claude/hooks/` do projeto e ligar no `.claude/settings.json` (modelo ao lado).
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# O `datetime.UTC` é do Python 3.11 e os moldes pedem só o 3.9: o fuso se faz com o `timezone`.
FUSO_UTC = timezone(timedelta(0))
LIMITE_DA_PAUSA = timedelta(minutes=60)
BYTES_DO_FIM = 1_000_000
TEXTO_DO_AVISO = (
    "Passou mais de uma hora desde a última resposta. A cache expirou e esta mensagem relê a conversa inteira. "
    "Antes de responder, diga ao usuário: se o trabalho continua, grave o handoff (skill `passando-o-trabalho`) e "
    "abra uma sessão nova que o lê; não compacte."
)


def fim_do_registro(caminho):
    """As linhas do fim do arquivo (a primeira pode vir cortada), ou [] se não der para ler."""
    try:
        with open(caminho, "rb") as registro:
            registro.seek(0, 2)
            registro.seek(max(0, registro.tell() - BYTES_DO_FIM))
            return registro.read().decode("utf-8", errors="replace").splitlines()
    except OSError:
        return []


def hora_da_entrada(linha):
    """A hora (com fuso) de uma linha do registro se for do assistente e tiver `timestamp`; senão None."""
    try:
        entrada = json.loads(linha)
        if entrada["type"] != "assistant":
            return None
        # O `fromisoformat` do 3.9 e do 3.10 não lê o «Z» final, por isso o `replace`.
        texto_da_hora = entrada["timestamp"].replace("Z", "+00:00")
        hora = datetime.fromisoformat(texto_da_hora)
    except (ValueError, KeyError, TypeError, AttributeError):
        return None
    return hora if hora.tzinfo else hora.replace(tzinfo=FUSO_UTC)


def ultima_resposta(caminho):
    """A hora da última entrada do assistente no fim do registro, ou None."""
    for linha in reversed(fim_do_registro(caminho)):
        hora = hora_da_entrada(linha)
        if hora:
            return hora
    return None


def passou_da_pausa(caminho, agora):
    """True se a última resposta do assistente tem mais de 60 minutos."""
    hora = ultima_resposta(caminho)
    return hora is not None and agora - hora > LIMITE_DA_PAUSA


def main():
    # Bytes em UTF-8: no Windows o stdin de texto usaria a página de código local e estragaria os acentos.
    pedido = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    caminho = pedido.get("transcript_path")
    if caminho and passou_da_pausa(Path(caminho), datetime.now(FUSO_UTC)):
        saida = {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": TEXTO_DO_AVISO}}
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(json.dumps(saida, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
