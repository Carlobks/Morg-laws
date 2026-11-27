---
titulo: que regras deve ter um handoff neste ERP (limites, estrutura e partir para a filha receber só a parte que precisa)?
data: 2026-11-26
area: geral
estado: concluida
destino: nenhum
---

**Conclusão curta.** O handoff **não é o que enche o contexto da filha**: o maior dos 41 tem 19,4 KB (~8,6 mil tokens),
a mediana 8,2 KB (~3,6 mil), um só passa as 150 linhas e nenhum chega aos 55 KB. O que falha é **o briefing**: 24 de
32 briefings de filhas desde 17-11 mandam ler o handoff inteiro, incluindo uma auditoria SQL «a frio», que não o
devia receber de todo. Recomendação (➡️): **limite** sim, curto e em bytes (≤150 linhas e ≤16 KB); **estrutura** a que
já existe, sem secções novas e sem a «Atualização» empilhada no topo; **partir** não em ficheiros, mas no briefing: a
mãe copia para a filha só o que ela precisa, e quando a filha precisa do handoff, nomeia as secções pelo título.

## Pergunta

O PO, a 26-11, para o envio ao Morg-laws de sexta 27-11: «montarmos regras para como fazer um handoff, limites,
estrutura e separar os handoffs, pois hoje mandamos ele inteiro para uma filha […] muitas vezes ela não precisa dele
inteiro». Para cada ideia (limites; estrutura fixa; partir), o que faz sentido e o que não faz, segundo a
documentação oficial do Claude, o Fabio Akita e o Morg-laws. Constrói em cima de
`docs/pesquisas/2026-11-19-contexto-da-sessao-filha-e-o-morg-laws.md` (o teto da Read, os ~60 mil tokens) e de
`.context/HANDOFF-contexto-das-sessoes-filhas.md` (as 6 decisões ainda abertas). Só leitura: nada mudou em skills,
hooks, `CLAUDE.md` ou no Morg-laws.

## Fontes lidas

- **Claude Code — How Claude remembers your project** — https://code.claude.com/docs/en/memory (lido agora)
- **Claude Code — Create custom subagents** — https://code.claude.com/docs/en/sub-agents (lido agora), salvo os últimos 14 mil caracteres da página
- **Claude Code — Manage costs effectively** — https://code.claude.com/docs/en/costs (lido agora)
- **Claude Code — Tools reference (Large files)** — https://code.claude.com/docs/en/tools-reference (do conhecimento do modelo), lida na pesquisa de 19-11 e não reaberta
- **Skill `passando-o-trabalho`** (a instalada, igual à do Morg-laws) — `C:\Users\Usuario\.claude\skills\passando-o-trabalho\SKILL.md`, secções 2, 4 e 5 (lido agora)
- **Skill `orquestrando-sessoes` do ERP** — `.claude/skills/orquestrando-sessoes/SKILL.md`, só os títulos (lido agora)
- **Morg-laws, commit `2325c49`** — `skills/orquestrando-sessoes/SKILL.md` (secções 2 a 4), `modelos/documentos/handoff.md` (lido agora)
- **Morg-laws, `biblia-akita/`** — `documentacao-e-memoria.md`, `pedidos-e-sessoes.md`, `arquivo-de-regras.md`: resumos do livro *Competente o Suficiente*, de Fabio Akita, com a página (lido agora); o livro em si não se abriu
- **Os 41 `.context/HANDOFF-*.md`**, medidos com `wc -c`/`wc -l` e `grep` (lido agora)
- **`scripts/entrega/ler-handoffs-da-entrega.mjs`**, o leitor da página da entrega (lido agora)
- **Os transcripts `.jsonl` do projeto** (primeira mensagem de cada sessão desde 17-11, por script) e a lista de sessões arquivadas por `list_sessions` (lido agora)

## O que se mediu

### 1. Os handoffs (26-11, 41 ficheiros)

