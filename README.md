# Morg-laws

Regras, boas práticas e aprendizados para trabalhar com agentes de IA no código
(Claude Code, Codex, Cursor, Copilot e outros). Tudo saiu do dia a dia de um sistema real em produção:
o que deu errado, a regra que nasceu disso e a fonte que a sustenta.

## O que tem aqui

| Pasta | O que guarda |
|---|---|
| `AGENTS.md` | O núcleo das regras e o índice. É o que o agente lê primeiro. |
| `skills/` | Regras por assunto (SQL, Supabase, Next.js, segurança, sessões…). O agente só abre o que o projeto usa. |
| `biblia-akita/` | Resumo, com palavras nossas, do livro *Competente o Suficiente*, de Fabio Akita, um arquivo por tema, cada conselho com a página e a skill que já o aplica. |
| `aprendizados/` | Notas datadas sobre bibliotecas, ferramentas e erros que custaram caro. |
| `modelos/` | Arquivos prontos para copiar, que transformam as regras em barreiras de máquina: hooks do Claude Code e `settings.json` em três colunas, hooks e portões do git, testes das regras, testes prontos da forma do código em Python e em TypeScript (vitest), changelog por fragmentos, CI e moldes de documento (AGENTS.md, CLAUDE.md, mapa das barreiras, plano, handoff, ADR). Índice em [modelos/README.md](modelos/README.md). |
| `tests/` e `scripts/testar.sh` | Os testes dos modelos: cobertura de linhas e ramos a 100 %, um projeto de exemplo em Python e outro em TypeScript (`tests/exemplo-ts/`, com o `package-lock.json` fixado) montados só com eles, e a prova de que as duas línguas dão o mesmo veredito. |
| `pesquisas/` | As pesquisas feitas para o repositório, uma por arquivo, com o índice em [pesquisas/README.md](pesquisas/README.md). |
| `projetos/` | O catálogo de projetos reais, anonimizados: de onde vem cada regra, com o incidente que a fez nascer. A regra de anonimato e o que barra cada commit estão em [projetos/README.md](projetos/README.md). |
| `FONTES.md` | Todas as fontes usadas, com a data em que foram lidas. |

O repositório está em construção: as pastas aparecem conforme as fases avançam.

## Como usar num projeto

```bash
npx skills add Carlobks/Morg-laws
```

O comando instala as skills em `.claude/skills/` (ou na pasta do agente que escolher). As regras não vêm com elas: copie o molde [modelos/documentos/AGENTS.md](modelos/documentos/AGENTS.md) para a raiz do projeto, como `AGENTS.md`, e preencha o que está entre `<…>`. No Claude Code, junte um `CLAUDE.md` com a linha `@AGENTS.md` (molde em [modelos/documentos/CLAUDE.md](modelos/documentos/CLAUDE.md)). O `AGENTS.md` da raiz deste repositório não se copia: leva também as regras de quem trabalha no próprio Morg-laws. Detalhes e versão testada em [aprendizados/2026-10-30-instalacao-das-skills.md](aprendizados/2026-10-30-instalacao-das-skills.md).

Para que as regras sejam cumpridas e não só lidas, copie os modelos que servem ao projeto: os passos estão em
[modelos/README.md](modelos/README.md). O mínimo recomendado é a guarda do git, o hook de segredos e o que pergunta
antes do push (`modelos/claude/`), o `pre-commit` com o comando único de testes (`modelos/git/`) e o
`test_regras.py`, que liga cada regra do `AGENTS.md` à barreira que a obriga. Para a forma do código (arquivo até 500
linhas, função nova até 20, nomes únicos, alarmes e testes saltados), copie os testes prontos de `modelos/testes/`
(Python) ou de `modelos/testes-ts/` (TypeScript, vitest); a skill `codigo-legivel` diz as regras e como adotá-las num
projeto que já viola.

## Para quem contribui

Ative os hooks depois de clonar:

```bash
git config core.hooksPath .githooks
```

O `pre-commit` recusa commits com e-mail que não seja o noreply do GitHub, com um nome de autor da lista negra, com AGENTS.md acima de 60 linhas e com dado pessoal ou identificador em `projetos/` (o teste lê o que está preparado).
Ele também procura nomes e dados sensíveis numa lista que fica **fora** do repositório
(`git config morg.listaNegra <arquivo>`); sem essa lista, só avisa. No GitHub, o `gitleaks` procura segredos em todo push.
O workflow `links` confere os links externos dos `.md` uma vez por semana e em cada mudança de `.md`: um vermelho dele quer dizer que um site não respondeu, e não que um teste partiu. Os links relativos e as fontes são conferidos pela suíte local, sem rede.

Mudou um modelo? Rode os testes antes de commitar (o CI roda os mesmos em todo push). Precisam do Python, do Node da
versão em `tests/exemplo-ts/.nvmrc` e do npm; o script roda o `npm ci` do exemplo quando o lockfile muda:

```bash
pip install coverage ruff
sh scripts/testar.sh
```

## Licença

Texto sob [CC BY 4.0](LICENSE): pode copiar e adaptar, citando a origem.
