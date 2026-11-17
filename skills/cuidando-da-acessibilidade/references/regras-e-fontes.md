# Regras e fontes

Cada número da skill `cuidando-da-acessibilidade`, com a fonte e, quando a regra foi medida, quantas das 10 páginas
dos ensaios às cegas de novembro de 2026 falharam nela. As 10 páginas foram as duas preferidas de cada um dos cinco
casos (um Kanban, uma ficha de funcionário, um painel de entrada, o site de uma empresa de serviços e o de uma
psicóloga), medidas num Chromium sem janela pelas diretrizes da Vercel. O resumo está na pesquisa
[`2026-11-17-ensaios-de-design.md`](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-17-ensaios-de-design.md)
do Morg-laws.

«Lido em» é a data em que a página oficial foi aberta. Uma regra sem fonte oficial diz de onde veio.

## Os números

| Regra | Número | Fonte | Lido em | Falhou nos ensaios |
|---|---|---|---|---|
| Alvo mínimo | ≥ 24 × 24 px | WCAG 2.2, critério 2.5.8 (AA) | 2026-10-30 | 3 de 10 |
| Alvo no toque | ≥ 44 × 44 pt (padrão); 28 × 28 pt (mínimo) | Apple, Human Interface Guidelines, Accessibility | 2026-10-30 | 9 de 10 (a 390 px) |
| Alvo no celular | ≥ 44 px; aumentar a área se o desenho é menor | Vercel, Web Interface Guidelines | 2026-11-17 | — |
| `touch-action: manipulation` | nos alvos | Vercel | 2026-11-17 | 8 de 10 |
| Contraste do texto normal | ≥ 4,5:1 | WCAG 2.2, critério 1.4.3 (AA) | 2026-10-30 | 9 de 10 |
| Contraste do texto grande | ≥ 3:1; grande é ≥ 18 pt (≈ 24 px) ou ≥ 14 pt em negrito (≈ 18,66 px) | idem | 2026-10-30 | — |
| Contraste de controles e gráficos | ≥ 3:1 contra as cores vizinhas, também nos estados (selecionado, focado) | WCAG 2.2, critério 1.4.11 (AA) | 2026-11-17 | não medido |
| APCA em vez do WCAG 2 | preferido | Vercel | 2026-11-17 | — |
| A cor não é o único sinal | nível A; link no texto: sublinhado ou 3:1 contra o texto em volta | WCAG 2.2, critério 1.4.1 | 2026-11-17 | não medido |
| Letra aumentada | até 200% sem perder conteúdo nem função | WCAG 2.2, critério 1.4.4 (AA) | 2026-11-17 | não medido |
| Largura mínima | 320 px sem scroll nos dois sentidos (exceto tabelas de dados, mapas, gráficos) | WCAG 2.2, critério 1.4.10 (AA) | 2026-11-17 | 1 de 10 (2 px a mais a 320 px) |
| Zoom ligado | nada de `user-scalable=no` nem `maximum-scale=1` | Vercel | 2026-11-17 | 0 de 10 |
| Letra dos campos no celular | ≥ 16 px | Vercel | 2026-11-17 | 1 de 6 com campos |
| Pausa no que se mexe | o que começa sozinho, dura mais de 5 s e está ao lado de conteúdo tem pausar, parar ou esconder; o que começa ao entrar na tela com o scroll também conta | WCAG 2.2, critério 2.2.2 (A) | 2026-11-17 | 2 de 10 |
| Só `transform` e `opacity` | nunca propriedades de layout | Vercel | 2026-11-17 | 5 de 10 |
| `transition: all` | nunca | Vercel | 2026-11-17 | 0 de 10 |
| Movimento reduzido | respeitar, com uma variante reduzida ou sem movimento | Vercel | 2026-11-17 | 0 de 10 |
| Movimento reduzido: o que fica | troca deslizar, mola e paralaxe por opacidade ou nada; mantém a opacidade e a cor que ajudam a entender | Emil Kowalski, skill `apple-design` | 2026-11-17 | — |
| O que mais incomoda o ouvido interno | fundo de tela inteira em movimento, oscilação lenta perto de um ciclo a cada 5 s, salto brusco de brilho | idem | 2026-11-17 | — |
| `0.01ms` e não `none` | o evento de fim só dispara com uma duração | a `desenhando-telas` do Morg-laws, de um incidente do projeto de origem | — | — |
| Transparência reduzida | o vidro fica sólido | Emil Kowalski, skill `apple-design`; a consulta de mídia no MDN, onde ainda é experimental | 2026-11-17 | — |
| Contraste maior | fundo quase sólido, borda que contrasta | Emil Kowalski, skill `apple-design` | 2026-11-17 | — |
| Foco preso, movido e devolvido | em diálogos | Vercel | 2026-11-17 | 1 de 2 com diálogo aberto |
| `overscroll-behavior: contain` | em modais e gavetas | Vercel | 2026-11-17 | 1 de 2 |
| Arrastar com alternativa | teclado e clique | Vercel | 2026-11-17 | 0 de 2 |
| «Pular para o conteúdo» | onde o primeiro Tab não cai no conteúdo | Vercel | 2026-11-17 | 1 de 5 onde se aplica |
| `scroll-margin-top` | nas âncoras, com cabeçalho fixo | Vercel | 2026-11-17 | 4 de 4 sites |
| Erro junto ao campo, foco no primeiro | ao enviar | Vercel | 2026-11-17 | 1 de 6 com formulário |
| Validação anunciada | `aria-live="polite"` | Vercel | 2026-11-17 | 1 de 10 |
| `type`, `autocomplete`, `inputmode` | certos | Vercel | 2026-11-17 | 1 de 4 sites |
| Corretor no e-mail | desligado | Vercel | 2026-11-17 | 3 de 4 com e-mail |
| Link que parece link | leva a algum lado | Vercel | 2026-11-17 | 1 de 10 |
| SVG decorativo | `aria-hidden` | Vercel | 2026-11-17 | 5 de 10 |
| `tabular-nums` | nos números que se comparam | Vercel | 2026-11-17 | 5 de 10 |
| `text-wrap: balance` | nos títulos | Vercel | 2026-11-17 | 6 de 10 |
| `theme-color` | com a cor do fundo | Vercel | 2026-11-17 | 6 de 10 (as 6 telas de sistema) |
| Estados vazio e de erro | previstos | Vercel | 2026-11-17 | 4 de 10 (pela leitura do código) |
| Hover não é affordance | a tabela da seção 10 | a `desenhando-telas` do Morg-laws | — | — |
| Duas cores de identidade da mesma família | evitar na mesma tela | regra do projeto de origem, sem fonte oficial | — | — |

