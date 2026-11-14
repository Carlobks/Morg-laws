---
name: comecando-um-projeto
description: Conduz o primeiro contato com um projeto, novo ou que já existe, em rondas de perguntas sobre o que ele é, para quem, o que faz e não faz, as restrições e a arquitetura, e deixa escritos o documento do projeto, o AGENTS.md, o primeiro plano e as ADR. Usar ao começar um projeto do zero, ao abrir pela primeira vez um projeto com código e sem documentos, ou quando o dono cola a mensagem inicial do Morg-laws. Não usar para um pedido ou mudança num projeto que já tem esses documentos (é a pondo-o-plano-a-prova), para dividir o trabalho entre sessões (é a orquestrando-sessoes) nem para mudar as regras de um AGENTS.md que já existe (é a escrevendo-regras-de-agente).
---

# Começando um projeto

Um projeto sem documentos obriga cada sessão a adivinhar o que ele é, e cada palpite errado custa uma volta de retrabalho. Esta skill faz as perguntas uma vez, em rondas curtas, e deixa as respostas escritas no projeto, para a sessão seguinte ler em vez de adivinhar.

## 1. Quando usar e o que deixa

Use no primeiro contato com um projeto: pasta vazia, repositório com código e sem documentos, ou um projeto antigo que vai adotar o Morg-laws. Não use dentro de um projeto que já tem esses documentos: um pedido ou uma mudança lá é da `pondo-o-plano-a-prova`.

| Skill | Pergunta a que responde | Quantas vezes por projeto |
|---|---|---|
| `comecando-um-projeto` | O que é este projeto e como ele se organiza? | Uma (ou ao adotar o Morg-laws num projeto antigo) |
| `pondo-o-plano-a-prova` | Este pedido ou mudança está claro o bastante? | Em cada pedido grande ou mudança |
| `orquestrando-sessoes` | Como divido o trabalho entre sessões? | Quando o trabalho é grande |
| `escrevendo-regras-de-agente` | Como escrevo ou mudo uma regra? | Quando uma regra nasce ou muda |

Esta skill **não repete** o método de perguntar: as regras das rondas (até 4 perguntas, opções com a recomendada, explicar o termo) e o oráculo estão na `pondo-o-plano-a-prova`. Na ronda do primeiro plano, quem pergunta é ela.

## 2. Projeto novo ou projeto que já existe

**Projeto novo:** as rondas 1 a 5 vêm antes de qualquer arquivo. Na ronda 5 proponha opções com a recomendada; as ADR nascem «proposta» e passam a «aceita» com o «sim» do dono.

**Projeto que já existe, com código e sem documentos:**
- pergunte só o que o código não diz (o porquê, para quem, o que não faz) e mostre o resto como «o que encontrei», para o dono confirmar;
- escreva a arquitetura **como está**. As escolhas já feitas viram ADR com o estado «aceita (registrada depois, AAAA-MM-DD)», com o contexto que o dono lembrar. Nunca invente um porquê: o agente cria um motivo plausível para o que não sabe;
- não mude código;
- um arquivo de destino da seção 4 que já existe (`AGENTS.md`, `CLAUDE.md`, `docs/README.md`, uma ADR…) **nunca se sobrescreve**: mostre a diferença e junte com o «sim». As ADR novas continuam a numeração que já houver;
- a Regra n.º 1 sai do histórico do projeto (o incidente mais caro), perguntada ao dono;
- a ronda 2 encolhe: ofereça só a última pergunta («o que faria você parar?») e, para a peça que o dono quer trocar ou construir, a busca de «Procurar o que já existe»; ele pode recusar as duas.

## 3. As rondas

Cada ronda fecha com um resumo curto que o dono confirma antes da seguinte. **Nada se escreve no projeto antes da ronda 7, fora o `docs/projeto.md` de quem desiste na ronda 2, com o «sim» do dono, e commitado por caminho.** Quem já decidiu começar pode dispensar as quatro perguntas da ronda 2: não insista, guarde no resumo da ronda «ronda dispensada pelo dono, AAAA-MM-DD», que vai para «Por que começar» na ronda 7, e siga. A busca continua, a menos que ele a dispense também.

