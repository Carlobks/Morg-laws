# Compactação no Claude Code e no Codex

Data: 2026-11-02.

## Pergunta

Para uma skill que guarda o trabalho num arquivo antes de a conversa ser compactada e o retoma depois: o que o
`/compact` aceita no Claude Code e no Codex, quando cada um compacta sozinho, o que volta ao agente depois da
compactação, e se o formato das skills e o `npx skills add` servem às duas ferramentas?

## Fontes

Todas lidas em 2026-11-02, na versão em texto quando a página a tem (o mesmo endereço terminado em `.md`). Cada uma
tem entrada no `FONTES.md`. O que se leu de cada uma:

- **Claude Code — comandos** — https://code.claude.com/docs/en/commands — só as linhas com `compact` (procura).
- **Claude Code — janela de contexto** — https://code.claude.com/docs/en/context-window — da seção «What survives
  compaction» até o fim; o começo da página, só as linhas com `compact`.
- **Claude Code — como funciona** — https://code.claude.com/docs/en/how-claude-code-works — só as linhas com
  `compact`.
- **Claude Code — glossário** — https://code.claude.com/docs/en/glossary — só as linhas com `compact` (a entrada
  «Compaction» e a do CLAUDE.md).
- **Claude Code — configuração do modelo** — https://code.claude.com/docs/en/model-config — a seção «Context window
  and auto-compaction» inteira, com as subseções da janela e dos limites por modelo.
- **Claude Code — referência das configurações** — https://code.claude.com/docs/en/settings-reference — o fim da
  entrada `autoCompactEnabled` e a entrada `idleCompaction` inteira.
- **Claude Code — custos** — https://code.claude.com/docs/en/costs — só as linhas com `compact`.
- **Codex — comandos** — https://developers.openai.com/codex/cli/slash-commands — as linhas com `compact`: a linha
  da tabela, a nota do `/recap` e a seção do `/compact`. O endereço redireciona para `learn.chatgpt.com`.
- **Codex — referência da configuração** — https://developers.openai.com/codex/config-reference — só as linhas com
  `compact`. Também redireciona para `learn.chatgpt.com`.
- **Codex — skills** — https://developers.openai.com/codex/skills — a página inteira. Também redireciona.
- **Agent Skills — especificação** — https://agentskills.io/specification — as seções dos campos `name` e
  `description` e as linhas com limites de tamanho.
- **skills (a ferramenta do `npx skills add`)** — https://github.com/vercel-labs/skills — o começo do README, a
  lista de agentes (`docs/agents.md`, procura por Codex e Claude Code) e os formatos de origem do `skills add`
  (`docs/commands.md`). É a documentação da própria ferramenta, não a de cada agente.

## O que se mediu

Tudo foi **lido** nas páginas; só a instalação (último item) foi executada, na prova da fase.

**O `/compact`:**

| | Claude Code | Codex |
|---|---|---|
| Instruções | Aceita: `/compact [instructions]`, com um foco para o resumo. | A página só mostra o comando sozinho: depois de escrito, o Codex pede confirmação e troca os turnos antigos por um resumo. Nenhum argumento está documentado. |
| Foco permanente | Uma seção «Compact instructions» no CLAUDE.md muda o que o resumo guarda (página dos custos e a do funcionamento). | A configuração `compact_prompt` troca o prompt da compactação (e há uma variante experimental que o lê de um arquivo). |
| Resumir sem compactar | — | O `/recap` faz um resumo e não libera contexto. |

**Quando compacta sozinho:**

- **Claude Code:** perto do limite da janela. Sem configurar, compacta ao chegar ao limite do modelo, com exceções
  por modelo (nos de 1 milhão de tokens, por volta de 967 mil). O `/autocompact` (ou `autoCompactWindow`, a opção
  `--autocompact` e a variável `CLAUDE_CODE_AUTO_COMPACT_WINDOW`) muda o tamanho em tokens a partir do qual compacta,
  entre 100 mil e 1 milhão. O `autoCompactEnabled` desliga a automática; o `/compact` manual continua.
