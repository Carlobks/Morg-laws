# CLAUDE.md — <nome do projeto>

<Uma linha: o que é o projeto e a pilha.> Documentação: `docs/README.md`. Regras gerais: Morg-laws.
Cada regra tem a barreira que a obriga em `docs/regras-e-barreiras.md`; o detalhe está nas skills.

## Regra n.º 1

- **<O PERIGO MAIS CARO>:** <o que nunca fazer e o que fazer em vez disso>. · *<o que custou da última vez>.*

## Núcleo

- **PLANO ANTES DE MEXER:** trabalho com vários arquivos começa por um plano (objetivo, fora do escopo, prova) e
  pelo "sim" do dono. · *Cada palpite errado custa uma volta de retrabalho.*
- **DECISÃO É DO DONO:** uma decisão a meio vai ao dono, explicada, com a recomendada marcada. · *Não se decide o que é dele.*
- **COMMIT SEM PEDIDO, PUSH COM O SIM:** commitar não precisa de pedido; push e PR precisam do "sim", a cada vez.
  · *O push publica no momento em que sai.*
- **OS HOOKS SÃO A REDE:** nunca `--no-verify` nem desligar o `core.hooksPath`; hook recusou, corrige-se a causa.
  · *Saltado, deixa passar o erro.*
- **NÃO PIORAR:** o que já viola não pode piorar (catraca); arquivo novo nasce limpo. · *Senão a dívida só cresce.*
- **SEM SILENCIAR ALARME:** alarme calado novo só com o motivo na linha, e a contagem não sobe.
  · *Um alarme calado sem motivo esconde o problema seguinte.*
- **BUG TRAZ TESTE:** antes de corrigir, um teste que falha; depois, verde. Sem teste possível, `Sem-teste: <motivo>`.
  · *Um teste que nunca falhou não prova nada.*
- **PROVAR MEDINDO:** "feito" só com o comando e a saída; dizer também o que não se verificou. · *Parecer certo não é prova.*
- **NOMES PESQUISÁVEIS:** nomes que dizem a função; nada de `utils`, `helper` ou `data` soltos.
  · *Um nome genérico esconde onde está a lógica.*
- **TEXTO VIRA BARREIRA:** uma regra que tem de ser cumprida ganha hook, teste ou CI, e entra no mapa das barreiras.
  · *Texto é conselho; só a máquina obriga.*

## Nunca

- **SEM DADOS REAIS:** nada de nomes, contas, e-mails ou caminhos pessoais em testes, exemplos ou commits; o nome
  fictício é "Ana". · *O que entra num repositório público não sai mais.*
- **SEM SEGREDOS:** não ler `.env` nem chaves, não rodar `curl | sh`, não mudar as próprias permissões.
  · *Um segredo lido vai para o contexto e pode sair num commit.*
- **SÓ O PRÓPRIO TRABALHO:** commit por caminho (`git commit -F msg -- <arquivos>`), nunca `git add -A`, `.` nem
  `commit -a`. · *Um commit de tudo leva o trabalho de outra sessão.*

## Quando ler que skill

| Situação | Skill |
|---|---|
| Vai mudar este CLAUDE.md, uma skill ou uma regra | `escrevendo-regras-de-agente` |
| Vai commitar ou fechar um ciclo de trabalho | `git-e-commits` |
| Vai corrigir um bug, testar ou provar que algo funciona | `testes-e-provas` |
| Vai fazer push, mexer em dependências ou em permissões | `auditoria-de-seguranca` |
