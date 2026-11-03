# AGENTS.md — <nome do projeto>

<Uma linha: o que é o projeto e a pilha.> Documentação: `docs/README.md`.
Lido inteiro em todo turno: por isso fica curto. Cada regra tem a barreira que a obriga em `docs/regras-e-barreiras.md`;
o detalhe está nas skills. Regras gerais: [Morg-laws](https://github.com/Carlobks/Morg-laws).
No Claude Code, o CLAUDE.md do projeto tem só a linha `@AGENTS.md` e o que vale apenas lá.

## Regra n.º 1

- **<O PERIGO MAIS CARO>:** <o que nunca fazer e o que fazer em vez disso>. · *<o que custou da última vez>.*

## Núcleo

- **PLANO ANTES DE MEXER:** mudança com vários arquivos começa por um plano e pelo "sim" do dono do projeto.
  · *Cada palpite errado custa uma volta de retrabalho.*
- **DECISÃO É DO DONO:** decisão a meio vai ao dono, explicada, com a opção recomendada marcada. · *Não se decide sozinho o que é dele.*
- **COMMIT SEM PEDIDO, PUSH COM O SIM:** commitar não precisa de pedido; push e PR precisam, a cada vez. Commit atômico, por caminho; nunca `git add -A` ou `.`.
  · *O push publica no momento em que sai.*
- **OS HOOKS SÃO A REDE:** nunca saltar (`--no-verify`) nem desligar. Hook recusou: corrige-se a causa. · *Saltado, deixa passar o erro.*
- **NÃO PIORAR:** o que já viola não pode piorar; arquivo novo nasce limpo. · *Senão a dívida só cresce.*
- **SEM SILENCIAR ALARME SEM MOTIVO:** corrige-se o apontado. Um `eslint-disable`, `@ts-expect-error` ou `noqa` novo só com o motivo na mesma linha,
  e a contagem por tipo não sobe. · *Um alarme calado sem motivo esconde o seguinte.*
- **BUG TRAZ TESTE:** bug corrigido traz o teste que o pega, visto a falhar antes da correção. · *Um teste que nunca falhou não prova nada.*
- **PROVAR MEDINDO:** comando e saída, tela, consulta; nunca "pronto". Dizer também o que não se verificou. · *Parecer certo não é prova.*
- **NOMES ÚNICOS E PESQUISÁVEIS:** nada de `data`, `utils`, `Props` genéricos: `grep` antes de criar. · *Um nome genérico esconde onde está a lógica.*
- **TEXTO VIRA BARREIRA:** texto é conselho; o que tem de ser cumprido vira hook, teste ou CI. · *Regra só escrita não se cumpre.*

## Nunca

- **SEM ESCRITA NO BANCO:** escrever no banco de produção (esquema ou dados) sem o "sim" explícito do dono. · *O banco de produção é de toda a gente.*
- **SEM DADOS REAIS:** dados reais (nomes, documentos, IDs de pessoas) em testes, exemplos ou commits. · *O que entra num repositório público não sai mais.*
- **SEM SEGREDOS:** ler `.env` e segredos; rodar `curl | sh`; mudar as próprias permissões do agente.
  · *Um segredo lido vai para o contexto e pode sair num commit.*
- **SÓ O PRÓPRIO TRABALHO:** commitar trabalho de outra sessão ou de outra pessoa que esteja na mesma pasta.
  · *Um commit de tudo leva o trabalho de outra sessão.*

## Índice: quando ler o quê

As skills abrem pelo nome, estejam onde estiverem instaladas. Instalar ou atualizar: `npx skills add Carlobks/Morg-laws`.

| Situação | Skill |
|---|---|
| Vai escrever ou mudar um CLAUDE.md, AGENTS.md ou skill | `escrevendo-regras-de-agente` |
| Pedido grande sem limites ou sem forma de validar | `pondo-o-plano-a-prova` |
| Vai dividir trabalho entre sessões ou agentes | `orquestrando-sessoes` |
| Vai compactar a conversa, parar ou retomar trabalho | `passando-o-trabalho` |
| Vai commitar ou fechar um ciclo de trabalho | `git-e-commits` |
| Vai corrigir um bug, testar ou provar que algo funciona | `testes-e-provas` |
| Vai criar, redesenhar ou rever uma tela | `desenhando-telas` |
| Vai fazer push de código | `auditoria-de-seguranca` |
| O projeto usa SQL, Supabase, Next.js ou React | `sql-postgres`, `supabase`, `nextjs-react` |
