# Hooks de compactação: a revisão de 2026-11-13

Data: 2026-11-13. Escrita com palavras próprias; as citações são curtas, de seções lidas nessa data. Esta pesquisa
revê a de [2026-11-02](2026-11-02-hooks-de-compactacao.md), que não muda: a história não se reescreve.

## Pergunta

Três hooks novos entraram nos moldes: um que para o `/compact` manual sem handoff, um que manda ler o handoff depois
de qualquer compactação e um aviso na primeira mensagem depois de uma pausa de mais de uma hora. O que as páginas
dizem hoje sobre os eventos deles mudou desde 2026-11-02? A entrada do `PreCompact` separa a compactação automática
preventiva da de recuperação e da de inatividade? Um hook quebrado pode parar a compactação ou a mensagem? O que o
Codex lista?

## Fontes

- **Claude Code — hooks** — https://code.claude.com/docs/en/hooks — lidas em 2026-11-13 só as seções do `PreCompact`,
  do `onFailure` e do `UserPromptSubmit`, com citações curtas. Entrada no `FONTES.md`.
- **Claude Code — referência das configurações** — https://code.claude.com/docs/en/settings-reference — lida só a
  seção da compactação por inatividade. Entrada no `FONTES.md`.
- **Claude Code — configuração do modelo** — https://code.claude.com/docs/en/model-config — lida só a seção da janela
  de compactação. Entrada no `FONTES.md`.
- **Codex — referência da configuração** — https://developers.openai.com/codex/config-reference — lidas só as linhas
  com `compact` e a tabela `hooks.<Event>`. Entrada no `FONTES.md`.

## O que se mediu

Tudo abaixo foi **lido**, não executado.

| Ponto | Em 2026-11-02 | Em 2026-11-13 |
|---|---|---|
| `PreCompact`, a saída | bloqueia com 2 ou `decision: block`; `systemMessage` e `continue` descartados | igual, e uma seção que a leitura anterior não trouxe: com saída 0 e sem bloquear, «Claude Code uses its stdout as instructions for the compaction summary», até 10.000 caracteres por hook |
| `PreCompact`, a entrada | `trigger` (`manual` ou `auto`) e `custom_instructions` | igual; nenhum campo diz se a automática é preventiva, de recuperação ou de inatividade |
| `auto` e a inatividade | o `auto` inclui a inatividade | confirmado nas tabelas do `PreCompact` e do `PostCompact`: o `auto` cobre a janela automática «and idle compaction» |
| `onFailure` | `continue` ou `block`, desde a v2.1.295 | igual; com `block`, a falha «does what exit code 2 does on that event», logo um hook quebrado com `block` num `PreCompact` bloqueia a compactação. O código 2 não é falha: as falhas são «Can't start», «Exit code other than 0 or 2», «HTTP error», «Timeout» e «Invalid output» |
| `SessionStart` | origem `compact` | igual |
| `UserPromptSubmit` | não lido | roda em cada mensagem, e também em turnos que a pessoa não escreveu: «`UserPromptSubmit` hooks don't fire only on prompts you type» (uma tarefa agendada, uma iteração do `/loop`, «a message from another session»); nenhum campo lido separa esses turnos |
| Inatividade | a partir de 200 mil tokens, cerca de uma hora parada | igual, e o limiar muda pela variável `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS` (abaixo de 100 mil sobe para 100 mil) |
| A janela | de 100 mil a 1 milhão | igual; quatro formas de pôr: o `/autocompact` (grava por modelo nas configurações do usuário), o `autoCompactWindow` num arquivo de configurações, a opção `--autocompact` e uma variável. Na mesma pasta de configurações, o valor do `/autocompact` vale mais que a chave |
| Codex | só as linhas com `compact` | a tabela `hooks.<Event>` lista 14 eventos, entre eles `PreCompact`, `PostCompact`, `SessionStart` e `UserPromptSubmit`; os campos e o bloqueio estão num guia de hooks à parte |

O que isto pede dos moldes: os hooks da compactação e da mensagem levam `onFailure: continue`, porque nenhum deles pode
parar a compactação nem a mensagem por estar quebrado, e o código 2 do que para o `/compact` continua a bloquear
mesmo assim. Como nenhum campo separa os tipos de compactação automática, nenhum hook dos moldes tenta bloqueá-la.

## O que não se verificou

- Nenhum hook foi rodado no Claude Code: tudo vem das páginas, lidas por seção.
- Não se sabe se o stdout do `PreCompact` como instruções do resumo é novo ou se a leitura de 2026-11-02 o perdeu, nem
  como ele se combina com o texto de um `/compact` manual.
- A ordem entre o `PostCompact` e o `SessionStart` com `compact`, e o lugar do `additionalContext` em relação ao
  resumo, continuam sem resposta nas seções lidas.
- Se a variável `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS` é nova.
- A precedência do `/autocompact` gravado por modelo contra uma chave num arquivo de outra pasta: a página fala do
  mesmo arquivo.
- Do Codex só a lista de eventos: os matchers, os campos e o bloqueio dependem do guia de hooks dele, que não foi lido.
- O formato do registro da conversa que o aviso da pausa lê não é documentado; se mudar, o aviso some calado.

## Conclusão

Nada do que a pesquisa de 2026-11-02 afirmava ficou falso. Três coisas foram acrescentadas: o stdout do `PreCompact`
pode virar instruções do resumo (os moldes não o usam), nenhum campo separa a compactação automática preventiva, a de
recuperação e a de inatividade, e o `UserPromptSubmit` também dispara em turnos que a pessoa não escreveu, o que deixa
um limite no aviso da pausa. Os moldes ficam só no Claude Code; a lista de eventos do Codex mostra que os nomes
existem lá, mas o que cada um faz depende de um guia que ainda não se leu.
