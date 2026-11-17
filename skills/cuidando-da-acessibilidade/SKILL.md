---
name: cuidando-da-acessibilidade
description: Mede e corrige a acessibilidade — contraste, daltonismo, alvos de toque, teclado, movimento reduzido, formulários e leitor de tela. Usar ao terminar ou rever uma tela ou um site. Não usar para desenhar (é a desenhando-telas ou a desenhando-sites) nem para provar que funciona (é a testes-e-provas).
---

# Cuidando da acessibilidade

**Limites que se medem, não proibições de gosto.** Esta skill não diz «sem vidro» nem «sem movimento». Diz que o texto
precisa de 4,5:1 sobre o pior fundo que passa por trás dele, e que com o movimento reduzido sobram só a opacidade e a
cor, ou nada. O vidro, o movimento com o scroll e a cor forte continuam permitidos quando a `desenhando-telas` ou a
`desenhando-sites` os pedem; aqui eles ganham seus limites.

Cada regra traz **como se mede**, porque uma tela bonita não é prova de que todo mundo consegue usá-la. O passo a passo,
com os trechos de JavaScript prontos, está em `references/como-medir.md`; cada número com a sua fonte, em
`references/regras-e-fontes.md`.

As regras vêm em ordem do que mais falhou nos ensaios às cegas de novembro de 2026, quando se mediram as 10 páginas
que a pessoa que julgou preferiu, feitas por agentes com e sem skills de design (o resumo está na pesquisa
[`2026-11-17-ensaios-de-design.md`](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-17-ensaios-de-design.md)).
As páginas preferidas também falharam: o gosto não mede acessibilidade.

## Quando esta skill entra

- **Ao terminar** uma tela, um site ou um componente: a passagem desta skill é o último passo antes de entregar.
- **Ao rever** o que outra pessoa ou outro agente fez.
- **Quando alguém pergunta** se um texto tem contraste, se um botão é pequeno demais, se o teclado chega a tudo.

Ela não decide a cara da tela; mede a que existe e propõe a correção mínima que passa no limite, mantendo o desenho.

## 1. Alvos de toque

- **≥ 24 × 24 px em todo alvo**, salvo o link dentro de uma frase: é a regra da Vercel, sem exceções, e esta skill a
  segue. **≥ 44 × 44 px onde há toque** (o tamanho padrão da Apple em iOS e iPadOS, e o que a Vercel pede no celular).
- **A WCAG 2.2 pede menos** (critério 2.5.8, nível AA): 24 × 24 px, com cinco exceções. Passa o alvo menor com espaço
  em volta (um círculo de 24 px centrado nele não toca outro alvo), o que tem um equivalente de 24 px na mesma página,
  o link dentro do texto, o controle desenhado pelo navegador e o tamanho que é essencial. No relatório, diga qual
  das réguas falhou: um botão de 20 px com folga em volta falha na Vercel e passa na WCAG.
- **Meça a caixa a 390 px**, depois de renderizada. Não a deduza do padding nem da altura da letra: nos ensaios, 9 de
  10 páginas tinham alvos abaixo de 44 px no celular, e todas pareciam ter botões normais.
- **Os que mais falharam:** abas de coluna, botões de ação dentro de cartões e de linhas, atalhos, o logotipo como
  link, links de telefone e botões só de ícone (copiar, favoritar, fixar).
- **Se o desenho pede um botão pequeno**, aumente a área de toque e não o desenho: `min-height`, padding ou um
  pseudo-elemento que estende a área clicável.
- **Exceção nas duas réguas:** um link dentro de uma frase segue o tamanho da linha.
- **`touch-action: manipulation`** nos alvos, para o toque duplo não ampliar a página (8 de 10 não declaravam).
- Caixa de seleção e botão de opção: o rótulo faz parte do alvo, sem zona morta entre os dois.

## 2. Contraste

