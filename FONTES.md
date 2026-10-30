# Fontes

Toda fonte citada no repositório entra aqui, com a data em que foi lida e o que ela sustenta.
Fonte secundária leva a marca *(secundária)* até ser conferida na original.

## Entrega de regras a agentes

- **Claude Code — memória, CLAUDE.md, AGENTS.md e imports** — https://code.claude.com/docs/en/memory — lido em 2026-10-29.
  Sustenta: CLAUDE.md com menos de 200 linhas; imports não economizam contexto; com CLAUDE.md e AGENTS.md juntos, o Claude lê só o CLAUDE.md.
- **Claude Code — skills** — https://code.claude.com/docs/en/skills — lido em 2026-10-29.
  Sustenta: só a descrição da skill carrega no início; o corpo carrega quando é usada.
- **Claude Code — marketplace de plugins** — https://code.claude.com/docs/en/plugin-marketplaces — lido em 2026-10-29.
- **Agent Skills (padrão aberto)** — https://agentskills.io — citado pela documentação do Claude Code, 2026-10-29.
- **Vercel — skills CLI** — https://vercel.com/docs/agent-resources/skills — 2026-10-29 *(secundária: lido via busca)*.
- **AAIF — Measuring AGENTS.md: what five runs show** — https://aaif.io/blog/measuring-agents-md-what-five-runs-show-that-one-doesn-t — lido em 2026-10-29.
  Sustenta: o AGENTS.md é orientação, não barreira. Com um AGENTS.md curto (12 linhas), o agente foi mais rápido e gastou menos (um repositório, um agente, 2 tarefas, 5 corridas com e sem). O estudo **não** compara arquivos curtos com longos, e o autor chama-lhe «one data point». Conferido de novo em 2026-10-30.
- **Evaluating AGENTS.md (arXiv 2602.11988)** — https://arxiv.org/abs/2602.11988 — resumo lido em 2026-10-30.
  Sustenta: os arquivos de contexto «do not generally improve task success rates» e sobem o custo de inferência em mais de 20%, em média. O resumo não fala do tamanho dos arquivos, e a página não mostra a afiliação dos autores.
- **agents.md** — https://agents.md — lido em 2026-10-30 (numa auditoria independente). Sustenta: o formato é mantido pela Agentic AI Foundation, sob a Linux Foundation, e a página lista 23 ferramentas que o leem.

## Git e contas

- **Git Credential Manager — várias contas** — https://github.com/git-ecosystem/git-credential-manager/blob/main/docs/multiple-users.md — lido em 2026-10-29.
  Sustenta: o usuário no endereço do repositório escolhe a conta só para aquele repositório.

- **Git — `lockfile.c` (mensagem do `index.lock`)** — https://github.com/git/git/blob/master/lockfile.c — lido em 2026-10-29.
  Sustenta: o git não manda apagar o lock; só diz que outro processo pode estar a correr ou que o lock pode estar velho.

## Segurança

- **React — Critical Security Vulnerability in React Server Components (CVE-2025-55182)** — https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components — lido em 2026-10-30.
  Sustenta: CVSS 10.0; versões 19.0, 19.1.0, 19.1.1 e 19.2.0 afetadas; vulnerabilidades novas acrescentadas depois.
- **Next.js — Security Advisory CVE-2025-66478** — https://nextjs.org/blog/CVE-2025-66478 — 2026-10-30 *(secundária: lida via busca)*.
- **Vercel — React2Shell Security Bulletin** — https://vercel.com/kb/bulletin/react2shell — 2026-10-30 *(secundária: lida via busca)*. Sustenta: atualizar é a única correção completa.
- **Vercel — Postmortem on Next.js middleware bypass (CVE-2025-29927)** — https://vercel.com/blog/postmortem-on-next-js-middleware-bypass — lido em 2026-10-30.
  Sustenta: o cabeçalho `x-middleware-subrequest` saltava o middleware em apps com servidor próprio; o middleware não deve ser a única proteção das rotas.

- **gitleaks** (licença MIT) — https://github.com/gitleaks/gitleaks — lido em 2026-10-30.
  Sustenta: `gitleaks git --log-opts=…` verifica um intervalo de commits; sai com 0 sem vazamentos e com 1 quando acha (usado em `modelos/pre-push`).
- **gitleaks-action** — https://github.com/gitleaks/gitleaks-action — lido em 2026-10-30. Sustenta: a chave `GITLEAKS_LICENSE` é «required for organizations, not required for user accounts».
- **npm audit** — https://docs.npmjs.com/cli/v11/commands/npm-audit — lido em 2026-10-30. Sustenta: `--audit-level` decide a partir de que gravidade o comando falha, sem filtrar o relatório; exige um lockfile.
- **OSV-Scanner — saída e códigos de saída** — https://google.github.io/osv-scanner/output/ — lido em 2026-10-30. Sustenta: sai com 1 quando há qualquer vulnerabilidade e com 128 quando não acha pacotes; não documenta um limiar de gravidade.

## Interface e acessibilidade

- **WCAG 2.2 — Contrast (Minimum), 1.4.3** — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — lido em 2026-10-30.
  Sustenta: 4,5:1 para texto normal e 3:1 para texto grande, que é ≥ 18 pt (≈ 24 px) ou ≥ 14 pt em negrito (≈ 18,5 px).
- **WCAG 2.2 — Target Size (Minimum), 2.5.8** — https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — lido em 2026-10-30. Sustenta: alvo ≥ 24 × 24 px (AA).
- **Apple HIG — Accessibility** — https://developer.apple.com/design/human-interface-guidelines/accessibility — lido em 2026-10-30. Sustenta: controles de 44 × 44 pt (padrão) e 28 × 28 pt (mínimo) em iOS e iPadOS.
- **Apple HIG — Tab bars** — https://developer.apple.com/design/human-interface-guidelines/tab-bars — lido em 2026-10-30. Sustenta: menos abas navegam melhor; aba "Mais"; lista personalizável com 5 ou menos. **Não** traz um teto de 6.
- **Material Design 3 — Tabs** — https://m3.material.io/components/tabs/guidelines — lido em 2026-10-30. Sustenta: não mais de 4 abas fixas.
- Os demais (NN/g, Rams, Tesler, Dynamics, Fiori e os tetos por confirmar do Oracle Redwood) estão em `skills/desenhando-telas/references/tetos-e-fontes.md`.

## Inspirações (nada copiado)

- **Matt Pocock — skill "grill-me"** (licença MIT) — https://github.com/mattpocock/skills — consultado em 2026-10-29.
  Inspirou a ideia de interrogar o dono antes de executar. A skill `pondo-o-plano-a-prova` foi escrita do zero, com estrutura própria.
- **OWASP Cheat Sheet Series** (CC BY-SA 4.0) — https://cheatsheetseries.owasp.org/ — referência de segurança. Indica-se só por link; o conteúdo não se copia, porque a licença ShareAlike não combina com a CC BY 4.0 deste repositório.

## Livros e autores

- **Fabio Akita — Competente o Suficiente** (livro). Citado por capítulo e página.
  - pp. 128–129: skills e ferramentas de terceiros só com leitura completa e uma dor concreta (usado em `escrevendo-regras-de-agente`).
  - p. 165: modelos esconderam uma biblioteca vulnerável numa lista de exceções (base de "sem silenciar alarme").
- **Fabio Akita — blog** — https://akitaonrails.com
