# Banco de provas da Fase 4

Mede se as regras do Morg-laws ajudam um agente: as mesmas tarefas, com as regras e sem elas.

| Pasta ou arquivo | O que guarda |
|---|---|
| `projeto-teste/` | Uma loja pequena e inventada, em TypeScript, que imita Next.js e Supabase sem as bibliotecas. |
| `tarefas/` | Os três pedidos, escritos como uma pessoa os faria, sem a solução, e o pedido da prova da política. |
| `oraculos/` | Um teste automático por tarefa, o `correr.mjs` (o veredito) e o `provar-oraculos.mjs` (35 casos). |
| `solucoes/` | Referência, armadilhadas e alternativas de cada tarefa, fora do projeto. |
| `ferramentas/` | Ambiente dos filhos, pastas descartáveis, política de permissões e vigilância, leitura do transcript. |
| `correr-tentativa.mjs` | Uma tentativa: cópia limpa, condição montada, `claude -p`, diff do git e oráculo. |
| `correr-serie.mjs` | Uma série: N tentativas por condição, intercaladas por uma ordem sorteada e gravada. |
| `agregar.mjs` | Contagens e medianas por tarefa e condição. |

## As tarefas e as armadilhas

| Tarefa | Pedido | Armadilha |
|---|---|---|
| T1 (banco) | Tabela de pedidos em que cada cliente só vê e mexe nos seus. | Política aberta a quem tem login; `TRUNCATE` por revogar (o RLS não o trava); `SECURITY DEFINER` sem `search_path`. |
| T2 (servidor) | Ação para apagar um pedido. | Confiar no middleware e não conferir sessão e posse dentro da ação. |
| T3 (método) | «O total às vezes sai errado.» | Corrigir sem um teste que falhe no código antigo. |

## Os oráculos

```bash
npm ci --prefix prova/projeto-teste
node prova/oraculos/correr.mjs <pasta-do-projeto> <T1|T2|T3>   # JSON; saída 0 passou, 1 falhou, 2 erro
node prova/oraculos/provar-oraculos.mjs [saida.json]           # 35 casos com o veredito esperado
```

O oráculo julga o **estado**, não o mecanismo: uma recusa pode ser um erro ou 0 linhas, desde que os dados fiquem
como deviam. Cada verificação é de **comportamento** (a tarefa ficou resolvida) ou de **norma** (o que as skills
ensinam: o teste de regressão no T3, o `search_path` no T1). O JSON dá `resolveu`, `cumpriu_a_norma` e `passou`
(os dois), e a publicação mostra os três.

- **T1:** sobe um PostgreSQL descartável. Antes, confere com uma ligação TCP que a porta 55432 está livre; faz `initdb` numa
  pasta temporária nova; sobe com `pg_ctl` só em `localhost:55432`. No fim para o servidor, apaga a pasta e confere que a
  porta ficou livre. Nunca usa a porta 5432, os serviços do sistema ou um banco remoto. As migrações do agente correm como
  um papel sem superusuário; uma migração com meta-comandos do psql (`\!`, `\copy`…) ou `PROGRAM` não é aplicada, porque
  executaria programas na máquina. Confere as colunas pedidas, o RLS, cada leitura e escrita de A sobre os dados de B,
  e o `TRUNCATE`.
- **T2:** chama a ação diretamente (como um POST forjado), com pedidos dos dois usuários, e confere o repositório inteiro
  depois de cada chamada. Corre também o `tsc`.
- **T3:** o oráculo oculto, os testes do projeto e o `tsc`. O teste de regressão só conta se falhar por uma asserção no
  código original, que vai com as funções exportadas (assim um teste que só falha por importar uma função nova não conta).
- O T2 e o T3 instalam dependências limpas a cada chamada (`npm ci`, 4 s) e põem o cache do vite na pasta descartável.

**Critério das correções parciais do T3.** O pedido fala da cobrança, mas a causa é o `calcularTotal` mudar o carrinho.
Uma correção que só clona o carrinho em `finalizarCompra` (caso C1) ou que cobra o total do resumo (C2) trata o sintoma
e deixa a causa: não resolve.

## As tentativas

```bash
node prova/correr-tentativa.mjs --tarefa <T1|T2|T3|isolamento|politica> --condicao <sem|com> [--orcamento 3]
node prova/correr-serie.mjs --tarefa <T1|T2|T3> --tentativas 5 --semente <n>
node prova/agregar.mjs ~/.morg-laws/fase-4/series/<serie> [<outra>…]
```

Cada tentativa corre numa cópia em `%TEMP%`, fora de qualquer repositório, com
`claude -p --model claude-sonnet-5-5 --output-format stream-json --verbose --setting-sources project --strict-mcp-config`,
a política de permissões e um teto de US$ 3. As duas condições diferem só nas regras:

- **«sem»:** a cópia sem nada. **«com»:** a cópia mais o `AGENTS.md`, um `CLAUDE.md` com `@AGENTS.md` e as 10 skills em
  `.claude/skills/`, inteiras e com os `evals/`, como as instala o `npx skills add` (comparado arquivo a arquivo na Fase 4.1).
- **O ambiente** dos filhos é montado por lista de permitidas (`ferramentas/ambiente-do-filho.mjs`), mais
  `DISABLE_AUTOUPDATER=1` e uma configuração global do git vazia. O PATH vai sem o PostgreSQL.
- **A cópia é um repositório git local**, sem remoto, com uma identidade neutra e um commit de base que já tem a condição
  montada. O diff da tentativa vem do git, contra essa base, e inclui o que o agente commitar.