| Texto | Mínimo (WCAG 2.2, AA) |
|---|---|
| Normal | **4,5:1** (critério 1.4.3) |
| Grande: ≥ 24 px, ou ≥ 18,66 px em negrito | **3:1** (critério 1.4.3) |
| Ícones e bordas que são a única pista de um controle | **3:1** (critério 1.4.11) |

- **O texto secundário pequeno é o que falha.** Nos ensaios, 9 de 10 páginas tinham códigos, datas, rótulos e
  legendas de 11 a 13 px em cinzas entre 3,2:1 e 4,4:1. É o primeiro lugar onde olhar.
- **Não clareie o texto para parecer leve.** Hierarquia sai do tamanho, do peso e da posição; um cinza abaixo do limite
  não é hierarquia, é texto que uma parte das pessoas não lê.
- **O pior fundo conta.** Texto sobre vidro, gradiente, imagem ou vídeo se mede contra o ponto mais claro e o mais
  escuro que passa por trás dele, com a página rolada até o fim. O método está no trecho 7 de
  `references/como-medir.md`.
- **Diga o método:** WCAG 2 (a fórmula da luminância) ou APCA, que a Vercel prefere. Os números não são os mesmos; um
  relatório que não diz qual usou não se confere.
- **Cada texto contra o seu limite.** O título que passa no limite do texto grande não é falha, mesmo ao lado de um
  texto pequeno da mesma cor que falha.
- **A opacidade conta.** Um texto esmaecido com `opacity` se mede com a cor que sobra depois de esmaecer, não com a cor
  declarada.

## 3. Cor e daltonismo

- **A cor nunca é o único sinal** (WCAG 2.2, critério 1.4.1, nível A). O que a cor separa leva também texto, ícone,
  forma ou posição: um ponto verde e um vermelho sem nada ao lado falham.
- **Estado ou identidade?** Estado (ok, erro, aviso, bloqueado) usa as cores de estado do projeto, que um tema de
  daltonismo pode trocar. Identidade (marca, categoria) é fixa. Pergunta de um segundo: uma pessoa daltônica precisa
  desta cor para saber se é bom ou ruim? Então é estado.
- **Duas cores de identidade da mesma família** (dois verdes, dois azuis) na mesma tela confundem quem vê pouco a
  diferença de matiz: separe por rótulo, forma ou claro contra escuro.
- **Link dentro do texto** se distingue por sublinhado, ou por cor com 3:1 contra o texto em volta.
- **Gráficos** seguem a mesma regra: série com rótulo direto ou padrão, não só a cor da legenda.
- **Verifique, não ache:** capture a tela em escala de cinza e com a deuteranopia simulada. O que deixou de se separar
  falha.

## 4. Letra que a pessoa escolhe

- Tamanhos em `rem`, não em `px` fixo: quem aumentou a letra no navegador recebe o tamanho que pediu.
- **Exceção escrita:** numa WebView sem configuração de letra (widgets, apps embutidas) o `1rem` é sempre 16 px e a
  escala do sistema chega por outro caminho. Aí o `px` é aceitável, como decisão escrita do projeto.
- O zoom nunca se desliga: nada de `user-scalable=no` nem `maximum-scale=1`.
- A letra aumenta até 200% sem perder conteúdo nem função (critério 1.4.4, AA), e a página cabe em 320 px de largura
  sem scroll horizontal (critério 1.4.10, AA; o vertical pode). Tabelas de dados, mapas e gráficos podem rolar de lado;
  o resto da página, não.

## 5. Movimento

O movimento pode ficar: o que muda é o que acontece quando a pessoa pede menos e quando ele não para.

- **Com o movimento reduzido, sai o movimento e fica o sinal.** O estado final aparece sem a viagem; o que entrava
  deslizando entra só com opacidade, ou já está lá. Uma troca de cor que diz alguma coisa (o estado que mudou) pode
  ficar. Nada some e nada fica escondido esperando uma animação que não vem.
- **`0.01ms`, não `none`**, ao zerar a duração: com `none` o evento de fim (`transitionend`, `animationend`) não
  dispara, e o código que espera por ele fica parado.
