---
name: orquestrando-sessoes
description: Guia como dividir trabalho entre sessões de agente — quando abrir uma sessão nova em vez de continuar ou de usar sub-agentes, como escrever o pedido para uma leitura independente e como várias sessões convivem na mesma pasta sem se atropelar. Usar ao planejar trabalho grande ou dividido em fases, ao abrir a fase seguinte, ao escrever o pedido de uma sessão filha e escolher o modelo dela, ao querer uma auditoria ou revisão independente, quando a sessão que orquestra já vive vários dias, ou quando várias sessões ou pessoas mexem no mesmo repositório. Não usar para escrever o handoff, compactar, retomar o trabalho ou decidir se uma conversa que cresceu se compacta ou passa para uma sessão nova (é a passando-o-trabalho), para escrever o conteúdo das regras (é a escrevendo-regras-de-agente) nem para os comandos de git do dia a dia (é a git-e-commits).
---

# Orquestrando sessões

Trabalho grande com agentes falha menos quando cada pedaço tem dono, contexto limpo e um resultado que alguém confere. Esta skill diz como dividir e como evitar que sessões estraguem o trabalho umas das outras.

## 1. Sub-agentes ou sessões novas: uma escolha, não uma lei

| | Sub-agente | Sessão nova |
|---|---|---|
| Quem vê o trabalho | Só o agente que o lançou recebe um resumo | O dono abre a sessão, lê tudo e corrige a meio |
| Custo | Barato para buscas amplas e tarefas paralelas | Mais lento de abrir |
| Risco | O erro volta no mesmo tom confiante dos acertos; ninguém o vê a errar | Mais trabalho de coordenação |