| Ronda | O que se pergunta |
|---|---|
| 0. Ler | Projeto que já existe: o README, os manifestos de dependências, a árvore, os testes, o CI e o `git log`; o que achou vai ao dono como «o que encontrei». Veja também que barreiras já existem (hooks em `.claude/hooks/` e `.githooks/`, testes, CI), para o mapa da seção 4. Projeto novo: só a pasta. |
| 1. O que é e para quem | O que o projeto é numa frase, sem jargão; quem usa, em que situação, e o que essa pessoa já fez, de fato, para resolver isso (o que aconteceu, não o que acha). O texto do dono guarda-se como ele escreveu. |
| 2. Vale a pena começar? | Quatro perguntas, nesta ordem: «Você conhece algo pronto que já resolva isso, ou que dê para adaptar?»; «Quanto tempo você aceita gastar nisso antes de ver se serve?»; «Imagine que, daqui a três meses, deu errado: por quê?» (os motivos viram restrições na ronda 4); «O que faria você parar, e até quando dá para ver isso?». Com as respostas, faça a busca de «Procurar o que já existe» e mostre a tabela. Fecha com a decisão do dono, escrita no resumo da ronda (vai para «Por que começar»): seguir, encolher, adaptar o que já existe ou desistir. Desistir encerra a skill: só se escreve o `docs/projeto.md`, se ele quiser guardar o motivo. |
| 3. O que faz e não faz | A primeira versão: o que entra, o que fica de fora, e por quê. |
| 4. Restrições | Prazo, custo, onde roda, quem mantém, dados pessoais, o que não tem volta. |
| 5. Arquitetura | Pilha, banco, onde se publica, e o porquê de cada escolha; se a ronda 2 escolheu adaptar, parta do candidato escolhido. Cada escolha grande (seção 5) vira ADR proposta. |
| 6. Regras | O perigo mais caro do projeto (a Regra n.º 1 do molde), com o título em maiúsculas e o motivo; o que pede o «sim»; o banco de produção. |
| 7. Confirmar e escrever | A lista dos arquivos a escrever e um resumo de cada; com o «sim», escrevem-se e commitam-se por caminho. Inclui o esqueleto do plano, `docs/planos/0001-<assunto>.md`, só com a F1, «as barreiras do mapa» (seção 4). |
| 8. Primeiro plano | Pela `pondo-o-plano-a-prova`, com o oráculo; preenche o esqueleto escrito na ronda 7 (molde `assets/molde-plano.md`). |

## 4. O que se escreve

As cópias estão em `assets/`, na pasta desta skill, ao lado deste `SKILL.md` (no Claude Code, `${CLAUDE_SKILL_DIR}/assets/`; no Codex a variável não se substitui). Leia-as com o Read e escreva no projeto os arquivos com os **nomes verdadeiros**. Nenhuma cópia se chama `AGENTS.md` nem `CLAUDE.md`: com esse nome, a ferramenta a carregaria sozinha como regra da sessão.

| Arquivo no projeto | Cópia na skill | Notas |
|---|---|---|
| `docs/projeto.md` | `assets/molde-projeto.md` | Seções na ordem: O que é; Para quem; Por que começar; O que já existe; O que faz; O que não faz; Restrições; Arquitetura (cada peça com o porquê e o link para a ADR); Palavras do dono (o texto original); Perguntas em aberto. |
| `docs/README.md` | — | Uma tabela, sem molde: o índice de cada `.md` de `docs/`, com o `docs/projeto.md`. O `AGENTS.md` cita este índice. |
| `AGENTS.md` | `assets/molde-AGENTS.md` | A Regra n.º 1 preenchida na ronda 6; o resto como está. |
| `CLAUDE.md` | `assets/molde-CLAUDE.md` | Só no Claude Code: a linha `@AGENTS.md`. |
| `docs/regras-e-barreiras.md` | `assets/molde-regras-e-barreiras.md` | O `AGENTS.md` cita-o. Preenche-se como diz o quadro abaixo. |
| `docs/planos/0001-<assunto>.md` | `assets/molde-plano.md` | Esqueleto na ronda 7, só com a F1 «as barreiras do mapa»; a ronda 8 o preenche, com o oráculo dentro de «Prova». |
| `docs/decisoes/0001-<decisao>.md`, … | `assets/molde-adr.md` | Uma por escolha grande. |

