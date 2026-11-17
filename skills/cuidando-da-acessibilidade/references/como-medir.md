# Como medir

O passo a passo da seção «Como medir» da skill, com os trechos prontos. Os trechos são JavaScript que roda **dentro
da página**: servem no console do navegador, no `page.evaluate` do Playwright ou na ferramenta de JavaScript do
navegador do agente. Use a ferramenta que o projeto já tem; nada aqui pede instalar coisa nova.

Os trechos foram rodados contra a página de exemplo da skill (`evals/files/agenda-da-barbearia.html`), num Chromium
sem janela, e acharam as falhas plantadas nela. Eles **apontam candidatos**; quem decide se é falha é você, olhando o
elemento. Um número sem o elemento ao lado não convence ninguém.

## Ordem

1. **Abrir a página e rolar até o fim** (trecho 1). Conteúdo que só aparece com o scroll (`opacity: 0` até entrar na
   tela) dá contraste falso de 1:1 se for medido antes. Nos ensaios às cegas de novembro de 2026 a primeira passagem
   sem este passo deu contrastes falsos nos sites, e teve de ser jogada fora.
2. **Medir em três larguras:** 1440 px (computador), 390 px (celular, com emulação de toque e 2× de densidade) e
   320 px (o celular estreito, onde aparece o scroll horizontal).
3. **Rodar os trechos 2 a 7** em cada largura que importa (os alvos, a 390 px; o resto, em qualquer uma).
4. **Emular o movimento reduzido** e rodar o trecho 4 de novo.
5. **Teclado de verdade:** apertar Tab (a tecla, não `element.focus()`), parando em cada alvo e olhando o anel de
   foco; abrir cada diálogo e apertar Tab 40 vezes, conferindo que o foco não saiu dele; Esc, e ver onde o foco voltou.
6. **Enviar cada formulário vazio** (trecho 6) e ler o que mudou.
7. **O pior fundo** de cada texto sobre vidro, gradiente ou imagem (trecho 7 e o método das capturas, no fim).
8. **Cor:** tirar uma captura em escala de cinza e outra com a deuteranopia simulada (no Chrome: DevTools, Rendering,
   «Emulate vision deficiencies»; pelo protocolo, `Emulation.setEmulatedVisionDeficiency`). O que só a cor separava
   deixa de se separar nas duas.
9. **Relatar** no formato da skill, com o que não se mediu.

Como emular, conforme a ferramenta:

| O quê | Playwright | Protocolo do DevTools (CDP) |
|---|---|---|
| Celular a 390 px | `browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true })` | `Emulation.setDeviceMetricsOverride` e `Emulation.setTouchEmulationEnabled` |
| Movimento reduzido | `page.emulateMedia({ reducedMotion: 'reduce' })` | `Emulation.setEmulatedMedia` com `prefers-reduced-motion: reduce` |
| Contraste maior | não tem atalho: use o CDP | `Emulation.setEmulatedMedia` com `prefers-contrast: more` |
| Tab de verdade | `page.keyboard.press('Tab')` | `Input.dispatchKeyEvent` |

Atenção: o Playwright, por padrão, roda **sem** preferência de movimento. Um teste que nunca liga o movimento reduzido
nunca vê a versão reduzida, e um que só o liga nunca vê a animação.

## Os trechos

Todos devolvem uma lista; cada item descreve o elemento pelo seletor curto e pelo texto. Cole primeiro o trecho 0,
que os outros usam.

### 0. As funções comuns

```js
function descrever(el) {
  const classe = typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).join('.') : '';
  const texto = (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 40);
  return `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}${classe}${texto ? ' «' + texto + '»' : ''}`;
}
function rgba(cor) {
  const n = (cor.match(/[\d.]+/g) || [0, 0, 0, 0]).map(Number);
  return [n[0], n[1], n[2], n.length > 3 ? n[3] : 1];
}
function compor(cima, baixo) {
  const a = cima[3];
  return [0, 1, 2].map((i) => cima[i] * a + baixo[i] * (1 - a)).concat(1);
}
function luminancia(cor) {
  const canal = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
  return 0.2126 * canal(cor[0]) + 0.7152 * canal(cor[1]) + 0.0722 * canal(cor[2]);
}
function razao(a, b) {
  const [claro, escuro] = [luminancia(a), luminancia(b)].sort((x, y) => y - x);
  return (claro + 0.05) / (escuro + 0.05);
}
function textoGrande(estilo) {
  const px = parseFloat(estilo.fontSize);
  return px >= 24 || (px >= 18.66 && Number(estilo.fontWeight) >= 700);
}
```

