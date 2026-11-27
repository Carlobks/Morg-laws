# Envio ao `main` por PR: a sequência do agente

Decisão: `docs/decisoes/2026-11-19-envio-ao-main-por-pr.md`. A `fechando-ciclo` («Push e release») aponta para aqui. Só se faz com o «sim» do PO ao envio; nada aqui se corre sem ele. O trabalho continua todo no `main` local: o ramo do PR só existe no GitHub, é igual ao `main` local no momento do envio, e **nunca se trabalha nele**.

**O «sim» do envio** (decisão do PO, B-3 da auditoria da 3c) cobre o push do ramo, o PR e o merge, **se o «Segurança» e o resto do CI ficarem verdes**. Se algo ficar vermelho, o agente pára e pede um «sim» novo **antes** de corrigir, porque a correção passa por uma auditoria; só depois tenta de novo (ver «Se o CI ficar vermelho»).

**Sem a proteção do `main`** (estado de 2026-11-19: plano Free, o PO decidiu seguir sem ela): o GitHub funde mesmo com o «Segurança» vermelho ou pendente, e aceitaria um push direto ao `main`. Desde a fase 4b o `pre-push` desta máquina recusa-o (ver «Os destinos que o `pre-push` aceita»); um push feito sem o hook (outra máquina, `--no-verify`) o GitHub ainda aceita. O resto da trava é o agente a seguir esta sequência.

## Antes

1. `git --no-optional-locks status`: nada por commitar que seja seu (os ficheiros de outras sessões não entram, ver a FILA DE COMMITS RULE).
2. `git fetch origin`, e `git merge-base --is-ancestor origin/main main`: tem de dizer sim. Se disser não, o `origin/main` andou (outro PR): incorpore-o no `main` local com um commit de merge pela fila antes de seguir (ver «O `git merge` e a fila»).
3. `npm run portao:financeiro` se o envio toca o Financeiro (PORTÃO DOS 5 PONTOS RULE).
4. O commit de topo **não leva** `[skip ci]`, `[ci skip]`, `[no ci]` nem `[skip actions]`: o CI não corria e o «Segurança» ficava pendente. Com a proteção, o merge ficaria bloqueado; sem ela, o GitHub fundia sem nada conferido.

## Enviar

5. Com o «sim» do PO, crie o ramo **no remoto**, sem criar nenhum ramo local:
   `git push origin main:refs/heads/envio/AAAA-MM-DD-<slug>`
   O `pre-push` corre como sempre e aceita este destino (ver «Os destinos que o `pre-push` aceita», abaixo).
6. Abra o PR:
   `gh pr create --base main --head envio/AAAA-MM-DD-<slug> --title "<título>" --body-file <ficheiro>`
   O corpo diz o que sobe (nº de commits, áreas, fragmentos do `changelog.d/`) e termina com a linha de atribuição do Claude Code.
7. Ligue o PR à sessão (`bind_pr`) e leia o estado do CI com `get_status`. **Não faça polling** do CI (`gh pr checks` em ciclo, `ScheduleWakeup`, `Monitor`).

## Fundir

8. **Antes de fundir, confira no `get_status` que o «Segurança» e o resto do CI estão verdes.** Sem a proteção, o GitHub funde mesmo com vermelho ou pendente: esta leitura é a única trava. Com tudo verde, o «sim» do envio já cobre o merge: `gh pr merge <nº> --merge --delete-branch`.
   - O PR só avança com o «E2E Smoke Tests» e o «Lighthouse CI» verdes (decisão do PO, 2026-11-20): correm nos PR do próprio repositório. Saltados, só se faltarem os secrets, e isso também pára o envio.
   - `--merge`, nunca `--squash` nem `--rebase`: o `main` local fica antepassado do `origin/main` e as linhas `Excecao-aceite:`/`Base-sobe:` dos commits continuam a existir.
   - Nunca `--admin` nem `--auto` (auto-merge só se o PO o pedir).
   - Nunca o botão **Update branch** do GitHub: cria um commit de merge no ramo remoto que o `main` local não tem, e o push seguinte para o mesmo ramo deixa de ser um avanço (ver «Casos sem caminho direto»).
