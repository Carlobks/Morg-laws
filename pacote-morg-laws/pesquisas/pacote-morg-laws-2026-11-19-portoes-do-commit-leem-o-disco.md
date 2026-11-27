---
titulo: Porque é que o commit de uma sessão é recusado pelo trabalho de outra, e como outros resolveram
data: 2026-11-19
area: infra
estado: concluida
destino: modelo-de-mudanca/fila-de-commits/plano-portoes-medem-a-copia-do-commit.md
---

## Pergunta

A 19-11, a sessão da fase 3b das exceções do npm audit foi recusada várias vezes pelo pre-commit. Na saída apareciam
ficheiros que eram da sessão das rescisões (Fase 7c). A mãe da adoção atribuiu a causa à leitura do índice inteiro
pelas catracas (`scripts/catracas/ler-do-git.mjs:17`). O PO pediu a quem desenhou a fila que auditasse, medisse,
procurasse como outros resolveram e planeasse a correção, sem mudar nada antes do «sim» dele.

## Fontes lidas

- **Quentin Santos — Efficient pre-commit hooks with checkout-index** — https://qsantos.fr/2023/11/08/the-secret-to-a-green-ci-efficient-pre-commit-hooks-with-checkout-index/ (lido agora). Exporta o índice para uma pasta temporária com `git checkout-index -af --prefix=<pasta>/` e corre lá os portões. A pasta apaga-se num `trap`, e as dependências apontam para as da raiz.
- **jyn — pre-commit hooks are fundamentally broken** — https://jyn.dev/pre-commit-hooks-are-fundamentally-broken (lido agora). Os hooks julgam o disco, não o commit. O autor prefere verificar no `pre-push`, sempre sobre o índice.
- **lint-staged — README (17.0.5)** — https://cdn.jsdelivr.net/npm/lint-staged@17.0.5/README.md (lido agora). Esconde o que não está preparado com um `stash` de reserva enquanto os portões correm, e avisa que isso mexe nos ficheiros da pasta.
- O `git commit -- <caminhos>` (`--only`) monta um índice temporário com o HEAD e os caminhos, e dá-o aos hooks em `GIT_INDEX_FILE`; a medição 1 confirma-o (do conhecimento do modelo)
- Os guias sobre vários agentes no mesmo repositório recomendam uma worktree por agente, já descartada no ERP pelo `.context/HANDOFF-fila-de-commits.md` (do conhecimento do modelo)

## O que se mediu

Tudo feito sem escrever no índice partilhado: índices de ensaio com `GIT_INDEX_FILE` no scratchpad e um repositório de rascunho.

1. **Num commit por caminho, o hook vê o HEAD mais os caminhos do commit, e nada do que outra sessão preparou.**
   Ensaio num repositório de rascunho: `a.txt` no HEAD, `alheio.txt` preparado, `git commit -m meu -- meu.txt`. Saída do hook:
   `GIT_INDEX_FILE=…/.git/next-index-24016.lock` e `ls-files: a.txt meu.txt`. Depois do commit, `alheio.txt` continua preparado.
   Git 2.54.0.windows.1. A auditoria F1 dos nomes de documentos (13-11) já tinha medido o mesmo.
2. **O vitest herda esse índice.** Com `GIT_INDEX_FILE` apontado para um índice vazio, `catraca-mapa-de-regras-e-barreiras`
   falha («leu o CLAUDE.md do índice: expected +0 to be 1»). Sem a variável, passa (11 de 11).
3. **Os testes que apagam `GIT_*` não contaminam os ficheiros seguintes.** `ler-do-git-nomes-com-acento` e o mapa, com
   `--maxWorkers=1` e o índice vazio: o mapa continua a falhar, ou seja, continua a ler o índice vazio.
4. **O HEAD nunca esteve vermelho na catraca de nomes.** A catraca `nomes-unicos` foi medida em cada um dos 16 commits de 19-11 entre as 09:31
   e as 11:16, cada um contra a linha de base do seu próprio commit: `pioraram=0` em todos.
5. **O HEAD mais os ficheiros de código da 3b passam.** Índice de ensaio = HEAD + `avisos-do-push-com-excecoes.mjs` + `relatorio-do-npm-audit-por-aviso.mjs`
   → `pioraram: 0`.
6. **A causa reproduzida está no disco.** O código das catracas, as linhas de base e os testes são lidos da pasta partilhada.
   Índice de ensaio = árvore de `0932c1d6` (antes das rescisões), com o `medir-seguranca-rotas-sem-sessao.mjs` do disco, que já
   tinha a rota nova. Resultado: `× cada rota pública tem o motivo escrito e ainda existe`, com `+ "app/api/rotinas/rescisoes-agendadas/route.ts"`.
   É a recusa que a 7.ª auditoria A sofreu num commit de um só `.md`.
7. **O tamanho do problema hoje.** `registo.jsonl` da fila, 19-11: 41 commits, 25 com código 1 (o git recusou). Não se sabe quantos têm esta causa.
8. **O custo de exportar o commit.** `git checkout-index -a -f --prefix=<scratchpad>/` dos 3603 ficheiros seguidos: 3339 ms.
   Só `scripts/catracas`, `__tests__/catracas` e `scripts/git-hooks` (98 ficheiros): 476 ms. Um commit pela fila leva hoje 50 a 110 s de vez.

## O que não se verificou

- **A saída exata do hook da 3b que listava ficheiros das rescisões.** As saídas das ferramentas não se leem pelas ferramentas de sessão.
  Pelas medições 1 a 5, um hook não podia vê-los. O mais provável é virem de corridas manuais das catracas
  (`npx vitest` fora do hook, que lê o índice real). A própria 3b escreveu «Estou a ver que nomes a catraca de nomes únicos recusa» antes de três chamadas Bash.
- **Se os portões correm iguais numa cópia do commit.** Não se mediu: os testes podem precisar de ficheiros não seguidos,
  o cache do `tsc`/vitest pode arrefecer e o `node_modules` pode não se ligar por junção no Windows. É a fase 1 do plano.
- **O erro do PowerShell `InvokeMethodOnNull` (`$_.StartTime` nulo) que a 7.ª auditoria A viu na fila.** Não se reproduziu.

## Conclusão

**A hipótese do índice inteiro está errada.** O que outra sessão deixa preparado no índice não entra no hook de um commit por caminho,
e um «exigir índice limpo» travaria sem necessidade. **A fuga está no disco:** o que os portões executam (o código das catracas, as
linhas de base, os testes, o `tsc` do projeto) vem da pasta partilhada. Quando outra sessão muda uma catraca ou uma linha de base sem a
commitar, todos os commits medem o índice novo com a régua dessa sessão.

Como outros resolvem:
- esconder o resto com `stash` (lint-staged, pre-commit), que aqui está proibido porque mexe nos ficheiros das outras sessões;
- correr os portões numa cópia do commit (`checkout-index`, Quentin Santos);
- passar as verificações para o `pre-push` (jyn);
- uma worktree por agente, que no ERP já está descartada.

A recomendação está no plano.
