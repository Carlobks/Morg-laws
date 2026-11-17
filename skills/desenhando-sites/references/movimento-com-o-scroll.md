# Movimento com o scroll

As receitas do movimento de um site: o revelar com o scroll, a entrada da capa e o paralaxe, mais a tabela dos tons de
movimento. O código foi escrito por nós e testado numa página isolada, num Chromium sem janela, em cinco modos: normal,
com o movimento reduzido emulado, com o JavaScript desligado, a 390 px de largura e com a transparência reduzida
emulada. O que se mediu está no fim de cada receita.

As regras vêm de Matthew Blode (`ui-animation`), Emil Kowalski (`choreograph`) e LottieFiles (`motion-design`), lidas
nos commits fixos e escritas com palavras nossas; os commits estão em `fontes.md`. Os limites de acessibilidade do
movimento (o que sobra com o movimento reduzido, a pausa do que dura mais de 5 s) estão na
`cuidando-da-acessibilidade` e não se repetem aqui: a receita só os aplica.

## 1. Revelar com o scroll

O estado escondido só existe quando o script marcou a raiz da página. Sem script, ou se ele quebrar, nada fica
escondido.

```html
<h2 data-revelar>Título da seção</h2>
<p data-revelar="apoio">O texto de apoio, que vem logo depois.</p>
<p data-revelar="calmo">O detalhe, que só esmaece.</p>
```

```css
:root { --saida-forte: cubic-bezier(0.23, 1, 0.32, 1); }

.revelar-ligado [data-revelar] {
  opacity: 0;
  transform: translateY(var(--revelar-distancia, 14px));
  transition: opacity 520ms var(--saida-forte), transform 520ms var(--saida-forte);
  transition-delay: var(--revelar-atraso, 0ms);
}
.revelar-ligado [data-revelar="apoio"] { --revelar-distancia: 10px; --revelar-atraso: 100ms; }
.revelar-ligado [data-revelar="calmo"] { --revelar-distancia: 0px; --revelar-atraso: 180ms; }
.revelar-ligado [data-revelar].revelado { opacity: 1; transform: none; }

@media (prefers-reduced-motion: reduce) {
  .revelar-ligado [data-revelar] { transform: none; transition: opacity 200ms linear; }
}
```

```js
(() => {
  const alvos = document.querySelectorAll("[data-revelar]");
  if (!("IntersectionObserver" in window) || alvos.length === 0) return;
  document.documentElement.classList.add("revelar-ligado");
  const observador = new IntersectionObserver((entradas) => {
    for (const entrada of entradas) {
      if (!entrada.isIntersecting) continue;
      entrada.target.classList.add("revelado");
      observador.unobserve(entrada.target);
    }
  }, { rootMargin: "0px 0px -12% 0px" });
  alvos.forEach((alvo) => observador.observe(alvo));
})();
```

Por que cada peça é assim:

- **`rootMargin` com −12 % embaixo:** o bloco começa a surgir quando já entrou cerca de 12 % na tela, dentro da faixa
  de 10 a 20 % da `ui-animation`. Mais cedo, a animação acaba antes de a pessoa olhar; mais tarde, ela vê um espaço
  vazio.
- **`unobserve` depois de revelar:** é o que faz o bloco surgir uma vez só. Sem isso, um script que tira a classe ao
  sair da tela faz o bloco piscar a cada subida.
- **Três papéis em vez de um atraso por índice:** o título lidera, o apoio vem 100 ms depois e anda menos, o detalhe
  só esmaece. Um atraso que cresce igual a cada filho (`--i * 80ms`) é o metrônomo que a onda evita.
- **A curva de saída forte** começa rápida e assenta devagar: a pessoa vê a resposta logo. O mesmo valor da
  `desenhando-telas`, com uma duração de site.
- **O que está na tela ao carregar não leva `data-revelar`.** O observador dispararia logo, mas a capa não deve
  depender do script: ela tem a sua própria entrada (seção 2).
- **Uma entrada por contêiner:** se a seção inteira leva `data-revelar`, os filhos dela não levam.

**Medido** (a 1440 px e a 390 px): antes do scroll, o título de uma seção abaixo da dobra tinha opacidade 0 e
`translateY(14px)`; 150 ms depois de a seção entrar na tela, opacidade 0,79; depois de 1 s, 1 e `transform: none`; o
apoio tinha `transition-delay` de 0,1 s; a transição nomeava só `opacity, transform`. Ao subir até o topo e voltar, a
classe continuava lá e a opacidade era 1 logo no primeiro quadro: não houve segunda animação. **Com o JavaScript
desligado**, a raiz não foi marcada e todos os blocos tinham opacidade 1 desde o carregamento. **Com o movimento
reduzido**, o `transform` ficou `none` antes e depois, e só a opacidade mudou, em 0,2 s.