| Medida | Valor |
|---|---|
| Maior | `HANDOFF-adocao-do-morg-laws.md`, 19 450 B, 121 linhas |
| Menor | `HANDOFF-valor-hora-dia-1-fase3-codigo.md`, 2 008 B, 23 linhas |
| Mediana | 8 170 B; 79 linhas |
| Acima de 150 linhas | 1 (`HANDOFF-valor-hora-dia-1.md`, 154) |
| Acima de 55 KB | 0 |
| Acima de 16 KB | 3 (`adocao-do-morg-laws` 19 450, `backups-bd` 18 092, `morg-laws` 16 744) |
| Com `## Atualização da entrega (…)` | 24 |
| Com `## Histórico …` | 1 (`adocao-do-morg-laws`, «Histórico de 20-11 (para consulta)», depois da mensagem de retoma) |
| Número de `## ` por ficheiro | 6 em 13; 7 em 22; 8 em 4; 1 e 10 num cada |

Em tokens, pela razão medida a 19-11 (o plano de 160 KB custou 72 600 tokens, ~2,25 B por token): o maior handoff
≈ 8,6 mil tokens, a mediana ≈ 3,6 mil. É um terço de uma chamada Read (25 mil) e ~6 % de uma fase de 150 mil.

**A «Atualização da entrega» empilha.** Foi posta no topo de 24 handoffs na entrega (24/25-11). Leva as três linhas
`Prioridade:`, `Prazo:`, `Depende de pessoa:` e, em vários, a `## Mensagem de retoma` antes do `## Objetivo`. O texto
antigo fica por baixo, com outro «Estado verificado» de outra data: em `HANDOFF-adocao-do-morg-laws.md` há o estado
«fim de 20-11» e a atualização de 24-11, e o «Histórico de 20-11» no fim. A skill diz o contrário: «Reescreva o
arquivo inteiro» (secção 2).

### 2. Os briefings das filhas (primeira mensagem, desde 17-11)

| | Sessões |
|---|---|
| Primeiras mensagens lidas | 376 |
| Citam um `HANDOFF-*.md` | 58 |
| … das quais briefings de filha (`Background`/`Task (from the session…)`) | 32 |
| … filhas com «inteiro» junto ao handoff | 24 |
| … filhas que apontam secções ou `offset` | 13 (sobrepõe-se às 24) |
| Retomas (o PO cola a mensagem de retoma) | 26, todas «leia inteiro» (o que a skill manda) |

Exemplo: a «auditoria SQL a frio» da migração 328 (transcript `2227a405`, 24-11) recebeu «Ler o `CLAUDE.md` inteiro e
`.context/HANDOFF-valor-hora-dia-1.md`», o handoff com mais linhas (154) e com as decisões da mãe. A regra SQL
AUDITADO NUMA SESSÃO NOVA pede texto neutro: ali o problema não é o tamanho, é a filha ler o raciocínio que devia
julgar. Noutra (`0b66edb6`, fase F6 da fila), o handoff ia como «estado e decisões do PO» ao lado do plano: a
filha precisava do «Descartado» e da linha F6, não do resto.

### 3. O que dizem as fontes

**Documentação oficial (Claude Code, 26-11).**
- Memória: o `CLAUDE.md` deve ficar «under 200 lines»; ficheiros maiores gastam contexto e «reduce adherence». Os
  `@imports` «help organize» mas **não reduzem** o custo, porque carregam juntos. Partir só poupa se quem lê ler só a parte.
- Subagentes: a filha começa sem a conversa; recebe uma mensagem de delegação que **resume** a tarefa. As regras de
  que ela precisa repetem-se no pedido; pede-se um resultado filtrado.
- Custos: «Keep spawn prompts focused», tudo o que vai no pedido entra no contexto desde o início. Cada mensagem entre
  sessões reenvia o contexto inteiro da que a recebe; o `/clear` entre tarefas sem relação.
- O que isto não diz: nada fala de handoffs nem de sessões da app (`start_session`); os subagentes são o caso mais
  próximo, não o mesmo.

**Fabio Akita (pelos resumos da `biblia-akita/`).**
- O contexto é relido a cada mensagem; enchê-lo custa dinheiro, tempo e precisão, e o meio perde-se (pp. 19, 29–31).
- Três gavetas: regras, decisões e pesquisas no git, e a passagem de turno só com o meio do caminho (p. 387). O
  histórico não é a passagem de turno.
