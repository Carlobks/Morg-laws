# Chamar skills, limites do nome e da descrição, moldes e decisões de arquitetura

Data: 2026-11-08.

## Pergunta

Como se chama uma skill pelo nome no Claude Code e no Codex, o que limita o nome e a descrição, onde vão os moldes de
uma skill e o que deve levar uma decisão de arquitetura escrita? A resposta sustenta o teste do formato das skills, o
alargamento da `pondo-o-plano-a-prova` às mudanças e a regra do título das sessões na `orquestrando-sessoes`.

## Fontes

Todas relidas em 2026-11-08 com o `WebFetch` (um modelo pequeno resume cada página, e as frases vêm desse resumo). Cada
uma tem a sua entrada no `FONTES.md`:

- **Chamar e abrir skills:** as skills do Claude Code — https://code.claude.com/docs/en/skills — e as skills do Codex —
  https://developers.openai.com/codex/skills
- **O formato do `name` e da `description`:** a especificação aberta — https://agentskills.io/specification — e a visão
  geral da plataforma — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- **Onde carregam os arquivos de uma subpasta:** a memória do Claude Code — https://code.claude.com/docs/en/memory
- **Renomear uma sessão:** os comandos do Claude Code — https://code.claude.com/docs/en/commands —, a app de desktop —
  https://code.claude.com/docs/en/desktop — e os comandos do Codex —
  https://developers.openai.com/codex/cli/slash-commands
- **Decisões de arquitetura:** Michael Nygard, *Documenting Architecture Decisions* —
  https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions

## O que se mediu

Contado nos arquivos do próprio repositório, em 2026-11-08:

| O quê | Resultado |
|---|---|
| Skills | 12 |
| Descrições | de 574 a 865 caracteres, 8.361 no total (contado antes do alargamento da `pondo-o-plano-a-prova`, no commit `e63d480`) |
| Skills com palavras de Portugal no `SKILL.md` | 9 de 12 (a `pondo-o-plano-a-prova` não tem nenhuma) |
| `AGENTS.md` da raiz | 60 linhas (o teto do `pre-commit`) |

O que as páginas dizem, com palavras nossas:

- **Chamar:** no Claude Code, `/nome-da-skill` no começo da mensagem abre a skill e o resto do texto chega como
  argumentos; no Codex, `/skills` ou `$` servem no CLI e na extensão. As duas ferramentas também abrem a skill sozinhas
  pela descrição.
- **Limites:** o `name` tem até 64 caracteres, só minúsculas, algarismos e hífens, sem hífen no começo, no fim ou
  repetido, igual à pasta; a plataforma da Anthropic proíbe também as palavras `anthropic` e `claude` e marcas XML. A
  `description` tem de 1 a 1.024 caracteres. O `SKILL.md` fica abaixo de 500 linhas.
- **Moldes:** a especificação reserva `assets/` para moldes de documento e `references/` para documentação lida sob
  demanda. Um `AGENTS.md` ou `CLAUDE.md` dentro de uma subpasta pode carregar como regra quando o Claude abre um arquivo
  lá; por isso as cópias dos moldes dentro de uma skill não levam esses nomes.
- **Compactação:** ao resumir a conversa, o Claude Code anexa de novo a chamada mais recente de cada skill com os
  primeiros 5.000 tokens dela, num orçamento comum de 25.000. Uma skill de cerca de cem linhas cabe inteira.
- **Codex e a lista inicial:** a lista de nomes e descrições usa no máximo 2 % da janela do modelo, ou 8.000
  caracteres se a janela não for conhecida, e com muitas skills o Codex encurta as descrições primeiro (e pode depois
  deixar skills de fora, com um aviso). O orçamento sobe com `skills.max_context_tokens`. Antes do alargamento da
  `pondo-o-plano-a-prova` (commit `e63d480`) elas somavam 8.361, e com as desta fase chegavam a 9.402: sem janela
  conhecida, passavam do limite. A página não diz que parte corta; com a janela conhecida o limite é 2 % dela, que a
  página não traduz em caracteres.
- **Claude Code e a lista inicial:** o orçamento da lista é 1 % da janela do modelo; a lista leva sempre todos os nomes
  e, quando transborda, tira primeiro as descrições das skills menos invocadas. Cada entrada (`description` mais
  `when_to_use`) é cortada em 1.536 caracteres, seja qual for o orçamento. Sobe-se com `skillListingBudgetFraction` ou
  `SLASH_COMMAND_TOOL_CHAR_BUDGET`. Os sinais «<» e «>» de uma descrição aparecem como `&lt;` e `&gt;`.
- **A soma de hoje e o teto:** as 13 descrições somam 7.368 caracteres, contados com o `yaml` nos `SKILL.md`. O teste
  `tests/test_formato_das_skills.py` trava a soma em 7.600, para ficar abaixo dos 8.000 do Codex com folga para uma
  skill nova. Este é um teto contado, não uma prova de que as duas ferramentas listam todas as descrições.
- **Renomear:** na app de desktop clica-se no título da sessão ou pede-se ao Claude; no terminal do Claude Code,
  `/rename [nome]` (sem nome, gera um; vale no modo não interativo; até 200 caracteres); no Codex, `/rename <nome>`.
- **Decisões:** Nygard pede cinco partes (título, contexto, decisão, estado, consequências), números seguidos que não se
  reutilizam, a decisão revertida marcada como substituída e não apagada, uma ou duas páginas, e só para o que afeta a
  estrutura, as características não funcionais, as dependências, as interfaces ou as técnicas de construção.

## O que não se verificou

- Nenhuma skill foi chamada pelo `/…` nem pelo `$…` nesta pesquisa: a forma vem das páginas, não de uma sessão observada.
- No Codex, as páginas falam do CLI e da extensão; o que vale na aplicação web, na de desktop e no Codex Cloud não foi lido.
- O carregamento dos arquivos de subpasta é leitura da página da memória, não uma sessão observada.
- Não se leu o fim da página das skills do Claude Code (os primeiros 100.000 de 118.986 caracteres), nem o fim da página
  da app de desktop (os primeiros 100.000 de 221.007).
- Não se renomeou nenhuma sessão pelo `/rename`, nem no terminal do Claude Code nem no Codex; a página do Codex não diz
  se a extensão ou a aplicação têm outra forma.
- Não se sabe que parte das descrições o Codex corta, nem quanto valem os 2 % do Codex e o 1 % do Claude Code em
  caracteres com a janela conhecida.
- Os resumos das páginas vêm de um modelo pequeno, não da leitura delas por uma pessoa.

## Conclusão

O nome e a descrição têm limites que um teste local confere sem rede, e uma descrição escrita para o Claude Code
serve ao Codex desde que a soma das descrições se mantenha curta. Chamar uma skill pelo nome é a forma mais curta de
abrir uma conversa que dependa dela, e os moldes de documento vão em `assets/` com nomes que não carregam como regra.
Uma decisão de arquitetura merece uma página própria, numerada e nunca apagada. Nada disto mede se as skills funcionam:
isso só se vê no uso real.
