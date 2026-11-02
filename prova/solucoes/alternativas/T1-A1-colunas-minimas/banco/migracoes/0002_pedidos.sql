create table public.pedidos (usuario_id uuid, descricao text, valor_centavos integer);
alter table public.pedidos enable row level security;
create policy le on public.pedidos for select to authenticated using (usuario_id = (select auth.uid()));
create policy cria on public.pedidos for insert to authenticated with check (usuario_id = (select auth.uid()));
create policy altera on public.pedidos for update to authenticated using (usuario_id = (select auth.uid())) with check (usuario_id = (select auth.uid()));
create policy apaga on public.pedidos for delete to authenticated using (usuario_id = (select auth.uid()));
