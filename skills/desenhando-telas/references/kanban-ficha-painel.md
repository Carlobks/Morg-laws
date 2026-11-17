# O quadro, a ficha e o painel

Uma receita por tipo de tela de sistema, descrita por **papéis** (não por classes), para servir em qualquer stack. As
regras por trás de cada peça estão no `SKILL.md` da `desenhando-telas`; aqui fica a montagem. Os números marcados
«nosso» não têm fonte: são o ponto de partida, a calibrar com o uso.

## O quadro (Kanban)

**A estrutura.**

- **Cabeçalho do quadro:** o nome do quadro, o filtro ativo, a contagem total e **a legenda de teclas**, na mesma faixa.
  A legenda começa pelo jeito de entrar («Tab para entrar no quadro») e lista as de dentro (setas, espaço, Esc,
  o atalho do «Mover para»). Uma linha só, em texto de apoio, sempre visível.
- **Colunas:** uma por estado, na ordem do fluxo. O cabeçalho de cada coluna tem o nome, a contagem e, se houver, o
  limite de itens em trabalho («4 / 5»). **Cada coluna rola sozinha**, com o cabeçalho dela parado; a página não rola
  de lado no celular.
- **Cartão:** o título em duas linhas no máximo, uma linha de meta (o responsável, a data, um ícone por tipo) e os
  sinais de estado. Nada de descrição longa no cartão: ela vive na lateral de detalhe.
- **Bloqueado ou atrasado:** um ícone e um toque de cor (um ponto, uma borda fina de um lado), com o texto
  «Bloqueado» ao lado ou no nome acessível. O cartão não muda de fundo inteiro.

**Mover.**

- **Pelo mouse ou pelo dedo:** o cartão sobe um degrau de elevação ao ser pego, segue o ponteiro 1:1 a partir do
  ponto onde foi pego, e o lugar de destino se abre entre os vizinhos enquanto ele passa. Ao soltar, assenta com a mola
  sem ressalto de `references/movimento-no-sistema.md`.
- **Pelo teclado:** Tab entra no quadro (o foco cai no primeiro cartão da primeira coluna); as setas andam entre os
  cartões e as colunas; **espaço pega o cartão** (o estado «pego» se vê: elevação e um anel); as setas o movem, e o
  cartão desliza para cada posição nova com a mesma curva curta; **espaço solta**; **Esc cancela** e o cartão volta ao
  lugar de onde saiu. Cada passo vai para uma região viva («Pego. Coluna Em análise, posição 3 de 5»).
- **«Mover para»:** um menu no cartão e na lateral de detalhe, com os estados em fila, na ordem do fluxo, o atual
  marcado e desativado. Funciona por clique e por teclado, e é o jeito de mover no celular.

**A lateral de detalhe.** Abre ao clicar no cartão (ou Enter com o foco nele), do lado direito, sem tirar o quadro de
vista.

- Grupos com título (resumo, responsável e datas, histórico, anexos), separados por **linhas finas** e por **fundos de
  tom um pouco diferente** entre o cabeçalho da lateral e o corpo.
- No topo, o «Mover para» com os estados em fila e a ação principal do cartão.
- O foco entra na lateral ao abrir, percorre os campos e os botões dela com Tab, e **Esc fecha e devolve o foco ao
  cartão**. A lateral não prende o quadro: com ela aberta, as setas ainda podem trocar de cartão se o projeto quiser,
  e a lateral acompanha.

**No celular (abaixo de 768 px, nosso).**

- Uma coluna de cada vez, ocupando a largura.
- Abas de estado no topo, roláveis se não couberem, cada uma com o nome, a contagem e pelo menos 44 px de altura; a
  aba ativa se vê pela elevação e pelo peso, não só pela cor.
- O cartão tem o «Mover para» como ação visível; o arrastar entre colunas sai, porque a coluna vizinha não está na
  tela.
- A lateral de detalhe vira uma tela cheia ou uma gaveta de baixo, com o mesmo conteúdo.

## A ficha (detalhe de uma entidade)

- **A entrada:** o nome grande (o maior texto da tela), uma linha de identificação em texto de apoio (o código, o
  tipo), ar suficiente em volta, e **uma só coisa em destaque à direita**: a que responde «e agora?» (o estado, o
  saldo, o próximo prazo). As ações da ficha ficam no cabeçalho, uma principal e as outras num menu.
- **O que precisa de atenção:** um bloco logo abaixo da entrada, com uma linha por pendência, cada uma com o ícone do
  tipo, o texto curto e a ação que a resolve. Sem pendências, o bloco diz isso numa linha («Nada pendente») ou some, se
  o projeto preferir.
- **Os blocos-resumo:** em grade, com a mesma altura por linha da grade. Cada um tem um título, de 3 a 5 linhas do
  essencial (nosso) e um rodapé com o resumo do que está escondido («Ver os 12 registros»). Clicar abre o resto numa
  lateral, numa gaveta ou numa aba.
- **Abas, se a ficha tiver muito:** no máximo 4 fixas, cada uma com contagem («Anexos · 9»); a primeira é o resumo.
  Dentro de uma aba com lista, os itens têm ícones diferentes por tipo, e o filtro mostra a contagem alinhada ao centro
  da linha com o rótulo.
