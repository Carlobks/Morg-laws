---
name: supabase
description: Guia o trabalho de um agente num projeto Supabase — RLS que realmente fecha, funções SECURITY DEFINER com guarda de papel, grants aos papéis anon e authenticated, a ordem de uma coluna nova por causa do PostgREST, tipos gerados, autenticação por cookies no servidor e Edge Functions que deixam o RLS decidir. Usar ao criar ou rever políticas RLS, grants ou funções no Supabase, ao acrescentar uma coluna que o cliente lê, ao escrever código que usa o cliente Supabase, ou quando aparecem os erros PGRST204, 42501 ou 42703. Não usar para regras de Postgres que valem fora do Supabase (é a sql-postgres) nem para a revisão de segurança antes do push (é a auditoria-de-seguranca).
---

# Supabase

O Supabase expõe as tabelas diretamente ao navegador através do PostgREST. A segurança está no banco (RLS e grants), não no código da aplicação. Esta skill reúne o que já falhou na prática. Vale junto com a `sql-postgres`.

## 1. Onde está a barreira decide o que se audita

| Tipo de acesso | Onde está a barreira | O que se audita |
|---|---|---|
| Tabela lida pelo cliente | RLS da tabela | As políticas da tabela, por comando |
| Função `SECURITY INVOKER` | RLS das tabelas por baixo | As políticas dessas tabelas |
| Função `SECURITY DEFINER` | **A própria função** (corre como o dono; no Supabase é o `postgres`, que tem `BYPASSRLS`, e ignora o RLS mesmo com `FORCE`. Só não ignora se o dono for outro papel sem `BYPASSRLS` e sem ser dono da tabela, ou dono dela com `FORCE ROW LEVEL SECURITY`) | Quem pode executá-la e o que ela confere por dentro |
| Vista | O dono da vista (no Supabase, o `postgres`), salvo `WITH (security_invoker = true)` | A opção da vista e os grants dela |

- **Nome de política não prova nada.** Uma política chamada `admin_*` com `USING (true)` para todos já existiu num projeto real. Leia a expressão.
- **"Tem login" não é barreira.** `USING (auth.uid() IS NOT NULL)` está aberta a **todas** as contas autenticadas, incluindo as de trabalhadores com acesso pelo celular.

## 2. RLS

- **Toda tabela de um esquema exposto tem RLS ativo.** Sem ele, qualquer papel com grant lê e escreve tudo. Prova: esta consulta não devolve nada.

```sql
SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p') AND NOT c.relrowsecurity;
```

- **Vista sobre uma tabela com RLS leva `WITH (security_invoker = true)`.** Sem isso, a vista aplica o RLS do dono e mostra as linhas de todos.
- **Política que substitui outra apaga a antiga na mesma migração** (`DROP POLICY IF EXISTS`). Políticas do mesmo comando combinam por OR: a antiga, esquecida, anula a nova. Confira em `pg_policy` que a antiga sumiu.
- **Uma política da tabela X nunca consulta a própria X**, nem uma Y cuja política volta a X: dá recursão infinita (`42P17`). A saída é uma função `SECURITY DEFINER` (seção 4) num esquema não exposto, chamada pela política: `USING (id IN (SELECT privado.equipes_do_usuario()))`.
- **Antes de apagar uma política solta, veja se ela é a única porta** de quem tem direito para aquele comando. Se for, o `DROP` fecha o buraco e parte a tela. Substitui-se por uma política certa, não se apaga.
- **Filtrar os apagados mesmo com RLS** (`.is('deleted_at', null)`): defesa em profundidade.
- **Desempenho:** cada política leva `TO authenticated` (ou o papel certo), para não correr para os outros; `auth.uid()` vai dentro de `(SELECT auth.uid())`, que o Postgres calcula uma vez por consulta e não uma vez por linha; e a coluna filtrada tem índice.
- **O RLS filtra sem erro** (ver `sql-postgres`, seção 3): a prova é a contagem com dois usuários. `SET LOCAL ROLE authenticated` sozinho deixa `auth.uid()` nulo, e as 0 linhas parecem um bloqueio. Finge-se o usuário assim:

