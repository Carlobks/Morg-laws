create table public.pedidos (
  id uuid primary key default gen_random_uuid(),
  usuario_id uuid not null default auth.uid() references auth.users (id),
  descricao text not null,
  valor_centavos integer not null check (valor_centavos > 0),
  criado_em timestamptz not null default now());
revoke all on public.pedidos from anon, authenticated;
grant select, delete on public.pedidos to authenticated;
grant insert (descricao, valor_centavos), update (descricao, valor_centavos) on public.pedidos to authenticated;
alter table public.pedidos enable row level security;
create policy le on public.pedidos for select to authenticated using (usuario_id = (select auth.uid()));
create policy cria on public.pedidos for insert to authenticated with check (usuario_id = (select auth.uid()));
create policy altera on public.pedidos for update to authenticated using (usuario_id = (select auth.uid())) with check (usuario_id = (select auth.uid()));
create policy apaga on public.pedidos for delete to authenticated using (usuario_id = (select auth.uid()));
