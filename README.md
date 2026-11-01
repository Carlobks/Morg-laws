# Morg-laws

Regras, boas práticas e aprendizados para trabalhar com agentes de IA no código
(Claude Code, Codex, Cursor, Copilot e outros). Tudo saiu do dia a dia de um sistema real em produção:
o que deu errado, a regra que nasceu disso e a fonte que a sustenta.

## O que tem aqui

| Pasta | O que guarda |
|---|---|
| `AGENTS.md` | O núcleo das regras e o índice. É o que o agente lê primeiro. |
| `skills/` | Regras por assunto (SQL, Supabase, Next.js, segurança, sessões…). O agente só abre o que o projeto usa. |
| `biblia-akita/` | Resumo, com palavras nossas, do livro *Competente o Suficiente*, de Fabio Akita, com capítulo e página. |
| `aprendizados/` | Notas datadas sobre bibliotecas, ferramentas e erros que custaram caro. |
| `modelos/` | Arquivos prontos para copiar, que transformam as regras em barreiras de máquina: hooks do Claude Code e `settings.json` em três colunas, hooks e portões do git, testes das regras, changelog por fragmentos, CI e moldes de documento (CLAUDE.md, mapa das barreiras, plano, handoff, ADR). Índice em [modelos/README.md](modelos/README.md). |
| `tests/` e `scripts/testar.sh` | Os testes dos modelos: cobertura de linhas e ramos a 100 % e um projeto de exemplo montado só com eles. |
| `FONTES.md` | Todas as fontes usadas, com a data em que foram lidas. |

O repositório está em construção: as pastas aparecem conforme as fases avançam.

## Como usar num projeto

```bash
npx skills add Carlobks/Morg-laws
```

O comando instala as skills em `.claude/skills/` (ou na pasta do agente que escolher). O `AGENTS.md` não vem com elas: copie-o para a raiz do projeto. No Claude Code, junte um `CLAUDE.md` com a linha `@AGENTS.md`. Detalhes e versão testada em [aprendizados/2026-10-30-instalacao-das-skills.md](aprendizados/2026-10-30-instalacao-das-skills.md).

Para que as regras sejam cumpridas e não só lidas, copie os modelos que servem ao projeto: os passos estão em
[modelos/README.md](modelos/README.md). O mínimo recomendado é a guarda do git, o hook de segredos e o que pergunta
antes do push (`modelos/claude/`), o `pre-commit` com o comando único de testes (`modelos/git/`) e o
`test_regras.py`, que liga cada regra do `CLAUDE.md` à barreira que a obriga.

## Para quem contribui

Ative os hooks depois de clonar:

```bash
git config core.hooksPath .githooks
```

O `pre-commit` recusa commits com e-mail que não seja o noreply do GitHub, com um nome de autor da lista negra e com AGENTS.md acima de 60 linhas.
Ele também procura nomes e dados sensíveis numa lista que fica **fora** do repositório
(`git config morg.listaNegra <arquivo>`); sem essa lista, só avisa. No GitHub, o `gitleaks` procura segredos em todo push.

Mudou um modelo? Rode os testes antes de commitar (o CI roda os mesmos em todo push):

```bash
pip install coverage ruff
sh scripts/testar.sh
```

## Licença

Texto sob [CC BY 4.0](LICENSE): pode copiar e adaptar, citando a origem.
