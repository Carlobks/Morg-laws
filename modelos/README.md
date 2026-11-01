# Modelos

Arquivos prontos para copiar para um projeto. Cada um transforma uma regra do `AGENTS.md` numa barreira de máquina
("texto é conselho; o que tem de ser cumprido vira hook, teste ou CI"). Saíram de um projeto real, onde rodam com
testes a 100 %. Os scripts são Python só com a biblioteca padrão; os hooks do git são `sh` (o Git for Windows traz um).

## O que tem aqui

| Arquivo | Vai para | O que faz |
|---|---|---|
| `claude/settings.json` | `.claude/settings.json` | Permissões em três colunas (deny, ask, allow), `disableBypassPermissionsMode` e os hooks abaixo ligados com `onFailure: block` |
| `claude/hooks/guarda_do_git.py` | `.claude/hooks/` | Recusa `--no-verify`, mudar o `core.hooksPath`, `git add -A`, `commit -a`, commit sem caminhos, `-m` com várias linhas e `git stash` |
| `claude/hooks/bloquear_segredos.py` | `.claude/hooks/` | Recusa ler segredos pela shell (o `deny` só cobre a ferramenta Read) e `curl … \| sh` |
| `claude/hooks/perguntar_antes.py` | `.claude/hooks/` | Pergunta antes de push, PR, instalações e mudanças às regras do agente, também no modo automático (onde as regras `ask` não perguntam) |
| `claude/hooks/limite_de_linhas.py` | `.claude/hooks/` | Recusa que um arquivo de código passe de 500 linhas e cresça |
| `git/hooks/pre-commit` | `.githooks/` | Identidade, lista negra e o comando único de testes (defina `COMANDO_DOS_TESTES`) |
| `git/hooks/commit-msg` | `.githooks/` | Formato da mensagem e lista negra |
| `git/hooks/pre-push` | `.githooks/` | Mostra o que sai, gitleaks e `npm audit` com linha de base |
| `git/portoes/*.py` | `scripts/portoes/` | A lógica dos hooks do git: `identidade`, `lista_negra`, `mensagem_commit` (marcas `Sem-teste:`, `Teste-mudado:`, `Sem-changelog:`), `versao_lancada`, `antes_do_push` |
| `pre-push` | `.githooks/pre-push` | Alternativa só em `sh`, sem Python |

## Como instalar

1. Copie as pastas para os destinos da tabela. Nos hooks do git, guarde a marca de executável:
   `git add --chmod=+x .githooks/*`.
2. Ligue os hooks do git: `git config core.hooksPath .githooks`.
3. Identidade só deste repositório: `git config --local user.email <id>+<conta>@users.noreply.github.com`.
4. Lista negra fora do repositório (um termo por linha): `git config morg.listaNegra ~/.config/morg-laws/lista-negra.txt`.
   A pasta `~/.config/morg-laws` já está no `deny` e no `bloquear_segredos.py`; se usar outra, ajuste os dois.
5. Ajuste ao projeto: `COMANDO_DOS_TESTES` no `pre-commit`; `TESTE` e `PUBLICADO` no `mensagem_commit.py`.
6. Python: os hooks usam `MORG_PY`, ou `py` (Windows), ou `python3`, sempre com `-I`.
7. Prove cada barreira com uma sonda antes de confiar nela (skill `auditoria-de-seguranca`, seção 8).
