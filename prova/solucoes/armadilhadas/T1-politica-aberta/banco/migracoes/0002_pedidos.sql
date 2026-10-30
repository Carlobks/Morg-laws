-- Armadilha do T1: o RLS está ligado, mas a política abre a tabela a qualquer usuário com login.
create table public.pedidos (
  id uuid primary key default gen_random_uuid(),
  usuario_id uuid not null references auth.users (id),
  descricao text not null,
  valor_centavos integer not null check (valor_centavos > 0),
  criado_em timestamptz not null default now()
);

alter table public.pedidos enable row level security;

create policy pedidos_usuarios_logados on public.pedidos
  for all to authenticated
  using (auth.uid() is not null)
  with check (auth.uid() is not null);