- Documentos curtos, um por assunto (pp. 36–37); um índice sempre carregado abaixo de ~200 linhas, a apontar para
  ficheiros de tópico (p. 34).
- Um pedido tem quatro partes: o que se quer, como, o que não se quer, como se valida (pp. 118, 120–121); um molde
  de quinze secções trata o sintoma, não a causa (pp. 118, 121).
- Duas versões do mesmo assunto em dois sítios: o modelo segue uma ou outra conforme o dia (pp. 94, 99).

**Morg-laws (`2325c49`).**
- `passando-o-trabalho`: um ficheiro por assunto, cinco títulos fixos, «menos de 150 linhas», reescrito inteiro e
  commitado a cada gravação; ao retomar, «Leia-o inteiro». Não fala de dar uma parte a uma filha.
- `orquestrando-sessoes` §4: o pedido da filha leva «o objetivo, os arquivos, o que já se descartou, como se prova e
  o modelo», sem mandar ler o handoff. §2: a leitura longa por partes (~60 mil tokens).
- O ERP acrescentou ao molde as três linhas, a `## Mensagem de retoma` e, na entrega, a «Atualização»: o Morg-laws
  não tem nenhuma das três.

### 4. O que o leitor da página exige (`scripts/entrega/ler-handoffs-da-entrega.mjs`)

- Lista só `.context/HANDOFF-*.md` (linha 25), sem subpastas: **cada ficheiro é um cartão** da página.
- As três linhas: vale a **última** de cada antes de `## Mensagem de retoma` (linhas 38–48), em qualquer sítio do
  topo; `Prioridade:` tem de começar por alta, média ou baixa (linha 58), senão rebenta.
- `## Mensagem de retoma` com um bloco ` ```text ` que fecha (linhas 63–69), senão rebenta.
- `FECHADO` nas primeiras 6 linhas (107); o título é a primeira linha `# ` (89); as linhas com «não medid» antes da
  mensagem sobem à página (3 no máximo, 72–78).

## O que não se verificou

- As contagens dos briefings são por expressão regular sobre a primeira mensagem («inteiro» perto de um handoff), não
  lidas uma a uma; e mostram o que se pediu, não o que a filha leu de facto.
- Os tokens vêm da razão de 19-11 (2,25 B/token num `.md` em português), não de um contador de tokens.
- O livro do Akita não se abriu: leram-se os resumos do Morg-laws, que citam a página.
- Não se leu o `test_docs_indices.py` do Morg-laws: não se sabe se acusa as secções que o ERP juntou.
- A página dos subagentes ficou por ler nos últimos 14 mil caracteres; a da Tools reference não se reabriu.
- Não se mediu se o tamanho do briefing piorou o trabalho de alguma filha: o único incidente medido (19-11) foi um
  plano de 160 KB, não um handoff.

## Conclusão

### Ideia 1: limites

**Faz sentido**, mas pela qualidade da leitura e não pelo teto da Read: o meio do contexto perde-se (Akita, pp. 29–31)
e um ficheiro maior é seguido pior («reduce adherence», doc. memória). **Não faz sentido** apertar por causa do teto:
o maior handoff é um terço de uma Read. Linhas sozinhas enganam (a pesquisa de 19-11 mostrou-o): conta-se em bytes.

➡️ **Proposta:** manter «menos de 150 linhas» e juntar **≤16 KB**. Hoje passam 3 (aparam-se ao serem tocados). Sem
catraca por agora: a regra nasce em texto e só vira máquina se voltar a falhar (Akita, pp. 127–129). Contra: um
número escolhido por nós, sem fonte que o dê; 16 KB é ~2× a mediana.

### Ideia 2: estrutura fixa

**Faz sentido, e já existe**: os cinco títulos do Morg-laws mais as três linhas e a mensagem de retoma do ERP.
**Não faz sentido** acrescentar secções (Akita: o molde de quinze secções). O que falta é cumprir a que existe.