## O que a régua dos ensaios mediu e o que não mediu

- **Mediu:** Tab de verdade, o movimento reduzido emulado, o formulário enviado vazio, os alvos a 1440, 390 e 320 px,
  o contraste pelo WCAG 2 em fundos sólidos, depois de rolar a página inteira.
- **Não mediu:** o APCA; o contraste sobre gradiente e imagem (pulou esses textos); os menus móveis dos sites;
  `:hover` e `:active`; os gráficos para daltonismo. Por isso «não medido» na tabela não quer dizer «passou».
- **Nenhuma das 10 falhou** em foco visível, foco tapado, alcance pelo teclado, zoom, movimento reduzido,
  `transition: all`, `<title>`, nomes acessíveis, ordem dos títulos e reticências. A skill não gasta linhas nisso:
  confere numa linha.

## As fontes

As páginas oficiais e as skills de terceiros estão no
[`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#interface-e-acessibilidade) do Morg-laws, com
o link, a data e o titular:

- **WCAG 2.2** (W3C), os critérios 1.4.1, 1.4.3, 1.4.4, 1.4.10, 1.4.11, 2.2.2 e 2.5.8, nas páginas «Understanding».
- **Apple, Human Interface Guidelines**, a página de acessibilidade.
- **MDN**, a consulta de mídia `prefers-reduced-transparency`.
- **Vercel Labs, Web Interface Guidelines** (`AGENTS.md`, commit `434b7f91`, MIT, Vercel Labs).
- **Emil Kowalski, skill `apple-design`** (`emilkowalski/skills`, commit `64eb3deb`, MIT, Emil Kowalski): a seção de
  movimento reduzido e acessibilidade.
- **A `desenhando-telas` do Morg-laws** (CC BY 4.0), de onde vieram a tabela do hover, o `0.01ms`, a letra em `rem`
  e o estado contra identidade.

Nada foi copiado: as regras estão destiladas com palavras nossas, e os números entram como valores, com a fonte ao lado.
