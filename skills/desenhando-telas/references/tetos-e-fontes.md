# Tetos e fontes

Cada número e cada regra da skill `desenhando-telas`, com a fonte e a data em que foi lida. Um número que não foi
confirmado na fonte oficial fica na seção «Por confirmar» e **não** se usa como regra. Um número marcado «nosso» não
tem fonte: é o ponto de partida da skill, a calibrar com o uso.

Os números de acessibilidade (contraste, alvos de toque, a cor como único sinal, o movimento reduzido) passaram para a
`cuidando-da-acessibilidade`, com as fontes em `references/regras-e-fontes.md` dela.

## Tetos confirmados

| O quê | Número | Fonte | Lido em |
|---|---|---|---|
| Abas fixas | no máximo 4 («a partir de cinco, o contêiner fica apertado») | Material Design 3, Tabs — https://m3.material.io/components/tabs/guidelines | 2026-10-30 |
| Abas na barra da Apple | sem número fixo: menos abas navegam melhor; as que não cabem vão para uma aba «Mais»; uma lista que a pessoa personaliza começa com 5 ou menos | Apple HIG, Tab bars — https://developer.apple.com/design/human-interface-guidelines/tab-bars | 2026-10-30 |
| Rótulo e valor | por cima do valor num contêiner estreito (≈ 200 px); lado a lado num médio (≈ 400 px), com o rótulo em ≈ 40 % da largura | Innovaccer, Key Value Pair — https://design.innovaccer.com/components/keyValuePair/usage/ | 2026-11-06 |
| Opções exclusivas que pedem botões de opção | mais de 2 (macOS); botões de opção em grupos de 2 a 5; mais de ≈ 5: menu suspenso | Apple HIG, Toggles — https://developer.apple.com/design/human-interface-guidelines/toggles | 2026-11-06 |
| Ação primária | exatamente 1 | Prática comum dos sistemas de design; sem número de uma fonte única | — |

## Das skills de terceiros (lidas nos commits fixos, destiladas com palavras nossas)

Lidas em 2026-11-16 e relidas em 2026-11-17; o `LICENSE` de cada repositório foi reaberto no commit em 2026-11-17.

| Regra da skill | Valor | Fonte |
|---|---|---|
| Pessoa, verbo e tom em palavras que dizem algo; o ponto focal dito antes | — | Damola Akinleye, `interface-design` (MIT), commit `2f9be320` |
| Escala de letra por razão | ≈ 1,2 (denso), ≈ 1,25 (comum) | idem |
| Três níveis num tamanho só | valor 600, rótulo 500, meta 400 | idem |
| Densidade decidida em px | 12–16 px numa tela de operação; com 24 px a tela já respira como material de divulgação | idem |
| Distribuição e acento | ≈ 60/30/10; uma cor de acento | idem |
| Uma estratégia de profundidade | bordas, sombras ou degraus de fundo, sem misturar | idem |
| Estados de cada bloco de dados | carregando, vazio, erro | idem |
| Teste da troca e de semicerrar os olhos | — | idem |
| Atalhos de alta frequência sem animação | centenas de vezes por dia | Emil Kowalski, `emil-design-eng` (MIT), commit `64eb3deb`; e `interface-design` |
| Durações e curvas | ver `movimento-no-sistema.md` | Emil Kowalski, `emil-design-eng` |
| Escalonamento e uma entrada por contêiner | 30–80 ms; o grupo abaixo de cerca de 300 ms | Emil Kowalski, `choreograph` (MIT), commit `64eb3deb` |
| Mola, arrasto e projeção | amortecimento 1,0, resposta 0,3–0,4 s; `d ≈ 0,998` | Emil Kowalski, `apple-design` (MIT), commit `64eb3deb` |
| Pressão | `scale(0.96)`; nunca abaixo de 0,95 | Jakub Krehel, `make-interfaces-feel-better` (MIT), commit `1a2aa969` |
| Traço do ícone pelo peso do texto | 1,5 px ao lado de 400; 2 px ao lado de 500–600 | idem |
| Rever o movimento a 10 % da velocidade | — | idem |

**Onde esta skill diverge das fontes, e por quê:**

- A `interface-design` põe a barra lateral com o mesmo fundo da tela e as bordas em `rgba` de baixa opacidade. Aqui a
  lateral de detalhe usa fundos de tom diferente (foi o que funcionou nos ensaios), e as bordas têm cor sólida com
  fronteira de pelo menos 1,2:1, que não muda com o que está atrás (um incidente do projeto de origem).
