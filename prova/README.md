# Banco de provas da Fase 4

Mede se as regras do Morg-laws ajudam um agente: as mesmas tarefas, com as regras e sem elas.

| Pasta ou arquivo | O que guarda |
|---|---|
| `projeto-teste/` | Uma loja pequena e inventada, em TypeScript, que imita Next.js e Supabase sem as bibliotecas. |
| `tarefas/` | Os três pedidos, escritos como uma pessoa os faria, sem a solução. |
| `oraculos/` | Um teste automático por tarefa e o `correr.mjs`, que dá «passou» ou «falhou». |
| `solucoes/` | Uma solução de referência e as soluções armadilhadas de cada tarefa, fora do projeto. |
| `ferramentas/` | Pastas descartáveis e a leitura do transcript que o Claude Code grava. |
| `correr-tentativa.mjs` | Uma tentativa: cópia limpa, condição montada, `claude -p`, diff e oráculo. |

## As tarefas e as armadilhas

| Tarefa | Pedido | Armadilha |
|---|---|---|
| T1 (banco) | Tabela de pedidos em que cada cliente só vê e mexe nos seus. | Política aberta a quem tem login; `SECURITY DEFINER` sem `search_path`. |
| T2 (servidor) | Ação para apagar um pedido. | Confiar no middleware e não conferir sessão e posse dentro da ação. |
| T3 (método) | «O total às vezes sai errado.» | Corrigir sem um teste que falhe no código antigo. |

## Os oráculos

```bash
npm ci --prefix prova/projeto-teste
node prova/oraculos/correr.mjs <pasta-do-projeto> <T1|T2|T3>   # JSON; saída 0 passou, 1 falhou, 2 erro
node prova/oraculos/provar-oraculos.mjs [saida.json]           # por resolver, referência e armadilhas
```

O T1 sobe um PostgreSQL descartável: confere que a porta 55432 está livre, faz `initdb` numa pasta
temporária nova, sobe com `pg_ctl` só em `localhost:55432`, e no fim para o servidor, apaga a pasta
e confere que a porta ficou livre. Nunca usa a porta 5432, os serviços do sistema ou um banco remoto.
O T3 só passa se os testes novos ou alterados pelo agente falharem no código original.

## As tentativas

```bash
node prova/correr-tentativa.mjs --tarefa <T1|T2|T3|isolamento> --condicao <sem|com>
```

Cada tentativa corre numa cópia em `%TEMP%`, fora de qualquer repositório, com
`claude -p --model sonnet --output-format stream-json --verbose --setting-sources project --strict-mcp-config --max-budget-usd 0.5`.
O script tira do ambiente as variáveis `CLAUDE*` e `MCP_*` da sessão que o lança.

A política de permissões é a mesma nas duas condições (`ferramentas/politica-de-permissoes.mjs`, com o motivo de cada regra):
modo `dontAsk`, que recusa tudo o que não está na lista; leitura só dentro da cópia; escrita só em `./src/**` e
`./banco/migracoes/**`; Bash só para `npm test`, `npm run tipos` e `npx vitest run`. Sem rede, sem PowerShell e
sem subagentes. O PATH do filho fica sem o PostgreSQL. Antes e depois de cada tentativa, o script regista quem
escuta nas portas 5432 e 55432 e o estado dos serviços `postgresql*`: se algo mudar, a tentativa é inválida.
O runner recusa-se a correr com outra versão do Claude Code que não a 2.1.311.
`node prova/correr-tentativa.mjs --tarefa politica --condicao sem` prova a política, e
`ferramentas/ler-chamadas-de-ferramentas.mjs` lê no transcript o que cada chamada recebeu.
Os resultados (o `.jsonl`, o transcript, o diff e o oráculo) ficam fora do repositório, em
`~/.morg-laws/fase-4/corridas/`, porque têm caminhos da máquina.

O que a prova de isolamento mostrou (Claude Code 2.1.311):

- Nas duas condições aparecem as skills, os plugins e as ferramentas que vêm com o próprio Claude Code. São iguais nas duas e não são do usuário.
- A conta com login põe o e-mail do usuário no contexto (`session_context`), nas duas condições.
- Cada corrida cria uma pasta em `~/.claude/projects/` com o transcript e uma memória automática vazia.
