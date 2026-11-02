# AGENTS.md — Morg-laws

Regras para trabalhar com agentes de código, tiradas de um sistema real em produção.
Lido inteiro em todo turno: por isso fica curto (máximo 60 linhas, o hook confere). O detalhe está nas skills.

## Núcleo (vale para qualquer projeto)

- **Plano antes de mexer.** Mudança com vários arquivos começa por um plano e pelo "sim" do dono do projeto.
- **Decisão a meio vai ao dono**, explicada, com a opção recomendada marcada. Não se decide sozinho o que é dele.
- **Commitar não precisa de pedido; push e PR precisam, a cada vez.** Commit atômico, por caminho; nunca `git add -A` ou `.`.
- **Os hooks são a rede.** Nunca saltar (`--no-verify`) nem desligar. Hook recusou: corrige-se a causa.
- **O que já viola não pode piorar;** arquivo novo nasce limpo. *Senão a dívida só cresce.*
- **Sem silenciar alarme sem motivo:** corrige-se o apontado. Um `eslint-disable`, `@ts-expect-error` ou `noqa` novo
  só com o motivo na mesma linha, e a contagem por tipo não sobe. *Um alarme calado sem motivo esconde o seguinte.*
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

As skills abrem pelo nome, estejam onde estiverem instaladas (`.claude/skills/`, `skills/`…).

| Situação | Skill |
|---|---|
| Vai escrever ou mudar um CLAUDE.md, AGENTS.md ou skill | `escrevendo-regras-de-agente` |
| Pedido grande sem limites ou sem forma de validar | `pondo-o-plano-a-prova` |
| Vai dividir trabalho entre sessões ou agentes | `orquestrando-sessoes` |
| Vai commitar ou fechar um ciclo de trabalho | `git-e-commits` |
| Vai corrigir um bug, testar ou provar que algo funciona | `testes-e-provas` |
| Vai criar, redesenhar ou rever uma tela | `desenhando-telas` |
| Vai fazer push de código | `auditoria-de-seguranca` |
| O projeto usa SQL, Supabase, Next.js ou React | `sql-postgres`, `supabase`, `nextjs-react` |

No repositório Morg-laws: o porquê das regras em `biblia-akita/`, hooks, portões e testes prontos a copiar em
`modelos/` e as notas em `aprendizados/`.
Instalar as skills num projeto: `npx skills add Carlobks/Morg-laws`. Projeto que só usa o Claude Code pode pôr
estas regras direto no CLAUDE.md; o arquivo de regras do projeto fica com até 100 linhas.

## Regras deste repositório

- Público: nunca nomes de pessoas ou empresas, e-mails, IDs de serviços, caminhos de máquina ou dados reais.
- Toda fonte usada entra em `FONTES.md`. Livros: resumo com palavras próprias, com página. Nunca texto copiado.
- Pesquisa que outra sessão vai reler vai para `pesquisas/`, com o índice; o CI confere as pesquisas e as fontes.
- Nada de terceiros copiado: escreve-se com estrutura própria e cita-se a inspiração em `FONTES.md`.
- Escrita em português do Brasil.