- **Mais de 5 s, ao lado de conteúdo, leva pausa** (WCAG 2.2, critério 2.2.2, nível A). Vale para o que começa sozinho,
  inclusive o que começa ao entrar na tela com o scroll, e vale para a animação finita longa, não só para a infinita.
  Duas das 10 páginas tinham várias animações infinitas sem
  nenhum controle.
- **Anime só `transform` e `opacity`.** Metade das páginas animava propriedades de layout: o acordeão das perguntas
  abrindo pela altura (`max-height`, `grid-template-rows`) e o link de pular para o conteúdo surgindo pelo `top`. O
  acordeão pode abrir sem animar a altura (abre direto e o conteúdo entra com opacidade); o link de pular entra com
  `transform`.
- **Nada de `transition: all`:** liste as propriedades.
- **Os movimentos que mais mexem com o equilíbrio** de quem tem sensibilidade vestibular: um objeto grande que cruza
  a tela, um fundo do tamanho da tela que anda, um balanço lento que volta mais ou menos a cada 5 s, e a passagem
  de claro para escuro sem transição. Com o movimento reduzido, estes saem primeiro. Sem ele, o objeto grande fica
  translúcido enquanto cruza, e os outros ficam curtos.
- **Paralaxe e revelar com o scroll** são permitidos nos sites; com o movimento reduzido, o conteúdo aparece no lugar,
  sem deslocamento. Sem JavaScript, o conteúdo já está visível: o script só esconde o que ele mesmo vai revelar.

**Quem decide o movimento reduzido:** a preferência do sistema **ou** um interruptor do projeto, nunca nenhum dos dois.
Cada lado tem o seu custo:

