# Linha de base do uso: quanto custava e como se comportava o trabalho com agentes antes das regras

Data: 2026-11-05 (as medições). Escrito em 2026-11-06. As fontes públicas foram lidas em 2026-11-06.

## Pergunta

Quanto custava, em uso do plano, e como se comportava o trabalho com agentes de código num projeto real, antes de
aplicar as regras deste repositório? E o que se vai medir depois, do mesmo jeito, para saber se as regras mudaram
alguma coisa?

Esta é a primeira de duas medições. A segunda vem quatro semanas depois de as regras entrarem no projeto, com a mesma
conta.

## Fontes

- **Medição privada do autor, não publicada.** Os registros exportados do **Token Use**, a ferramenta de medição
  usada, em três janelas (7 dias, 30 dias e desde o primeiro registro), e as três análises feitas sobre eles, cada
  número conferido contra os registros chamada a chamada. Os registros e as análises ficam privados.
- **O histórico do git do projeto**, contado em 2026-11-06.
- **Claude Code — boas práticas** — https://code.claude.com/docs/en/best-practices — Entrada no `FONTES.md`.
- **Claude Code — custos** — https://code.claude.com/docs/en/costs — Entrada no `FONTES.md`.
- **Anthropic — Building effective agents** — https://www.anthropic.com/engineering/building-effective-agents —
  Entrada no `FONTES.md`.
- **Anthropic — How we built our multi-agent research system** —
  https://www.anthropic.com/engineering/multi-agent-research-system — Entrada no `FONTES.md`.

**Sobre a ferramenta.** O Token Use é nomeado só para dizer de onde vêm os números. Estes achados são de um não
profissional, medindo o próprio uso, e não são uma crítica à ferramenta: os números dela batem com os registros; o
que se discute abaixo é só a leitura que ela faz deles para um jeito de trabalhar que não é o mais comum.

## O que se mediu

**O projeto.** Um sistema interno em produção, de uma pequena empresa de serviços, feito por uma pessoa só com
agentes de código. Quase todo o uso medido é dele: 98% do custo.

**A régua dos dólares.** O plano é uma assinatura **Max**, semanal, de valor fixo. Os dólares abaixo são o preço de
tabela que a ferramenta põe em cada chamada: **não são fatura**, servem de régua para comparar o que cada coisa gastou
do limite. Como o preço do modelo principal caiu no fim de setembro (reler o contexto ficou 2,5 vezes mais barato),
as comparações entre épocas usam também **preços constantes**: todas as chamadas recalculadas com o preço de hoje.

### O período e o volume

| Medida | Valor |
|---|---|
| Período dos registros | 2026-07-06 a 2026-11-05, 123 dias de calendário |
| Dias com uso | 52, nenhum no fim de semana, sempre em dois blocos fixos (manhã e tarde) |
| Sessões | 88 |
| Chamadas ao modelo | 23 926 (23 497 do Claude Code; 429 de outra ferramenta) |
| Horas com chamadas rodando | ~165 a 188 h (**estimativa**: a soma dos intervalos entre chamadas seguidas abaixo de 15 ou de 30 minutos) |
| Turnos de mais de 5 minutos | 772 (média de 823 s) |

### O gasto

| Medida | Valor |
|---|---|
| Total, a preços da época | **$5 300** |
| Total, a preços de hoje | **$3 744** (**estimativa**) |
| Por mês, a preços da época | julho $1 485 · agosto $765 · setembro $1 481 · outubro $1 121 · novembro (até o dia 5) $448 |
| Custo por chamada, a preços de hoje | $0,185 → $0,122 (−34%) |
| Uma semana do plano, na régua | ~$550–600 (**estimativa**); a semana em curso ia em $512 com o limite a **91%** |
| Orçamento por dia útil | ~$100, cerca de 18% do limite |

O limite chega a 100% todas as semanas, de propósito: o plano é para ser usado. O problema é chegar lá **antes do
fim da semana** e ter de parar.

### Por dia de uso: antes, nos últimos 30 dias e nos últimos 7

«Antes» são os 34 dias de uso anteriores a 2026-10-08. Os 7 dias estão dentro dos 30.