```sql
BEGIN;
SET LOCAL ROLE authenticated;
SELECT set_config('request.jwt.claims', '{"sub":"<uuid do dono>","role":"authenticated"}', true);
SELECT count(*) FROM public.t;   -- as linhas do dono
SELECT set_config('request.jwt.claims', '{"sub":"<uuid de outro>","role":"authenticated"}', true);
SELECT count(*) FROM public.t;   -- só as dele
ROLLBACK;
```

## 3. Grants

- **`REVOKE ... FROM PUBLIC` não chega.** O Supabase dá grants individuais a `anon` e `authenticated`; revogue de cada papel pelo nome.
- **O RLS não trava `TRUNCATE`.** Nunca escreva `GRANT ALL` aos papéis do cliente: conceda só `SELECT, INSERT, UPDATE, DELETE`, o que a tabela usa. E não basta: num projeto Supabase, os privilégios por omissão do `public` já dão `TRUNCATE`, `REFERENCES` e `TRIGGER` a `anon` e `authenticated` em cada tabela nova (confira os do seu em `pg_default_acl`). Depois de criar uma tabela: `REVOKE TRUNCATE, REFERENCES, TRIGGER ON public.t FROM anon, authenticated`, ou mude a omissão com `ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE TRUNCATE, REFERENCES, TRIGGER ON TABLES FROM anon, authenticated`, corrido pelo papel que cria as tabelas. Confira com `has_table_privilege('authenticated', 'public.t', 'TRUNCATE')`, que deve devolver false. O PostgREST não expõe o `TRUNCATE`: o risco vem de uma ligação direta ou de SQL dinâmico numa função.

## 4. Funções `SECURITY DEFINER`

- Revogue `EXECUTE` de `anon` e de `PUBLIC`.
- **Toda `SECURITY DEFINER` leva `SET search_path = ''` e os nomes com esquema** (`public.perfis`, `auth.uid()`). A que não é para ser chamada pela API (a de uma política, por exemplo) fica fora dos esquemas expostos. Sem o `search_path`, quem cria uma tabela temporária `perfis` passa pela guarda: o esquema temporário é pesquisado primeiro, mesmo com `SET search_path = public`.
- **O `EXECUTE` diz quem entra, não o que se autoriza.** Toda função `SECURITY DEFINER` chamável por `authenticated` confere o papel por dentro, antes de fazer qualquer coisa:

```sql
CREATE FUNCTION public.acao_restrita() RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM public.perfis
    WHERE id = (SELECT auth.uid()) AND papel = ANY (ARRAY['admin'])
  ) THEN
    RAISE EXCEPTION 'sem permissão' USING ERRCODE = '42501';
  END IF;
  -- a ação
END $$;
REVOKE EXECUTE ON FUNCTION public.acao_restrita() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION public.acao_restrita() TO authenticated;
```

- Os papéis que passam **medem-se** contra a permissão que a tela exige; não se adivinham. Antes de pôr a guarda, veja quem chama hoje a função: pode haver um chamador legítimo que não é admin.
- Se só uma rotina agendada chama a função, revogue o `EXECUTE` de `authenticated` em vez de pôr guarda.
- Prova: o papel sem permissão recebe `42501`; o papel com permissão passa e cai no erro de negócio a seguir (ver `sql-postgres`, seção 3).

## 5. Coluna nova: a ordem obrigatória

**O PostgREST falha a operação inteira** quando o pedido tem uma coluna que não existe. Não a ignora. No payload de um `insert` ou `update` o erro é `PGRST204`; no `select=` chega o `42703` do Postgres.

1. Migração aplicada.
2. Conferida no `information_schema`.
3. Só então a coluna entra na lista de colunas do cliente e no tipo.