A fórmula é a do WCAG 2 (luminância relativa, limite de 0,04045). O APCA, que a Vercel prefere, dá outro número;
diga qual dos dois usou.

### 1. Rolar a página inteira

```js
async function rolarAPaginaInteira() {
  const passo = Math.max(200, innerHeight * 0.8);
  for (let y = 0; y < document.documentElement.scrollHeight; y += passo) {
    scrollTo(0, y);
    await new Promise((pronto) => setTimeout(pronto, 150));
  }
  scrollTo(0, 0);
  await new Promise((pronto) => setTimeout(pronto, 150));
}
```

### 2. Contraste sobre fundo sólido

```js
function medirContraste() {
  const falhas = [], semFundoSolido = [];
  for (const el of document.querySelectorAll('body *')) {
    const temTexto = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
    const caixa = el.getBoundingClientRect();
    if (!temTexto || !caixa.width || caixa.bottom < 0 || caixa.right < 0) continue;
    const estilo = getComputedStyle(el);
    if (estilo.visibility === 'hidden' || Number(estilo.opacity) === 0) continue;
    const camadas = [];
    let solido = true, opaco = false;
    for (let a = el; a; a = a.parentElement) {
      const s = getComputedStyle(a);
      if (s.backgroundImage !== 'none' || s.backdropFilter !== 'none') solido = false;
      const cor = rgba(s.backgroundColor);
      if (cor[3] > 0) camadas.push(cor);
      if (cor[3] === 1) { opaco = true; break; }
      if (s.position === 'fixed' || s.position === 'sticky') { solido = false; break; }
    }
    if (!solido || !opaco) { semFundoSolido.push(descrever(el)); continue; }
    const fundo = camadas.reverse().reduce((baixo, cima) => compor(cima, baixo));
    const valor = razao(compor(rgba(estilo.color), fundo), fundo);
    const minimo = textoGrande(estilo) ? 3 : 4.5;
    if (valor < minimo) falhas.push({ elemento: descrever(el), razao: valor.toFixed(2), minimo, letra: estilo.fontSize });
  }
  return { falhas, semFundoSolido };
}
```

`semFundoSolido` é a lista de textos que este trecho **não sabe** medir (vidro, gradiente, imagem, camada fixa
translúcida): vão para o trecho 7. Nunca os conte como aprovados.

### 3. Alvos

```js
function medirAlvos() {
  const seletor = 'a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button], [tabindex]:not([tabindex="-1"])';
  const resultado = [];
  for (const el of document.querySelectorAll(seletor)) {
    const alvo = (el.type === 'checkbox' || el.type === 'radio') && el.labels && el.labels[0] ? el.labels[0] : el;
    const caixa = alvo.getBoundingClientRect();
    if (!caixa.width || !caixa.height || caixa.bottom < 0 || caixa.right < 0) continue;
    const dentroDoTexto = el.tagName === 'A' && getComputedStyle(el).display === 'inline' && el.closest('p, li, td, dd');
    if (dentroDoTexto) continue;
    const menor = Math.min(caixa.width, caixa.height);
    if (menor < 44) resultado.push({ elemento: descrever(el), largura: Math.round(caixa.width), altura: Math.round(caixa.height), abaixoDe24: menor < 24 });
  }
  return resultado;
}
function semTouchAction() {
  return [...document.querySelectorAll('a[href], button, [role=button]')]
    .filter((el) => !['manipulation', 'none'].includes(getComputedStyle(el).touchAction))
    .map(descrever);
}
```

O link dentro de uma frase fica de fora: é a exceção do critério 2.5.8. Rode a 390 px; abaixo de 24 px falha sempre,
abaixo de 44 px falha onde há toque.

### 4. Movimento

