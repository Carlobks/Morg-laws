# O que mudou na criando-skills

Origem: pesquisa de 26-11-2026 (`docs/pesquisas/2026-11-26-skill-de-criar-skills-nossa-vs-skill-creator.md`, «Conclusão»).
A cópia de partida é a sincronizada do claude.ai (plugin `criando-skills`, 49 linhas); o resto do texto ficou igual.

## 1. Formato dos testes

- **Antes:** «Casos de execução em `evals/evals.json`: `skill_name` e `evals` com `id`, `prompt`, `expected_output`, `files` e `expectations`.»
- **Depois:** «Casos de execução: uma pasta por caso em `evals/`, no formato da `skill-creator` (leia o `references/schemas.md` dela, para não fixar um formato que ela já mudou).»

## 2. Sem sub-agentes

- **Antes:** «Rode com e sem a skill em agentes independentes…» e «…porque o agente lê o arquivo da skill inteiro.»
- **Depois:** «Rode com e sem a skill numa sessão nova, sem a skill e depois com ela… Se o ambiente proíbe sub-agentes, a comparação às cegas e o benchmark da `skill-creator` ficam de fora.» e «…porque a sessão lê o arquivo…»

## 3. Revelação progressiva e scripts

- **Antes:** nada (a secção «Limites e estilo» só remetia o resto do estilo à `skill-creator`).
- **Depois:** linha nova em «Limites e estilo»: o longo vai para `references/`, o repetido ou frágil vira script em `scripts/` (a `skill-creator` explica como); referências a **um** nível do `SKILL.md`; índice no topo a partir de 100 linhas.

## 4. Entrega

- **Antes:** entrega só pelo cartão `propose_skills`; «proponha o arquivo completo».
- **Depois:** o cartão fica «No claude.ai»; nova linha: no Claude Code a entrega é o arquivo na pasta de skills do projeto ou no Morg-laws, commitado pela fila de commits. «Proponha» passou a «entregue».
- **Consequência na descrição (frontmatter):** «entrega pelo cartão de propostas» → «entrega do arquivo».

## Descrição (frontmatter)

Segue o que a documentação oficial pede: `name` com 15 caracteres, minúsculas e hífen; `description` abaixo de 1024 caracteres, em terceira pessoa, diz o que faz e quando usar e termina com «Não usar…».

## Não verificado

- Não se testou a skill a disparar numa sessão nova (nem os 3 modelos).
- Não se leu o `references/schemas.md` da `skill-creator`: a skill manda lê-lo, não o descreve.
- A regra «um nível» e «índice a partir de 100 linhas» vem da pesquisa, não de nova leitura da documentação oficial.