Há também uma corrida entre o deploy e o cache de esquema do PostgREST: o código novo pode chegar antes de o cache ver a coluna. `NOTIFY pgrst, 'reload schema'` manda o PostgREST recarregar o cache.

## 6. Código que usa o cliente

- **Tipos gerados:** o cliente usa o tipo `Database` gerado do esquema. Um cast `as unknown as T[]` desliga o compilador justamente onde ele ajudaria. Mantenha um tipo que espelhe o `select`, e alargue o `select` e o tipo na mesma edição.
- **Colunas de auditoria** (`deleted_at`, `deleted_by`, quem criou) não entram na lista de colunas que o cliente pede.
- **Consultas em lote** com `.in('id', ids)`, nunca uma consulta por item num laço.
- **Usuários criam-se pela API de administração**, nunca com `INSERT` direto em `auth.users`.
- **No servidor, a sessão vem dos cookies**, não do `localStorage`.
- **No servidor, a identidade confere-se com `getClaims()` (ou `getUser()`)**, nunca com `getSession()`, que lê o cookie sem o revalidar.
- **`user_metadata` (`raw_user_meta_data`) é editável pelo próprio usuário:** não serve para autorizar, nem em políticas nem em guardas.
- **A chave de serviço nunca vai para o cliente** (nada de variável `NEXT_PUBLIC_*` com ela).
- **Cada rota de servidor confere a sessão por si**, sem confiar no middleware. Um download confere primeiro a posse, com uma consulta sujeita ao RLS, e só depois usa a chave de serviço.

## 7. Edge Functions que fazem de proxy

Uma Edge Function que chama uma API externa em nome do usuário cria o cliente Supabase com o cabeçalho `Authorization` que recebeu e deixa o RLS decidir. Não refaça à mão verificações contra tabelas de acesso: duplicam a regra e divergem.

## 8. Erros e o que provam

| Código | O que é | Prova bloqueio? |
|---|---|---|
| `42501` | Sem permissão: falta de grant, ou o `WITH CHECK` do RLS. Pela API chega como HTTP 401 (`anon`) ou 403 (autenticado) | Sim |
| 0 linhas, `UPDATE 0`, `DELETE 0` | O `USING` do RLS filtrou, sem erro | Só com a assimetria: o dono vê a linha, o outro não |
| `PGRST204` / `42703` | Coluna desconhecida (`PGRST204` no payload, `42703` no `select`) | **Não**: é erro de esquema |
| `42P17` | Recursão infinita entre políticas | Não: é a política que está errada |
| `23503` | Chave estrangeira | Não. Mostra que a permissão passou e a regra de negócio parou |

## Fontes

Consultadas em 30 de outubro de 2026 (as mesmas linhas estão em `FONTES.md`):

- Supabase, Row Level Security: https://supabase.com/docs/guides/database/postgres/row-level-security
- Supabase, Securing your API: https://supabase.com/docs/guides/api/securing-your-api
- Supabase, Server-Side Auth for Next.js: https://supabase.com/docs/guides/auth/server-side/nextjs
- Supabase, Testing Overview: https://supabase.com/docs/guides/local-development/testing/overview
- PostgREST, Errors: https://docs.postgrest.org/en/stable/references/errors.html
- PostgreSQL 18, Row Security Policies: https://www.postgresql.org/docs/18/ddl-rowsecurity.html
- PostgreSQL 18, CREATE FUNCTION («Writing SECURITY DEFINER Functions Safely»): https://www.postgresql.org/docs/18/sql-createfunction.html
- PostgreSQL 18, CREATE VIEW (`security_invoker`): https://www.postgresql.org/docs/18/sql-createview.html

Os trechos de SQL foram testados no PostgreSQL 18.3, num banco descartável com os papéis e o `auth.uid()` do Supabase imitados, em 30 de outubro de 2026. O PostgREST (`PGRST204`, `NOTIFY pgrst`, os códigos HTTP) e o código do cliente (seção 6) não foram testados.
