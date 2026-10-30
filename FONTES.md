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
  Sustenta: arquivo curto e concreto rende mais; o AGENTS.md é orientação, não barreira.
- **ETH Zurich — Evaluating AGENTS.md (arXiv 2602.11988)** — https://arxiv.org/html/2602.11988v1 — 2026-10-29 *(secundária: lido via resumo)*.
  Sustenta: arquivos de contexto longos podem baixar o acerto e subir o custo em mais de 20%.
- **AGENTS.md como padrão aberto da Linux Foundation** — https://codex.danielvaughan.com/2026/04/07/agents-md-open-standard-cross-tool-portability — 2026-10-29 *(secundária)*.

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

## Livros e autores

- **Fabio Akita — Competente o Suficiente** (livro). Citado por capítulo e página.
  - pp. 128–129: skills e ferramentas de terceiros só com leitura completa e uma dor concreta (usado em `escrevendo-regras-de-agente`).
  - p. 165: modelos esconderam uma biblioteca vulnerável numa lista de exceções (base de "sem silenciar alarme").
- **Fabio Akita — blog** — https://akitaonrails.com
