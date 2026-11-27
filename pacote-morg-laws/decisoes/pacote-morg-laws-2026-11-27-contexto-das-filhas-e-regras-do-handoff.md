# O contexto das sessões-filhas e o handoff passam a ter limites escritos

- **Data:** 2026-11-27 · **Estado:** aceite
- **Onde se aplica:** a skill `orquestrando-sessoes` (secção 3b e `references/briefing-molde.md`) e a skill `passando-o-trabalho` (secção 2; vive em `~/.claude/skills/`, fora do repositório)

**Contexto:** uma filha rebentou o teto da ferramenta Read ao ler um plano de ~160 KB (pesquisa de 19-11:
`docs/pesquisas/2026-11-19-contexto-da-sessao-filha-e-o-morg-laws.md`). A pesquisa de 26-11
(`docs/pesquisas/2026-11-26-regras-do-handoff-limites-estrutura-partir.md`) mediu 41 handoffs: 3 passam de 16 KB.

**Decisão** (PO, 27-11, ronda de perguntas):
1. **Contexto das filhas: «A+B+E já, D depois».** A mãe mede o que manda ler e escrever (teto de ~60 mil tokens, leitura e escrita
   somadas) e parte a tarefa se passar; a filha lê por secções (`grep -n '^#'`, `Read` com `offset`/`limit`); o briefing segue um molde
   com secção, linhas e tamanho medido de cada ficheiro, o que não ler, o que se escreve, orçamento, prova, modelo e fim.
2. **Regras do handoff: «Aceitar as 7».** Limite de 150 linhas e 16 KB, sem catraca; a «Atualização da entrega» funde-se na próxima
   gravação de cada handoff; histórico só no git e em `docs/decisoes/`; a mãe copia para o briefing só o que a filha precisa e aponta
   secções pelo título quando ela continua o assunto; a auditoria a frio nunca recebe o handoff; nada de um ficheiro por parte; levar
   ao Morg-laws. O formato que `scripts/entrega/ler-handoffs-da-entrega.mjs` lê não muda.

**Porquê:** o teto da Read e o meio do contexto perdido são medidos; escrever o limite em texto custa pouco e só vira máquina se voltar a falhar.

**Fica para quem herda:** catraca de tamanho em bytes para os `.md` de plano (D); partir planos grandes só quando forem tocados (C).
**Alternativas recusadas:** hook no `start_session` (F, não verificado); ficheiro por parte e índice com números de linha; catraca dos handoffs já.
