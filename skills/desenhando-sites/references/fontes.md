# Fontes da desenhando-sites

Cada regra da skill com a sua fonte. As skills de terceiros foram lidas como texto nos commits fixos abaixo, nada foi
executado, e as regras estão escritas com palavras nossas. O titular e a licença de cada uma estão no
[`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#ensaios-de-design), com a data em que o
`LICENSE` foi reaberto.

| Marca | Fonte | Commit |
|---|---|---|
| **ensaios** | os ensaios às cegas de novembro de 2026: o site de uma empresa de serviços e o de uma psicóloga, ordenados por uma pessoa sem saber qual skill fez cada página (o resumo público está na pesquisa [`2026-11-17-ensaios-de-design.md`](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-17-ensaios-de-design.md)) | — |
| **régua** | a régua de acessibilidade aplicada às páginas dos ensaios, com as diretrizes da Vercel (mesma pesquisa) | — |
| **fd** | Anthropic, `frontend-design` (Apache-2.0) | `e4bb5d96` |
| **lottie** | LottieFiles, `motion-design` (MIT) | `f9a8a041` |
| **mblode** | Matthew Blode, `ui-animation`, a referência do scroll (MIT) | `7df4b7ed` |
| **apple** | Emil Kowalski, `apple-design` (MIT) | `64eb3deb` |
| **choreo** | Emil Kowalski, `choreograph` (MIT) | `64eb3deb` |
| **emil** | Emil Kowalski, `emil-design-eng` (MIT) | `64eb3deb` |
| **jakub** | Jakub Krehel, `make-interfaces-feel-better` (MIT) | `1a2aa969` |
| **nosso** | valor ou forma proposta por nós, sem fonte: ponto de partida, a calibrar na prova seguinte | — |

## As regras, seção por seção

| Seção do `SKILL.md` | Regra | Fonte |
|---|---|---|
| 1 | Duas passagens: plano curto e revisto contra o pedido, depois o código | fd |
| 1 | Escrever a hipótese do assunto, do público e do que a visita deve render, e pedir a confirmação; as escolhas saem do dia a dia do cliente | fd |
| 1 | 4 a 6 cores com nome; as letras e o papel de cada uma; layout em uma frase e em ASCII, com o alinhamento | fd |
| 1 | Uma família de letra ou duas, bem diferentes; a letra como parte do desenho | fd |
| 1 | Um tom de movimento só, mantido; as faixas de cada tom | lottie (a tabela das personalidades e o mapa das emoções); a coluna do tipo de site, a regra de a duração valer só para as respostas a um gesto e os 500 ms do calmo num clique são nossos |
| 1 | O teste do cliente vizinho: o que ele receberia sem estranhar é padrão | fd |
| 2 | Nem todo site é uma página só | ensaios (todas tiveram a mesma estrutura, e quem julgou viu nisso um problema grande) |
| 2 | As três estruturas e quando cada uma serve | nosso |
| 3 | O primeiro impacto é a capa | ensaios (nenhuma teve bom primeiro impacto no site da empresa) |
| 3 | Abrir com o mais típico do mundo do cliente; o número grande com gradiente é a capa de sempre | fd |
| 3 | A capa funciona com e sem foto | ensaios (o pedido não deixava usar fotos); as três capas sem foto são nossas |
| 3 | Espaçamento negativo no título grande, perto de zero no texto corrido | apple |
| 3 | O cabeçalho com o nome e os links alinhados | ensaios (na maior parte das páginas, os textos do cabeçalho ficaram desalinhados); a forma é nossa |
| 3 | Título de 2,5 a 5,5 rem, entrelinha perto de 1, até −0,03 em | nosso; o −0,02 em é o exemplo da apple |
| 3 | Uma foto forte em vez de várias fracas | nosso |
| 3 | Contorno de 1 px a 10 %, preto no claro e branco no escuro | jakub |
| 4 | Cartão simples, com ícone e poucas palavras | ensaios (o site que ficou em primeiro); o teto de 25 palavras é nosso |
| 4 | Destacar um dos serviços | ensaios (todas as que destacaram subiram no julgamento) |
| 4 | Um destaque só | nosso |
| 4 | Blocos de texto numa grade clara, com a mesma largura por linha | ensaios (a queixa da arrumação confusa dos blocos de texto); a grade e a largura são a nossa resposta |
| 4 | Linhas com menos de 80 caracteres; serifa com um pouco mais | fd |
| 4 | O formulário em duas colunas, três informações e os campos | ensaios (o formulário elogiado); a coluna única no celular é nossa |
| 4 | Escrever do lado de quem lê; o botão diz o que acontece | fd |
| 4 | Nada de depoimento, número ou prêmio inventado | nosso |
| 5 | Nem apertado nem vazio | ensaios (seções afastadas demais) |
| 5 | 96–128 px e 56–80 px; nenhuma seção com mais de meia tela vazia; menos espaço dentro da seção do que entre as seções | nosso |
| 6 | A ação principal numa lateral que acompanha o scroll | ensaios (a marcação do site que ficou em primeiro) |
| 6 | A barra fixa embaixo no celular, o espaço dela no fim e no `scroll-padding-bottom` | nosso; o tamanho do alvo e o foco que não se esconde vêm da `cuidando-da-acessibilidade` |
| 6 | Uma ação só na lateral; o `sticky` quebra com `overflow` | nosso (o aviso do `overflow` é o mesmo da `desenhando-telas`) |
| 7 | Os textos surgem com o scroll na página toda | ensaios (decidiu o primeiro lugar nos dois sites) |
| 7 | 10–16 px, saída forte, 400–600 ms; disparar com 10–20 % na tela; uma vez só; em onda de 80–120 ms; o menor só esmaece; conteúdo visível sem script; a capa não espera; nunca um evento de scroll | mblode |
| 7 | Disparar por `threshold`, nunca por `rootMargin` negativo (o último bloco nunca surgiria) | nosso, medido no Chromium |
| 7 | A curva `cubic-bezier(0.23, 1, 0.32, 1)` | emil |
| 7 | Na receita: 14 px no título, 10 px e 100 ms no apoio, 180 ms no detalhe, 520 ms | nosso, dentro das faixas da mblode |
| 7 | Uma entrada por contêiner | mblode; choreo |
| 7 | A entrada de um site visto uma vez: passos de 100–150 ms, entradas de 0,5–0,6 s | choreo; o 0,7 s da receita é nosso; o elogio a uma entrada animada vem dos ensaios |
| 7 | Paralaxe só decorativo, só `transform`, até cerca de 15 %, sem duração, sem celular; não prender o scroll | mblode |
| 7 | Fora: as três camadas sempre e a saída com `ease-in` | lottie (o que ela pede); a recusa é nossa, porque contradiz a `emil-design-eng` e a régua |
| 8 | O cabeçalho de vidro | ensaios (elogiado no site da empresa) |
| 8 | Fundo semi-opaco com desfoque e o conteúdo por baixo; nunca vidro sobre vidro; texto mais pesado e com mais contraste; a cor numa camada sólida | apple |
| 8 | Opacidade de 0,72 e desfoque de 16 px | nosso |
| 8 | Na dúvida, uma das camadas fica sólida | `cuidando-da-acessibilidade` |
| 9 | As âncoras não param sob o cabeçalho | régua (os quatro sites da régua falharam) |
| 9 | `scroll-padding-top` no `html` com a variável do cabeçalho, e `scroll-padding-bottom` com a barra no celular, para as âncoras e o foco | nosso, medido no Chromium |
| 10 | O padrão que serve a qualquer cliente não é escolha; os dois exemplos; uma só aposta por página | fd |
| 11 | Capturas e crítica antes de mostrar; tirar um enfeite antes de entregar | fd |
| 11 | Rolar até o fim e voltar; desligar o JavaScript | nosso, a partir das regras da seção 7 |
| 11 | Beleza não é evidência | nosso (a regra da casa, também na `desenhando-telas`) |
| 12 | O manual de marca vence | nosso |

## Onde as fontes discordam

- **Revelar em toda a página.** A `frontend-design` vê o mesmo surgir em cada seção como a cara de uma página gerada e
  pede um só momento orquestrado; a `ui-animation` corta o revelar para 2 a 4 momentos. Nos ensaios, quem julgou
  premiou o contrário: o movimento ao longo da página toda. A skill segue o julgamento e usa as técnicas dessas mesmas
  fontes (uma vez só, em onda, conteúdo visível sem script) para não ficar genérica.
- **A saída.** A LottieFiles pede saída com aceleração (`ease-in`); a `emil-design-eng` a proíbe na interface. A skill
  fica com a curva de saída forte nas duas direções.
- **O vidro.** A `desenhando-telas` mantém as superfícies sólidas nas telas de sistema; nos sites o vidro é permitido,
  e os limites medidos ficam na `cuidando-da-acessibilidade`.
