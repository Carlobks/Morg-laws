-- Catálogo de produtos: público, qualquer visitante pode ver.
create table public.produtos (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  preco_centavos integer not null check (preco_centavos > 0),
  criado_em timestamptz not null default now()
);

alter table public.produtos enable row level security;

create policy produtos_catalogo_visivel_a_todos on public.produtos
  for select to anon, authenticated
  using (true);
