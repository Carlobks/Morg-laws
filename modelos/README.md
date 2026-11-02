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
| `claude/hooks/perguntar_antes.py` | `.claude/hooks/` | Pergunta antes de push, de tudo o que escreve no GitHub (PR, issue, comentário, versão, `gh api` de escrita), instalações e mudanças às regras do agente, também no modo automático (onde as regras `ask` não perguntam) |
| `claude/hooks/limite_de_linhas.py` | `.claude/hooks/` | Recusa que um arquivo de código passe de 500 linhas e cresça |
| `git/hooks/pre-commit` | `.githooks/` | Identidade, lista negra e o comando único de testes (defina `COMANDO_DOS_TESTES`) |
| `git/hooks/commit-msg` | `.githooks/` | Formato da mensagem e lista negra |
| `git/hooks/pre-push` | `.githooks/` | Mostra o que sai, gitleaks e `npm audit` com linha de base |
| `git/portoes/*.py` | `scripts/portoes/` | A lógica dos hooks do git: `identidade`, `lista_negra`, `mensagem_commit` (marcas `Sem-teste:`, `Teste-mudado:`, `Sem-changelog:`), `versao_lancada`, `antes_do_push` |
| `pre-push` | `.githooks/pre-push` | Alternativa só em `sh`, sem Python |
| `changelog/juntar_changelog.py` | `scripts/changelog/` | Junta os fragmentos no `CHANGELOG.md`, calcula a versão SemVer pelas categorias e escreve o `VERSION` |
| `changelog/changelog.d/README.md` | `changelog.d/` | O formato dos fragmentos (`AAAA-MM-DD-assunto.md`, categoria na 1.ª linha) |
| `github/workflows/ci.yml` | `.github/workflows/` | O comando único de testes numa máquina limpa e o gitleaks em todo o histórico, com actions por SHA e o binário conferido por sha256 |
| `github/ISSUE_TEMPLATE/erro.yml` | `.github/ISSUE_TEMPLATE/` | Formulário de erro: resumo, passos, esperado, acontecido, versão e relatório revisto |
| `testes/test_regras.py` | `tests/` | O arquivo de regras curto, cada regra com motivo e com linha no mapa das barreiras, caminhos citados que existem, índice das skills igual ao instalado |
| `testes/test_docs_indices.py` | `tests/` | Índice dos docs, ADRs seguidas, pesquisa com data, armadilhas A1…An, planos com "Fora do escopo" e "Prova", handoffs com hashes que existem |
| `testes/test_alarmes.py` | `tests/` | Alarme calado só com o motivo na mesma linha (também em `/* */`), contagem por tipo que não sobe e desce com quem tira um, `noqa` só de regras que o ruff tem ligadas |
| `testes/test_nomes.py` | `tests/` | Nenhum arquivo, pasta ou identificador com nome genérico solto |
| `testes/test_dados_pessoais.py` | `tests/` | Sem caminhos de pastas pessoais, e-mails pessoais nem termos da lista negra |
| `testes/test_tamanho_das_funcoes.py` | `tests/` | Funções Python até 20 linhas (decisão do dono), com catraca para as antigas |
| `testes/test_fins_de_linha.py` | `tests/` | LF no git; CRLF no disco só no que o Windows roda |
| `testes/test_permissoes.py` | `tests/` | As três colunas, o modo que salta as permissões desligado, os hooks ligados com `onFailure: block` |
| `testes/test_ci.py` | `tests/` | Actions fixadas por SHA, token só de leitura, nada baixado direto para uma shell |
| `testes/carregar_por_caminho.py` | `tests/` | Carrega os scripts pelo caminho e roda-os como `__main__` no processo, para contarem na cobertura |
| `documentos/CLAUDE.md` | `CLAUDE.md` | Arquivo de regras no formato que o `test_regras.py` confere (`- **TÍTULO:** regra. · *motivo*`) |
| `documentos/regras-e-barreiras.md` | `docs/` | O mapa: cada regra e a barreira que a obriga, ou o motivo de ficar em texto |
| `documentos/plano.md` | `docs/planos/` | Contexto, decisões do dono, fora do escopo, passos com caixas e prova |
| `documentos/verificacao.md` | `docs/` | Verificação independente: contagens fechadas antes de ler a anterior |
| `documentos/handoff.md` | `.context/HANDOFF-<assunto>.md` | Estado verificado, decisões do dono e técnicas, descartado, próximos passos |
| `documentos/adr.md` | `docs/decisoes/` | Decisão no formato de Nygard, com o exemplo "o histórico publicado não se reescreve" |
| `documentos/armadilhas.md` | `docs/` | Tabela A1, A2, … com a regra para evitar cada uma |

## Como instalar

1. Copie as pastas para os destinos da tabela. Nos hooks do git, guarde a marca de executável:
   `git add --chmod=+x .githooks/*`.
2. Ligue os hooks do git: `git config core.hooksPath .githooks`.
3. Identidade só deste repositório: `git config --local user.email <id>+<conta>@users.noreply.github.com`.
4. Lista negra fora do repositório (um termo por linha): `git config morg.listaNegra ~/.config/morg-laws/lista-negra.txt`.
   A pasta `~/.config/morg-laws` já está no `deny` e no `bloquear_segredos.py`; se usar outra, ajuste os dois.
5. Ajuste ao projeto: `COMANDO_DOS_TESTES` no `pre-commit`; `TESTE` e `PUBLICADO` no `mensagem_commit.py`; o
   bloco "Ajuste ao projeto" no início de cada teste. Uma parte cuja pasta não existe é saltada, não falha.
6. Python: os hooks usam `MORG_PY`, ou `py` (Windows), ou `python3`, sempre com `-I`.
7. Prove cada barreira com uma sonda antes de confiar nela (skill `auditoria-de-seguranca`, seção 8).
