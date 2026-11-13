# Modelos

Arquivos prontos para copiar para um projeto. Cada um transforma uma regra do `AGENTS.md` numa barreira de máquina
("texto é conselho; o que tem de ser cumprido vira hook, teste ou CI"). Saíram de um projeto real, onde rodam com
testes a 100 %. Os scripts são Python só com a biblioteca padrão; os hooks do git são `sh` (o Git for Windows traz um).
Os testes prontos de `testes-ts/` são a exceção: TypeScript, com o `vitest` e o `typescript`.

## O que tem aqui

| Arquivo | Vai para | O que faz |
|---|---|---|
| `claude/settings.json` | `.claude/settings.json` | Permissões em três colunas (deny, ask, allow), `disableBypassPermissionsMode` e os hooks abaixo ligados: os do `PreToolUse` com `onFailure: block`, os da compactação com `onFailure: continue`; sem o `deny` da ferramenta `Agent`, que é opção (passo 8) |
| `claude/hooks/guarda_do_git.py` | `.claude/hooks/` | Recusa `--no-verify`, mudar o `core.hooksPath`, `git add -A`, `commit -a`, commit sem caminhos, `-m` com várias linhas e `git stash` |
| `claude/hooks/bloquear_segredos.py` | `.claude/hooks/` | Recusa ler segredos pela shell (o `deny` só cobre a ferramenta Read) e `curl … \| sh` |
| `claude/hooks/perguntar_antes.py` | `.claude/hooks/` | Pergunta antes de push, de tudo o que escreve no GitHub (PR, issue, comentário, versão, `gh api` de escrita), instalações e mudanças às regras do agente, também no modo automático (onde as regras `ask` não perguntam) |
| `claude/hooks/limite_de_linhas.py` | `.claude/hooks/` | Recusa que um arquivo de código passe de 500 linhas e cresça |
| `claude/hooks/lembrar_o_handoff.py` | `.claude/hooks/` | No `PreCompact` (só o `/compact` manual): para se o texto não cita um `.context/HANDOFF-<assunto>.md` que existe e está commitado (sem git, ou com a pasta ignorada, basta existir); a marca «sem handoff» deixa compactar; o texto diz a quem vai parar que não compacte |
| `claude/hooks/retomar_pelo_handoff.py` | `.claude/hooks/` | No `SessionStart` depois de compactar (manual ou automática): manda o agente ler o handoff do assunto, lista os que existem com a data de cada e manda perguntar se não souber qual; sem handoff, não diz nada; nunca bloqueia |
| `git/hooks/pre-commit` | `.githooks/` | Identidade, lista negra e o comando único de testes (defina `COMANDO_DOS_TESTES`) |
| `git/hooks/commit-msg` | `.githooks/` | Formato da mensagem e lista negra |
| `git/hooks/pre-push` | `.githooks/` | Mostra o que sai, gitleaks e `npm audit` com linha de base em cada pasta com `package-lock.json` |
| `git/portoes/*.py` | `scripts/portoes/` | A lógica dos hooks do git: `identidade`, `lista_negra`, `mensagem_commit` (marcas `Sem-teste:`, `Teste-mudado:`, `Sem-changelog:` e `Alarme-novo:`, a que deixa subir a contagem dos alarmes calados), `versao_lancada`, `antes_do_push` |
| `pre-push` | `.githooks/pre-push` | Alternativa só em `sh`, sem Python |
| `changelog/juntar_changelog.py` | `scripts/changelog/` | Junta os fragmentos no `CHANGELOG.md`, calcula a versão SemVer pelas categorias e escreve o `VERSION` |
| `changelog/changelog.d/README.md` | `changelog.d/` | O formato dos fragmentos (`AAAA-MM-DD-assunto.md`, categoria na 1.ª linha) |
| `github/workflows/ci.yml` | `.github/workflows/` | O comando único de testes numa máquina limpa (com `MORG_BASE_DE_COMPARACAO` e todo o histórico, para o «só encolhe» das linhas de base) e o gitleaks em todo o histórico, com actions por SHA e o binário conferido por sha256 |
| `github/ISSUE_TEMPLATE/erro.yml` | `.github/ISSUE_TEMPLATE/` | Formulário de erro: resumo, passos, esperado, acontecido, versão e relatório revisto. O validador de esquema dos formulários do Morg-laws (`tests/test_esquema_dos_formularios.py`) também confere a forma dele |
| `testes/test_regras.py` | `tests/` | O arquivo de regras curto, cada regra com motivo e com linha no mapa das barreiras, caminhos citados que existem, índice das skills igual ao instalado |
| `testes/test_docs_indices.py` | `tests/` | Índice dos docs, ADRs seguidas, pesquisa com data, armadilhas A1…An, planos com "Fora do escopo" e "Prova", handoffs com hashes que existem |
| `testes/test_alarmes.py` | `tests/` | Alarme calado só com o motivo na mesma linha (também em `/* */`), contagem por tipo no projeto inteiro que não sobe (salvo com `Alarme-novo:` no commit) e desce com quem tira um, `noqa` só de regras que o ruff tem ligadas, com linha de base |
| `testes/test_nomes.py` | `tests/` | Nenhum arquivo, pasta ou identificador Python (lido pela árvore) com nome genérico solto, com linha de base; a lista é a do molde TypeScript |
| `testes/test_tamanho_dos_arquivos.py` | `tests/` | Arquivos de código até 500 linhas, de todas as línguas (o limite do hook `limite_de_linhas.py`), com linha de base |
| `testes/test_nomes_unicos.py` | `tests/` | Nomes de topo do Python e nomes de arquivo de código únicos, com linha de base; isenta `main`, `__x__` e a interface comum dos portões e hooks |
| `testes/test_testes_saltados.py` | `tests/` | Nenhum `skip` sem condição nem sem motivo escrito (unittest e pytest), com linha de base |
| `testes/linha_de_base.py` | `tests/` | O motor dos seis testes prontos (estes três e os de funções, nomes e alarmes): a linha de base em `tests/linhas-de-base/<regra>.json` não piora, não tem folga e só encolhe (no CI, contra `MORG_BASE_DE_COMPARACAO`); `MORG_CRIAR_LINHA_DE_BASE=1` cria a que falta ou completa a que ainda não está commitada |
| `testes-ts/*.test.ts` | `tests/catracas/` | Os mesmos seis em TypeScript/vitest (tamanho de arquivo e de função, nomes genéricos e únicos, alarmes e testes saltados), com os mesmos limites e listas e a linha de base no mesmo formato; o código lê-se pela árvore do `typescript` (`ler-codigo-ts.ts`, `linha-de-base.ts`) |
| `testes/test_dados_pessoais.py` | `tests/` | Sem caminhos de pastas pessoais, e-mails pessoais, termos da lista negra nem os números de documento que o projeto ligar |
| `testes/test_tamanho_das_funcoes.py` | `tests/` | Funções Python até 20 linhas (decisão do dono), contadas como no TypeScript, com linha de base por arquivo |
| `testes/test_fins_de_linha.py` | `tests/` | LF no git; CRLF no disco só no que o Windows roda |
| `testes/test_permissoes.py` | `tests/` | As três colunas, o modo que salta as permissões desligado, os hooks ligados: `onFailure: block` nos do `PreToolUse` e um `onFailure` escrito nos dos outros eventos |
| `testes/test_ci.py` | `tests/` | Actions fixadas por SHA, token só de leitura, nada baixado direto para uma shell |
| `testes/carregar_por_caminho.py` | `tests/` | Carrega os scripts pelo caminho e roda-os como `__main__` no processo, para contarem na cobertura |
| `documentos/AGENTS.md` | `AGENTS.md` | Arquivo de regras no formato que o `test_regras.py` confere (`- **TÍTULO:** regra. · *motivo*`): a Regra n.º 1 por preencher, o núcleo e o "Nunca" (iguais aos do `AGENTS.md` do Morg-laws, um teste confere) e o índice das skills |
| `documentos/CLAUDE.md` | `CLAUDE.md` | A linha `@AGENTS.md` e o que vale só no Claude Code; não repete as regras |
| `documentos/regras-e-barreiras.md` | `docs/` | O mapa: cada regra e a barreira que a obriga, ou o motivo de ficar em texto |
| `documentos/projeto.md` | `docs/projeto.md` | O documento do projeto: o que é, para quem, o que faz e não faz, restrições, arquitetura com o porquê, as palavras do dono e as perguntas em aberto |
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
   bloco "Ajuste ao projeto" no início de cada teste. Uma parte cuja pasta não existe é pulada, não falha.
   Projeto em TypeScript: copie `testes-ts/` para `tests/catracas/`, instale o `vitest` e o `typescript` com as
   versões fixadas no `package-lock.json`, fixe o Node num `.nvmrc` (o bloco TypeScript do molde de CI usa-o) e ponha `npx vitest run` no comando único. Projeto que já viola: rode os
   testes uma vez com `MORG_CRIAR_LINHA_DE_BASE=1`, leia as bases criadas em `tests/linhas-de-base/` e faça
   `git add` (skill `codigo-legivel`).
