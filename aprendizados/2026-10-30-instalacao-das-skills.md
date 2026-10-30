# Instalação das skills num projeto

Teste feito numa pasta vazia, com o repositório já publicado.

## `npx skills add` instala as skills, mas não o AGENTS.md

**O que aconteceu:** o comando `DISABLE_TELEMETRY=1 npx --yes skills@latest add Carlobks/Morg-laws -a claude-code -y` copiou as 10 skills para `.claude/skills/` e criou um `skills-lock.json` com a origem e o hash de cada uma. Comparámos arquivo a arquivo com o repositório (incluindo os `evals/`): 0 diferenças.
**Por que:** a ferramenta procura a pasta `skills/` do repositório, e só essa. O `AGENTS.md` e o `CLAUDE.md` da raiz não fazem parte de nenhuma skill, por isso ficam de fora.
**Como fazer:** depois do `npx skills add`, copie à mão o `AGENTS.md` para a raiz do projeto. Se a ferramenta for o Claude Code, junte um `CLAUDE.md` com a linha `@AGENTS.md`. Sem o AGENTS.md, o projeto fica sem o núcleo e sem o índice de «quando ler o quê». As skills continuam a abrir pela descrição.
**Versão:** pacote `skills` 1.7.4, testado em 2026-10-30.

## A instalação traz o aviso certo

**O que aconteceu:** no fim da instalação, a ferramenta avisa que as skills devem ser revistas antes de usar, porque correm com todas as permissões do agente.
**Como fazer:** trate uma skill de terceiros como código. Leia-a inteira antes de a instalar, e só a instale se ela resolver um problema concreto. O `skills-lock.json` permite saber depois de onde veio cada skill.