## 2. A entrada da capa

A capa entra uma vez, ao carregar, só com CSS: não espera pelo scroll nem pelo script.

```css
.capa h1 { animation: capa-entra 700ms var(--saida-forte) both; }
.capa p  { animation: capa-entra 700ms var(--saida-forte) 120ms both; }

@keyframes capa-entra   { from { opacity: 0; transform: translateY(16px); } }
@keyframes capa-esmaece { from { opacity: 0; } }

@media (prefers-reduced-motion: reduce) {
  .capa h1, .capa p { animation-name: capa-esmaece; animation-duration: 300ms; }
}
```

- Os passos de 120 ms e as entradas de 0,7 s ficam perto da faixa da `choreograph` para a entrada de um site visto uma
  vez por visita (passos de 100–150 ms, entradas de 0,5–0,6 s); o 0,7 s é nosso, para uma capa de título grande.
- O `both` mantém o estado inicial enquanto o atraso corre, para o texto de apoio não aparecer antes e depois sumir.

**Medido:** 1,2 s depois de carregar, o título tinha opacidade 1 e `transform` sem deslocamento, com e sem
JavaScript. Com o movimento reduzido, a animação usada foi `capa-esmaece` e o `transform` ficou `none`.

## 3. Paralaxe

Só decorativo, só com `transform`, preso à posição do scroll (sem duração nem curva), só onde o navegador sabe fazer
isso fora do script, e nunca no celular.

```css
@supports (animation-timeline: view()) {
  @media (min-width: 768px) and (prefers-reduced-motion: no-preference) {
    .forma-decorativa { animation: forma-sobe linear both; animation-timeline: view(); }
    @keyframes forma-sobe { from { transform: translateY(40px); } to { transform: translateY(-40px); } }
  }
}
```

- **`linear` aqui está certo, e só aqui:** a mão de quem rola é o relógio; qualquer curva distorceria a relação de 1
  para 1 com o scroll (Matthew Blode, `ui-animation`).
- **O `@supports` não é opcional:** num navegador sem `animation-timeline`, o elemento fica no estado final, parado,
  em vez de preso no primeiro quadro.
- **Os 80 px de percurso** (de 40 a −40) para uma forma que atravessa a tela inteira ficam bem abaixo dos cerca de
  15 % da distância rolada; o valor é nosso.
- **O celular fica de fora** pela largura, e o movimento reduzido pela preferência.

**Medido:** a 1440 px, a forma estava em `translateY(40px)` quando apontava na base da tela e em `translateY(-26px)`
quando o topo dela chegava ao topo da tela; a 390 px e com o movimento reduzido, nenhuma animação.

## 4. Âncoras suaves, sem prender o scroll

```css
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
```

É o único lugar onde o site mexe no scroll. A margem das âncoras com o cabeçalho fixo está em `capa-e-estrutura.md`.

## 5. Os tons de movimento

Um tom para o site inteiro, escolhido no plano. A tabela é da `motion-design` da LottieFiles, com os nomes traduzidos
por nós; a coluna «Para que site» é nossa.

| Tom (LottieFiles) | Duração | Ressalto | Para que site |
|---|---|---|---|
| Premium (sofisticado) | 350–600 ms | nenhum | marca de luxo, ateliê, trabalho autoral |
| Corporate (profissional) | 200–400 ms | 0–3 % | serviços, empresa, escritório |
| Playful (brincalhão) | 150–300 ms | 10–20 % | infantil, lazer, evento |
| Energetic (enérgico) | 100–250 ms | 15–30 % | esporte, lançamento |

E, do mapa das emoções da mesma fonte, a **calma**: 500–1000 ms, numa curva suave nas duas pontas (seno), em caminhos
de curvas leves. É o tom para um consultório, uma terapia ou um cuidado.

O revelar com o scroll (seção 1) tem a sua própria faixa de 400–600 ms, que vale em qualquer tom: um tom rápido não o
leva a 200 ms, porque a velocidade de uma tela de sistema parece nervosa num site.

**O que não se usa da LottieFiles:** a regra das três camadas de movimento sempre presentes e a saída com aceleração.
As duas contradizem a `emil-design-eng` e a régua de acessibilidade dos ensaios; uma camada de ambiente, quando
existir, é opcional e leva os limites da `cuidando-da-acessibilidade`.
