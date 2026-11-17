---
name: desenhando-sites
description: Guia o desenho de sites de empresa ou profissional — capa forte, letra, poucas palavras, textos que surgem com o scroll e vidro. Usar ao criar, redesenhar ou rever um site ou landing page. Não usar para telas de sistema (é a desenhando-telas) nem para acessibilidade (é a cuidando-da-acessibilidade).
---

# Desenhando sites

**Um site se visita poucas vezes e tem de causar impressão logo na entrada.** Quem chega ao site de uma empresa ou de
um profissional decide em segundos se fica, e quase sempre veio fazer uma coisa só: entender o que se oferece e pedir
um contato. Por isso o site leva mais movimento, mais letra e menos texto do que uma tela de sistema, e cada seção
existe para levar a pessoa até a ação principal.

Onde ler o resto:

- `references/movimento-com-o-scroll.md`: a receita testada do revelar com o scroll, a entrada da capa, o paralaxe e
  a tabela dos tons de movimento.
- `references/capa-e-estrutura.md`: as estruturas possíveis e quando cada uma serve, capas sem foto, o cabeçalho de
  vidro, a ação que segue o scroll e o formulário em duas colunas.
- `references/fontes.md`: cada regra com a fonte e o commit fixo.

As regras vêm dos ensaios às cegas de novembro de 2026, em que o site de uma empresa de serviços e o de uma psicóloga
foram pedidos a agentes com e sem skills de design e uma pessoa ordenou as páginas sem saber qual era qual (o resumo
está na pesquisa
[`2026-11-17-ensaios-de-design.md`](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-17-ensaios-de-design.md)).
Quem julgou não gostou dos sites no geral. Parte da culpa foi do pedido, que exigia uma página só e não deixava usar
fotos; o resto está nas regras abaixo. Sem skill nenhuma, o agente ficou em 6.º lugar nos dois sites (de 9 e de 8):
aqui as regras podem ser mais diretas do que nas telas de sistema.

**O que mora em outra skill:** contraste (também sobre o vidro), alvos de toque, foco, teclado, hover, o movimento
reduzido e a pausa do que se mexe por muito tempo se medem com a `cuidando-da-acessibilidade`; telas de sistema com
muitos dados (ERP, painel, Kanban) são da `desenhando-telas`. Esta skill pede o movimento e o vidro; a de
acessibilidade põe os limites. Nenhuma das duas proíbe o que a outra pede.

## 1. Plano antes do código

Trabalhe em duas passagens. Primeiro um plano curto, por escrito; depois o código.

1. **Do que é o site, para quem, e o que a pessoa vem fazer.** Se o pedido não diz, proponha um assunto concreto, o
   público e o trabalho principal da página, e confirme. O mundo do cliente (o ofício, os materiais, o vocabulário) é
   de onde saem as escolhas que não são genéricas.
2. **As cores:** de 4 a 6, cada uma com um nome e o valor (um papel claro para cada: fundo, texto, acento, apoio).
3. **As letras e o papel de cada uma.** Uma família ou duas; se forem duas, bem diferentes entre si. A letra é onde a
   página mostra a personalidade: o título é parte do desenho, não só o lugar onde o texto mora.
4. **A estrutura** (seção 2), com o porquê.
5. **O layout** em uma frase e um esboço em ASCII, com o alinhamento (à esquerda, ao centro) decidido.
6. **O tom do movimento**, um só para o site inteiro e mantido do começo ao fim. Ponto de partida:

   | Tipo de site | Tom | Duração das entradas |
   |---|---|---|
   | Consultório, terapia, cuidado | calmo, sem ressalto | 500–1000 ms, curva suave nas duas pontas |
   | Marca de luxo, ateliê, trabalho autoral | sofisticado, sem ressalto | 350–600 ms |
   | Serviços, empresa, escritório | profissional | 200–400 ms |

   Os nomes e os números vêm da `motion-design` da LottieFiles (a tabela completa está em
   `references/movimento-com-o-scroll.md`). O revelar com o scroll tem a sua própria faixa (seção 7), que vale para
   todos os tons.

Depois **reveja o plano contra o pedido**: imagine outro pedido parecido e veja se chegaria ao mesmo plano. A parte que
sairia igual para qualquer cliente é um padrão, não uma escolha; troque-a e diga o que trocou e por quê. Só então
escreva o código.