```js
const PROPRIEDADES_DE_LAYOUT = /^(top|left|right|bottom|width|height|max-height|min-height|max-width|min-width|margin.*|padding.*|grid-template-.*|inset.*|font-size)$/;
function emHifen(nome) { return nome.replace(/[A-Z]/g, (letra) => '-' + letra.toLowerCase()); }
function medirMovimento() {
  const animacoes = document.getAnimations().map((animacao) => {
    const quadros = animacao.effect.getKeyframes();
    const propriedades = [...new Set(quadros.flatMap(Object.keys))]
      .filter((p) => !['offset', 'easing', 'composite', 'computedOffset'].includes(p)).map(emHifen);
    const tempo = animacao.effect.getComputedTiming();
    return {
      elemento: descrever(animacao.effect.target), propriedades,
      infinita: tempo.iterations === Infinity, duracaoTotalMs: tempo.endTime,
      soOpacidadeOuCor: propriedades.every((p) => /^(opacity|color|background-color|border-color|fill|stroke)$/.test(p)),
    };
  });
  const transicoesDeLayout = [];
  for (const el of document.querySelectorAll('*')) {
    const s = getComputedStyle(el);
    const nomes = s.transitionProperty.split(',').map((n) => n.trim());
    const duracoes = s.transitionDuration.split(',').map((d) => parseFloat(d) * (d.includes('ms') ? 1 : 1000));
    nomes.forEach((nome, i) => {
      const duracao = duracoes[i % duracoes.length];
      if (duracao > 1 && (nome === 'all' || PROPRIEDADES_DE_LAYOUT.test(nome))) transicoesDeLayout.push({ elemento: descrever(el), propriedade: nome, duracaoMs: duracao });
    });
  }
  return { animacoes, transicoesDeLayout };
}
```

Leia o resultado assim:

- **Sem emulação:** `transicoesDeLayout` e as `animacoes` com propriedades fora de `transform` e `opacity` são falha
  (anima o layout). As `animacoes` com `infinita: true` precisam de um botão de pausa à vista.
- **Com o movimento reduzido emulado:** sobra só o que tem `soOpacidadeOuCor: true`, ou nada. Uma animação infinita que
  continua com `transform` é falha.
- O trecho só vê as animações que estão rodando e as transições declaradas. A transição de um acordeão só aparece em
  `getAnimations()` enquanto ele abre; por isso a lista de transições lê o CSS de cada elemento.

### 5. SVG e âncoras

```js
function svgSemNome() {
  return [...document.querySelectorAll('svg')]
    .filter((svg) => svg.getAttribute('aria-hidden') !== 'true' && !svg.getAttribute('aria-label')
      && !svg.getAttribute('aria-labelledby') && !svg.querySelector('title'))
    .map((svg) => descrever(svg.parentElement) + ' > svg');
}
function ancorasSobOCabecalho() {
  const fixo = [...document.querySelectorAll('body *')].find((el) => {
    const s = getComputedStyle(el);
    return (s.position === 'fixed' || s.position === 'sticky') && el.offsetHeight > 0 && el.getBoundingClientRect().top <= 1 && el.offsetWidth >= innerWidth * 0.9;
  });
  if (!fixo) return { cabecalho: null, ancoras: [] };
  const daRaiz = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
  const ancoras = [...new Set([...document.querySelectorAll('a[href^="#"]')].map((a) => a.hash.slice(1)).filter(Boolean))]
    .map((id) => document.getElementById(decodeURIComponent(id))).filter(Boolean)
    .filter((alvo) => daRaiz + (parseFloat(getComputedStyle(alvo).scrollMarginTop) || 0) < fixo.offsetHeight)
    .map(descrever);
  return { cabecalho: descrever(fixo), alturaPx: fixo.offsetHeight, ancoras };
}
```

Um SVG sem `aria-hidden` e sem nome é decorativo esquecido ou um ícone sem nome: os dois falham.

### 6. Formulário enviado vazio

```js
function enviarVazioELer(formulario) {
  formulario.querySelectorAll('input, textarea, select').forEach((campo) => { if (campo.type !== 'hidden') campo.value = ''; });
  formulario.requestSubmit();
  const regioesVivas = [...document.querySelectorAll('[aria-live], [role=alert], [role=status]')]
    .filter((r) => r.getAttribute('aria-live') !== 'off').map((r) => r.textContent.trim()).filter(Boolean);
  const campos = [...formulario.querySelectorAll('input, textarea, select')].filter((c) => c.type !== 'hidden').map((c) => ({
    campo: c.name || c.id, type: c.type, autocomplete: c.getAttribute('autocomplete'), inputmode: c.getAttribute('inputmode'),
    letraPx: parseFloat(getComputedStyle(c).fontSize), corretor: c.spellcheck,
    ariaInvalid: c.getAttribute('aria-invalid'),
    mensagem: (c.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean)
      .map((id) => document.getElementById(id)?.textContent.trim()).join(' ') || null,
  }));
  return { focoFoiPara: descrever(document.activeElement), regioesVivas, campos };
}
```

