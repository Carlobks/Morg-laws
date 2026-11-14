# As regras

Esta parte lê o `AGENTS.md` do Morg-laws regra por regra: o que ela manda, o porquê que está escrito nele e onde fica o detalhe. São dez regras do núcleo, quatro do “Nunca”, o índice das skills e as regras do próprio repositório. O `AGENTS.md` é lido inteiro em todo turno, por isso é curto, e cada regra tem a mesma forma: o título, o que fazer e o porquê numa frase. O detalhe de cada regra está na skill que ela cita.

## O núcleo

As dez regras valem para qualquer projeto.

**Plano antes de mexer.** Uma mudança com vários arquivos começa por um plano e pelo “sim” do dono do projeto. O porquê escrito: cada palpite errado custa uma volta de retrabalho. Skill: [`pondo-o-plano-a-prova`](https://github.com/Carlobks/Morg-laws/blob/main/skills/pondo-o-plano-a-prova/SKILL.md), que se apoia no livro *Competente o Suficiente*, de Fabio Akita (pp. 118, 120–121). O procedimento está na parte 06 (P18).

**Decisão é do dono.** Uma decisão no meio do trabalho vai ao dono, explicada, com a opção recomendada marcada. O porquê: não se decide sozinho o que é dele. Skill: a mesma, [`pondo-o-plano-a-prova`](https://github.com/Carlobks/Morg-laws/blob/main/skills/pondo-o-plano-a-prova/SKILL.md). Ver a parte 06 (P18).

**Commit sem pedido, push com o “sim”.** Commitar não precisa de pedido; o push e o PR precisam, a cada vez. O commit é atômico, por caminho, e nunca se usa `git add -A` nem `git add .`. O porquê: o push publica no momento em que sai. Skill: [`git-e-commits`](https://github.com/Carlobks/Morg-laws/blob/main/skills/git-e-commits/SKILL.md), que se apoia no livro (pp. 230, 382). Ver a parte 06 (P19 e P22).

**Os hooks são a rede.** Nunca se pula um hook com `--no-verify` nem se desliga; se um hook recusou, se corrige a causa. O porquê: pulado, o hook deixa passar o erro. Skill: [`git-e-commits`](https://github.com/Carlobks/Morg-laws/blob/main/skills/git-e-commits/SKILL.md), e o livro manda passar cada commit pela mesma bateria (pp. 408–409). Ver a parte 06 (P20) e a parte 08.

**Não piorar.** O que já viola não pode piorar, e um arquivo novo nasce limpo. O porquê: senão a dívida só cresce. O mecanismo é a catraca, uma linha de base que só encolhe. Skills: [`codigo-legivel`](https://github.com/Carlobks/Morg-laws/blob/main/skills/codigo-legivel/SKILL.md) e [`testes-e-provas`](https://github.com/Carlobks/Morg-laws/blob/main/skills/testes-e-provas/SKILL.md). Como ela funciona por dentro está na parte 08.

**Sem silenciar alarme sem motivo.** Se corrige o que o alarme aponta. Um `eslint-disable`, um `@ts-expect-error` ou um `noqa` novo só entra com o motivo na mesma linha, e a contagem por tipo não sobe. O porquê: um alarme calado sem motivo esconde o seguinte. O livro dá a razão de fundo: uma exceção a um alarme só vale com a razão escrita (p. 165). Skill: [`codigo-legivel`](https://github.com/Carlobks/Morg-laws/blob/main/skills/codigo-legivel/SKILL.md).

**Bug traz teste.** Um bug corrigido traz o teste que o pega, visto falhando antes da correção. O porquê: um teste que nunca falhou não prova nada. Skill: [`testes-e-provas`](https://github.com/Carlobks/Morg-laws/blob/main/skills/testes-e-provas/SKILL.md), e o livro manda prender cada bug com um teste (pp. 80–81). Ver a parte 06 (P21).

**Provar medindo.** Cada “funciona” leva o comando e a saída, a tela ou a consulta, nunca só “pronto”, e diz também o que não se verificou. O porquê: parecer certo não é prova. Skill: [`testes-e-provas`](https://github.com/Carlobks/Morg-laws/blob/main/skills/testes-e-provas/SKILL.md), com o livro (pp. 157, 172, 252, 276–277).

**Nomes únicos e pesquisáveis.** Nada de `data`, `utils` ou `Props` genéricos, e um `grep` antes de criar um nome. O porquê: um nome genérico esconde onde está a lógica. Skill: [`codigo-legivel`](https://github.com/Carlobks/Morg-laws/blob/main/skills/codigo-legivel/SKILL.md).

**Texto vira barreira.** O texto é conselho; o que tem de ser cumprido vira hook, teste ou CI. O porquê: regra só escrita não se cumpre. Skill: [`escrevendo-regras-de-agente`](https://github.com/Carlobks/Morg-laws/blob/main/skills/escrevendo-regras-de-agente/SKILL.md), e a parte 08 mostra as barreiras prontas.

## O “Nunca”

São quatro proibições. Três têm barreira de máquina na parte 08; a do banco fica em texto, porque nenhuma máquina sabe se houve o seu “sim” (o mapa das barreiras do molde diz isso).

**Sem escrita no banco.** Nunca se escreve no banco de produção, nem no esquema nem nos dados, sem o “sim” explícito do dono. O porquê: o banco de produção é de todo mundo. Skill: [`sql-postgres`](https://github.com/Carlobks/Morg-laws/blob/main/skills/sql-postgres/SKILL.md).

**Sem dados reais.** Nunca entram dados reais (nomes, documentos, identificadores de pessoas) em testes, exemplos ou commits. O porquê: o que entra num repositório público não sai mais. A lista negra e o detector de dados pessoais, que recusam o commit, estão na parte 08 e no procedimento P4, e o teste pronto é [`test_dados_pessoais.py`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes/test_dados_pessoais.py).

**Sem segredos.** Nunca se lê um `.env` nem outros segredos, nunca se roda `curl | sh` e o agente nunca muda as próprias permissões. O porquê: um segredo lido vai para o contexto e pode sair num commit. Skill: [`auditoria-de-seguranca`](https://github.com/Carlobks/Morg-laws/blob/main/skills/auditoria-de-seguranca/SKILL.md), e o livro manda tirar do alcance do agente o que ele não deve usar (pp. 164–165).

**Só o próprio trabalho.** Nunca se commita o trabalho de outra sessão ou de outra pessoa que esteja na mesma pasta. O porquê: um commit de tudo leva o trabalho de outra sessão. Skill: [`orquestrando-sessoes`](https://github.com/Carlobks/Morg-laws/blob/main/skills/orquestrando-sessoes/SKILL.md). Ver a parte 05 (P17) e a parte 06 (P19).

## O índice das skills

O `AGENTS.md` traz uma tabela de nove situações, cada uma com a skill que se abre. As skills abrem pelo nome, estejam onde estiverem instaladas.

| Situação | Skill | O que ela faz |
|---|---|---|
| Escrever ou mudar um `CLAUDE.md`, um `AGENTS.md` ou uma skill | `escrevendo-regras-de-agente` | Diz onde cada coisa vai, a forma curta com o motivo e quando um texto vira barreira |
| Projeto novo, pedido grande ou mudança sem limites | `comecando-um-projeto`, `pondo-o-plano-a-prova` | A primeira conduz o começo do projeto; a segunda interroga o dono até o plano poder ser executado |
| Dividir trabalho entre sessões ou agentes | `orquestrando-sessoes` | Escolhe entre sessão nova e sub-agente, pede a leitura independente e organiza várias sessões na mesma pasta |
| Compactar a conversa, parar ou retomar | `passando-o-trabalho` | Guarda o estado num handoff, o commita e conduz a retomada |
| Commitar ou fechar um ciclo | `git-e-commits` | Commit por caminho, mensagem com o porquê, hooks que não se pulam e changelog por fragmento |
| Escrever ou partir código, corrigir um bug, testar | `codigo-legivel`, `testes-e-provas` | A primeira fixa a forma do código; a segunda diz como provar que funciona |
| Criar, redesenhar ou rever uma tela | `desenhando-telas` | Decide o que mostrar, quantas abas e ações cabem, cor, contraste e movimento |
| Fazer push de código | `auditoria-de-seguranca` | Revisa segredos, bibliotecas e rotas antes de enviar, com achados e cobertura em vez de uma nota |
| O projeto usa Postgres, Supabase, Next.js ou React | `sql-postgres`, `supabase`, `nextjs-react` | Cada uma traz as armadilhas da sua tecnologia que só aparecem em produção |

A linha de uma skill que você não instalou sai do seu `AGENTS.md`, ou só o nome dela, onde a linha tiver mais de uma. Esta tabela é só um mapa para você achar a skill certa. A fonte de cada skill está na seção “Fontes” do próprio arquivo dela.

## As regras do próprio repositório

O `AGENTS.md` fecha com cinco regras que valem só para o Morg-laws, e que vale a pena imitar se o seu repositório também for público.

**Público.** Nunca se escrevem nomes de pessoas ou de empresas, e-mails, identificadores de serviços, caminhos de máquina ou dados reais. O porquê é o da regra “Sem dados reais”: o que entra num repositório público não sai mais. A barreira é a lista negra do `pre-commit`, na parte 08.

**Toda fonte entra no `FONTES.md`.** Cada fonte citada tem ali a data em que foi lida e o que ela sustenta, e um teste do CI confere o formato. Livros entram como resumo com palavras próprias e com a página, nunca como texto copiado. A regra está no início do [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md).

**Pesquisa que outra sessão vai reler vai para `pesquisas/`.** Fica lá com o índice, em um arquivo por pesquisa, para não ter de ser refeita, e o CI confere as pesquisas e as fontes delas. O formato está em [`pesquisas/README.md`](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/README.md).

**Nada de terceiros copiado.** Escreve-se com estrutura própria, e a inspiração se cita no `FONTES.md`, na seção [“Inspirações (nada copiado)”](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#inspirações-nada-copiado).

**Escrita em português do Brasil.** Um teste do repositório recusa as formas de Portugal nos textos, como neste manual. A regra está no [`AGENTS.md`](https://github.com/Carlobks/Morg-laws/blob/main/AGENTS.md).