9. Traga o `main` de volta: `git fetch origin` e `git merge --ff-only origin/main`. Confirme com `git rev-list --left-right --count origin/main...main`: `0 0`. Se o `--ff-only` recusar, o `main` local andou entre o envio e o merge (ver «Casos sem caminho direto»).
10. Confirme que o ramo desapareceu: `git ls-remote --heads origin "envio/*"` sem linhas. Se sobrar um, apague-o com o «sim» do PO: `git push origin --delete envio/AAAA-MM-DD-<slug>`.

## Depois do merge: tag e Release

Só quando o envio leva um `chore(release): X.Y.Z` (plano em `modelo-de-mudanca/release-no-github/`). A tag sobe depois do passo 9, e a página de Release no GitHub nasce como rascunho: siga os passos 5 a 9 da secção «Push e release» da skill `fechando-ciclo` (conferir que a tag está no `origin/main`, o push da tag com o «sim», as notas, o rascunho e a publicação com outro «sim»). Não se copiam aqui, para haver um texto só.

## Se o CI ficar vermelho

- **Pare.** Não funda e não corrija ainda: diga ao PO o que ficou vermelho e porquê, e peça um «sim» novo **antes** de corrigir. A correção passa por uma auditoria (numa sessão nova), como qualquer outra.
- Com o «sim» novo e a correção auditada, faça commits novos no `main` local (pela fila) e volte a empurrar para o **mesmo** ramo: `git push origin main:refs/heads/envio/AAAA-MM-DD-<slug>`. É um avanço normal, nunca `--force`. Depois, volte ao passo 7.
- Se o motivo é um aviso grave sem exceção, **não** o acrescente à linha de base: é o caso das exceções com prazo (fase 5).

## Casos sem caminho direto (B-2 da auditoria da 3c)

- **O `main` local andou entre o envio e o merge** (outra sessão commitou na pasta partilhada): no passo 9, o `--ff-only` recusa e o `rev-list` dá `1 N` (o commit de merge do GitHub à esquerda, os `N` commits novos à direita). Faça o commit de merge local pela fila (ver «O `git merge` e a fila»); os `N` commits seguem no próximo envio. Nunca `reset` nem `rebase`.
- **O `origin/main` andou com o PR aberto** (com a proteção, «exigir ramo atualizado» bloqueia o merge): não use o **Update branch**. Traga o `origin/main` para o `main` local (`git fetch origin` e o commit de merge pela fila, ver «O `git merge` e a fila») e empurre outra vez para o mesmo ramo, como no passo 5: é um avanço, porque o `main` local contém a ponta do ramo.
- **Alguém já carregou no Update branch:** o ramo remoto tem um commit que o `main` local não tem e o push recusa (não é avanço). Nunca `--force`: com o «sim» do PO, feche o PR, apague o ramo (`git push origin --delete envio/…`) e recomece no passo 2 com outro nome (`envio/AAAA-MM-DD-<slug>-2`).

## O `git merge` e a fila

O commit de merge passa pela fila e pelos hooks (B-2 da auditoria da 3d): a fila aceita `commit -F <ficheiro>` sem caminhos quando há um merge a meio (procura o `MERGE_HEAD`). Por isso, no passo 2 e nos dois primeiros casos acima:

1. `git --no-optional-locks status`: sem `.git/index.lock`, sem outra sessão a meio de um commit e **sem ficheiros estagiados de outras sessões**, porque o merge escreve o índice e o commit de merge leva o índice inteiro. Se houver, pare e chame o PO. Nunca `git stash`.
2. `git merge --no-commit --no-ff origin/main` (direto: a fila não tem o `merge`). Se aborta por tocar em ficheiros por commitar, pare e chame o PO.
3. A mensagem escreve-se num ficheiro (com a ferramenta Write) e fecha-se com `node scripts/git-hooks/fila-de-commits.mjs commit -F <msg>` (timeout 600000, nunca em segundo plano), sem caminhos. Se o merge traz uma exceção nova ao `npm-audit-excecoes.json` (chegou ao `origin/main` por outra máquina), a mensagem leva `Excecao-aceite: <id> <decisão>`: o `commit-msg` compara o índice com o `main` local, que não a tinha, e recusa sem a linha (B-4 da auditoria da fase 4).

Só o passo 9 corre direto: o `git merge --ff-only origin/main` não cria commit nenhum, por isso não há nada para a fila nem para os hooks. Um *fast-forward* pode seguir com ficheiros estagiados de outra sessão sem os tocar (do conhecimento, não medido): mesmo assim, confira o `git --no-optional-locks status` antes.

