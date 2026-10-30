---
name: sql-postgres
description: Guia como um agente mexe num banco Postgres sem estragar dados nem derrubar o servidor — medir antes de mudar, migrações que só contam depois de conferidas no catálogo, provas dentro de transação que se desfaz, dados com histórico que nunca se apagam, tabelas de registro imutáveis e as armadilhas do Postgres (sequências, ENUM, TRUNCATE). Usar ao escrever SQL que muda esquema ou dados, ao criar uma migração, ao testar uma permissão ou uma função no banco, ou ao decidir como guardar e corrigir dados. Não usar para o que é específico do Supabase, como RLS com papéis anon e authenticated e o PostgREST (é a supabase), nem para consultas de leitura simples.
---

# SQL e Postgres

O banco de produção é de toda a gente que trabalha nele. Um erro no código volta atrás com um commit; um `UPDATE` errado ou um servidor derrubado não. Esta skill tem pouca liberdade de propósito: segue-se a ordem.

## 1. Ler é livre, escrever pede o "sim"

- Consultas de leitura, ao catálogo (`information_schema`, `pg_catalog`) e às estatísticas: à vontade.
- **Qualquer escrita** (esquema ou dados) só com o "sim" do dono do projeto **para aquela mudança**, nesta conversa.
- Mudança de risco passa antes por uma auditoria numa sessão nova (ver a skill `orquestrando-sessoes`).

## 2. A ordem de uma migração

```
1. Medir o estado vivo: colunas, restrições, distribuição real dos dados (GROUP BY)
2. Escrever o arquivo da migração, com o porquê no cabeçalho
3. Auditoria numa sessão nova (a migração e a prova)
4. Mostrar o SQL exato ao dono e esperar o "sim"
5. Aplicar
6. Conferir no catálogo (tabela abaixo)
7. Só agora mexer no código que depende da mudança
```

**Um arquivo em `migrations/` não prova que a migração foi aplicada.** Num projeto real, uma migração ficou marcada como feita durante semanas sem existir no banco. Confere-se no catálogo:

| Mudança | Prova no banco |
|---|---|
| Coluna nova | `SELECT count(*) FROM information_schema.columns WHERE table_name = 't' AND column_name = 'c'` devolve 1 |
| Função | `SELECT pg_get_functiondef('f(args)'::regprocedure)` mostra o corpo novo, igual ao arquivo commitado (`'f'::regproc`, sem argumentos, falha com `42725` quando há duas `f`) |
| Permissão retirada | `SELECT has_function_privilege('papel', 'f(args)', 'EXECUTE')` devolve false |

A tabela de controle de migrações da ferramenta não serve de prova: o que se aplica por fora dela não aparece lá.

Um número escrito à mão num documento ("vamos na migração 140") envelhece: mede-se. Duas sessões que criam migrações ao mesmo tempo podem escolher o mesmo número; confira antes de commitar.

## 3. Provar sem arriscar

```sql
BEGIN;
  -- a mudança
  SET LOCAL ROLE papel_sem_permissao;
  -- a operação que devia ser bloqueada
ROLLBACK;
```

- **A prova forte é a assimetria:** a mesma operação com dois papéis. O que não tem permissão recebe `42501`; o que tem passa, ou cai **noutro** erro (por exemplo, `23503`, chave estrangeira). Assim se prova que fecha e que não partiu nada.
- **Leia o SQLSTATE.** `42703` (coluna inexistente) é erro de **esquema**: parece um bloqueio e não prova nada.
- **Sequências não obedecem ao `ROLLBACK`.** Chamar `nextval` para testar queima o número. Não se testa uma função que consome uma sequência: lê-se o corpo.

## 4. Não martelar o servidor

- Uma consulta avulsa: à vontade. Laços, retentativas automáticas, reabrir telas pesadas dezenas de vezes: não.
- Uma passagem por cenário, dentro de `BEGIN`/`ROLLBACK`.
- Num projeto real, um dia de testes em ciclo gastou mais de 6 GB de tráfego, e o banco ficou mais de uma hora e meia inutilizável para todos.

## 5. Como guardar dados

- **Dado com histórico nunca leva `DELETE`.** Marca-se como apagado (`deleted_at`, `deleted_by`) e preservam-se os registros ligados (pagamentos, horas, períodos).
- **Tabela de registro é imutável:** só `SELECT` e `INSERT`. Um erro corrige-se com uma linha nova de correção, nunca editando a antiga. Escrever nela fica a cargo de um gatilho, não da aplicação: a aplicação só tem `SELECT` nela, e a função do gatilho é `SECURITY DEFINER` (sem isso o gatilho recebe `42501`).
- **O mesmo dado em duas colunas:** uma é a verdade e a outra deriva dela. Escolha qual e escreva-o; senão as duas divergem.
- **Categoria que o usuário cria: tabela, não ENUM.** Num `ENUM` só se acrescentam valores (`ADD VALUE`); remover não existe, e cada valor novo pede migração e deploy.
- **Estado de processo calcula-se, não se digita.** Um estado digitado apodrece. Quando falta um dado, o resultado é "indeterminado", nunca "falhou".
- **Campo obrigatório que bloqueia um caso legítimo produz dados falsos:** a pessoa inventa um valor para passar.
- **Dado sensível omite-se no `SELECT`**, não se anula depois na saída.
- **Normalizar só na apresentação** (maiúsculas, acentos). O valor cru fica para consultas e filtros.

## 6. Armadilhas

- **Consultas em lote** (`WHERE id = ANY($1)` ou `IN (...)`) em vez de uma consulta por linha num laço (N+1).
- **Nada de `UPDATE` em massa "por arrumação"** sem medir quantas linhas e sem o "sim": pode desfazer o que alguém está a ver hoje.
- **Filtrar por uma coluna que a tabela não tem** esvazia a lista em silêncio, sem erro, em alguns clientes. Confira o esquema.
- **O que se aplica tem de ser igual ao que está commitado.** Copiar e colar à mão um SQL ligeiramente diferente cria um banco que ninguém consegue reconstruir.

## Fontes

Ver `FONTES.md`. Os trechos de SQL seguem a documentação do Postgres. Foram testados no PostgreSQL 18.3, num banco descartável, em 30 de outubro de 2026.