## 2. A estrutura

**Nem todo site é uma página só com as seções em fila.** Nos ensaios, todas as páginas tiveram a mesma estrutura, e
quem julgou viu nisso um problema grande: faltou variar (a culpa ali foi do pedido, que exigia uma página só). Escolha
a estrutura pelo conteúdo e diga no plano por que é essa (as três abaixo são nossas):

- **Uma página com âncoras:** pouco conteúdo, uma ação só, quem chega quer ler tudo de uma vez.
- **Várias páginas curtas:** serviços com detalhe próprio, públicos diferentes, conteúdo que cresce (artigos, obras).
- **Uma página com uma parte que abre à parte:** a lista de serviços que abre o detalhe de cada um, ou a marcação
  num passo próprio, sem tirar a pessoa da página.

Se o pedido fixa a estrutura, siga o pedido. Os critérios de cada uma, com exemplos, estão em
`references/capa-e-estrutura.md`.

## 3. A capa

**O primeiro impacto é a capa.** No site da empresa, nenhuma página teve um bom primeiro impacto: faltou uma capa
bonita na entrada.

- **Abra com o que é mais típico do mundo do cliente,** na forma que melhor o mostra: um título, uma imagem, uma
  animação, uma amostra do trabalho. O número grande com um rótulo pequeno e um acento em gradiente é a capa de
  sempre: só use se for de fato a melhor.
- **A capa tem de funcionar com foto e sem foto.** Sem foto, o peso fica na letra, na forma e na cor: um título grande
  com o espaçamento entre as letras um pouco negativo e a entrelinha apertada, uma forma ou um bloco de cor que ocupa
  parte da capa, e uma entrada animada ao carregar. As receitas estão em `references/capa-e-estrutura.md`.
- **Letra grande pede espaçamento negativo,** e o texto corrido fica perto de zero: um mesmo `letter-spacing` em todos
  os tamanhos está errado em algum deles (Emil Kowalski, `apple-design`).
- **O cabeçalho é parte da capa.** Nos ensaios, a maior parte dos cabeçalhos ficou feia, com os textos mal
  posicionados. O logotipo ou o nome de um lado, a navegação alinhada na mesma linha de base, a ação principal
  separada dos links, e nada encostado na borda (a forma é nossa).
- **Com fotos:** uma foto forte vale mais do que várias fracas (valor nosso). Cada imagem leva um contorno de 1 px,
  preto a 10 % de opacidade no tema claro e branco a 10 % no escuro, para a borda da foto não se perder no fundo
  (Jakub Krehel, `make-interfaces-feel-better`).
- **A capa não espera pelo scroll:** ela entra uma vez, ao carregar (seção 7).

## 4. Poucas palavras

O texto demais foi uma das queixas dos dois sites. Uma página de site se percorre com os olhos; ninguém lê parágrafos
inteiros antes de decidir.

- **Cada ideia num cartão simples, com um ícone bonito e poucas palavras.** No site que ficou em primeiro, as duas
  formas de atendimento couberam em dois cartões curtos, cada um com um ícone, e a mensagem chegou assim. Até 25
  palavras por cartão é o nosso ponto de partida, a calibrar.
- **Destaque um dos serviços** na lista dos serviços (o mais pedido, ou o que o cliente quer vender): nos ensaios,
  todas as páginas que fizeram isso ganharam pontos. Um destaque só; dois destaques são nenhum.
- **Os blocos de texto numa grade clara,** alinhados e com a mesma largura por linha, não caixas soltas em posições
  diferentes. Uma organização estranha das caixas de texto foi outra queixa dos ensaios.
- **Linhas com menos de 80 caracteres;** com letra serifada a linha pode ser um pouco maior e pede mais entrelinha
  (Anthropic, `frontend-design`).
- **O formulário de pedido em duas colunas:** à esquerda, três informações curtas; à direita, os campos. Foi o
  formulário elogiado nos ensaios, pelo aspecto limpo. Que três informações são é escolha do caso (por exemplo, quando
  vem a resposta e o que acontece depois do envio; exemplo nosso). No celular as colunas viram uma, com as informações em cima.