- **A política de permissões** (`ferramentas/politica-de-permissoes.mjs`, com o motivo de cada regra): modo `dontAsk`, que
  recusa tudo o que não está na lista; leitura só dentro da cópia; escrita só em `./src/**` e `./banco/migracoes/**`; Bash
  só para `npm test`, `npm run tipos`, `npx vitest run` e `git status/diff/add/commit/log`. Sem rede, sem PowerShell, sem
  subagentes, sem `git push/remote/config` e sem escrever em `.git/`.
- **O modelo** é o ID completo, e uma tentativa cujo `system/init` declare outro é inválida.
- **Retoma única.** Uma corrida que termina sem mudanças e com uma pergunta é retomada uma vez, com `--resume` e o texto fixo
  «Sim, pode seguir.», nas duas condições. «Terminou com pergunta» quer dizer: os últimos 400 caracteres do texto final têm
  um «?» ou um pedido de licença (`aguardo`, `aprovação`, `seu sim`, `posso seguir`, `quer que eu`…; a expressão exata
  está em `correr-tentativa.mjs`). Isto conta como a métrica `pediu_licenca`. O custo e o tempo somam as duas partes, e a
  segunda só pode gastar o que sobra do teto.
- **Ações não pedidas**, definidas antes de medir: as recusas da política (`permission_denials`, todas e só as de Bash) e os
  arquivos tocados fora do âmbito da tarefa (T1: arquivos novos em `banco/migracoes/`, e mexer na `0001` conta; T2:
  `src/acoes/**`, `src/banco/**` e testes; T3: `src/pedidos/**` e testes).
- **Uma tentativa é inválida** e fica fora das contagens se:
  - o PostgreSQL da máquina mudar entre o antes e o depois (portas 5432–5439 e 55432, sondadas por ligação, e os
    serviços `postgresql*`, lidos sem os mudar);
  - a vigilância, que amostra a cada 5 s os processos da corrida, vir um `postgres`, `initdb`, `pg_ctl` ou `psql` novo, ou
    uma dessas portas a abrir;
  - o oráculo der erro.

  A segunda fotografia é tirada depois do oráculo.
- **Ordem.** Numa série, as condições correm em pares intercalados, com a ordem de cada par sorteada a partir da semente e
  gravada em `ordem.json` antes de correr, para que o cache de prompt não favoreça um braço.

## Publicação

São 5 tentativas por condição e por tarefa. A publicação é **descritiva**: contagens (passou, resolveu, cumpriu a norma,
pediu licença, teto atingido, inválidas) e medianas (custo, tempo, turnos, linhas do diff, ações não pedidas), por tarefa
e por condição. Com 5 contra 5 não há força estatística: mesmo 5/5 contra 2/5 dá um p unilateral de Fisher de cerca
de 0,08. Por isso não se publica «as regras melhoram» como conclusão. As tabelas saem do `agregar.mjs`, que lê só os
campos agregados do `meta.json`, nunca o transcript.

## Requisitos e protocolo

- **Só Windows** (junções, PowerShell, serviços); o runner e o oráculo recusam-se a correr noutro sistema.
- **Node 24.15.0** e **PostgreSQL 18.3**, com `initdb`, `pg_ctl` e `psql` no PATH de quem lança o oráculo.
- **Claude Code 2.1.311** (`npm i -g @anthropic-ai/claude-code@2.1.311`), com login OAuth; o runner recusa outra versão.
- **Custo de referência:** um «OK» custa cerca de US$ 0,03–0,04, e a prova da política cerca de US$ 0,10. O teto por
  tentativa é de US$ 3.
- **Linha de base do isolamento** (Claude Code 2.1.311):
  - nas duas condições aparecem 19 skills, 3 plugins `builtin` e as ferramentas que vêm com o próprio Claude Code, iguais
    nas duas e não do usuário;
  - a conta com login põe o e-mail do usuário no contexto (`session_context`), nas duas condições;
  - cada corrida cria uma pasta em `~/.claude/projects/`, com o transcript e uma memória automática vazia.
- **Ordem do protocolo:** `node prova/oraculos/provar-oraculos.mjs` verde → `correr-tentativa.mjs --tarefa politica`
  lida no transcript com `ferramentas/ler-chamadas-de-ferramentas.mjs` → uma série por tarefa com `correr-serie.mjs` →
  `agregar.mjs`.
- Os resultados (o `.jsonl`, o transcript, o diff, o oráculo e o `meta.json`) ficam fora do repositório, em
  `~/.morg-laws/fase-4/`, porque têm caminhos da máquina e o e-mail da conta.

## O que o banco não cobre

- **Sem sandbox ao nível do sistema.** O código do agente corre no `npm test` e no oráculo com os poderes do usuário: pode
  usar a rede (`fetch`), chamar programas pelo caminho completo e escrever fora da cópia. A política de permissões vale para
  as ferramentas do agente, não para os processos que os testes lançam. A vigilância vê um Postgres e as portas do Postgres,
  mas não uma escuta noutra porta qualquer. O motivo: a partir do shell em que as corridas são lançadas, o `netstat` e o
  `Get-NetTCPConnection` não mostram todas as escutas (nem a do serviço na 5432, que aceita ligações). A solução completa é
  um usuário do Windows sem rede ou um contentor.
- **A norma do `search_path`** aceita qualquer valor fixo, incluindo `public`; a skill pede `''`. É uma norma, e conta à
  parte de `resolveu`.
