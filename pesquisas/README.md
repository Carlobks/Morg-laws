# Pesquisas

Toda pesquisa feita para o Morg-laws que outra sessão ou outra pessoa vai reler fica aqui: um arquivo por
pesquisa, com o nome `AAAA-MM-DD-<assunto>.md`, para não ter de ser refeita.

Cada pesquisa tem cinco seções, nesta ordem: **Pergunta**, **Fontes**, **O que se mediu**, **O que não se
verificou** e **Conclusão**. Escreve-se com palavras próprias; o texto das fontes nunca se copia.

O teste `tests/test_fontes_e_pesquisas.py` (no CI) confere que cada pesquisa fica direto nesta pasta (sem
subpastas), está no índice abaixo com a data na última coluna, tem as cinco seções na ordem e que cada link dela
está no `FONTES.md`.

## Índice

| Arquivo | Pergunta | Data |
|---|---|---|
| [Hooks de compactação](2026-11-02-hooks-de-compactacao.md) | Que hooks do Claude Code disparam em volta de uma compactação, o que recebem e o que podem fazer? | 2026-11-02 |
| [Compactação no Claude Code e no Codex](2026-11-02-compactacao-claude-code-e-codex.md) | O que o `/compact` aceita em cada ferramenta, quando compactam sozinhas, o que volta depois e se a mesma skill serve às duas? | 2026-11-02 |
| [Código morto](2026-11-03-codigo-morto.md) | Como achar sempre do mesmo jeito o código que ficou para trás, e o que a ferramenta (knip) não vê? | 2026-11-03 |
| [Linha de base do uso](2026-11-05-linha-de-base-do-uso.md) | Quanto custava e como se comportava o trabalho com agentes num projeto real antes das regras, e o que se vai comparar depois? | 2026-11-05 |
| [Modelos de issue e de PR](2026-11-08-modelos-de-issue-e-de-pr.md) | Que modelos de issue e de PR o GitHub aceita, como se pede a prova sem deixá-la fugir e como se manda a segurança para um canal privado num repositório público? | 2026-11-08 |
| [Chamar skills e registrar decisões](2026-11-08-chamar-skills-e-registrar-decisoes.md) | Como se chama uma skill pelo nome no Claude Code e no Codex, o que limita o nome e a descrição, onde vão os moldes de uma skill e o que deve levar uma decisão de arquitetura escrita? | 2026-11-08 |
| [Páginas duplas num manual técnico](2026-11-09-paginas-duplas.md) | Vale pôr a prática numa página e a teoria na da frente num manual impresso, que livros já fazem assim, quanto custa no Typst ou no CSS de impressão e qual é a forma mais simples? | 2026-11-09 |
| [Hooks de compactação, a revisão](2026-11-13-hooks-de-compactacao-revisao.md) | O que mudou nas páginas dos hooks desde 2026-11-02, se a compactação automática se distingue pela entrada do `PreCompact`, se um hook quebrado pode parar a compactação ou a mensagem e o que o Codex lista? | 2026-11-13 |
| [Antes de começar um projeto](2026-11-14-antes-de-comecar-um-projeto.md) | Que perguntas decidem se um projeto vale a pena começar, e como um agente procura, no início, o que já existe pronto para adaptar? | 2026-11-14 |
| [Instalar só algumas skills](2026-11-14-instalar-so-algumas-skills.md) | O `npx skills add` deixa escolher as skills do Morg-laws uma a uma, o que se perde ao instalar só uma parte e o que muda no manual, no molde e nos testes? | 2026-11-14 |
| [Ensaios de design](2026-11-17-ensaios-de-design.md) | Qual skill de design faz as melhores telas com o mesmo modelo e o mesmo pedido, a `desenhando-telas` ajuda, ERP e sites pedem as mesmas regras, e que falhas de acessibilidade se repetem nas páginas que ganharam? | 2026-11-17 |