- **O último bloco não estica a página:** se sobrou um bloco sozinho numa linha da grade, ele ocupa a largura toda com
  pouca altura, ou se junta a outro.

## O painel (panorama)

- **O cabeçalho:** o título, o período escolhido, a legenda dos atalhos de navegação (números para as vistas, `/` para
  a busca) e nada de faixa vazia.
- **Os KPIs:** uma grade de 3 × 2, agrupada por categoria (dois de dinheiro juntos, dois de prazo juntos…), cada um com
  o rótulo, o número grande com `tabular-nums` e a variação com um sinal além da cor (seta ou texto). Abaixo de 768 px,
  2 × 3 ou uma coluna.
- **A lateral do que precisa de atenção:** uma coluna à direita que acompanha o scroll (seção 5 do `SKILL.md`; a
  receita está na seção seguinte). Uma linha por pendência, com ícone por tipo, contagem e o link para resolver. No
  celular, um bloco recolhido no topo com o resumo.
- **Os gráficos:** abaixo dos KPIs, cada um com o título que diz a pergunta («Chamados abertos por semana»). Ao passar o mouse,
  a série ou a barra sob o ponteiro fica acesa e as outras se apagam um pouco, com o valor num rótulo ao lado; o mesmo
  com o foco do teclado.
- **As listas longas:** histórico, últimos movimentos, a atividade recente: embaixo de tudo, na largura toda, com 5 a 8
  linhas (nosso) e um «ver tudo». Nunca numa coluna estreita e alta ao lado dos gráficos.
- **A entrada:** os blocos entram escalonados, na ordem da importância (os KPIs, a lateral, os gráficos, as listas),
  30–80 ms entre eles, o grupo todo abaixo de cerca de 300 ms. Uma entrada por bloco; o que está dentro já está lá.
- **Os estados:** cada KPI e cada gráfico tem o seu «carregando» (o esqueleto do mesmo tamanho), o «vazio» (o período
  sem dados, com a ação de trocar o período) e o «erro» (o bloco que falhou diz o que houve; os outros continuam).

## A lateral que acompanha o scroll, com animação

O `position: sticky` sozinho prende a lateral no topo, mas não anima: ele não mexe no `transform`, e uma transição de
`transform` nunca dispara. Para a lateral chegar à posição nova com movimento, é preciso um script. A receita tem dois
modos:

- **Sem script, ou com o movimento reduzido:** `position: sticky`, sem transição. É o modo que funciona sempre.
- **Com o script:** a lateral deixa de ser `sticky`, ganha uma transição de `transform` e, a cada scroll, recebe um
  `translateY` que a leva até a altura da tela, limitado ao fim da coluna (para não passar do fim do painel).

```css
.lateral-de-atencao { position: sticky; top: 16px; align-self: start; }
.lateral-de-atencao.lateral-segue {
  position: relative; top: auto;
  transition: transform 250ms cubic-bezier(0.23, 1, 0.32, 1);
}
```

```js
const FOLGA_DO_TOPO = 16; // o mesmo `top` do sticky e o padding de cima da grade
const grade = document.querySelector(".grade-do-painel");
const lateral = grade.querySelector(".lateral-de-atencao");
let quadroPedido = false;

function posicionarLateral() {
  quadroPedido = false;
  const topoDaGrade = grade.getBoundingClientRect().top + scrollY;
  const fim = grade.clientHeight - lateral.offsetHeight - 2 * FOLGA_DO_TOPO;
  const alvo = Math.min(Math.max(scrollY - topoDaGrade, 0), fim);
  lateral.style.transform = `translateY(${alvo}px)`;
}
function pedirQuadro() {
  if (!quadroPedido) { quadroPedido = true; requestAnimationFrame(posicionarLateral); }
}
// Com o interruptor de movimento do projeto, troque a consulta pela leitura dele.
if (!matchMedia("(prefers-reduced-motion: reduce)").matches) {
  lateral.classList.add("lateral-segue");
  addEventListener("scroll", pedirQuadro, { passive: true });
  addEventListener("resize", pedirQuadro);
  posicionarLateral();
}
```

A conta supõe que a grade tem `FOLGA_DO_TOPO` de padding em cima e embaixo e que a lateral começa no topo da grade;
se a página for outra, ajuste a conta. Um quadro por `requestAnimationFrame` e o ouvinte passivo evitam trabalho a
mais durante o scroll.

**Medido** num Chromium sem janela, a 1440 × 900, numa página de teste com a grade de 3032 px e a lateral de 240 px:
rolando de 0 para 1200 px, a lateral sai de −1184 px (onde o scroll a deixou) e passa por −853, −575, −366… px do topo
da tela, quadro a quadro, até assentar em 16 px em cerca de 200 ms; no fim da página fica dentro da grade (a lateral
termina em 256 px, a grade em 300 px); com o movimento reduzido emulado, fica `sticky` em 16 px, sem nenhuma animação.
O código acima foi colado sem mudança na página de teste. Não foi medido num navegador com janela, com
o scroll de verdade do mouse, nem no Safari e no Firefox.

**Cuidado com o `overflow`:** um `overflow: hidden` ou `auto` num antepassado da lateral quebra o `sticky` (o modo
sem script). Um `transform` num antepassado não quebra o `sticky`, mas tira da janela os elementos `fixed`.
