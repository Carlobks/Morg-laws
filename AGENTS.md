# AGENTS.md — Morg-laws

Regras e aprendizados para trabalhar com agentes de código, tirados de um sistema real em produção.
Este arquivo é lido inteiro em todo turno: por isso fica curto (máximo 60 linhas, o hook confere).

## Como usar

- Este arquivo traz só o núcleo, que vale para qualquer projeto.
- O resto está em `skills/`: cada skill tem uma descrição e só deve ser aberta quando o assunto aparecer.
  Projeto sem SQL não precisa abrir a skill de SQL.
- Instalar as skills num projeto: `npx skills add Carlobks/Morg-laws` (em construção).

## Núcleo

> Em construção (fase 2). Cada regra entra na forma curta, com o motivo numa frase e a fonte em `FONTES.md`.

## Índice: quando ler o quê

| Situação | Onde ler |
|---|---|
| Vai escrever ou mudar um CLAUDE.md ou AGENTS.md | `skills/escrevendo-regras-de-agente/` (em construção) |
| Vai dividir trabalho entre sessões | `skills/orquestrando-sessoes/` (em construção) |
| Vai commitar | `skills/git-e-commits/` (em construção) |
| Vai corrigir um bug ou provar que algo funciona | `skills/testes-e-provas/` (em construção) |
| Vai fazer push de código | `skills/auditoria-de-seguranca/` (em construção) |
| O projeto usa SQL ou Postgres | `skills/sql-postgres/` (em construção) |
| O projeto usa Supabase | `skills/supabase/` (em construção) |
| O projeto usa Next.js ou React | `skills/nextjs-react/` (em construção) |
| Quer o porquê de uma regra | `biblia-akita/` e `aprendizados/` (em construção) |

## Regras deste repositório

- Repositório público: nunca nomes de pessoas ou empresas, e-mails, IDs de serviços, caminhos de máquina ou dados reais.
- Toda fonte usada entra em `FONTES.md`, com a data em que foi lida.
- Livros: resumo com palavras próprias, com capítulo e página. Nunca texto copiado.
- Escrita em português do Brasil.
