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
| Função `SECURITY DEFINER` | **A própria função** (ignora o RLS) | Quem pode executá-la e o que ela confere por dentro |

- **Nome de política não prova nada.** Uma política chamada `admin_*` com `USING (true)` para todos já existiu num projeto real. Leia a expressão.
- **"Tem login" não é barreira.** `USING (auth.uid() IS NOT NULL)` está aberta a **todas** as contas autenticadas, incluindo as de trabalhadores com acesso pelo celular.

## 2. RLS

- **Política que substitui outra apaga a antiga na mesma migração** (`DROP POLICY IF EXISTS`). Políticas do mesmo comando combinam por OR: a antiga, esquecida, anula a nova. Confira em `pg_policy` que a antiga sumiu.
- **Uma política da tabela X nunca consulta a própria X:** dá recursão infinita.
- **Antes de apagar uma política solta, veja se ela é a única porta** de quem tem direito para aquele comando. Se for, o `DROP` fecha o buraco e parte a tela. Substitui-se por uma política certa, não se apaga.
- **Filtrar os apagados mesmo com RLS** (`.is('deleted_at', null)`): defesa em profundidade.

## 3. Grants

- **`REVOKE ... FROM PUBLIC` não chega.** O Supabase dá grants individuais a `anon` e `authenticated`; revogue de cada papel pelo nome.
- **O RLS não trava `TRUNCATE`.** Nunca escreva `GRANT ALL` aos papéis do cliente: conceda só `SELECT, INSERT, UPDATE, DELETE`, o que a tabela usa. Depois de criar uma tabela, confira com `has_table_privilege('authenticated', 'tabela', 'TRUNCATE')`, que deve devolver false.

## 4. Funções `SECURITY DEFINER`

- Revogue `EXECUTE` de `anon` e de `PUBLIC`.
- **O `EXECUTE` diz quem entra, não o que se autoriza.** Toda função `SECURITY DEFINER` chamável por `authenticated` confere o papel por dentro, antes de fazer qualquer coisa:

```sql
IF NOT EXISTS (
  SELECT 1 FROM perfis
  WHERE id = (SELECT auth.uid()) AND papel = ANY (ARRAY['admin'])
) THEN
  RAISE EXCEPTION 'sem permissão' USING ERRCODE = '42501';
END IF;
```

- Os papéis que passam **medem-se** contra a permissão que a tela exige; não se adivinham. Antes de pôr a guarda, veja quem chama hoje a função: pode haver um chamador legítimo que não é admin.
- Se só uma rotina agendada chama a função, revogue o `EXECUTE` de `authenticated` em vez de pôr guarda.
- Prova: o papel sem permissão recebe `42501`; o papel com permissão passa e cai no erro de negócio a seguir (ver `sql-postgres`, seção 3).

## 5. Coluna nova: a ordem obrigatória

**O PostgREST falha a operação inteira** (`PGRST204`) quando o `select` ou o payload têm uma coluna que não existe. Não a ignora.

1. Migração aplicada.
2. Conferida no `information_schema`.
3. Só então a coluna entra na lista de colunas do cliente e no tipo.

Há também uma corrida entre o deploy e o cache de esquema do PostgREST: o código novo pode chegar antes de o cache ver a coluna.

## 6. Código que usa o cliente

- **Tipos gerados:** o cliente usa o tipo `Database` gerado do esquema. Um cast `as unknown as T[]` desliga o compilador justamente onde ele ajudaria. Mantenha um tipo que espelhe o `select`, e alargue o `select` e o tipo na mesma edição.
- **Colunas de auditoria** (`deleted_at`, `deleted_by`, quem criou) não entram na lista de colunas que o cliente pede.
- **Consultas em lote** com `.in('id', ids)`, nunca uma consulta por item num laço.
- **Usuários criam-se pela API de administração**, nunca com `INSERT` direto em `auth.users`.
- **No servidor, a sessão vem dos cookies**, não do `localStorage`.
- **Cada rota de servidor confere a sessão por si**, sem confiar no middleware. Um download confere primeiro a posse, com uma consulta sujeita ao RLS, e só depois usa a chave de serviço.

## 7. Edge Functions que fazem de proxy

Uma Edge Function que chama uma API externa em nome do usuário cria o cliente Supabase com o cabeçalho `Authorization` que recebeu e deixa o RLS decidir. Não refaça à mão verificações contra tabelas de acesso: duplicam a regra e divergem.

## 8. Erros e o que provam

| Código | O que é | Prova bloqueio? |
|---|---|---|
| `42501` | Sem permissão (RLS ou grant) | Sim |
| `PGRST204` / `42703` | Coluna desconhecida | **Não**: é erro de esquema |
| `23503` | Chave estrangeira | Não. Mostra que a permissão passou e a regra de negócio parou |

## Fontes

Ver `FONTES.md`. Os trechos de SQL ainda não foram rodados num banco de teste: isso fica para a Fase 4.
