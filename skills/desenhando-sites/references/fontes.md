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
| **jakub** | Jakub Krehel, `make-interfaces-feel-better` (MIT) | `1a2aa969` |
| **nosso** | valor ou forma proposta por nós, sem fonte: ponto de partida, a calibrar na prova seguinte | — |

## As regras, seção por seção

| Seção do `SKILL.md` | Regra | Fonte |
|---|---|---|
| 1 | Duas passagens: plano curto e revisto contra o pedido, depois o código | fd |
| 1 | 4 a 6 cores com nome; as letras e o papel de cada uma; layout em uma frase e em ASCII, com o alinhamento | fd |
| 1 | Uma família de letra ou duas, bem diferentes; a letra como parte do desenho | fd |
| 1 | Um tom de movimento só, mantido; as faixas de cada tom | lottie (a tabela das personalidades e o mapa das emoções); a coluna do tipo de site é nossa |
| 1 | O teste do pedido parecido: o que sairia igual é padrão | fd |
| 2 | Nem todo site é uma página só | ensaios (todas tiveram a mesma estrutura, e quem julgou viu nisso um problema grande) |
| 2 | As três estruturas e quando cada uma serve | nosso |
| 3 | O primeiro impacto é a capa | ensaios (nenhuma teve bom primeiro impacto no site da empresa) |
| 3 | Abrir com o mais típico do mundo do cliente; o número grande com gradiente é a capa de sempre | fd |
| 3 | A capa funciona com e sem foto | ensaios (o pedido não deixava usar fotos); as três capas sem foto são nossas |
| 3 | Espaçamento negativo no título grande, perto de zero no texto corrido | apple |
| 3 | O cabeçalho com os textos bem posicionados | ensaios (a maior parte ficou feia, com os textos mal posicionados); a forma é nossa |
| 3 | Uma foto forte em vez de várias fracas | nosso |
| 3 | Contorno de 1 px a 10 %, preto no claro e branco no escuro | jakub |
| 4 | Cartão simples, com ícone e poucas palavras | ensaios (o site que ficou em primeiro); o teto de 25 palavras é nosso |
| 4 | Destacar um dos serviços | ensaios (todas as que destacaram ganharam pontos) |
| 4 | Blocos de texto numa grade clara | ensaios (a queixa das caixas de texto numa organização estranha); a grade é a nossa resposta |
| 4 | Linhas com menos de 80 caracteres; serifa com um pouco mais | fd |
| 4 | O formulário em duas colunas, três informações e os campos | ensaios (o formulário elogiado); a coluna única no celular é nossa |
| 4 | Escrever do lado de quem lê; o botão diz o que acontece | fd |
| 5 | Nem apertado nem vazio | ensaios (espaço vazio demais entre as partes) |
| 5 | 96–128 px e 56–80 px; nenhuma seção com mais de meia tela vazia | nosso |
| 6 | A ação principal numa lateral que acompanha o scroll | ensaios (a marcação do site que ficou em primeiro) |
| 6 | A barra fixa embaixo no celular | nosso; o tamanho do alvo vem da `cuidando-da-acessibilidade` |
| 7 | Os textos surgem com o scroll na página toda | ensaios (decidiu o primeiro lugar nos dois sites) |
| 7 | 10–16 px, saída forte, 400–600 ms; começar com 10–20 % na tela; uma vez só; em onda de 80–120 ms; o menor só esmaece; conteúdo visível sem script; a capa não espera; nunca um evento de scroll | mblode |
| 7 | Uma entrada por contêiner | mblode; choreo |
| 7 | A entrada de um site visto uma vez: passos de 100–150 ms, entradas de 0,5–0,6 s | choreo |
| 7 | Paralaxe só decorativo, só `transform`, até cerca de 15 %, sem duração, sem celular; não prender o scroll | mblode |
| 7 | Fora: as três camadas sempre e a saída com `ease-in` | lottie (o que ela pede); a recusa é nossa, porque contradiz a `emil-design-eng` e a régua |
| 8 | O cabeçalho de vidro | ensaios (elogiado no site da empresa) |
| 8 | Fundo semi-opaco com desfoque e o conteúdo por baixo; nunca vidro sobre vidro; texto mais pesado e com mais contraste; a cor numa camada sólida | apple |
| 8 | Opacidade de 0,72 e desfoque de 16 px | nosso |
| 9 | `scroll-margin-top` igual à altura do cabeçalho | régua (os quatro sites medidos falharam); a variável única é nossa |
| 10 | O padrão que serve a qualquer cliente não é escolha; os dois exemplos; a ousadia num lugar só | fd |
| 11 | Capturas e crítica antes de mostrar; tirar um enfeite antes de entregar | fd |
| 11 | Rolar até o fim e voltar; desligar o JavaScript | nosso, a partir das regras da seção 7 |
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
