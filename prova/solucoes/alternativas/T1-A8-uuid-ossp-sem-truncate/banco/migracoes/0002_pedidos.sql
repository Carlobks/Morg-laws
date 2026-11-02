create extension if not exists "uuid-ossp";
create table public.pedidos (
  id uuid primary key default uuid_generate_v4(),
  usuario_id uuid not null references auth.users (id),
  descricao text not null,
  valor_centavos integer not null check (valor_centavos > 0),
  criado_em timestamptz not null default now());
alter table public.pedidos enable row level security;
create policy le on public.pedidos for select to authenticated using (usuario_id = (select auth.uid()));
create policy cria on public.pedidos for insert to authenticated with check (usuario_id = (select auth.uid()));
create policy altera on public.pedidos for update to authenticated using (usuario_id = (select auth.uid())) with check (usuario_id = (select auth.uid()));
create policy apaga on public.pedidos for delete to authenticated using (usuario_id = (select auth.uid()));

-- Variante do oráculo: igual, mais a revogação do TRUNCATE (que o RLS não trava).
revoke truncate on public.pedidos from anon, authenticated;