| Medida (por dia de uso) | Antes | 30 dias | 7 dias |
|---|---|---|---|
| Custo, a preços constantes | $64 | $87 | **$110** (+72%) |
| Chamadas | 345 | 654 | **902** |
| Contexto médio relido em cada chamada | 488 mil tokens | 371 mil | **309 mil** |
| Chamadas acima de 500 mil tokens | 46% | 24% | 11% |
| Regravações do contexto depois de mais de 1 h parada | 1,6 | 4,9 | **9,0** |
| Turnos acordados por avisos de outras sessões (% do custo) | 2% | 25,7% | **42,7%** |
| Sessões com chamadas | 1,3 | 7,1 | **11,8** |
| Chamadas em Sonnet ou Haiku | 17,5% | 3,6% | **0,6%** |

### Para onde vai o dinheiro

- **Composição do custo** (família Opus, todo o período): reler o contexto **64%**, regravá-lo 27%, a saída e a
  entrada nova 9%. O gasto é quase todo o tamanho da conversa, relida em cada chamada.
- **Concentração:** as 3 maiores sessões fazem **66%** do custo, e as sessões abertas 3 dias ou mais, **80%**. As duas
  maiores ficaram abertas 35 e 40 dias, com contexto médio perto de 500 mil e máximo perto de 1 milhão.
- **Modelo:** a família Opus fez 91,7% do custo. O Sonnet teve de 31% a 51% das chamadas em algumas semanas de julho e
  agosto, custava cerca de metade por chamada e deixou de ser usado em setembro, sem regra que o dissesse.

### O que é antigo e o que é novo

- **Antigo, e melhorando:** o contexto grande (488 → 309 mil) e as sessões de semanas (a mais longa de outubro durou
  23 dias, não 40).
- **Antigo, e já resolvido:** os sub-agentes. A ferramenta que os lança foi chamada 28, 25, 3, 5 e 0 vezes de julho a
  novembro, depois de uma regra escrita que os proíbe.
- **Novo, desde meados de outubro:** muitas sessões em paralelo, uma sessão que orquestra as outras e acorda a cada
  aviso, as regravações depois de pausas, carregar skills em quase todo turno (de 5% para 17% do custo) e 2,6 vezes mais
  chamadas por dia. Coincide com **mais trabalho de suporte desde meados de outubro**, com interrupções no meio do dia.

### Os commits do projeto

Contados no git em 2026-11-06, pela data do autor.

- **Total:** 2 755 commits, desde **março de 2026**.
- **Com co-autoria de agente**, por mês:

  | Julho | Agosto | Setembro | Outubro | Novembro (até o dia 6) |
  |---|---|---|---|---|
  | 223 | 725 | 472 | 791 | 195 |

- Antes de julho não há commit com co-autoria de agente registrada.
- Nas duas lacunas dos registros de uso de agosto e de setembro há 533 commits, quase todos com agente: o trabalho
  foi feito em outra máquina. **Os registros de uso medem uma máquina; os commits medem o projeto todo.** Por isso, um
  custo dividido por commits sai errado nesses meses.

### O que a ferramenta apontou e o que se confirmou

Conferido chamada a chamada:

| Achado | Veredito | Por quê, numa linha |
|---|---|---|
| Mega Sessions | Verdadeiro, e subestimado | As sessões abertas por dias valem 80% do custo |
| Session Drift | Verdadeiro | É o mesmo problema: a sessão longa acaba misturando assuntos |
| Runaway Agent Loops | Em parte | Os turnos com 40 ferramentas ou mais (178, média de 63) são fases grandes, não um agente andando em círculos |
| Slow Responses | Sintoma | Vem do contexto grande e das fases grandes |
| Verbose Model Output | Pesa pouco | A saída é 9% a 15% do custo |
| Broken Flow State | Em parte | Há muita troca entre sessões, mas vem do método de trabalho |
| Repeated Prompts | Falso alarme | Cada chamada de um mesmo turno conta como um pedido repetido |
| Speed Accept | Falso alarme | A mensagem seguinte era automática (um aviso, uma skill), não um aceite da pessoa |
| Vibe Coding | Falso alarme | Eram sessões filhas que começam de um plano já aprovado |
| Copy-Paste Blindness | Falso alarme | Sessões pequenas, uma delas seguida de auditoria |
| Lazy Prompting | Falso alarme | Respostas curtas a perguntas com opções: aí, curto é o certo |
| Low Constraint | Falso alarme | O detector não lê português; cerca de 25% dos pedidos longos têm restrições |
| Frustration Signals | Falso alarme | Maiúsculas de siglas e de prudência |
| Single-Project Tunnel Vision | Ignorar | Trabalhar num projeto principal não é defeito |

A ferramenta conta bem; os juízos supõem quem trabalha sozinho, em inglês e sem sessões filhas.

