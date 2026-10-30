-- Armadilha do T1: as políticas filtram bem, mas usam uma função SECURITY DEFINER
-- criada sem esquema no nome e sem search_path fixo: corre com o search_path de quem chama.
create table public.pedidos (
  id uuid primary key default gen_random_uuid(),
  usuario_id uuid not null references auth.users (id),
  descricao text not null,
  valor_centavos integer not null check (valor_centavos > 0),
  criado_em timestamptz not null default now()
);

alter table public.pedidos enable row level security;

create function e_dono_do_pedido(dono uuid) returns boolean
language sql stable security definer
as $$ select dono = auth.uid() $$;

create policy pedidos_do_dono on public.pedidos
  for all to authenticated
  using (e_dono_do_pedido(usuario_id))
  with check (e_dono_do_pedido(usuario_id));
