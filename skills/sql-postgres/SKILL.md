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
| Coluna nova | `SELECT count(*) FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 't' AND column_name = 'c'` devolve 1, corrido pelo dono (sem `table_schema`, a mesma tabela noutro esquema conta também; e o `information_schema` esconde as colunas de um papel sem acesso, o `pg_attribute` não) |
| Função | `SELECT prosrc FROM pg_proc WHERE oid = 'public.f(args)'::regprocedure` mostra o corpo entre `$$` igual ao arquivo commitado. O `pg_get_functiondef` devolve uma versão equivalente, mas normalizada; e `'f'::regproc`, sem argumentos, falha com `42725` quando há duas `f` |
| Permissão retirada | `SELECT has_function_privilege('papel', 'public.f(args)', 'EXECUTE')` devolve false |

A tabela de controle de migrações da ferramenta não serve de prova: o que se aplica por fora dela não aparece lá.

Um número escrito à mão num documento ("vamos na migração 140") envelhece: mede-se. Duas sessões que criam migrações ao mesmo tempo podem escolher o mesmo número; confira antes de commitar.

Uma migração numa tabela com uso não pode trancá-la:

- **`SET LOCAL lock_timeout = '2s'` antes do DDL.** O `ALTER TABLE` pede um lock exclusivo: enquanto espera por uma leitura longa, as consultas seguintes ficam na fila atrás dele. Com o limite, ele desiste com `55P03` em vez de parar o sistema.
- **Coluna nova com `DEFAULT` volátil** (`clock_timestamp()`, `random()`) reescreve a tabela inteira; com um `DEFAULT` constante, não.
- **Restrição nova numa tabela grande:** `ADD CONSTRAINT ... NOT VALID` (vale só para as linhas novas) e, noutro passo, `VALIDATE CONSTRAINT`.
- **Índice numa tabela com uso:** `CREATE INDEX CONCURRENTLY`, que não corre dentro de uma transação (`25001`).

## 3. Provar sem arriscar

```sql
BEGIN;
  SET LOCAL lock_timeout = '2s';
  -- a mudança
  SET LOCAL ROLE papel_sem_permissao;
  -- a operação que devia ser bloqueada
ROLLBACK;
```

- **A prova forte é a assimetria:** a mesma operação com dois papéis. Quando a barreira é um grant (ou o `WITH CHECK` do RLS), o que não tem permissão recebe `42501`; o que tem passa, ou cai **noutro** erro (por exemplo, `23503`, chave estrangeira). Assim se prova que fecha e que não partiu nada.
- **O RLS em `SELECT`, `UPDATE` e `DELETE` não dá erro: filtra.** A linha que a política `USING` exclui some em silêncio (0 linhas, `UPDATE 0`, `DELETE 0`). Aí a assimetria está na contagem: o mesmo `UPDATE ... RETURNING id` devolve a linha a quem tem direito e nada a quem não tem. Zero linhas, sozinho, não prova nada.
- **Leia o SQLSTATE.** `42703` (coluna inexistente) é erro de **esquema**: parece um bloqueio e não prova nada.
- **Sequências não obedecem ao `ROLLBACK`.** Chamar `nextval`, ou um `INSERT` numa coluna `IDENTITY`/`serial` que depois falha (o próprio teste do `23503`), queima o número; o `setval` também não se desfaz. Não se testa uma função que consome uma sequência: lê-se o corpo.

## 4. Não martelar o servidor

- Uma consulta avulsa: à vontade. Laços, retentativas automáticas, reabrir telas pesadas dezenas de vezes: não.
- Uma passagem por cenário, dentro de `BEGIN`/`ROLLBACK`.
- **O `ROLLBACK` não torna a prova inofensiva.** Um DDL dentro do `BEGIN` tranca a tabela, até para leituras, enquanto a transação estiver aberta. Em produção: `SET LOCAL lock_timeout` no início e o `ROLLBACK` logo a seguir.
- Num projeto real, um dia de testes em ciclo gastou mais de 6 GB de tráfego, e o banco ficou mais de uma hora e meia inutilizável para todos.

## 5. Como guardar dados