O formulário passa se: cada campo vazio obrigatório tem `ariaInvalid: "true"` e uma `mensagem` em texto; o foco foi
para o primeiro campo com erro; a mensagem chegou a uma região viva; a letra dos campos é ≥ 16 px a 390 px; o e-mail
tem `type: "email"`, `autocomplete: "email"` e `corretor: false`. Um formulário com validação nativa do navegador
(sem `novalidate`) para o envio antes do código da página: aí confira a bolha do navegador e o foco, à mão.

### 7. O pior fundo de um texto sobre camada translúcida

Para texto numa camada fixa translúcida (o cabeçalho de vidro) com conteúdo **de cores sólidas** passando por trás:

```js
function piorFundoDaCamada(textoEl) {
  let camada = textoEl;
  while (camada && !['fixed', 'sticky'].includes(getComputedStyle(camada).position)) camada = camada.parentElement;
  if (!camada) return null;
  const corDaCamada = rgba(getComputedStyle(camada).backgroundColor);
  const corDoTexto = rgba(getComputedStyle(textoEl).color);
  const fundosQuePassam = new Map();
  for (const el of document.querySelectorAll('html, body, body *')) {
    if (camada.contains(el) || el.matches('input, textarea, select, button')) continue;
    const largoEAlto = el.offsetWidth >= camada.offsetWidth * 0.8 && el.offsetHeight >= camada.offsetHeight;
    const s = getComputedStyle(el);
    const cor = rgba(s.backgroundColor);
    if (cor[3] === 1 && largoEAlto && s.backgroundImage === 'none') fundosQuePassam.set(String(cor), { cor, exemplo: descrever(el) });
  }
  const medidas = [...fundosQuePassam.values()].map(({ cor, exemplo }) => {
    const fundo = compor(corDaCamada, cor);
    return { passaPorTras: exemplo, razao: Number(razao(compor(corDoTexto, fundo), fundo).toFixed(2)) };
  }).sort((a, b) => a.razao - b.razao);
  const minimo = textoGrande(getComputedStyle(textoEl)) ? 3 : 4.5;
  return { texto: descrever(textoEl), minimo, pior: medidas[0], melhor: medidas[medidas.length - 1], todas: medidas };
}
```

Ele mistura a cor da camada com cada fundo sólido da página largo o bastante para passar inteiro por trás dela (os
campos, os botões e os detalhes pequenos ficam de fora) e mede o texto contra cada mistura; **o pior conta**. O
desfoque (`backdrop-filter`) não entra na conta: ele espalha as cores, mas não clareia nem escurece a média de um
fundo liso. Se o cabeçalho passa sobre uma imagem ou um gradiente, este trecho não basta: use as capturas.

**O método das capturas** (para imagem, gradiente, vídeo, ou para conferir o trecho 7):

1. Esconda o texto (`color: transparent` no elemento) para fotografar só o que está por trás dele.
2. Tire a captura da caixa do texto (no Playwright, `locator.screenshot()`; pelo protocolo,
   `Page.captureScreenshot` com `clip`).
3. Ache o pixel mais claro e o mais escuro da captura e meça o contraste do texto contra os dois. O pior conta.
4. Com vidro, repita com a página rolada até que o conteúdo mais claro e o mais escuro tenham passado por trás.

A régua dos ensaios de novembro de 2026 não fez isto e pulou os textos sobre gradiente e imagem: é o buraco que esta
skill fecha.

## O que estes trechos não veem

- O contraste em `:hover`, `:active` e no meio de uma transição; o texto de `::before` e `::after`.
- A ordem de leitura do leitor de tela e o que ele anuncia: isso se confere com o leitor de tela de verdade (NVDA,
  VoiceOver, TalkBack), ou fica escrito como não medido.
- Um gráfico: a paleta dele se confere pela simulação de daltonismo, não por estes trechos.
- O que só um aparelho mostra: as áreas seguras do celular, o tamanho de letra do sistema numa WebView.
