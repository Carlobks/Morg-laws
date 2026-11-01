# Hooks e permissões do Claude Code

## No modo automático, as regras `ask` não perguntam

**O que aconteceu:** um `git push --dry-run` e a escrita de um hook rodaram sem pergunta, com `Bash(git push *)` e `Edit(.claude/hooks/**)` na coluna `ask` do `settings.json` (confirmado pelo dono).
**Como fazer:** o que tem de pedir o "sim" passa por um hook `PreToolUse` que devolve `permissionDecision: "ask"`; esse pergunta em qualquer modo. As regras `ask` ficam, mas não são a barreira. Modelo: `modelos/claude/hooks/perguntar_antes.py`.

## O `deny` de leitura só cobre a ferramenta Read

**O que aconteceu:** com `Read(**/.env)` no `deny`, ler o mesmo arquivo pelo terminal passava.
**Como fazer:** um hook para Bash e PowerShell recusa o comando que nomeia um segredo. Ele lê o comando como texto, por isso recusa também um heredoc que só cita o segredo (aconteceu com uma mensagem de commit): escreva a mensagem num arquivo e rode o commit por um script. Modelo: `modelos/claude/hooks/bloquear_segredos.py`.

## Hook em falta numa sessão mudada de pasta bloqueia tudo

**O que aconteceu:** depois de a sessão mudar de pasta, todas as ferramentas ligadas a um hook ficaram bloqueadas, e o agente não conseguia corrigir o `settings.json` sozinho.
**Por que:** o `$CLAUDE_PROJECT_DIR` continua a ser a pasta onde a sessão começou; o script do hook não existe lá, o Python sai com 2 e o Claude Code lê 2 como "bloquear".
**Como fazer:** o comando do hook procura o script em `$CLAUDE_PROJECT_DIR` e, se não existir, na raiz do git (`git rev-parse --show-toplevel`). Para desbloquear, a pessoa renomeia o `.claude/settings.json`.

## Um hook roda antes do comando inteiro

**O que aconteceu:** num único comando "criar arquivo e depois commitar", o hook de testes rodou sem o arquivo novo, e um teste falhado entrou no commit.
**Como fazer:** crie ou mude arquivos num comando e commite noutro. Os testes que têm de valer sempre vão no hook do **git** (`pre-commit`), que roda na hora do commit e também à mão.

## Um hook que lê o comando como texto dá falsos alarmes

**O que aconteceu:** código Python colado num heredoc parecia, para o hook, um comando proibido, e foi recusado.
**Como fazer:** código vai para um arquivo, escrito com a ferramenta de escrita; a shell só roda `python -I arquivo.py`. O falso alarme fica do lado seguro.

## Verificar um hook com uma sonda

**O que aconteceu:** um hook ligado com o caminho errado nunca rodou, e ninguém notou.
**Como fazer:** mande um JSON de exemplo no stdin do hook e confira a saída (2 e o motivo no stderr, ou o JSON de "ask" no stdout). Ligue-o com `onFailure: block`: um hook que quebra e deixa passar é uma barreira que some sem ninguém ver.
