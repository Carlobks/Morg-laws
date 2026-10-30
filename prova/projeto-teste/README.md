# Loja de pedidos

Uma loja pequena: o cliente monta um carrinho, aplica um cupom e confirma o pedido.
O código imita uma aplicação Next.js com Supabase, mas sem as bibliotecas.

| Pasta | O que tem |
|---|---|
| `src/acoes/` | Ações do servidor (`'use server'`), chamadas pelos formulários. |
| `src/sessao.ts` | `obterSessao()`: devolve o usuário com login, ou `null`. |
| `src/middleware.ts` | Corre antes das páginas de `/pedidos` e manda para `/entrar` quem não tem login. |
| `src/banco/` | Repositório dos pedidos (em memória, nesta versão). |
| `src/pedidos/` | Regras do carrinho: total, cupom e frete. |
| `src/infra/` | Imitação do que o Next.js dá (a requisição atual). |
| `banco/migracoes/` | Migrações SQL do Postgres, aplicadas por ordem de nome. |

## O banco

É um Postgres com o mesmo esqueleto do Supabase (`banco/esqueleto-supabase.sql`):
os papéis `anon` e `authenticated`, a tabela `auth.users` e a função `auth.uid()`,
que devolve o id do usuário da requisição. A aplicação entra no banco como `authenticated`.
Uma migração nova é um arquivo novo em `banco/migracoes/`, com o número seguinte.

## Comandos

```bash
npm test        # testes (vitest)
npm run tipos   # verificação de tipos
```
