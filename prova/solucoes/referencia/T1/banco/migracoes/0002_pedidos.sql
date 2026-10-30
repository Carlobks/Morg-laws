-- Solução de referência do T1: cada usuário só vê e mexe nos próprios pedidos.
create table public.pedidos (
  id uuid primary key default gen_random_uuid(),
  usuario_id uuid not null references auth.users (id) on delete cascade,
  descricao text not null check (length(trim(descricao)) > 0),
  valor_centavos integer not null check (valor_centavos > 0),
  criado_em timestamptz not null default now()
);

create index pedidos_usuario_id_idx on public.pedidos (usuario_id);

alter table public.pedidos enable row level security;

-- O papel anônimo não tem nada a fazer aqui.
revoke all on public.pedidos from anon;
-- TRUNCATE passa por cima do RLS: a aplicação não precisa dele.
revoke truncate, references, trigger on public.pedidos from authenticated;

create policy pedidos_dono_le on public.pedidos
  for select to authenticated
  using (usuario_id = (select auth.uid()));

create policy pedidos_dono_cria on public.pedidos
  for insert to authenticated
  with check (usuario_id = (select auth.uid()));

create policy pedidos_dono_altera on public.pedidos
  for update to authenticated
  using (usuario_id = (select auth.uid()))
  with check (usuario_id = (select auth.uid()));

create policy pedidos_dono_apaga on public.pedidos
  for delete to authenticated
  using (usuario_id = (select auth.uid()));
