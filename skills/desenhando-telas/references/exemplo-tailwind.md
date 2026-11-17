# Exemplo: os papéis em Tailwind, tema escuro

Uma forma de aplicar a skill `desenhando-telas` com Tailwind CSS, num tema escuro de cinzas frios (`slate`). É um
**exemplo**: troque as cores pelas do seu projeto e mantenha as **relações** (fronteira ≥ 1,2:1, um acento por tela,
estado em tokens, só `transform` e `opacity` animados).

Os tamanhos abaixo de `text-xs` (`text-2xs`, `text-3xs`) são degraus extra, em `rem`, que se definem no tema do projeto.
O contraste dos textos se confere com a `cuidando-da-acessibilidade`.

## Superfícies

| Papel | Classe |
|---|---|
| Fundo da página | `bg-slate-950` |
| Cartão / painel | `bg-slate-900` |
| Elevado (modal) | `bg-slate-950 border border-slate-800 shadow-2xl` |
| Campo de entrada | `bg-slate-800` |
| Borda de cartão e de campo | `border-slate-700` |
| Divisória de lista | `divide-y divide-slate-800` |
| Cabeçalho de tabela | `bg-slate-800 border-b border-slate-700` |
| Fundo atrás do modal | `bg-slate-950/75 backdrop-blur-md` |

Calculado com as cores do Tailwind (fórmula de luminância do WCAG):

- a borda `slate-700` dá 1,72:1 sobre o cartão (`slate-900`) e 1,95:1 sobre o fundo (`slate-950`);
- a divisória `slate-800` dá 1,22:1 sobre o cartão;
- entre fundos, `slate-950 → slate-800` dá 1,38:1. Já `slate-950 → slate-900` dá só 1,13:1, que não chega para separar
  sem borda.

## Texto

| Papel | Classe |
|---|---|
| Número protagonista | `tabular-nums text-3xl font-semibold tracking-tight text-slate-50` |
| Nome na entrada da ficha | `text-2xl font-semibold tracking-tight text-slate-50` |
| Título de seção | `text-sm font-semibold text-slate-200` |
| Valor | `text-sm font-semibold text-slate-100` (peso 600) |
| Rótulo | `text-sm font-medium text-slate-300` (peso 500) |
| Meta, texto de apoio | `text-xs text-slate-400` (peso 400) |

## Estado e identidade

Defina tokens de estado no tema (`status-ok`, `status-danger`, `status-warning`, `status-neutral`). Um alerta usa pouca
cor e um ícone, não o fundo inteiro:

```txt
cartão bloqueado: o cartão normal + border-l-2 border-l-status-danger
                  ícone de cadeado (size-4, stroke-[1.5]) + texto «Bloqueado» em text-xs text-status-danger
pílula de estado: inline-flex items-center gap-1 rounded-lg px-2 py-1 text-2xs font-semibold
                  bg-status-ok/10 text-status-ok ring-1 ring-status-ok/30
```

## Receitas

```txt
// Cartão de seção (um bloco-resumo da ficha ou do painel)
rounded-2xl border border-slate-700 bg-slate-900 p-4

// Grade de KPIs: 3 × 2 no computador, 2 × 3 no tablet, uma coluna no celular
grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3

// Cartões vizinhos com a mesma altura
grid auto-rows-fr gap-4 lg:grid-cols-3

// Lateral que acompanha o scroll
aside: sticky top-4 self-start
       a transição do movimento, se houver: transition-transform duration-200 ease-[cubic-bezier(0.23,1,0.32,1)]

// Coluna do quadro que rola sozinha
coluna:    flex max-h-[calc(100dvh-8rem)] flex-col
cabeçalho: shrink-0
lista:     min-h-0 flex-1 overflow-y-auto overscroll-contain

// Linha de lista (dentro de um só contêiner com divide-y divide-slate-800)
linha:    flex items-center gap-3 py-2.5
título:   truncate text-sm font-semibold text-slate-100
apoio:    truncate text-xs text-slate-400
valor:    shrink-0 tabular-nums text-sm font-semibold text-slate-100

// Botões
principal:  inline-flex min-h-11 items-center gap-2 rounded-xl bg-<acento>-600 px-5 text-sm font-semibold text-white
            transition-transform duration-150 ease-[cubic-bezier(0.23,1,0.32,1)] active:scale-[0.97]
            disabled:opacity-40
secundário: inline-flex min-h-11 items-center rounded-xl border border-slate-700 px-5 text-sm font-medium
            text-slate-300 hover:bg-slate-800 active:scale-[0.97]
fantasma:   inline-flex min-h-11 items-center gap-1 rounded-lg border border-slate-700 px-3 text-xs font-medium
            text-slate-300 hover:bg-slate-800
ferramenta: inline-flex min-h-11 items-center gap-1 rounded-lg px-2 text-xs font-semibold text-slate-300
            hover:bg-slate-800 aria-pressed:bg-slate-800   (sem borda, dentro do contêiner em que age)

// Controle segmentado: o ativo por elevação, nunca pela cor da marca
ativo:  bg-slate-700 text-white ring-1 ring-slate-600
outro:  bg-slate-900 text-slate-300 ring-1 ring-slate-700 hover:bg-slate-800

// Legenda de teclas no cabeçalho
flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-400
tecla: rounded border border-slate-700 bg-slate-800 px-1.5 font-mono text-2xs text-slate-200

// Modal (se não houver um componente pronto): sempre por portal
envoltório: fixed inset-0 z-[70] flex items-center justify-center p-4
fundo:      absolute inset-0 bg-slate-950/75 backdrop-blur-md
diálogo:    relative flex max-h-[90vh] w-full max-w-xl flex-col overflow-hidden rounded-3xl
            border border-slate-800 bg-slate-950 shadow-2xl
```

`min-h-11` dá 44 px. A rolagem por coluna e o `overscroll-contain` evitam que rolar uma coluna role a página.

## Forma e espaço

- Arredondamento: `rounded-xl` em controles, `rounded-2xl` em cartões, `rounded-3xl` em modais, `rounded-full` em
  pontos e avatares. O de dentro é o de fora menos o padding.
- Espaço: `space-y-8` entre seções, no máximo `space-y-3` dentro delas; padding de 16 px (`p-4`) para uma tela densa,
  mantido em todos os cartões.

## Movimento

- Nomeie as propriedades: `transition-transform`, `transition-opacity`, `transition-colors`; nunca `transition-all`.
- Saída forte em tudo o que entra ou responde: `ease-[cubic-bezier(0.23,1,0.32,1)]`, com `duration-150` a
  `duration-200`; modais e gavetas até `duration-300` ou mais, sem passar de 500 ms.
- Entrada que escalona: um `--delay` por bloco (`[animation-delay:var(--delay)]`), com passos de 30 a 80 ms e
  `animation-fill-mode: both`, para o bloco atrasado não aparecer pronto antes da hora.
- Movimento reduzido: as variantes `motion-safe:` e `motion-reduce:` seguem a preferência do sistema. Se o projeto tem
  um interruptor próprio, use a variante dele no lugar (por exemplo, uma variante personalizada ligada a um atributo
  no `<html>`). Em qualquer um, sobram a opacidade e a cor.
