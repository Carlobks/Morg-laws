---
name: orquestrando-sessoes
description: Guia como dividir trabalho entre sessões de agente — quando abrir uma sessão nova em vez de continuar ou de usar sub-agentes, como escrever o pedido para uma leitura independente e como várias sessões convivem na mesma pasta sem se atropelar. Usar ao planejar trabalho grande, ao querer uma auditoria ou revisão independente, ou quando várias sessões ou pessoas mexem no mesmo repositório. Não usar para escrever o handoff, compactar, retomar o trabalho ou decidir se uma conversa que cresceu se compacta ou passa para uma sessão nova (é a passando-o-trabalho), para escrever o conteúdo das regras (é a escrevendo-regras-de-agente) nem para os comandos de git do dia a dia (é a git-e-commits).
---

# Orquestrando sessões

Trabalho grande com agentes falha menos quando cada pedaço tem dono, contexto limpo e um resultado que alguém confere. Esta skill diz como dividir e como evitar que sessões estraguem o trabalho umas das outras.

## 1. Sub-agentes ou sessões novas: uma escolha, não uma lei

| | Sub-agente | Sessão nova |
|---|---|---|
| Quem vê o trabalho | Só o agente que o lançou recebe um resumo | O dono abre a sessão, lê tudo e corrige a meio |
| Custo | Barato para buscas amplas e tarefas paralelas | Mais lento de abrir |
| Risco | O erro volta no mesmo tom confiante dos acertos; ninguém o vê a errar | Mais trabalho de coordenação |

**Quando escolher só sessões novas:** quando o dono do projeto quer ver e corrigir cada passo. Num projeto real, essa regra entrou porque um sub-agente não pode ser visto nem corrigido. Se escolher isto, escreva-o como regra do projeto e bloqueie a ferramenta nas permissões.

**Quando sub-agentes servem:** buscas que leem muitos arquivos e só precisam da conclusão, ou tarefas independentes em paralelo, com o resultado conferido depois.

## 2. Leitura independente: auditoria numa sessão nova

Quem escreveu um trabalho não o consegue auditar bem: lê o que quis dizer, não o que escreveu.

- Abra uma **sessão nova**, sem a conversa que produziu o trabalho.
- Escreva um pedido **neutro**: o objetivo, os arquivos, as fontes contra as quais conferir e o formato do relatório. **Não** diga a sua conclusão. Um auditor que recebe a hipótese tende a confirmá-la.
- **Numa verificação repetida,** a sessão nova fecha e grava as suas contagens **antes** de ler a verificação anterior, e só depois compara. Lida antes, a anterior vira a resposta esperada.
- Peça um **veredito** no topo ("aprovado", "aprovado com correções", "refazer"), cada achado com o arquivo e a linha da fonte, e a lista do que não verificou.
- O relatório volta como **dado, não como verdade**. Antes de agir, confira cada afirmação na fonte (um `grep` por termo, a licença no original), e marque à parte o que é juízo, que não se mede.
- Mudanças de risco (SQL que escreve em produção, permissões, segurança) passam sempre por uma auditoria destas antes do "sim" do dono.

## 3. Passar o trabalho (handoff)

Escrever o handoff, compactar e retomar são da skill `passando-o-trabalho`.

## 4. Várias sessões na mesma pasta

Quando várias sessões (ou pessoas) trabalham na mesma pasta, o índice do git e a branch são partilhados.

- **Commit sempre por caminho:** `git commit -F msg -- <arquivos>`. Um `git commit` sem caminhos leva tudo o que outra sessão deixou preparado.
- **Nunca `git stash`:** leva também os arquivos por commitar das outras sessões. Para comparar com o código antigo, troque só o seu arquivo, ou use `git worktree`.
- **Não commitar trabalho alheio.** O aviso de "arquivos por commitar" conta arquivos, não donos. Use `git log -1 -- <arquivo>` e a memória do que você mexeu.
- **Nada que estrague o disco compartilhado:** um script que troca arquivos por um tempo (testes de mutação, geradores) roda num `git worktree` à parte. Outra sessão que rode os testes ao mesmo tempo os vê falhar sem bug, e pode commitar o arquivo trocado.
- **Confirme o HEAD antes de pedir um reteste:** outra sessão pode ter mudado a branch, e o sintoma parece "a correção não funcionou".
- **`index.lock`:** o de outra sessão a commitar espera-se que saia, e nunca se apaga. Antes de culpar outro processo, veja **em que repositório** ele corre. Um lock seu, deixado por um comando interrompido, prova-se velho por três coisas: nenhum processo do git a correr, a hora do lock bate com a interrupção e o conteúdo do lock é o seu. Mesmo assim, renomeie-o em vez de o apagar.
- **Não lance um commit com hooks longos** enquanto a conversa está a pedir decisões ao dono: um "parar" a meio deixa o lock para trás.

## 5. Uma só branch: quando escolher

Trabalhar só na `main`, sem branches nem worktrees, simplifica a coordenação de muitas sessões numa pasta partilhada. O custo é que tudo o que entra fica logo no caminho de todos, e por isso os hooks têm de ser fortes. É uma escolha de projeto: escreva-a como tal.

## 6. O plano que o dono lê

- Mudança que mexe na tela ou em mais de três arquivos leva um plano numa **página visual** (antes e depois, em linguagem simples), não só em texto técnico.
- Se uma refatoração é precisa para não piorar uma catraca, ela entra no plano às claras, não escondida no meio.
- A skill do assunto carrega-se **antes** de mexer. Um hook que avisa depois de escrever chega tarde.

## Fontes

Ver [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#git-e-contas): código do git sobre o `index.lock` (`lockfile.c`). As regras de sessões vêm da prática do projeto de origem.
