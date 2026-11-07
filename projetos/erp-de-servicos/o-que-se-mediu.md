# O que se mediu

Os números do projeto de origem, cada um com o mês em que foi medido e o comando que o deu. Todos foram contados em novembro de 2026, no repositório do projeto, sem escrever nada nele. Os comandos rodam na raiz desse repositório.

Duas ausências de propósito: não há aqui quantos bugs estão abertos, nem no total nem por área, e as falhas de segurança têm um registro à parte, que não se publica.

## O histórico

| O quê | Número | Comando |
|---|---|---|
| commits no total | 2771 | `git log --oneline \| wc -l` |
| commits do tipo `fix` | 580 | `git log --format=%s \| grep -c '^fix[(:!]'` |
| mês do primeiro commit | março de 2026 | `git log --reverse --date=short --format=%ad \| head -1 \| cut -c1-7` |
| mês do último commit medido | novembro de 2026 | `git log -1 --date=short --format=%ad \| cut -c1-7` |
| pastas de módulo no painel de administração | 12 | `ls -d app/dashboard/admin/*/ \| grep -v '/components/$' \| wc -l` |
| partes do módulo Financeiro | 5 | `ls -d app/dashboard/admin/financeiro/*/ \| grep -v '/components/$' \| wc -l` |

## Os `fix` por área

São defeitos já corrigidos, contados pelo escopo que a mensagem do commit declara. Entram as quatro áreas com mais `fix`, pelo escopo exato; as outras ficam de fora, e com elas os 28 sem escopo e o escopo das falhas de segurança.

| Área | `fix` | Comando |
|---|---|---|
| Financeiro | 96 | `git log --format=%s \| grep -c '^fix(financeiro)'` |
| Tarefas | 48 | `git log --format=%s \| grep -c '^fix(tarefas)'` |
| Documentos (escopo `ged`) | 48 | `git log --format=%s \| grep -c '^fix(ged)'` |
| Interface | 25 | `git log --format=%s \| grep -c '^fix(ui)'` |

## Os bugs registrados

O projeto registra cada bug por corrigir numa pasta por área; um bug corrigido fica no registro, marcado como resolvido, e o commit `fix` o traz. Aqui só entra o total de arquivos de registro por área, abertos e resolvidos juntos, e nada do seu conteúdo.

| Área | Total de registros |
|---|---|
| Financeiro | 8 |
| Funcionários | 7 |
| Documentos | 3 |
| Infraestrutura | 9 |
| Inventário | 1 |
| Tarefas | 6 |
| **Todas** | **34** |

Comando por área: `git ls-files docs/erros-conhecidos | grep -v README.md | cut -d/ -f3 | sort | uniq -c`. Comando do total: o mesmo, com `wc -l` no lugar de `cut`, `sort` e `uniq`.

## As catracas

Uma catraca é um teste que conta uma coisa ruim e recusa que o número cresça: o que já viola fica numa linha de base que só encolhe, e o arquivo novo nasce limpo. O projeto tem 9, uma por assunto (`git ls-files __tests__/catracas/linhas-de-base | wc -l`):

| Catraca | O que conta |
|---|---|
| código morto | o que ninguém mais usa |
| exceções ao alarme | os alarmes que alguém calou de propósito |
| fontes por registrar | as fontes citadas em documentos que ainda não estão no registro de fontes |
| nomes genéricos | nomes como `data` ou `utils` |
| nomes únicos | nomes repetidos que deviam ser pesquisáveis |
| números repetidos | o mesmo número escrito em vários lugares |
| tamanho de arquivo | arquivos grandes demais |
| tamanho de função | funções grandes demais |
| testes pulados | testes desligados |

## Os incidentes com número

Os valores abaixo são os que o próprio projeto escreveu ao lado da regra que o incidente criou. Hoje se mediu só o mês, pelo primeiro commit que traz o texto da segunda coluna no arquivo de regras (`git log -S"<texto>" --date=short --format=%ad -- CLAUDE.md | tail -1 | cut -c1-7`); o número em si não foi recontado.

| Incidente | Número | Texto pesquisado | Mês |
|---|---|---|---|
| arquivos que viveram só num disco, sem ir ao repositório | 109 | `109 ficheiros por commitar` | julho de 2026 |
| volume que o banco serviu num único dia, até ficar inutilizável | 6,37 GB | `6,37 GB` | agosto de 2026 |
| tempo fora do ar nesse dia | cerca de 1h40 | `1h40` | agosto de 2026 |
| `fix` sem teste de regressão, no momento da regra que os exige | 86 de 199 | `86 de 199` | outubro de 2026 |
| tamanho a que chegou o arquivo de regras lido a cada sessão | 328 KB | `328 KB` | agosto de 2026 |
