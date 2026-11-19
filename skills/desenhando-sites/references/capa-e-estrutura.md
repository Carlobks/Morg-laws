# Capa e estrutura

A estrutura do site, as capas sem foto, o cabeçalho de vidro e o formulário em duas colunas. O código foi escrito por nós e testado numa página isolada, num Chromium sem janela (a 1440 px e a 390 px, com
e sem a transparência reduzida emulada); o que se mediu está no fim de cada receita. Os valores sem fonte dizem
«nosso» e são um ponto de partida.

## 1. As estruturas

| Estrutura | Serve quando | Não serve quando |
|---|---|---|
| **Uma página com âncoras** | o conteúdo cabe em 5 a 7 seções curtas; há uma ação só; quem chega quer ver tudo de uma vez | cada serviço tem detalhe próprio, ou há públicos diferentes que querem coisas diferentes |
| **Várias páginas curtas** | os serviços têm detalhe, preço ou etapas próprias; o conteúdo cresce (obras, artigos, casos); a busca precisa achar cada serviço pela sua página | o site tem três parágrafos e um formulário |
| **Uma página com uma parte que abre à parte** | a lista dos serviços abre o detalhe de cada um num painel, ou a marcação acontece num passo próprio, sem tirar a pessoa da página | o detalhe é longo demais para um painel (vira página) |

A escolha e o critério são nossos, tirados de uma queixa dos ensaios: todas as páginas tiveram a mesma estrutura.
Diga no plano qual é a escolhida e por quê. Com várias páginas, o cabeçalho, as cores e a ação principal são os
mesmos em todas, e a página de entrada leva a capa; as outras levam uma entrada mais baixa.

## 2. Capas sem foto

Uma capa forte sem nenhuma imagem é possível; ela só precisa de outro protagonista. Escolha um (os três são ideias
nossas; o espaçamento negativo no título grande é de Emil Kowalski, `apple-design`, que usa −0,02 em no exemplo
dele):

- **A letra:** o título ocupa a capa, entre 2,5 e 5,5 rem conforme a largura (`clamp`), com a entrelinha perto de 1 e
  o espaçamento entre letras negativo, por volta de −0,02 a −0,03 em (o tamanho, a entrelinha e o −0,03 são nossos). O texto de apoio fica pequeno e longe, para o
  título ter ar. Funciona quando o nome ou a promessa do cliente é curta.
- **A forma:** um bloco de cor, um círculo grande ou um recorte geométrico que ocupa de um terço à metade da capa, com
  o título ao lado ou por cima. A forma pode vir do mundo do cliente (o perfil de uma peça, o desenho de uma planta, a
  silhueta de uma ferramenta), desenhada em SVG.
- **A cor:** a capa inteira numa cor forte da paleta, com o título em contraste, e o resto do site em neutros. A
  passagem da capa para a primeira seção é o primeiro momento do movimento.

Nos três casos a capa entra ao carregar (`movimento-com-o-scroll.md`, seção 2), e o que mais importa vem primeiro na
ordem da entrada.

## 3. O cabeçalho de vidro

```css
:root { --altura-cabecalho: 4rem; }

.cabecalho {
  position: fixed; inset: 0 0 auto 0; height: var(--altura-cabecalho); z-index: 10;
  display: flex; align-items: center; gap: 1.5rem; padding: 0 1.5rem;
  background: rgb(246 244 239 / 0.72);
  backdrop-filter: blur(16px) saturate(160%);
  -webkit-backdrop-filter: blur(16px) saturate(160%);
}
.cabecalho a { font-weight: 600; letter-spacing: 0.01em; }

@media (prefers-reduced-transparency: reduce) {
  .cabecalho { background: #f6f4ef; backdrop-filter: none; -webkit-backdrop-filter: none; }
}
@media (prefers-contrast: more) {
  .cabecalho { background: rgb(246 244 239 / 0.97); border-bottom: 1px solid #1d1b18; }
}

/* As âncoras e o foco param abaixo do cabeçalho: a mesma variável nos dois lugares */
html { scroll-padding-top: var(--altura-cabecalho); }
```

- **A cor do fundo é a do site,** com opacidade; a opacidade de 0,72 e o desfoque de 16 px são nossos (a `apple-design`
  usa um exemplo parecido). Mais transparente do que isso e o texto do cabeçalho depende demais do que passa por trás.
- **Os links do cabeçalho com peso 600 e um pouco de espaçamento:** é o texto mais pesado que o vidro pede (Emil
  Kowalski, `apple-design`).
- **Uma variável só para a altura:** se o cabeçalho crescer no celular, o espaço das âncoras cresce junto.
- **`scroll-padding-top` no `html`, e não `scroll-margin-top` em cada seção:** vale para qualquer alvo de âncora (uma
  seção, um título com `id`) e também para o elemento que recebe o foco do teclado, que o navegador rola para a
  vista respeitando esse espaço. O `scroll-margin-top` só vale para os alvos que o levam, e o foco continua debaixo do
  cabeçalho (forma nossa, medida abaixo).
- **O contraste do texto se mede sobre o pior fundo** que passa por trás (uma foto clara, um bloco escuro), com a
  página rolada até o fim: o método está na `cuidando-da-acessibilidade`.

**Medido:** com a transparência reduzida emulada, o fundo virou `rgb(246, 244, 239)` e o `backdrop-filter` ficou
`none`; sem ela, `rgba(246, 244, 239, 0.72)` com `blur(16px) saturate(1.6)`. Ao clicar no link de uma seção, o topo
dela parou em 64 px, rente ao fim do cabeçalho; na mesma página **sem** a linha do `scroll-padding-top`, parou em 0,
debaixo do cabeçalho. Um campo posto logo acima da tela e focado por script parou com o topo a 412 px (1440 px) e a
362 px (390 px), fora do cabeçalho; com a versão anterior desta receita (`scroll-margin-top` nas seções) ficava a
10 px do topo, debaixo dele. A variante de `prefers-contrast: more` não foi emulada nesta sessão.

## 4. O formulário em duas colunas

```css
.pedido { display: grid; grid-template-columns: minmax(14rem, 2fr) 3fr; gap: 3rem; align-items: start; }
.pedido-informacoes { display: grid; gap: 1.5rem; }
.pedido-campos { display: grid; gap: 1rem; }

@media (max-width: 767px) {
  .pedido { grid-template-columns: 1fr; gap: 2rem; }
}
```

```html
<section id="pedido" class="pedido">
  <div class="pedido-informacoes">
    <h2>Peça o seu orçamento</h2>
    <p><strong>Resposta em um dia útil.</strong> Pelo telefone ou pelo e-mail que você deixar.</p>
    <p><strong>Sem compromisso.</strong> O orçamento não obriga a contratar.</p>
    <p><strong>Prefere falar?</strong> O telefone está no rodapé.</p>
  </div>
  <form class="pedido-campos"><!-- os campos, cada um com rótulo visível --></form>
</section>
```

- **Três informações curtas, cada uma com uma frase em negrito e uma de apoio;** quais são depende do caso, e as do
  exemplo são nossas.
- **As informações à esquerda e mais estreitas:** a pessoa lê primeiro o que vai acontecer, depois preenche.
- **No celular uma coluna,** com as informações em cima: quem lê de cima para baixo vê o mesmo caminho.
- Os campos (rótulos, tipos, `autocomplete`, o erro junto ao campo) seguem a `cuidando-da-acessibilidade`.

**Medido:** a 1440 px, a grade tinha duas colunas, com as informações à esquerda e mais estreitas do que os campos; a
390 px, uma coluna, com as informações acima dos campos.