- A `emil-design-eng` não anima nada que o teclado dispara. Aqui o cartão movido pelo teclado anima, curto; o atalho
  continua sem animação.
- A `interface-design` cita 44 × 44 px como regra da WCAG. A WCAG pede 24 × 24 px no nível AA (critério 2.5.8); os
  44 × 44 são do nível AAA dela (critério 2.5.5, citado de memória, não relido) e o padrão da Apple. Os alvos estão na
  `cuidando-da-acessibilidade`.

## Dos ensaios às cegas (novembro de 2026)

Regras que vêm do julgamento de uma pessoa, às cegas, sobre telas de sistema feitas por agentes com e sem skills (o
resumo está na pesquisa
[`2026-11-17-ensaios-de-design.md`](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-17-ensaios-de-design.md)).
Um só juiz e um ensaio por skill: valem como direção, não como lei.

- Cartões-resumo que abrem ao clicar, ou abas com contagem: todas as fichas mostraram informação demais.
- A entrada da ficha com o nome em destaque e uma só coisa à direita; o bloco do que precisa de atenção com ícone por
  tipo.
- KPIs em 3 × 2 agrupados, não numa linha; cartões com a mesma altura; nenhum cartão alto e estreito sozinho; sem
  espaço vazio no cabeçalho.
- A lateral `sticky` do que precisa de atenção, com a entrada e o movimento ao acompanhar o scroll.
- A legenda de teclas à vista, dizendo como começar; o teclado de mover com espaço, setas, espaço e Esc; o teclado
  também dentro da lateral.
- O «Mover para» com os estados em fila; a lateral de detalhe com linhas finas e fundos de tom diferente.
- No escuro, pouca cor; nada de listras nem barras decorativas; o alerta com pouca cor e um ícone.
- O quadro no celular falhou em todas: a solução de uma coluna por vez é nossa, ainda sem prova.
- Animações ao mover cartões e na entrada do painel pesaram no julgamento.

## Por confirmar (não usar como regra)

Estes números vieram de uma pesquisa anterior que citava o Oracle Redwood. O site do Redwood pede login e não foi
possível ler a fonte.

| O quê | Número citado | Origem citada |
|---|---|---|
| Painéis lado a lado numa ficha | 2 a 8 | Oracle Redwood (page templates) |
| Passos de um processo guiado | 2 a 25 | Oracle Redwood |
| Informação de contexto num cabeçalho | 1 a 4 | Oracle Redwood |
| Ações secundárias | 1 a 10 | Oracle Redwood |
| Filtros visíveis | 0 a 5 | pesquisa anterior, sem fonte primária |

Uma versão anterior destas regras dizia «≤ 6 abas, segundo a Apple». A página da Apple **não** traz esse número (ver
acima).

## Princípios citados

- **«Menos, mas melhor»**: Dieter Rams, nos seus dez princípios de bom design.
- **Lei da conservação da complexidade**: Larry Tesler. A complexidade não some, só muda de quem a carrega.
- **Heurística 8, «design estético e minimalista»**: Nielsen Norman Group — https://www.nngroup.com/articles/ten-usability-heuristics/
- **Abas bem usadas**: Nielsen Norman Group — https://www.nngroup.com/articles/tabs-used-right/
- **Região comum** (a caixa agrupa com mais força do que o espaço; tente primeiro só com espaço, e caixas a mais são
  ruído): Nielsen Norman Group — https://www.nngroup.com/articles/common-region/ (lido em 2026-11-06)
- **Proximidade** (o rótulo junto do campo; o espaço dentro de um grupo menor do que entre grupos; o afastado se lê como
  não relacionado): Nielsen Norman Group — https://www.nngroup.com/articles/gestalt-proximity/ (lido em 2026-11-06)
- **Interruptores** (gravam na hora; o que espera por um botão usa botões de opção ou uma caixa de seleção; não se
  misturam os dois): Nielsen Norman Group — https://www.nngroup.com/articles/toggle-switch-guidelines/ (lido em
  2026-11-06)
- **Padrões de ERP** (página de trabalho, navegação, plantas de página): Microsoft Dynamics 365
  (https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/user-interface/workspace-form-pattern) e SAP
  Fiori (https://www.sap.com/design-system/fiori-design-web/v1-136/page-types/floorplans/when-to-use-which-floorplan).
  *Citados pela pesquisa anterior; não relidos agora.*
