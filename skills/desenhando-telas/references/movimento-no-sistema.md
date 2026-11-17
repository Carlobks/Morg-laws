# Movimento no sistema

As tabelas do movimento de uma tela de sistema, com a fonte de cada número. As fontes de terceiros foram lidas nos
commits fixos e estão destiladas com palavras nossas; o titular de cada uma está no
[`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#interface-e-acessibilidade). Um número sem
fonte diz «nosso» e é um ponto de partida, a calibrar.

Os limites de acessibilidade do movimento (o movimento reduzido, a pausa do que dura mais de 5 s, os movimentos que
mexem com o equilíbrio) estão na `cuidando-da-acessibilidade` e não se repetem aqui.

## Anima ou não anima

| Com que frequência | O que fazer | Fonte |
|---|---|---|
| Centenas de vezes por dia: atalhos, paleta de comandos, trocar de vista | Sem animação | Emil Kowalski (`emil-design-eng`); Damola Akinleye (`interface-design`) |
| Dezenas de vezes por dia: navegar numa lista, hover, abrir uma linha | Pouca ou nenhuma | Emil Kowalski (`emil-design-eng`) |
| Mover um cartão, pelo mouse ou pelo teclado | Anima, curto: confirma para onde o cartão foi | os ensaios às cegas de novembro de 2026 |
| Às vezes: modal, gaveta, aviso | Animação normal | Emil Kowalski (`emil-design-eng`) |
| Uma vez por visita: a entrada do painel | Escalonada, curta | Emil Kowalski (`choreograph`); os ensaios às cegas |

A fonte de terceiros diz para não animar nada que o teclado dispara. Os ensaios mostraram a exceção: mover um cartão
pelo teclado com uma animação curta foi elogiado, porque a pessoa precisa ver onde o cartão caiu. A regra fica: o
**atalho** não anima; o **objeto que muda de lugar** anima.

## Durações

| O quê | Duração | Fonte |
|---|---|---|
| Pressão de botão | 100–160 ms | Emil Kowalski (`emil-design-eng`) |
| Tooltip, popover pequeno | 125–200 ms | idem |
| Menu, seleção | 150–250 ms | idem |
| Modal, gaveta | 200–500 ms | idem |
| O resto da interface de sistema | abaixo de 300 ms | idem; Damola Akinleye (`interface-design`) |
| Escalonamento da entrada | 30–80 ms entre itens, o grupo todo abaixo de cerca de 300 ms | Emil Kowalski (`choreograph`) |
| A lateral acompanhando o scroll (com script; ver `kanban-ficha-painel.md`) | ≤ 300 ms, só `transform` | nosso |
| O cartão deslizando para a posição nova pelo teclado | 150–250 ms | nosso, dentro da faixa do menu |

As saídas são mais curtas e mais simples do que as entradas, e saem todas juntas, sem escalonar ao contrário
(Emil Kowalski, `choreograph`).

## Curvas

| Para quê | Curva | Fonte |
|---|---|---|
| Entrar, responder a uma ação | `cubic-bezier(0.23, 1, 0.32, 1)` (saída forte) | Emil Kowalski (`emil-design-eng`); Damola Akinleye (`interface-design`) |
| Algo que já está na tela e muda de lugar | `cubic-bezier(0.77, 0, 0.175, 1)` (entrada e saída fortes) | idem |
| Nunca | `ease-in` | idem: a resposta fica parada justo no começo, quando a pessoa procura o sinal de que o clique contou |

## Escala e origem

| O quê | Valor | Fonte |
|---|---|---|
| Pressão no `:active` | `scale(0.96)` a `scale(0.97)`; nunca abaixo de 0,95 | Jakub Krehel (`make-interfaces-feel-better`) usa 0,96; Emil Kowalski (`emil-design-eng`) usa 0,97 |
| Entrada de um elemento | de `scale(0.95)` com opacidade 0; nunca de `scale(0)` | Emil Kowalski (`emil-design-eng`) |
| Origem do popover | o botão que o abriu (`transform-origin`); o modal fica no centro | idem |

## A mola e o arrasto

Vêm da `apple-design` de Emil Kowalski, que traduz para a web a palestra *Designing Fluid Interfaces* da Apple
(WWDC 2018).

- **A mola se descreve por dois números:** o **amortecimento** (1,0 assenta sem ressalto; abaixo disso, passa do
  ponto e volta) e a **resposta** (em segundos, quanto tempo leva a chegar perto do alvo; não é uma duração fixa).
- **Padrão da interface:** amortecimento 1,0, resposta de 0,3 a 0,4 s. Um ressalto leve (amortecimento ≈ 0,8) só
  quando o próprio gesto trouxe impulso, como um cartão atirado com força; ao soltar um cartão no lugar, sem
  ressalto.
- **Seguir o ponteiro 1:1** durante todo o arrasto, e respeitar o ponto onde o elemento foi pego, sem pular para o
  centro.
- **A velocidade passa do gesto para a mola:** ao soltar, a animação começa na velocidade do ponteiro, para não haver
  costura entre arrastar e assentar. Algumas bibliotecas pedem a velocidade relativa: a do gesto dividida pela
  distância que falta até o alvo.
- **Projetar onde o gesto vai parar** antes de escolher o destino: o ponto final é a posição atual mais
  `(v / 1000) × d / (1 − d)`, com `v` em px/s e `d ≈ 0,998` (o valor do scroll normal; 0,99 para um efeito mais seco).
  O destino é a posição válida mais perto desse ponto projetado, não a mais perto do ponto onde o dedo soltou.
- **Interromper a qualquer momento:** um elemento em movimento pode ser pego de novo e muda de alvo sem esperar a
  animação acabar. Para o que a pessoa arrasta, mola; transições de CSS e `@keyframes` não se deixam pegar no meio.
- **Um limiar de cerca de 10 px** antes de decidir que o toque virou arrasto, para um toque não mover o cartão sem
  querer.

## A coreografia da entrada

Da `choreograph` de Emil Kowalski, com palavras nossas:

- **Uma entrada por contêiner:** escolha entre animar o bloco e animar os filhos dele. Com os dois, a tela só fica
  pronta quando a última peça de dentro chega, e a espera soma.
- **Sem escalonar o que se usa o dia todo** (linhas de lista, itens de menu, o conteúdo de uma aba): esses aparecem
  juntos, ou sem animação.
- **Escalonamento igual em todos é mecânico:** o mais importante entra primeiro e anda um pouco mais; o de apoio, menos;
  o decorativo só esmaece no lugar.
- **A animação não segura a mão de ninguém:** um botão que já apareceu responde ao clique, mesmo que o bloco ao lado
  ainda esteja entrando.

## Verificar

- Uma animação se verifica pelo que pinta: o valor resolvido (`getComputedStyle`) ou os pixels entre quadros, não a
  variável que a alimenta. Vem da versão anterior desta skill, de um incidente do projeto de origem.
- Reveja a 10 % da velocidade (o painel de animações do navegador deixa desacelerar): é onde se vê o salto no começo, o
  vizinho que se mexe depois e a mola que passa do ponto (Jakub Krehel, `make-interfaces-feel-better`).