- **Escreva do lado de quem lê,** com verbos claros: o botão diz o que acontece ao clicar («Pedir orçamento», não
  «Enviar»), e o mesmo nome segue até a mensagem de confirmação (Anthropic, `frontend-design`).
- **Nada de texto falso que parece de verdade:** depoimentos, números de clientes e prêmios inventados não entram; se o
  pedido não os dá, deixe o lugar marcado como exemplo.

## 5. Espaço entre as seções

Nem apertado nem vazio demais: espaço vazio demais entre as partes do site foi outra queixa dos ensaios.

- **Uma escala fixa de espaço vertical entre as seções,** decidida no plano e usada em todas: por exemplo 96–128 px no
  computador e 56–80 px no celular (valores nossos, a calibrar).
- **Nenhuma seção deixa mais de meia tela vazia** sem conteúdo (valor nosso). Uma seção que precisa de uma tela inteira
  de altura para ter impacto (a capa) tem conteúdo para ocupá-la.
- **Dentro de uma seção, menos espaço do que entre as seções:** o olho separa as partes pelo espaço antes de precisar
  de uma linha.

## 6. A ação principal que segue o scroll

No site que ficou em primeiro, a marcação ficava numa lateral que acompanhava o scroll, e funcionou bem.

- **No computador:** a ação principal (marcar, pedir orçamento) numa coluna lateral com `position: sticky`, logo abaixo
  do cabeçalho fixo, ao lado das seções de conteúdo.
- **No celular:** a lateral vira uma barra fixa embaixo, com o botão da ação ocupando a largura, a altura do alvo que a
  `cuidando-da-acessibilidade` pede e a margem da área segura (valor e forma nossos). O fim da página leva um espaço
  extra do tamanho da barra, para ela não cobrir o último conteúdo.
- **Uma ação só nela.** A lateral não vira um segundo menu.
- **O `sticky` quebra com um `overflow`** (`hidden`, `auto`) num antepassado: confira antes de dizer que funciona.

A receita testada está em `references/capa-e-estrutura.md`.

## 7. Movimento com o scroll

Foi o que decidiu o primeiro lugar nos dois sites: no da empresa, a primeira passou a segunda só pelas animações, e no
da psicóloga as animações fluidas mantiveram a primeira no lugar. Faltou movimento acompanhando o scroll na página
toda, e as páginas em que os textos surgiam com o scroll ganharam pontos. As duas fontes que mais falam de scroll pedem o contrário: a `frontend-design` vê
o mesmo surgir em cada seção como a cara de uma página gerada, e a `ui-animation` corta o revelar para poucos momentos
por página. Aqui vale o gosto de quem julgou: **os blocos surgem ao longo da página toda**. As técnicas dessas mesmas
fontes impedem que fique genérico.

**A receita** (Matthew Blode, `ui-animation`; o código testado está em `references/movimento-com-o-scroll.md`):

- **De opacidade 0 a 1, com uma subida de 10 a 16 px,** numa curva de saída forte, em 400–600 ms. A velocidade de uma
  tela de sistema (200 ms) parece nervosa num site.
- **Comece cedo:** quando o bloco entra de 10 a 20 % na tela, para ele chegar junto com a pessoa, e não depois de ela
  parar diante de um espaço vazio. Use um `IntersectionObserver`, nunca um evento de scroll que roda a cada quadro.
- **Uma vez só.** Depois de revelado, o bloco deixa de ser observado: subir e descer a página não repete a animação.
- **Em onda, não em metrônomo.** O título lidera, o texto de apoio segue de 80 a 120 ms depois e anda menos, e o que
  menos importa só esmaece, sem se mexer. Um atraso igual para todos apaga a hierarquia. É isso que responde à crítica
  da «cara de página gerada»: o efeito muda com a importância do bloco.
- **Uma entrada por contêiner:** anime a seção ou os filhos dela, nunca os dois, senão a pessoa espera as duas entradas
  (Emil Kowalski, `choreograph`).
- **O conteúdo existe sem JavaScript.** Sem script, tudo está visível no lugar. O script marca a página e só então o
  estado escondido passa a valer; um script que quebra nunca deixa a página em branco.