**O mapa das barreiras num projeto novo.** O molde do mapa cita hooks, testes e portões que esta skill não instala; copiado como está, ele diria que existem barreiras que não existem. Preencha-o assim:
- **linha cuja barreira existe no projeto** (vista na ronda 0): fica como no molde;
- **linha cuja barreira não está instalada:** a coluna «Barreira» passa a `por fazer (F1)` (seguida de `; texto` quando o molde já dizia que uma parte é texto). A coluna «Onde» diz em palavras o que falta e onde se faz, por exemplo «instalar a guarda do git (passo a passo em [modelos/README.md](https://github.com/Carlobks/Morg-laws/blob/main/modelos/README.md#como-instalar)); fase F1 de `docs/planos/0001-<assunto>.md`». **Não ponha entre crases um caminho que ainda não existe**: o teste do molde confere que cada caminho entre crases no mapa existe. O do plano já existe, porque o esqueleto se escreve na ronda 7, antes do mapa;
- **linhas só de texto** (DECISÃO É DO DONO, SEM ESCRITA NO BANCO): ficam como no molde;
- **a Regra n.º 1** preenche-se **igual** no `AGENTS.md` e no mapa: o mesmo título em maiúsculas nos dois, a barreira (`por fazer (F1)`, se ainda não existe) e o «Onde» em palavras.

**A F1 do primeiro plano**, «as barreiras do mapa»: instalar as que o dono quiser, pelo [passo a passo dos moldes](https://github.com/Carlobks/Morg-laws/blob/main/modelos/README.md#como-instalar), e passar a `texto`, com o motivo, as que ele não quiser. O texto da F1 diz que, ao copiar o [teste do mapa](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes/test_regras.py) dos moldes, se troca o `PLANO` para esse arquivo no bloco «Ajuste ao projeto» do próprio teste, e que, ao marcar a F1 como feita, se atualiza o mapa: é o que o teste passa então a exigir.

## 5. Escolhas grandes viram ADR

Uma escolha grande é a que mexe na estrutura, nas características não funcionais, nas dependências, nas interfaces ou nas técnicas de construção. Exemplos: a linguagem, o banco, onde roda, a forma de login. A biblioteca de datas não é.

Escreva uma ADR por escolha, em `docs/decisoes/`, com o contexto, a decisão e o porquê. Sem porquê, a escolha vai para «Perguntas em aberto» do `docs/projeto.md`; o porquê nunca se inventa.

## 6. Mensagem inicial

O dono cola uma destas mensagens para abrir a skill. O corpo depois do prefixo é o mesmo nas duas ferramentas; só o prefixo muda.

No Claude Code:

```text
/comecando-um-projeto Quero começar (ou organizar) este projeto com você. Antes de escrever código, me faça as perguntas em rondas, confirme comigo cada resposta e deixe escritos o documento do projeto, o AGENTS.md, o primeiro plano e as decisões de arquitetura.
```

No Codex:

```text
$comecando-um-projeto Quero começar (ou organizar) este projeto com você. Antes de escrever código, me faça as perguntas em rondas, confirme comigo cada resposta e deixe escritos o documento do projeto, o AGENTS.md, o primeiro plano e as decisões de arquitetura.
```

## 7. O que entregar no fim

- a lista dos arquivos escritos, e os commits (por caminho);
- as linhas do mapa que ficaram `por fazer (F1)`, com o que falta para cada uma;
- as perguntas em aberto, com quem responde e até quando;
- a decisão da ronda 2 e a tabela do que já existe.

## 8. Procurar o que já existe

Antes de construir, procure o que já resolve o problema, inteiro ou em parte: o agente acelera a direção que lhe dão e, se ninguém disser que há um caminho mais curto, pode seguir pelo mais longo. Procure **sem baixar, instalar nem rodar nada** do que achar, e só com o que é gratuito.

1. Escreva em duas ou três linhas o problema e os termos de busca, a partir das rondas 1 e 2.
2. Procure na busca de repositórios do GitHub (com `pushed:>=` de um ano para trás, `archived:false` e `license:`), no registro de pacotes da pilha (`npm search`; o deps.dev para os outros), na lista «awesome» do tema e, na web, nos produtos e serviços prontos.
3. Para cada candidato, leia na página dele: a data do último commit e da última versão; as issues abertas e se alguém responde; quantas pessoas fazem metade do trabalho; a nota do OpenSSF Scorecard, quando houver; a licença, pelo nome curto (`MIT`, `Apache-2.0`, `GPL-3.0`). O que a página não mostrar fica «não conferido» (a página de contribuidores do GitHub, por exemplo, monta o gráfico no navegador e, lida sem JavaScript, vem vazia).
4. Separe em três: serve como está; serve com adaptação (uma cópia própria ou um módulo por fora, e quem mantém); não serve, e por quê.
5. Mostre ao dono a tabela e a recomendação, e guarde no resumo da ronda o que se procurou, onde, em que data e o veredito de cada candidato, com o porquê: vai para «O que já existe» do `docs/projeto.md` quando ele se escrever (na ronda 7, ou na ronda 2 se o dono desistir).

Sem acesso à rede, diga isso ao dono e peça os nomes que ele conhece. **Nunca invente um candidato**, uma data ou uma licença: o que não se leu fica «não conferido».

**Só o dono decide:** adotar, adaptar ou construir; se a licença serve ao uso que ele vai dar (sobretudo a GPL, se ele for distribuir o programa, e a AGPL, que pesa mesmo só num serviço na internet); se aceita manter uma cópia própria; se o problema é o diferencial dele ou algo comum, que se usa pronto.

Quem já decidiu começar e dispensou as perguntas da ronda 2 não dispensou esta busca: ela continua, porque custa ao dono só ler a tabela, a menos que ele a dispense também.

## Fontes

Ver [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#antes-de-começar-um-projeto): as perguntas que decidem se um projeto vale a pena começar e como se procura o que já existe; [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#entrega-de-regras-a-agentes): como cada ferramenta carrega as regras e as skills; [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#livros-e-autores): o livro de onde vêm partir das palavras de quem pede, o arquivo de regras no primeiro dia, os documentos curtos numa pasta e a solução pronta antes de construir; e [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#testes-e-decisões): o registro das decisões de arquitetura, de Michael Nygard.