6. Python: os hooks usam `MORG_PY`, ou `py` (Windows), ou `python3`, sempre com `-I`.
   Os hooks do `PreToolUse` travam se falharem (`"onFailure": "block"`), o que exige o Claude Code v2.1.295 ou mais
   novo; numa versão antiga o campo é ignorado e um hook que não arranca deixa passar. Os dois da compactação
   (`lembrar_o_handoff.py` e `retomar_pelo_handoff.py`) vêm com `"onFailure": "continue"`: um hook quebrado (sai
   com 1) não para a compactação nem a sessão; a parada de propósito do `lembrar_o_handoff.py` sai com 2, que não é
   falha, e segue parando.
   **O `test_permissoes.py` mudou:** antes exigia `onFailure: block` em todos os hooks; agora exige `block` só nos
   do `PreToolUse` e um `onFailure` escrito nos outros. Quem já tem o molde e copia o teste novo sem o
   `settings.json` novo continua verde; quem copia o `settings.json` novo sem o teste novo vê o teste antigo falhar.
7. Prove cada barreira com uma sonda antes de confiar nela (skill `auditoria-de-seguranca`, seção 8).
8. **Só sessões, sem sub-agentes** (opção; skill `orquestrando-sessoes`, seção 1): acrescente `"Agent"` ao
   `deny` do `.claude/settings.json` e ponha `SO_SESSOES = True` no `test_permissoes.py`. O nome da ferramenta
   sozinho tira-a do contexto do agente; `Agent(Explore)` nega um sub-agente só. O molde vem sem esta linha.

## A compactação fora do molde

As duas configurações abaixo ficam de fora: num `.claude/settings.json` commitado valeriam para todos os que clonam o
projeto. As fontes estão no `FONTES.md` (os comandos e a referência das configurações do Claude Code).

- **A janela da compactação automática:** quem quiser uma janela menor a põe nas próprias configurações com
  `/autocompact 150k`, que grava por modelo nas configurações do usuário. A automática compacta sem handoff; uma
  janela pequena faz que ela chegue antes do `/compact` manual com handoff.
- **A compactação por inatividade** (`idleCompaction`, ligada por padrão): compacta a conversa grande (a partir de
  200 mil tokens; o limiar muda com a variável `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS`) parada há cerca de uma hora,
  justamente a que a skill `passando-o-trabalho` manda deixar por uma sessão nova. Para desligar:
  `"idleCompaction": false` nas suas configurações. Ligada, o `retomar_pelo_handoff.py` aponta o handoff na volta.
- **Codex:** o Codex tem eventos de hook com os mesmos nomes (`PreCompact`, `SessionStart`), mas os campos e o
  comportamento não foram conferidos; estes hooks não foram feitos para ele.