- **Dado com histórico nunca leva `DELETE`.** Marca-se como apagado (`deleted_at`, `deleted_by`) e preservam-se os registros ligados (pagamentos, horas, períodos).
- **Tabela de registro é imutável:** só `SELECT` e `INSERT`. Um erro corrige-se com uma linha nova de correção, nunca editando a antiga. Escrever nela fica a cargo de um gatilho, não da aplicação: a aplicação só tem `SELECT` nela, e a função do gatilho é `SECURITY DEFINER SET search_path = ''`, com os nomes qualificados (sem `SECURITY DEFINER`, o gatilho recebe `42501`; sem o `search_path`, fica contornável, ver a skill `supabase`, seção 4). Tirar os grants não trava o dono nem o superusuário: isso faz-se com os gatilhos do fim desta seção.
- **O mesmo dado em duas colunas:** uma é a verdade e a outra deriva dela. Escolha qual e escreva-o; senão as duas divergem.
- **Categoria que o usuário cria: tabela, não ENUM.** Num `ENUM` acrescenta-se (`ADD VALUE`) e renomeia-se (`RENAME VALUE`); remover e reordenar não existem. O valor novo só se usa depois do commit (`55P04`), por isso não serve na mesma migração, e cada valor novo pede migração e deploy.
- **Estado de processo calcula-se, não se digita.** Um estado digitado apodrece. Quando falta um dado, o resultado é "indeterminado", nunca "falhou".
- **Campo obrigatório que bloqueia um caso legítimo produz dados falsos:** a pessoa inventa um valor para passar.
- **Dado sensível omite-se no `SELECT`**, não se anula depois na saída.
- **Normalizar só na apresentação** (maiúsculas, acentos). O valor cru fica para consultas e filtros.

A trava da tabela de registro, que vale para todos (o `UPDATE`, o `DELETE` e o `TRUNCATE` do dono e do superusuário caem no erro):

```sql
CREATE FUNCTION public.registro_imutavel() RETURNS trigger
LANGUAGE plpgsql SET search_path = '' AS $$
BEGIN
  RAISE EXCEPTION 'registro é imutável: corrija com uma linha nova';
END $$;
CREATE TRIGGER registro_sem_update_delete BEFORE UPDATE OR DELETE ON public.registro
  FOR EACH ROW EXECUTE FUNCTION public.registro_imutavel();
CREATE TRIGGER registro_sem_truncate BEFORE TRUNCATE ON public.registro
  FOR EACH STATEMENT EXECUTE FUNCTION public.registro_imutavel();
```

## 6. Armadilhas

- **Consultas em lote** (`WHERE id = ANY($1)` ou `IN (...)`) em vez de uma consulta por linha num laço (N+1).
- **Nada de `UPDATE` em massa "por arrumação"** sem medir quantas linhas e sem o "sim": pode desfazer o que alguém está a ver hoje.
- **Filtrar por uma coluna que a tabela não tem** esvazia a lista em silêncio, sem erro, em alguns clientes. Confira o esquema.
- **O que se aplica tem de ser igual ao que está commitado.** Copiar e colar à mão um SQL ligeiramente diferente cria um banco que ninguém consegue reconstruir.

## Fontes

Documentação do PostgreSQL 18, consultada em 30 de outubro de 2026 (as mesmas linhas estão em `FONTES.md`):

- Row Security Policies: https://www.postgresql.org/docs/18/ddl-rowsecurity.html
- CREATE FUNCTION («Writing SECURITY DEFINER Functions Safely»): https://www.postgresql.org/docs/18/sql-createfunction.html
- information_schema.columns: https://www.postgresql.org/docs/18/infoschema-columns.html
- Sequence Manipulation Functions: https://www.postgresql.org/docs/18/functions-sequence.html
- Enumerated Types: https://www.postgresql.org/docs/18/datatype-enum.html
- ALTER TYPE: https://www.postgresql.org/docs/18/sql-altertype.html
- ALTER TABLE: https://www.postgresql.org/docs/18/sql-altertable.html

Os trechos de SQL foram testados no PostgreSQL 18.3, num banco descartável, em 30 de outubro de 2026. Os locks foram provados com duas ligações ao mesmo banco.