- **A preferência do sistema** (`prefers-reduced-motion`) é o que a pessoa já escolheu, sem pedir nada a ela. Mas pode
  estar ligada por outra razão: num projeto real, o sistema operacional do próprio dono tinha os efeitos de animação
  desligados por velocidade, o navegador leu isso como movimento reduzido e a animação de uma comemoração aparecia
  parada para ele. O teste de tela não pegou, porque a ferramenta de teste roda sem preferência por padrão. Por isso
  aquele projeto passou a ter um interruptor seu
  ([regras e incidentes do projeto, regra 27](https://github.com/Carlobks/Morg-laws/blob/main/projetos/erp-de-servicos/regras-e-incidentes.md#telas-e-design)).
- **O interruptor do projeto** exige que a pessoa o ache. Começar pelo valor da preferência do sistema poupa esse
  trabalho a quem precisa, mas traz de volta o custo do primeiro lado até a pessoa achar o interruptor; o projeto de
  origem preferiu não começar por ela. Escreva qual das duas o projeto escolheu.
- **Nos dois casos**, os testes de tela rodam nos dois sentidos: com e sem movimento.

## 6. Transparência e contraste do sistema

- **Vidro passa no contraste sem depender de nenhuma preferência.** O cabeçalho translúcido se mede pelo pior fundo
  (seção 2) com a preferência desligada.
- **`prefers-reduced-transparency: reduce`:** o vidro fica sólido (fundo opaco, sem desfoque). O suporte dos
  navegadores ainda é parcial: é um ganho a mais, não a garantia do contraste.
- **`prefers-contrast: more`:** com contraste maior, o vidro fica quase opaco e ganha uma borda visível; o texto
  secundário sobe para a cor do texto principal.
- **Vidro sobre vidro** (uma gaveta translúcida sobre um cabeçalho translúcido) se mede pelo pior fundo das duas
  camadas juntas, com o conteúdo de trás rolando sob as duas. Se não dá para achar esse pior caso, torne sólida uma
  das camadas.

## 7. Teclado e foco

As páginas preferidas acertaram o básico sozinhas (foco visível em tudo, nada tapado, tudo alcançável): basta
conferir. O que falhou foi o resto.

- **Diálogos e gavetas prendem o foco, o levam para dentro ao abrir, fecham com Esc e devolvem o foco a quem os
  abriu.** Uma janela
  com `aria-modal="true"` em que o Tab saía para a página de trás estava entre as preferidas.
- **`overscroll-behavior: contain`** em modais e gavetas, para rolar o conteúdo deles não rolar a página por trás.
- **Arrastar tem alternativa** por teclado e por clique (um menu «Mover para», ou pegar, mover com as setas e soltar).
- **«Pular para o conteúdo»** quando o primeiro Tab não cai no conteúdo (uma navegação de vários links antes dele).
- **`scroll-margin-top`** nos alvos das âncoras quando há cabeçalho fixo: os 4 sites dos ensaios tinham cabeçalho fixo,
  links para as seções e nenhum, e o título da seção ficava debaixo do cabeçalho.
- **O foco não se esconde:** um elemento fixo nunca cobre o alvo focado.
- **O anel de foco:** `:focus-visible`, nunca `outline: none` sem um substituto que se veja.

## 8. Formulários

- **O erro fica junto ao campo, em texto**, ligado por `aria-describedby`, com `aria-invalid="true"` no campo. Uma
  borda vermelha sozinha não é mensagem (e falha também na cor como único sinal).
- **Ao enviar, o foco vai para o primeiro campo com erro.**
- **Mensagens e avisos** chegam a uma região `aria-live="polite"` que já existe na página antes da mensagem.
- **`type`, `name`, `autocomplete` e `inputmode` certos:** `type="email"` com `autocomplete="email"`, telefone com
  `type="tel"`, nome com `autocomplete="name"`. Desligar o `autocomplete` do único campo de contato tira o
  preenchimento automático de quem mais precisa dele.
- **Corretor desligado** (`spellcheck="false"`) no e-mail, em códigos e em nomes de usuário (3 de 4 páginas com
  e-mail o deixavam ligado).
- **Letra dos campos ≥ 16 px no celular:** abaixo disso o iOS amplia a página ao tocar no campo.
- Rótulo visível em cada campo; o placeholder não é rótulo. Colar nunca se bloqueia.

## 9. Leitor de tela e semântica

- **Semântica nativa antes de ARIA:** `button` para fazer, `a` para ir, `label`, `table`, títulos `h1`–`h6` em ordem.
- **Parece link, leva a algum lado.** Um `href="#"` na navegação que não navega falha.
- **SVG decorativo com `aria-hidden="true"`;** SVG que informa, com nome. Metade das páginas esquecia o atributo no
  logotipo, nas setas e nas ilustrações; é um atributo só.
- **Botão só de ícone tem nome** (`aria-label` ou texto escondido visualmente). O `title` sozinho não basta.
- **O `<title>` da página diz onde a pessoa está.**

## 10. Hover não é affordance

Em tablet e celular não há hover. O que só aparece com o mouse em cima não existe para quem toca.

| Situação | Regra |
|---|---|
| Ação principal de uma linha | Sempre visível |
| Ação secundária que existe em outro lugar | Pode aparecer só no hover |
| Rótulo de um ícone | Sempre visível, nunca só no tooltip |
| Enriquecimento puro | Hover à vontade |

O que aparece no hover fica visível em `@media (hover: none)`, e também com o foco do teclado (`:focus-within`).

## 11. Acabamento que se mede

- **`font-variant-numeric: tabular-nums`** em todo número que se compara, também fora das tabelas: telefones, anos,
  preços e horas de uma lista foram os esquecidos.
- **`text-wrap: balance`** nos títulos, para não sobrar uma palavra sozinha na última linha.
- **`<meta name="theme-color">`** com a cor do fundo; `color-scheme: dark` no tema escuro.
- **Estados vazio e de erro** previstos e escritos: o painel e a lista que só mostram o caminho feliz deixam a pessoa
  sem saber o que houve.
- `…` e não `...`; aspas curvas.

## 12. Como medir

Resumo de `references/como-medir.md`, com a ferramenta que o projeto já tiver (Playwright, o navegador do agente, o
console do navegador):

1. **Role a página inteira antes de medir.** Conteúdo que entra com o scroll dá contraste falso se for medido antes.
2. **Três larguras:** 1440, 390 (com toque e 2× de densidade) e 320 px.
3. **Os trechos prontos:** contraste sobre fundo sólido, alvos, movimento, SVG e âncoras, formulário enviado vazio e o
   pior fundo da camada translúcida.
4. **O movimento reduzido emulado**, e os trechos de movimento de novo.
5. **Tab de verdade** (a tecla), parando em cada alvo; num diálogo, 40 vezes, e o Esc.
6. **Cor:** a captura em cinza e com a deuteranopia simulada.
7. **Os candidatos não são falhas** até você olhar o elemento: o trecho aponta, você confirma.

**Sem navegador**, leia o código e diga que leu: «medido no código, não na tela» é um resultado diferente de «medido na
tela», e o relatório diz qual foi.

## 13. O relatório

Feche sempre com estas três partes, nesta ordem:

**Falhas**, uma linha por regra, da mais grave para a menos:

| Regra | Onde (elemento) | Medido | Limite | Correção mínima |
|---|---|---|---|---|
| Contraste | `span.codigo` «#A-1042», 11 px | 3,6:1 (WCAG 2) | 4,5:1 | cor do código com ≥ 4,5:1 sobre o fundo da linha |

**Passou**, em uma linha: o que se conferiu e estava certo (para a próxima revisão não refazer).

**Não medido**, sempre presente: o que não se conferiu e por quê (sem navegador, sem leitor de tela, estado que não se
conseguiu abrir, contraste em `:hover`). Um relatório sem esta parte diz mais do que mediu.

Não invente falhas para encher a tabela: uma regra que passou vai para «Passou». Um título que passa no limite do
texto grande não é falha, e um link dentro de uma frase segue a altura da linha.

## 14. Lista de verificação

- [ ] A página foi rolada até o fim antes de medir?
- [ ] Alvos medidos a 390 px: ≥ 24 px todos (Vercel; a WCAG tem exceções), ≥ 44 px no toque? `touch-action: manipulation`?
- [ ] Contraste ≥ 4,5:1 (3:1 no texto grande), começando pelo texto secundário pequeno? O método foi dito?
- [ ] Texto sobre vidro, gradiente ou imagem medido pelo pior fundo?
- [ ] A cor nunca é o único sinal? Captura em cinza e com deuteranopia conferida?
- [ ] Tamanhos em `rem`? Zoom ligado? 320 px sem scroll horizontal?
- [ ] Com movimento reduzido sobram só a opacidade e a cor, ou nada? O sinal fica? `0.01ms` em vez de `none`?
- [ ] O que se mexe mais de 5 s tem pausa? Só `transform` e `opacity` animados? Nada de `transition: all`?
- [ ] Quem decide o movimento reduzido está escrito (sistema ou interruptor do projeto)? Os testes rodam nos dois
  sentidos?
- [ ] Vidro sólido com `prefers-reduced-transparency`, borda com `prefers-contrast: more`?
- [ ] Diálogos prendem, movem e devolvem o foco? `overscroll-behavior: contain`? Arrastar tem alternativa?
- [ ] «Pular para o conteúdo» onde precisa? `scroll-margin-top` com cabeçalho fixo?
- [ ] Formulário enviado vazio: erro em texto junto ao campo, `aria-invalid`, foco no primeiro, região viva?
- [ ] `type`, `autocomplete`, `inputmode` certos? Corretor desligado no e-mail? Letra dos campos ≥ 16 px?
- [ ] SVG decorativo com `aria-hidden`? Botão de ícone com nome? Link que parece link leva a algum lado?
- [ ] Nada principal só no hover?
- [ ] `tabular-nums` nos números? Estados vazio e de erro?
- [ ] O relatório tem Falhas, Passou e Não medido?

## Fontes

Cada número com a fonte e a frequência com que falhou nos ensaios está em `references/regras-e-fontes.md`. As
fontes, com o titular de cada uma, estão em
[`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#interface-e-acessibilidade). Nada foi
copiado: as regras estão escritas com palavras nossas.