## O que não se verificou

- **O limite exato do plano.** Os registros não trazem o limite; a equivalência de ~$550–600 por semana é uma ordem
  de grandeza, só para preços de hoje.
- **A qualidade.** Não se sabe se o Sonnet ou conversas mais curtas fariam um trabalho pior, nem quantos erros as
  auditorias evitaram.
- **A causa da subida desde meados de outubro.** O método das sessões filhas, mais trabalho de suporte e mais volume
  coincidem no tempo; os dados não os separam.
- **O histórico incompleto.** Parte foi em outra máquina e, antes de julho, em outra ferramenta. Os números de antes
  de outubro ficam abaixo do real: a coluna «antes» serve só como indicação.
- **Os sub-agentes e as compactações.** Os registros não os separam bem; só há a contagem das chamadas à ferramenta.
- **As horas.** São uma estimativa do tempo com chamadas rodando, não do tempo da pessoa no computador, e dependem do
  limiar (15 ou 30 minutos).
- **Os preços constantes** assumem o mesmo uso com o preço de hoje; o preço de cada modelo foi deduzido dos próprios
  custos dos registros.
- **Os commits** contam a data do autor e incluem os merges.

## Conclusão

**Os cinco problemas**, cada um ligado ao que as regras deste repositório já têm (ou ainda não):

| Problema | O número que o prova | O que já existe aqui |
|---|---|---|
| Conversa comprida demais, relida em cada chamada | 309 mil tokens por chamada nos 7 dias (eram 488 mil); reler é 64% do custo | Só texto: a skill `passando-o-trabalho` manda compactar à mão. O limiar em tokens está por decidir |
| A sessão que orquestra vive dias e acorda a cada filha | Os avisos de outras sessões passaram de 2% para 42,7% do custo | Por fazer |
| Voltar a uma sessão grande depois de mais de 1 h parada | 1,6 → 9,0 regravações por dia | Por fazer: está só descrito em `pesquisas/2026-11-02-compactacao-claude-code-e-codex.md` |
| O modelo mais caro em tudo | 99% das chamadas em Opus nos 7 dias | Só texto, em `biblia-akita/` (escolher pelo preço), sem aplicação |
| Muito volume por dia | 345 → 902 chamadas e 1,3 → 11,8 sessões por dia | Por fazer |

Dos comportamentos verdadeiros ou em parte, **nenhum** é hoje recusado por uma máquina (hook, teste ou CI): metade
está só em texto e metade não tem proteção nenhuma. As fontes públicas dizem o mesmo por outras palavras: cada pedido
manda a conversa inteira, a primeira mensagem depois de a cache expirar reprocessa tudo, e uma sessão nova sai mais
barata quando o histórico não faz falta (boas práticas e custos do Claude Code); vários agentes gastam muito mais
tokens do que um só, e só compensam quando a tarefa vale esse custo (os dois artigos da Anthropic).

**Como se compara depois.**

1. **A mesma ferramenta e as mesmas janelas** (7 e 30 dias), quatro semanas depois de as regras entrarem no projeto,
   com as mesmas contas e a mesma estimativa das horas.
2. **A preços constantes**: senão, uma mudança de preço parece efeito das regras.
3. **Por dia de uso e por semana do plano**, não por mês. A medida principal é **em que dia da semana o limite chega a
   100%** e o **% do limite por dia útil** (alvo: 18% ou menos). O objetivo não é gastar menos: é o limite durar a
   semana inteira.
4. **Um indicador por problema:**

   | Problema | Indicador |
   |---|---|
   | Conversa comprida | Contexto médio e parte das chamadas acima de 150 mil tokens |
   | A sessão que orquestra | Avisos de outras sessões (% do custo) |
   | Pausa de mais de 1 h | Regravações depois de mais de 1 h, por dia |
   | Modelo mais caro em tudo | Parte das chamadas em Sonnet ou Haiku |
   | Volume | Sessões com chamadas por dia |

5. **Um controle de produção**, para separar «gastou menos» de «trabalhou menos»: os commits com co-autoria de agente
   por dia útil e os commits de correção por mês, tirados do git (que vê todas as máquinas) para os dois períodos.
6. **O que não se vai poder concluir:** a qualidade, a menos que se meça à parte (por exemplo, as reprovações das
   auditorias a frio).
7. **A publicação:** a segunda medição entra como `pesquisas/AAAA-MM-DD-uso-depois-das-regras.md`, com a mesma
   tabela lado a lado, e aponta para esta.