- **O que está na tela ao carregar não espera pelo scroll:** a capa e o que se vê sem rolar entram uma vez, com uma
  animação de carga, em passos de 100–150 ms com entradas de 0,5–0,6 s (Emil Kowalski, `choreograph`, para a entrada
  de um site visto uma vez por visita).
- **Paralaxe só como tempero:** só em elementos decorativos, nunca em texto que se lê; só com `transform`; a diferença
  entre as camadas fica em até cerca de 15 % da distância rolada; **sem paralaxe no celular**, onde a tela curta e o
  scroll com impulso o transformam em tremor. O paralaxe e as barras de progresso presas ao scroll não têm duração nem
  curva: a posição do scroll é o relógio.
- **O scroll é de quem lê:** nada de prender a página, trocar o passo da roda do mouse ou fazer um giro da roda virar
  uma tela inteira. `scroll-behavior: smooth` só para as âncoras.
- **Só `transform` e `opacity`** nos elementos que se mexem, com as propriedades nomeadas na transição.
- **O movimento reduzido** (o que sobra dele, e o que acontece com a pausa de uma animação longa) segue a
  `cuidando-da-acessibilidade`. A receita do `references/` já traz a variante.

**O que fica de fora da LottieFiles,** apesar de ela ter ganhado um dos sites: as «três camadas de movimento sempre»
(principal, de apoio e de ambiente) e a saída com aceleração (`ease-in`). A camada de ambiente, quando existir, é
opcional e leva os limites da `cuidando-da-acessibilidade`; a saída usa a mesma curva de saída forte, mais curta.

## 8. Vidro

O cabeçalho translúcido, com o conteúdo passando desfocado por baixo, foi elogiado nos ensaios. Nos sites ele é
permitido (nas telas de sistema, não: ver a `desenhando-telas`).

- **Onde:** o cabeçalho fixo e os painéis que flutuam sobre o conteúdo. Fundo semi-opaco com `backdrop-filter: blur()`,
  e o conteúdo rola por baixo dele (Emil Kowalski, `apple-design`).
- **Nunca vidro sobre vidro:** duas camadas translúcidas claras empilhadas e o texto deixa de se ler (idem).
- **O texto no vidro** fica um pouco mais pesado, com mais contraste e um pouco mais de espaço entre as letras do que o
  mesmo texto num fundo sólido; a cor forte vai numa camada sólida, não no vidro (idem).
- **Os limites estão na `cuidando-da-acessibilidade`:** o contraste se mede sobre o pior fundo que passa por trás, e o
  vidro fica sólido quando a pessoa pede menos transparência e quase opaco quando pede mais contraste. A receita, com
  as duas variantes, está em `references/capa-e-estrutura.md`.

## 9. Âncoras com o cabeçalho fixo

Com cabeçalho fixo e links para as seções, cada alvo de âncora leva `scroll-margin-top` igual à altura do cabeçalho,
senão o título da seção fica escondido debaixo dele. Os quatro sites medidos nos ensaios falharam aqui. A regra e o
modo de medir estão na `cuidando-da-acessibilidade`; o que cabe a esta skill é guardar a altura do cabeçalho numa
variável só, usada pelo cabeçalho e pela margem, para as duas nunca divergirem.

## 10. Fugir do padrão

Um padrão que serviria a qualquer cliente não é uma escolha (Anthropic, `frontend-design`). Dois exemplos, com palavras
nossas:

- **O site inteiro picado em cartões iguais,** com o mesmo arredondamento em tudo, a mesma sombra cinza clara embaixo
  de cada um e manchas de gradiente como enfeite.
- **Uma etiqueta pequena em maiúsculas, com as letras afastadas, por cima de cada título,** sem dizer nada que o título
  já não diga.

A `frontend-design` da Anthropic tem uma lista mais longa (paletas, layouts e acabamentos que aparecem em qualquer
página gerada). Todos servem a algum pedido; o erro é chegar neles sem ter escolhido. Se o pedido pede um deles, o
pedido vence.

**Gaste a ousadia num lugar só:** um elemento memorável (a capa, a letra, uma forma) e o resto calmo e disciplinado em
volta dele.

## 11. Como trabalhar

