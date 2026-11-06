# Tetos e fontes

Cada número da skill `desenhando-telas`, com a fonte e a data em que foi lido. Um número que não foi confirmado na fonte oficial fica na seção "Por confirmar" e **não** se usa como regra.

## Confirmados

| O quê | Número | Fonte | Lido em |
|---|---|---|---|
| Contraste de texto normal | ≥ 4,5:1 | WCAG 2.2, critério 1.4.3 (AA) — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | 2026-10-30 |
| Contraste de texto grande | ≥ 3:1 | idem | 2026-10-30 |
| O que é "texto grande" | ≥ 18 pt (≈ 24 px) ou ≥ 14 pt em negrito (≈ 18,5 px) | idem (1 pt = 1,333 px) | 2026-10-30 |
| A cor não é o único sinal | critério 1.4.1 (nível A) | WCAG 2.2 — https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html | *por ler; citado de memória* |
| Alvo de toque (mínimo da norma) | ≥ 24 × 24 px | WCAG 2.2, critério 2.5.8 (AA) — https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | 2026-10-30 |
| Alvo de toque (Apple, iOS e iPadOS) | 44 × 44 pt padrão; 28 × 28 pt mínimo | Apple HIG, Accessibility — https://developer.apple.com/design/human-interface-guidelines/accessibility | 2026-10-30 |
| Abas fixas | no máximo 4 ("a partir de cinco, o contentor fica apertado") | Material Design 3, Tabs — https://m3.material.io/components/tabs/guidelines | 2026-10-30 |
| Abas na barra da Apple | sem número fixo: menos abas navegam melhor; as que não cabem vão para uma aba "Mais"; uma lista que a pessoa personaliza começa com 5 ou menos | Apple HIG, Tab bars — https://developer.apple.com/design/human-interface-guidelines/tab-bars | 2026-10-30 |
| Rótulo e valor | por cima do valor num contentor estreito (≈ 200 px); lado a lado num médio (≈ 400 px), com o rótulo em ≈ 40 % da largura | Innovaccer, Key Value Pair — https://design.innovaccer.com/components/keyValuePair/usage/ | 2026-11-06 |
| Opções exclusivas que pedem botões de opção | mais de 2 (macOS); botões de opção em grupos de 2 a 5; mais de ≈ 5: menu suspenso | Apple HIG, Toggles — https://developer.apple.com/design/human-interface-guidelines/toggles | 2026-11-06 |
| Ação primária | exatamente 1 | Prática comum dos sistemas de design; sem número de uma fonte única | — |

## Por confirmar (não usar como regra)

Estes números vieram de uma pesquisa anterior que citava o Oracle Redwood. O site do Redwood pede login e não foi possível ler a fonte.

| O quê | Número citado | Origem citada |
|---|---|---|
| Painéis lado a lado numa ficha | 2 a 8 | Oracle Redwood (page templates) |
| Passos de um processo guiado | 2 a 25 | Oracle Redwood |
| Informação de contexto num cabeçalho | 1 a 4 | Oracle Redwood |
| Ações secundárias | 1 a 10 | Oracle Redwood |
| Filtros visíveis | 0 a 5 | pesquisa anterior, sem fonte primária |

Uma versão anterior destas regras dizia "≤ 6 abas, segundo a Apple". A página da Apple **não** traz esse número (ver acima).

## Princípios citados

- **"Menos, mas melhor"**: Dieter Rams, nos seus dez princípios de bom design.
- **Lei da conservação da complexidade**: Larry Tesler. A complexidade não some, só muda de quem a carrega.
- **Heurística 8, "design estético e minimalista"**: Nielsen Norman Group — https://www.nngroup.com/articles/ten-usability-heuristics/
- **Abas bem usadas**: Nielsen Norman Group — https://www.nngroup.com/articles/tabs-used-right/
- **Região comum** (a caixa agrupa com mais força do que o espaço; tente primeiro só com espaço, e caixas a mais são ruído): Nielsen Norman Group — https://www.nngroup.com/articles/common-region/ (lido em 2026-11-06)
- **Proximidade** (o rótulo junto do campo; o espaço dentro de um grupo menor do que entre grupos; o afastado lê-se como não relacionado): Nielsen Norman Group — https://www.nngroup.com/articles/gestalt-proximity/ (lido em 2026-11-06)
- **Interruptores** (gravam na hora; o que espera por um botão usa botões de opção ou uma caixa de seleção; não se misturam os dois): Nielsen Norman Group — https://www.nngroup.com/articles/toggle-switch-guidelines/ (lido em 2026-11-06)
- **Padrões de ERP** (página de trabalho, navegação, plantas de página): Microsoft Dynamics 365 (https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/user-interface/workspace-form-pattern) e SAP Fiori (https://www.sap.com/design-system/fiori-design-web/v1-136/page-types/floorplans/when-to-use-which-floorplan). *Citados pela pesquisa anterior; não relidos agora.*
