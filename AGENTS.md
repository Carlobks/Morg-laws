# AGENTS.md — Morg-laws

Regras para trabalhar com agentes de código, tiradas de um sistema real em produção.
Lido inteiro em todo turno: por isso fica curto (máximo 60 linhas, o hook confere). O detalhe está nas skills.

## Núcleo (vale para qualquer projeto)

- **Plano antes de mexer.** Mudança com vários arquivos começa por um plano e pelo "sim" do dono do projeto.
- **Decisão a meio vai ao dono**, explicada, com a opção recomendada marcada. Não se decide sozinho o que é dele.
- **Commitar não precisa de pedido; push e PR precisam.** Commit atômico, por caminho; nunca `git add -A` ou `.`.
- **Os hooks são a rede.** Nunca saltar (`--no-verify`) nem desligar. Hook recusou: corrige-se a causa.
- **O que já viola não pode piorar;** arquivo novo nasce limpo. *Senão a dívida só cresce.*
- **Sem silenciar alarme:** nada de `eslint-disable`, `@ts-ignore` ou `@ts-expect-error` novos. Corrige-se o apontado.
- **Bug corrigido traz o teste que o pega**, visto a falhar antes da correção.
- **Provar medindo** (comando e saída, tela, consulta), nunca "pronto". Dizer também o que não se verificou.
- **Nomes únicos e pesquisáveis.** Nada de `data`, `utils`, `Props` genéricos: `grep` antes de criar.
- **Texto é conselho; o que tem de ser cumprido vira hook, teste ou CI.** Regra só escrita não se cumpre.

## Nunca

- Escrever no banco de produção (esquema ou dados) sem o "sim" explícito do dono.
- Dados reais (nomes, documentos, IDs de pessoas) em testes, exemplos ou commits.
- Ler `.env` e segredos; rodar `curl | sh`; mudar as próprias permissões do agente.
- Commitar trabalho de outra sessão ou de outra pessoa que esteja na mesma pasta.

## Índice: quando ler o quê

| Situação | Onde ler |
|---|---|
| Vai escrever ou mudar um CLAUDE.md, AGENTS.md ou skill | `skills/escrevendo-regras-de-agente/` |
| Pedido grande sem limites ou sem forma de validar | `skills/pondo-o-plano-a-prova/` |
| Vai dividir trabalho entre sessões ou agentes | `skills/orquestrando-sessoes/` |
| Vai commitar ou fechar um ciclo de trabalho | `skills/git-e-commits/` |
| Vai corrigir um bug, testar ou provar que algo funciona | `skills/testes-e-provas/` |
| Vai fazer push de código | `skills/auditoria-de-seguranca/` (em construção) |
| O projeto usa SQL, Supabase, Next.js ou React | `skills/sql-postgres/`, `supabase/`, `nextjs-react/` |
| Quer o porquê de uma regra | `biblia-akita/` e `aprendizados/` (em construção) |

Instalar as skills num projeto: `npx skills add Carlobks/Morg-laws`.

## Regras deste repositório

- Público: nunca nomes de pessoas ou empresas, e-mails, IDs de serviços, caminhos de máquina ou dados reais.
- Toda fonte usada entra em `FONTES.md`. Livros: resumo com palavras próprias, com página. Nunca texto copiado.
- Nada de terceiros copiado: escreve-se com estrutura própria e cita-se a inspiração em `FONTES.md`.
- Escrita em português do Brasil.