1. **Escreva o plano da seção 1** e reveja-o contra o pedido antes do código.
2. **Monte a estrutura e a capa primeiro;** o movimento entra depois de o conteúdo estar certo sem ele.
3. **Tire captura a 1440 px e a 390 px** quando houver navegador, e critique antes de mostrar: a capa tem impacto sem
   rolar? Algum cartão passa do limite de palavras? Alguma seção deixa meia tela vazia? A ação principal está à vista
   nas duas larguras?
4. **Role a página inteira, devagar, e depois suba:** cada bloco surge uma vez, em onda, e nada some ao voltar.
5. **Desligue o JavaScript e recarregue:** todo o texto tem de aparecer.
6. **Tire um enfeite antes de entregar.** Olhe a página uma última vez e remova o que não serve ao pedido (Anthropic,
   `frontend-design`).
7. **No fim, passe a `cuidando-da-acessibilidade`** e diga o que não se verificou.

**Beleza não é evidência.** Um site se valida com uma pessoa real ou com um número medido (uma captura lida, uma caixa
medida, o estado do elemento depois do scroll), nunca com um «parece bonito».

## 12. Precedência

**O manual de marca do cliente vence onde divergir** desta skill: cores, letras, tom e até o movimento. Esta skill
preenche o que o manual não diz. Quando os dois divergem, siga o manual e diga a divergência no relatório.

## 13. Lista de verificação

- [ ] O plano (assunto, público, 4–6 cores com nome, letras e papéis, estrutura, layout em ASCII, tom do movimento)
  foi escrito e revisto contra o pedido antes do código?
- [ ] A estrutura foi escolhida pelo conteúdo, com o porquê, e não por hábito?
- [ ] A capa tem impacto sem rolar, com foto ou sem ela? O título grande tem espaçamento negativo? O cabeçalho está
  alinhado, com os textos bem posicionados?
- [ ] Cada imagem tem o contorno de 1 px a 10 %?
- [ ] Cartões com poucas palavras e um ícone? Um serviço em destaque? Blocos numa grade clara? Linhas abaixo de 80
  caracteres?
- [ ] O formulário em duas colunas no computador (três informações curtas e os campos) e numa no celular? Botões com
  verbo e resultado?
- [ ] Espaço entre seções numa escala fixa, sem meia tela vazia?
- [ ] A ação principal numa lateral `sticky` no computador e numa barra fixa embaixo no celular, sem `overflow` que
  quebre o `sticky`?
- [ ] Os blocos surgem com o scroll ao longo da página toda, de 10 a 16 px, em 400–600 ms, uma vez só?
- [ ] A onda segue a hierarquia (título, apoio 80–120 ms depois, o menor só esmaece)? Uma entrada por contêiner?
- [ ] Sem JavaScript todo o texto aparece? A capa entra ao carregar, sem esperar o scroll?
- [ ] Paralaxe só decorativo, até cerca de 15 %, sem duração, desligado no celular? Nada prende o scroll?
- [ ] Só `transform` e `opacity` animados, sem `transition: all`?
- [ ] Vidro só no cabeçalho e em painéis flutuantes, nunca empilhado? O texto nele mais pesado e com mais contraste?
- [ ] Os alvos de âncora com `scroll-margin-top` igual à altura do cabeçalho, tirada da mesma variável?
- [ ] Nenhum padrão de página gerada que ninguém escolheu? A ousadia num lugar só?
- [ ] Capturas a 1440 e a 390 px criticadas, a página rolada até o fim e de volta, o JavaScript desligado uma vez?
- [ ] O manual de marca, se existe, foi seguido, e a divergência dita?
- [ ] A `cuidando-da-acessibilidade` passou (contraste sobre o vidro, movimento reduzido, alvos), e o que não se
  verificou está dito?

## Fontes

Cada regra com a sua fonte e o commit fixo está em `references/fontes.md`; as fontes, com o titular de cada uma, em
[`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#ensaios-de-design). Nada foi copiado: as regras
das skills de terceiros (`motion-design` da LottieFiles, `apple-design` e `choreograph` de Emil Kowalski,
`make-interfaces-feel-better` de Jakub Krehel e `ui-animation` de Matthew Blode, todas MIT, e a `frontend-design` da
Anthropic, Apache-2.0) estão escritas com palavras nossas.