- **Claude Code, por inatividade:** liga-se sozinha numa conversa longa (por padrão a partir de 200 mil tokens)
  parada há cerca de uma hora, em sessão interativa, com a automática ligada. A chave `idleCompaction` desliga-a.
- **Codex:** `model_auto_compact_token_limit` é o limite em tokens da compactação automática (sem valor, vale o do
  modelo). `model_post_turn_compact_threshold_percent` compacta no fim de um turno quando o contexto passa de uma
  **percentagem** da janela útil; desligada por padrão. A página não recomenda nenhum valor.

**O que volta depois (Claude Code):** o prompt de sistema e o estilo continuam; o CLAUDE.md da raiz, as regras sem
`paths:`, a memória automática e o plano do modo de plano voltam do disco; as descrições das skills são refeitas; o
retrato do `git status` é lido de novo; as regras com `paths:` e os CLAUDE.md das subpastas só voltam quando um
arquivo delas é aberto. Até **cinco** arquivos lidos ou editados voltam, os mudados mais recentemente; um arquivo com
mais de 5 mil tokens volta só como caminho. O corpo das skills usadas volta, cortado em 5 mil tokens por skill e 25
mil no total, e o corte guarda o começo: **o mais importante vai no topo do `SKILL.md`**. O que um hook pôs no
contexto entra no resumo; os `SessionStart` com a origem `compact` rodam e o que devolvem entra no contexto
compactado (pesquisa dos hooks, `2026-11-02-hooks-de-compactacao.md`).

**Skills nas duas ferramentas:**

- O Codex segue o padrão aberto de Agent Skills: uma pasta com `SKILL.md` que tem `name` e `description`. Começa só
  com o nome, a descrição e o caminho, e lê o corpo quando escolhe a skill. Procura skills em `.agents/skills`, da
  pasta atual até a raiz do repositório, e em `~/.agents/skills`.
- Na especificação: `name` com 1 a 64 caracteres, só minúsculas, algarismos e hífens, sem hífen no começo, no fim
  ou repetido, e igual ao nome da pasta; `description` com 1 a 1024 caracteres, dizendo o que faz e quando usar.
  O corpo fica abaixo de 500 linhas.
- A ferramenta `skills` lista o Claude Code (instala em `.claude/skills/`) e o Codex (em `.agents/skills/`) entre os
  agentes, aceita uma pasta local como origem e escolhe os agentes com `-a`.

## O que não se verificou

- Nenhuma página foi lida de ponta a ponta, fora a das skills do Codex: as ausências abaixo valem para os trechos
  lidos.
- **O `/compact` do Codex com texto a seguir** não foi experimentado: a página não diz que aceita argumentos, nem que
  os recusa. A skill trata-o como comando sem argumentos.
- **Quando compactar:** nenhuma página lida dá uma percentagem da janela para compactar à mão. As do Claude Code
  dizem só que dá para compactar antes da automática, com um foco. A percentagem do Codex é uma configuração, sem
  valor recomendado.
- O que o Codex devolve ao agente depois de compactar (arquivos de instruções, skills, arquivos lidos) não estava
  nos trechos lidos.
- Como se vê a percentagem da janela já usada no Codex não foi procurado; no Claude Code, o `/context` mostra o que
  ocupa a janela.
- O comportamento da compactação não foi medido em nenhuma das duas ferramentas: só se leu.

## Conclusão

1. O estado tem de ir para um **arquivo no disco** antes de compactar: o resumo é gerado pelo modelo e nenhuma das
   duas ferramentas garante que um arquivo escrito na sessão volte inteiro (no Claude Code voltam até cinco, e só os
   pequenos).
2. **Claude Code:** `/compact` com instruções que apontam para o arquivo; depois, uma mensagem que manda lê-lo.
   **Codex:** `/compact` sozinho, e a mensagem de retoma logo a seguir, porque não há onde pôr as instruções.
3. As instruções importantes da skill vão **no começo** do `SKILL.md`: depois de compactar, o Claude Code corta o
   corpo das skills pelo fim.
4. O `npx skills add` instala a mesma skill para o Claude Code e para o Codex, com `-a`.
5. Compactar por volta de metade da janela não vem de nenhuma destas páginas: se a skill o aconselha, diz de quem é
   o número.