## Nunca

- Trabalhar, commitar ou fazer `checkout` no ramo `envio/…` (nem criar ramo local).
- `git push origin main` direto: o `pre-push` recusa-o desde a fase 4b («suba por PR»); sem o hook, o GitHub sem a proteção aceita-o e salta o PR e o CI antes do merge.
- Fundir sem ter lido o «Segurança» verde no `get_status`.
- `--no-verify`, `--force`, bypass de administrador, `--admin`.

## Os destinos que o `pre-push` aceita (fase 4b)

Decisão do PO de 2026-11-19 (I-1 da auditoria da 3c), apertada pelo plano da Release no GitHub (§0, `modelo-de-mudanca/release-no-github/plano-release-no-github.md`, aprovado pelo PO): antes de qualquer outra verificação, o `pre-push` lê o destino de cada linha do stdin (`scripts/git-hooks/destino-do-push-no-envio.mjs`). Aceitar como destino só `refs/heads/envio/*` (criar, avançar e apagar) e `refs/tags/vN.N.N` (só criar, com o sha remoto zero), recusando o resto: outros ramos, outras tags, e apagar ou mover uma tag.
- o ramo do envio, `refs/heads/envio/<nome>`: o push do passo 5, o segundo push para o mesmo ramo, e apagá-lo no passo 10;
- a tag de versão nova, `^refs/tags/v\d+\.\d+\.\d+$` (por exemplo `refs/tags/v10.67.0`), com o sha remoto da linha a zeros: a `fechando-ciclo` empurra a tag com um «sim» à parte.

Um push ao `refs/heads/main` (também apagá-lo) recusa com «O main só recebe por PR: suba pelo fluxo do envio», sem correr o gitleaks nem o npm audit. Qualquer outro destino recusa e diz os dois destinos aceites: `refs/heads/feature/x`, `refs/heads/envio` sem nome, as tags `refs/tags/prova`, `refs/tags/v2-rascunho` e `refs/tags/antes-do-feedback-v2`, apagar ou mover uma `refs/tags/vN.N.N` (sha local ou remoto não zero), `refs/notes/…`. Uma linha que não se lê recusa. Testes: `__tests__/hooks-do-agente/destino-do-push-no-envio.test.ts` e os dois «I-1 (fase 4b)» do `portao-do-push.test.ts`.

O destino só se lê da linha do stdin, que o próprio git escreve: um push sem o hook (`--no-verify`, outra máquina) não passa por aqui, e é o que a proteção do `main` fecharia.

## O `pre-push` antes da fase 4b: os nomes das refs não contavam

Lido e medido a 2026-11-19: `refs/heads/main <sha do main> refs/heads/envio/2026-11-19-prova <40 zeros>` no stdin do `node scripts/git-hooks/pre-push.mjs` correu o portão inteiro (Achados, Cobertura) e só recusou pelas razões de conteúdo (4 commits de outra sessão sem fragmento do changelog), nunca pelo nome do ramo. Todas as verificações leem só `shaLocal` e `shaRemoto` da linha do stdin e ignoram os nomes das refs:
- sha remoto zero (ramo novo): o «antes» é o `main` do GitHub por `git ls-remote origin refs/heads/main` (F1), não o `origin/main` local; o gitleaks varre `<sha> --not --remotes`;
- a regra «a linha de base só encolhe» e a trava 4 das exceções comparam com esse «antes»;
- a segunda vez que se empurra para o mesmo ramo, o «antes» passa a ser a ponta do ramo no remoto.

Estas verificações continuam iguais; a fase 4b só lhes pôs à frente a regra do destino (secção anterior), num módulo-folha, com o `pre-push.mjs` a 271 linhas.

**Feito na fase 4:** o `perguntar-antes` mostra as exceções também no envio `git push origin main:refs/heads/envio/…` (com o `HEAD` no `main`, conta como o push do `HEAD`); a frase compara com o `origin/main`, que é a base do PR. Quando não sabe o que o push leva (outra origem, `--delete`, o `origin/main` local fora do histórico do `HEAD`…) diz «não sei o que este push leva». O passo 10 (`--delete`) pergunta sempre e diz «não sei», porque apagar não leva commits.