**Quando escolher só sessões novas:** quando o dono do projeto quer ver e corrigir cada passo. Num projeto real, essa regra entrou porque um sub-agente não pode ser visto nem corrigido. Se escolher isto, escreva-o como regra do projeto e bloqueie a ferramenta nas permissões: no Claude Code, `"Agent"` na coluna `deny` (o [passo 8 da instalação dos moldes](https://github.com/Carlobks/Morg-laws/blob/main/modelos/README.md#como-instalar)).

**Quando sub-agentes servem:** buscas que leem muitos arquivos e só precisam da conclusão, ou tarefas independentes em paralelo, com o resultado conferido depois.

## 2. Leitura independente: auditoria numa sessão nova

Quem escreveu um trabalho não o consegue auditar bem: lê o que quis dizer, não o que escreveu.

- Abra uma **sessão nova**, sem a conversa que produziu o trabalho.
- Escreva um pedido **neutro**: o objetivo, os arquivos, as fontes contra as quais conferir e o formato do relatório. **Não** diga a sua conclusão. Um auditor que recebe a hipótese tende a confirmá-la.
- **Numa verificação repetida,** a sessão nova fecha e grava as suas contagens **antes** de ler a verificação anterior, e só depois compara. Lida antes, a anterior vira a resposta esperada.
- Peça um **veredito** no topo ("aprovado", "aprovado com correções", "refazer"), cada achado com o arquivo e a linha da fonte, e a lista do que não verificou.
- O relatório volta como **dado, não como verdade**. Antes de levar um achado ao dono, uma filha só de conferência confere cada afirmação na fonte (um `grep` por termo, a licença no original); antes de agir, pode conferi-la a filha que corrige. Marca à parte o que é juízo, que não se mede. A orquestradora lê só o veredito e o resultado dessa conferência (seção 4).
- Mudanças de risco (SQL que escreve em produção, permissões, segurança) passam sempre por uma auditoria destas antes do "sim" do dono.

## 3. Fases: uma de cada vez, cada uma curta

- **A fase seguinte só abre depois da auditoria da anterior** e das correções que ela pediu. Várias fases abertas ao mesmo tempo multiplicam as sessões vivas, e cada uma que acorda relê o contexto inteiro.
- **Uma fase cabe numa sessão curta,** abaixo do limiar de compactação da skill `passando-o-trabalho` (~150 mil tokens). Uma fase que não cabe parte-se no plano, antes de começar, e não no meio.

## 4. A orquestradora magra e diária

Num trabalho com várias fases, uma sessão orquestra: escreve o pedido de cada filha, recebe o resultado e decide o passo seguinte. Cada aviso de uma filha acorda a orquestradora, e cada vez que ela acorda relê o contexto inteiro. Viva vários dias, cada aviso fica mais caro que o anterior.

- **Só encaminha:** ler código, implementar e auditar ficam nas filhas. A orquestradora escreve pedidos e decide.
- **Lê só o veredito:** o topo do relatório, a lista do que ficou por verificar e o resultado da conferência, não o relatório inteiro nem os diffs. Antes de um achado ir ao dono, uma filha só de conferência confere cada afirmação na fonte; antes de agir sobre ele, pode conferi-la a filha que corrige.
- **As filhas avisam no fim da fase,** numa mensagem curta: o veredito, o commit e o que ficou por fazer. Um aviso no meio acorda a orquestradora sem decisão para tomar.
- **Renova-se todo dia:** no fim do dia, grava o handoff (skill `passando-o-trabalho`) e fecha; no dia seguinte, uma orquestradora nova o lê.
- **O pedido da filha** leva o objetivo, os arquivos, o que já se descartou, como se prova e o modelo, por esta tabela:

| Tarefa da filha | Modelo |
|---|---|
| Buscas, contagens, leituras mecânicas, revisão de texto | O pequeno (Haiku) |
| Implementar um plano aprovado, escrever testes, aplicar as correções de uma auditoria | O médio (Sonnet) |
| Escrever um plano, auditar a frio, segurança, bug difícil | O maior (Opus) |

Os nomes entre parênteses são os do Claude Code; em outra ferramenta, use o modelo do mesmo tamanho. O modelo escolhe-se ao abrir a filha, e não no `settings.json`: um `model` fixo valeria para todas. Um modelo mais barato pode baixar a qualidade; por isso o plano e a auditoria ficam no maior. Uma segunda auditoria, em outro modelo ou em outra ferramenta, continua a valer.

## 5. Passar o trabalho (handoff)

Escrever o handoff, compactar e retomar são da skill `passando-o-trabalho`.

## 6. Várias sessões na mesma pasta

Quando várias sessões (ou pessoas) trabalham na mesma pasta, o índice do git e a branch são partilhados.

- **Commit sempre por caminho:** `git commit -F msg -- <arquivos>`. Um `git commit` sem caminhos leva tudo o que outra sessão deixou preparado.
- **Nunca `git stash`:** leva também os arquivos por commitar das outras sessões. Para comparar com o código antigo, troque só o seu arquivo, ou use `git worktree`.
- **Não commitar trabalho alheio.** O aviso de "arquivos por commitar" conta arquivos, não donos. Use `git log -1 -- <arquivo>` e a memória do que você mexeu.
- **Nada que estrague o disco compartilhado:** um script que troca arquivos por um tempo (testes de mutação, geradores) roda num `git worktree` à parte. Outra sessão que rode os testes ao mesmo tempo os vê falhar sem bug, e pode commitar o arquivo trocado.
- **Confirme o HEAD antes de pedir um reteste:** outra sessão pode ter mudado a branch, e o sintoma parece "a correção não funcionou".
- **`index.lock`:** o de outra sessão a commitar espera-se que saia, e nunca se apaga. Antes de culpar outro processo, veja **em que repositório** ele corre. Um lock seu, deixado por um comando interrompido, prova-se velho por três coisas: nenhum processo do git a correr, a hora do lock bate com a interrupção e o conteúdo do lock é o seu. Mesmo assim, renomeie-o em vez de o apagar.
- **Não lance um commit com hooks longos** enquanto a conversa está a pedir decisões ao dono: um "parar" a meio deixa o lock para trás.

## 7. Uma só branch: quando escolher

Trabalhar só na `main`, sem branches nem worktrees, simplifica a coordenação de muitas sessões numa pasta partilhada. O custo é que tudo o que entra fica logo no caminho de todos, e por isso os hooks têm de ser fortes. É uma escolha de projeto: escreva-a como tal.

## 8. O plano que o dono lê

- Mudança que mexe na tela ou em mais de três arquivos leva um plano numa **página visual** (antes e depois, em linguagem simples), não só em texto técnico.
- Se uma refatoração é precisa para não piorar uma catraca, ela entra no plano às claras, não escondida no meio.
- A skill do assunto carrega-se **antes** de mexer. Um hook que avisa depois de escrever chega tarde.

## Fontes

Ver [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#git-e-contas): código do git sobre o `index.lock` (`lockfile.c`); e [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#uso-e-custo-de-agentes): as boas práticas e os custos do Claude Code (a conversa relida a cada pedido, o aviso que acorda uma sessão parada, o modelo pela tarefa) e a [linha de base do uso](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-05-linha-de-base-do-uso.md). As regras de sessões, das fases e da orquestradora vêm da prática do projeto de origem.
