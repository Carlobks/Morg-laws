# Pedidos prontos

Esta parte reúne os pedidos principais que as outras partes ensinam, já escritos para você copiar. Cada um vem num bloco, com uma linha antes que diz quando usar e uma remissão ao procedimento que o explica. Os exemplos falam de um projeto inventado, um aplicativo de lista de compras, e você troca os trechos entre sinais de menor e maior pelo que é seu. Os pedidos seguem as skills [`comecando-um-projeto`](https://github.com/Carlobks/Morg-laws/blob/main/skills/comecando-um-projeto/SKILL.md), [`orquestrando-sessoes`](https://github.com/Carlobks/Morg-laws/blob/main/skills/orquestrando-sessoes/SKILL.md) e [`pondo-o-plano-a-prova`](https://github.com/Carlobks/Morg-laws/blob/main/skills/pondo-o-plano-a-prova/SKILL.md), e cada seção abaixo diz de qual.

## A primeira mensagem

Use ao abrir o agente num projeto, novo ou que já existe, antes de pedir qualquer código. Explicado no procedimento P5, na parte 02.

```
/comecando-um-projeto Quero começar (ou organizar) este projeto com você. Antes de escrever código, me faça as perguntas em rondas, confirme comigo cada resposta e deixe escritos o documento do projeto, o AGENTS.md, o primeiro plano e as decisões de arquitetura.
```

No Codex, o mesmo texto, com `$` no lugar da barra ([documentação do Codex](https://developers.openai.com/codex/skills)).

A fonte é a seção 6 da skill [`comecando-um-projeto`](https://github.com/Carlobks/Morg-laws/blob/main/skills/comecando-um-projeto/SKILL.md), a mensagem inicial, igual nas duas ferramentas fora o prefixo.

## Uma tarefa nas quatro partes

Use quando a tarefa é de verdade e você quer o resultado de primeira. Explicado no procedimento P6, na parte 03. A terceira parte, o que você não quer, é a que mais vale, e o critério de pronto da quarta é algo que o agente consegue conferir sozinho.

```
O que quero: que a lista de compras mostre o total de itens marcados no topo da tela.
Como: acrescentar um contador à tela que já existe; se achar melhor outro caminho, diga antes de começar.
O que não quero: mexer no cadastro de itens, mudar o desenho dos botões ou acrescentar uma biblioteca nova.
Como vou saber que ficou certo: um teste novo para o contador passa, os testes antigos continuam passando, e você me mostra a tela com três itens marcados.
```

A fonte é a seção 6 da skill [`pondo-o-plano-a-prova`](https://github.com/Carlobks/Morg-laws/blob/main/skills/pondo-o-plano-a-prova/SKILL.md): o resumo que ela manda entregar tem o objetivo, o que fica de fora e a prova de pronto, as mesmas peças do pedido.

## O oráculo

Use junto com uma tarefa que muda algo que a pessoa vê, antes de o agente começar. Explicado no procedimento P7, na parte 03.

```
Oráculo
- Dado <a situação>, quando <a pessoa faz X>, então <o que ela vê ou o estado que fica>.
- Continua igual: <o que não se mexe>, conferido por <tela, comando, número>.
```

A fonte é a seção 3 da skill [`pondo-o-plano-a-prova`](https://github.com/Carlobks/Morg-laws/blob/main/skills/pondo-o-plano-a-prova/SKILL.md), que traz o molde e pede pelo menos uma linha “Continua igual”.

## Pôr o plano à prova

Use quando o pedido é grande, antes de o agente executar qualquer coisa. Explicado no procedimento P9, na parte 03. Para uma tarefa pequena e clara, não use: ela dispensa as perguntas.

```
Antes de começar, ponha este plano à prova. Leia primeiro o que puder ler no projeto e só pergunte o que depende de mim.
Faça as perguntas em rondas de no máximo quatro, cada uma com opções e a recomendada marcada com ➡️, e o porquê dela numa frase.
No fim, entregue um resumo curto: o objetivo, o que fica de fora, como vou saber que ficou pronto, o que não tem volta e quem decide o quê.
Eu o confirmo antes de você começar. Se eu disser “chega”, pare de perguntar.
```

A fonte são as seções 4 e 6 da skill [`pondo-o-plano-a-prova`](https://github.com/Carlobks/Morg-laws/blob/main/skills/pondo-o-plano-a-prova/SKILL.md): como perguntar e o que entregar no fim.

## Pedir o plano

Use quando a mudança mexe em vários arquivos, antes de o agente escrever qualquer coisa. Explicado no procedimento P18, na parte 05. Leia o plano e só então diga “sim”.

```
Antes de mexer em qualquer arquivo, me entregue um plano: o que muda, em quais arquivos, em que ordem e como cada passo se prova.
Quando houver uma decisão que é minha, pergunte, explicada, com a opção recomendada marcada.
Não comece antes do meu “sim”.
```

A fonte é a seção 8 da skill [`orquestrando-sessoes`](https://github.com/Carlobks/Morg-laws/blob/main/skills/orquestrando-sessoes/SKILL.md), o plano que o dono lê, e a seção 6 da [`pondo-o-plano-a-prova`](https://github.com/Carlobks/Morg-laws/blob/main/skills/pondo-o-plano-a-prova/SKILL.md), o resumo que o dono confirma antes de começar.

## Abrir uma sessão filha

Use quando um passo do plano é trabalho de verdade e merece uma sessão só dele. Explicado no procedimento P11, na parte 04. O que a filha não faz tem de estar escrito, porque ela faz a mais, e o que já falhou também, porque ela o repete.

```
Título: ATIVO | LISTA · implementação do passo 2

Implemente o passo 2 do plano em <caminho do plano>. Você trabalha na pasta do projeto, em commits locais, sem push.
Antes de começar, confira que a árvore está limpa e que o último commit é <o combinado>.

Leia primeiro, e só isto: o plano (as seções 2 e 4), as regras do projeto e os testes que não podem quebrar.
O que se faz é o que o plano manda, e mais nada. Se algo não bater, não improvise: registre um desvio.
Já falhou e não se repete: <o que se tentou e não deu>.

Em cada commit: adicione só os caminhos dele, rode os testes, commite por caminho. Um commit por passo.
Está proibido: ler segredos, escrever no banco, lançar sub-agentes, fazer push.
O relatório vai para <arquivo do relatório>: os commits, a prova de cada passo, os desvios e o que não se verificou.
Quando acabar, troque o título para OK e avise num parágrafo.
```

A fonte são as seções 4 e 6 da skill [`orquestrando-sessoes`](https://github.com/Carlobks/Morg-laws/blob/main/skills/orquestrando-sessoes/SKILL.md): o que leva o pedido da filha, o título e o commit por caminho. A escolha do modelo da filha está no procedimento P12.

## O papel da orquestradora

Use ao abrir a sessão que orquestra um trabalho de várias fases. Explicado no procedimento P14, na parte 04.

```
Papel: escrever os pedidos das filhas, receber os resultados, conferir cada um por amostra no git,
levar as decisões ao dono e registrá-las. Mais ninguém as registra.
Não faz: implementar, auditar, lançar sub-agentes.
Cada fase vai para uma sessão nova, com o modelo escolhido na hora: o maior para plano, auditoria
e conferência; o médio para implementar e corrigir.
Quando uma filha acaba, chega um aviso curto. Em cada troca de fase: handoff gravado, depois compactar.
```

A fonte é a seção 4 da skill [`orquestrando-sessoes`](https://github.com/Carlobks/Morg-laws/blob/main/skills/orquestrando-sessoes/SKILL.md), a orquestradora magra e diária: ela só encaminha, lê só o veredito e se renova todo dia.

## Uma auditoria a frio

Use quando um trabalho está pronto e você quer uma leitura independente, antes de levá-lo adiante. Explicado no procedimento P15, na parte 04. Abra uma sessão nova, no maior modelo, e não conte a ela o que você acha do trabalho: um auditor que recebe a conclusão tende a confirmá-la.

```
Audite, só lendo, o trabalho em <pasta ou arquivos>. Você não escreve nada no projeto.
Objetivo do trabalho: <uma frase>.
Confira o trabalho contra estas fontes: <o plano, as regras do projeto, os testes>.
Entregue o relatório em <arquivo do relatório>, com um veredito no topo (“aprovado”, “aprovado com correções” ou “refazer”),
cada achado com o arquivo e a linha da fonte onde se vê, e no fim a lista do que você não verificou.
Marque à parte o que é juízo, e não medida.
```

A fonte é a seção 2 da skill [`orquestrando-sessoes`](https://github.com/Carlobks/Morg-laws/blob/main/skills/orquestrando-sessoes/SKILL.md), a leitura independente numa sessão nova.

## Uma conferência

Use depois da auditoria, antes de agir sobre o relatório. Explicado no procedimento P15, na parte 04. A conferência é outra sessão: o relatório volta a você como dado, e não como verdade.

```
Confira o relatório em <arquivo do relatório>. Você não escreve nada no projeto.
Para cada achado, abra a fonte que ele cita e diga se ela diz o que o relatório afirma, com um grep por termo.
Entregue, por achado: confirmado, afinado (diga a correção que a fonte permite) ou não confirmado, e a prova.
Se a correção que o relatório propõe puder reprovar o que o próprio texto precisa escrever, diga isso.
No fim, a lista do que você não conseguiu conferir.
```

A fonte é a mesma seção 2 da skill [`orquestrando-sessoes`](https://github.com/Carlobks/Morg-laws/blob/main/skills/orquestrando-sessoes/SKILL.md): antes de levar um achado ao dono, uma sessão só de conferência o confere na fonte.

## Passar o trabalho antes de compactar

Use quando a conversa está longa e vai ser compactada, ou quando o trabalho vai parar por mais de uma hora. Explicado no procedimento P16, na parte 04.

```
Antes de compactar, grave o handoff deste assunto em .context/HANDOFF-<assunto>.md, no molde de seis seções:
objetivo, estado verificado, decisões e porquê, descartado, próximos passos e cuidados.
O estado verificado vem do git (status, log e o resultado dos testes), e não da sua memória.
Ponha em “Descartado” o que já falhou e não se repete. Commite só esse arquivo, pelo caminho.
Depois, me dê o comando de compactar pronto para colar.
```

A fonte são as seções 1 a 4 da skill [`passando-o-trabalho`](https://github.com/Carlobks/Morg-laws/blob/main/skills/passando-o-trabalho/SKILL.md): conferir o estado, gravar o handoff, commitá-lo sozinho e compactar. A [`orquestrando-sessoes`](https://github.com/Carlobks/Morg-laws/blob/main/skills/orquestrando-sessoes/SKILL.md) manda essa tarefa para ela.

## Ao retomar

Use na sessão nova, depois de compactar ou no dia seguinte. Explicado no procedimento P16, na parte 04.

```
Leia .context/HANDOFF-<assunto>.md inteiro. Depois rode git status -s e git log -3 e diga se batem com o que o arquivo afirma.
Se não baterem, o que vale é o git. Não comece nada antes de eu confirmar o que você entendeu.
```

A fonte é a seção 5 da skill [`passando-o-trabalho`](https://github.com/Carlobks/Morg-laws/blob/main/skills/passando-o-trabalho/SKILL.md), a retomada.
