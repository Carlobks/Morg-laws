-- Esqueleto mínimo que imita o Supabase num Postgres local.
-- Já existe no banco antes das migrações: não é para mudar.

create role anon nologin;
create role authenticated nologin;
create role service_role nologin bypassrls;

grant usage on schema public to anon, authenticated, service_role;

create schema auth;
grant usage on schema auth to anon, authenticated, service_role;

create table auth.users (
  id uuid primary key,
  email text not null unique
);

-- O id do usuário da requisição (vem do token de login).
create function auth.uid() returns uuid
language sql stable
as $$ select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid $$;

-- Como no Supabase: as tabelas novas de public ficam acessíveis aos papéis da API;
-- quem decide o que cada um vê são as políticas de RLS.
alter default privileges in schema public grant all on tables to anon, authenticated, service_role;
alter default privileges in schema public grant all on sequences to anon, authenticated, service_role;
alter default privileges in schema public grant execute on functions to anon, authenticated, service_role;
