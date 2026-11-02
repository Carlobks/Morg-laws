create table public.pedidos (
  id uuid primary key default gen_random_uuid(),
  usuario_id uuid not null references auth.users (id),
  descricao text not null,
  valor_centavos integer not null check (valor_centavos > 0),
  criado_em timestamptz not null default now());
alter table public.pedidos enable row level security;
create function public.e_dono(dono uuid) returns boolean language sql stable security definer set search_path = public as $$ select dono = auth.uid() $$;
create policy dono on public.pedidos for all to authenticated using (public.e_dono(usuario_id)) with check (public.e_dono(usuario_id));
