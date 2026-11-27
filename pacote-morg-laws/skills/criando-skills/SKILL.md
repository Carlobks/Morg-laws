---
name: "criando-skills"
description: "Acrescenta as regras do usuário ao criar, melhorar ou auditar skills, sempre junto com a skill-creator: decidir se é skill, CLAUDE.md, conector ou memória, conferir sobreposição com skills existentes, medir o que o modelo faz sem a skill, limites oficiais de nome e descrição, fontes e código testados, e entrega do arquivo. Usar sempre que o usuário pedir para criar, melhorar, revisar ou auditar uma skill, ou transformar um procedimento repetido em skill, mesmo sem dizer \"skill\". Não usar quando o pedido é só usar uma skill que já existe."
---

# Criando skills: regras do usuário

Use junto com `skill-creator`, que traz o processo (rascunho, execuções com e sem a skill, revisão dos resultados, otimização da descrição). Esta skill cobre só o que ela não cobre ou o que não serve neste ambiente. Em conflito, vale a regra mais restritiva.

Por quê: uma skill mal escrita custa contexto em toda conversa, aciona na hora errada e dá falsa confiança.

## Antes de escrever

1. **Qual é o lugar certo?** Fato permanente do projeto (stack, convenções, "nunca rodar SQL destrutivo em produção"): `CLAUDE.md`. Procedimento com passos, checklist ou formato de saída que se repete: skill. Dado ou ação em sistema externo: conector (MCP); nunca guarde dados numa skill. Preferência pessoal: memória.
2. **Já existe algo parecido?** Liste as skills e leia a descrição das vizinhas: gatilhos que se sobrepõem ativam a skill errada. Prefira melhorar a existente. Se a nova depende de outra, cite-a pelo nome.
3. **O que o modelo já faz sozinho?** Rode dois ou três pedidos reais sem a skill, antes de escrever. Nos nossos testes o modelo já acertava o básico; o ganho esteve em portas de confirmação, formato fixo de fecho, limites e regras específicas do usuário. Escreva só isso.

## Limites e estilo

- `name`: até 64 caracteres, minúsculas, números e hífens, sem "claude" nem "anthropic"; siga o padrão da coleção.
- `description`: até 1024 caracteres, terceira pessoa, diz o que faz e quando usar, termina com "Não usar...", sem resumir o fluxo.
- Mesmo idioma na descrição e no corpo: o do usuário. Sem caminhos fixos de máquina nem informação que envelhece (versões, preços); se for inevitável, marque "a confirmar".
- O restante do estilo (explicar o porquê, menos de 500 linhas, descrição insistente) já está na `skill-creator`.
- Revelação progressiva: o que é longo ou de consulta vai para `references/`, e o que é repetido ou frágil vira script em `scripts/`; a `skill-creator` explica como. A documentação oficial pede ainda: cada referência a **um** nível de distância do `SKILL.md` (nada de arquivo que aponta para outro arquivo) e, a partir de 100 linhas, um índice no topo do arquivo de referência.

## Fatos e código

- Baseie-se em documentação oficial e leia as páginas, não só os resultados da busca. Cite as fontes.
- Separe o que foi lido agora do que vem do conhecimento do modelo (por exemplo, números de artigos de lei) e diga isso ao usuário.
- Teste o código, o SQL e os comandos que entram na skill (por exemplo, num Postgres de teste).
- Em tema legal ou financeiro, a skill não decide: manda confirmar com o profissional.
- Fonte de terceiros: indicativa, com aviso. Skill de terceiros: leia o SKILL.md e todos os scripts antes de instalar.

## Testes (formato da skill-creator)

- Casos de execução: uma pasta por caso em `evals/`, no formato da `skill-creator` (leia o `references/schemas.md` dela, para não fixar um formato que ela já mudou).
- Casos de gatilho em `trigger-eval.json`: lista de `query` e `should_trigger`. Inclua quase-acertos que partilham palavras com a skill mas pedem outra coisa; perguntas óbvias não testam nada. Para otimizar a descrição, a `skill-creator` pede cerca de 20.
- Rode com e sem a skill numa sessão nova, sem a skill e depois com ela, só texto, sem ações reais. Se o ambiente proíbe sub-agentes, a comparação às cegas e o benchmark da `skill-creator` ficam de fora. Sem navegador, mostre o resultado numa tabela na conversa.
- Diga que modelo foi testado (o ideal é Haiku, Sonnet e Opus) e que o teste de gatilho é simulado, porque a sessão lê o arquivo da skill inteiro.
- Corrija só o que os testes ou a revisão mostrarem.

## Entrega neste ambiente

- No claude.ai, entregue pela proposta de skill (`propose_skills`), com o SKILL.md completo. O cartão leva só esse arquivo, sem scripts nem pastas: se a skill precisar deles, avise. Gerar um arquivo `.skill` só se o usuário pedir.
- No Claude Code o cartão não existe: a entrega é o arquivo (com `scripts/` e `references/`, se houver) na pasta de skills do projeto ou no Morg-laws, commitado pela fila de commits.
- Para melhorar uma skill existente, leia o SKILL.md atual inteiro na mesma vez e entregue o arquivo completo atualizado, mantendo o nome e o que já funciona.
- Meça antes de entregar: descrição até 1024 caracteres, menos de 500 linhas, frontmatter válido.
- Feche com **Feito**, **Conferido** e **Não verificado**, e o próximo passo.

## Exemplo

Pedido: "transforma o fecho mensal da folha numa skill".

Resposta adequada: "O fecho mensal tem passos e formato de saída fixos, então faz sentido como skill; as regras permanentes (nunca inventar valores) iriam para o `CLAUDE.md`. Vou ver se já existe skill parecida. Três perguntas: (1) quais passos e prazos você segue hoje? (2) a saída é planilha ou relatório? (3) em que situações a skill não deve acionar? Depois testo três pedidos sem a skill, escrevo o rascunho e proponho o arquivo completo."