➡️ **Proposta:**
- Ordem: `# título` → as três linhas → `## Objetivo` → `## Estado verificado (data, ramo)` → `## Decisões e porquê`
  → `## Descartado` → `## Próximos passos` → `## Mensagem de retoma` (por último, com o bloco `text`).
- **Sem «Atualização» no topo nem «Histórico» no fim.** Na próxima gravação de cada um, a atualização funde-se no
  «Estado verificado» e nos «Próximos passos», e o texto velho sai. Não se reescrevem os 24 agora.
- **O histórico vai para o git**, não para o ficheiro: cada gravação é um commit, e `git log -p -- .context/HANDOFF-x.md`
  mostra o que foi. A decisão que dura vai para `docs/decisoes/`; o estudo, para `docs/pesquisas/` (Akita, p. 387).
- Para o script: esta ordem não parte nada (as três linhas valem em qualquer sítio antes da mensagem). Parte se
  mudar o nome `## Mensagem de retoma`, a cerca ` ```text `, ou se `Prioridade:` não começar pelo nível.

### Ideia 3: partir o handoff

**Faz sentido o fim** (a filha recebe só o que precisa: doc. subagentes e custos; Morg-laws §4). **Não faz sentido o
meio** de partir o ficheiro: são pequenos, um `@import` ou várias partes não poupam nada se a filha as ler todas, e
duas cópias do mesmo estado divergem (Akita, pp. 94, 99).

| Forma | Como | Contras |
|---|---|---|
| ➡️ **A. Briefing autocontido** | A mãe copia para o pedido só o objetivo da fase, os ficheiros, as linhas do «Descartado» que tocam a fase (literais), como se prova. Não manda ler o handoff. | A mãe gasta escrita; se esquecer uma linha do «Descartado», a filha repete o erro. |
| ➡️ **B. Secções pelo título** | Quando a filha continua o mesmo assunto: «do `HANDOFF-x.md`, leia só «Descartado» e «Próximos passos»» (ela acha-as com `grep -n "^## "` e lê com `offset`). | Os títulos têm de ser únicos; a filha pode ler tudo na mesma; contradiz o «Leia-o inteiro» da skill, que passa a valer só na retoma. |
| C. Um ficheiro por parte (`HANDOFF-x--fase-2.md`) | Cada parte num ficheiro. | Cada ficheiro vira um cartão na página da entrega, e sem as três linhas mostra «Sem prioridade escrita»; o estado duplica-se; o `test_docs_indices.py` pode exigir os cinco títulos em cada um (não verificado). |
| D. Índice no topo com números de linha | Uma tabela «secção → linhas». | Os números mudam a cada reescrita; a 80 linhas, o `grep -n "^## "` faz o mesmo de graça. |

E uma regra que não depende da forma: **a auditoria a frio nunca recebe o handoff**, só o objeto auditado e a
pergunta neutra (SQL AUDITADO NUMA SESSÃO NOVA RULE). Se um assunto não cabe em 16 KB, não se parte em partes:
parte-se em **dois assuntos**, dois handoffs, como a skill já manda («um por assunto»).

### Decisões do PO

1. Limite: manter 150 linhas e juntar ≤16 KB? ➡️ sim.
2. A «Atualização da entrega» no topo de 24 handoffs: fundir na próxima gravação de cada um (não agora)? ➡️ sim.
3. Histórico: só no git e em `docs/decisoes/`, nunca uma secção «Histórico» no handoff? ➡️ sim.
4. Briefing da filha: forma A por omissão, B quando continua o assunto, e a auditoria a frio nunca recebe o handoff? ➡️ sim.
5. Ficheiro por parte (C) ou índice com linhas (D)? ➡️ não.
6. Catraca de tamanho dos handoffs já? ➡️ não; só se voltarem a passar o limite.
7. Levar ao Morg-laws, no envio de sexta: a regra 4 na `orquestrando-sessoes` (§4) e as 1 a 3 na
   `passando-o-trabalho` (§2)? ➡️ sim. As três linhas e a mensagem de retoma ficam do ERP (só a página as lê).

Junta-se às 6 decisões de `.context/HANDOFF-contexto-das-sessoes-filhas.md`: a 4 daqui é a forma concreta da «E»
(molde de briefing) de lá.
