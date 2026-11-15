# Antes de começar um projeto: vale a pena? já existe?

Data: 2026-11-14.

## Pergunta

Com agentes de código, começar um projeto ficou barato; ver qual **não** vale a pena começar continua difícil. Que
perguntas, tiradas de livros, artigos e publicações, decidem se um projeto deve começar (seguir, encolher, desistir ou
adaptar algo que já existe)? E como um agente procura, no início, o que já existe (código aberto, pacote, produto
pronto) e julga se serve? A resposta serve a um pedido do autor do Morg-laws (2026-11-13) e ao lugar natural dele, a skill
`comecando-um-projeto`.

## Fontes

Lidas em 2026-11-14 com o `WebFetch` (um modelo pequeno resume cada página; as frases curtas e os números vêm desse
resumo) e o livro pela página impressa. Cada link tem a sua entrada no `FONTES.md`.

**(a) As perguntas antes de começar**

- **O catecismo de Heilmeier (DARPA)** — https://www.darpa.mil/about/heilmeier-catechism — oito perguntas que George
  Heilmeier, diretor da DARPA de 1975 a 1977, fazia a quem propunha um programa: o que se quer fazer, sem jargão; como
  se faz hoje e onde isso esbarra; o que é novo e por que daria certo; quem se importa e que diferença faz; os riscos;
  o custo; o prazo; e as provas do meio e do fim para saber se deu certo. A página não dá a data em que ele as criou.
- **Os quatro riscos, de Marty Cagan** (SVPG, 2017-12-04) — https://www.svpg.com/four-big-risks/ — antes de construir,
  se enfrentam quatro riscos: valor (alguém vai querer usar ou comprar?), uso (a pessoa consegue usar?), viabilidade
  técnica (dá para construir com o que se tem?) e viabilidade do negócio (serve às vendas, aos contratos, ao jurídico,
  à marca?). Cada um tem um dono no time.
- **Working Backwards, da Amazon** (Werner Vogels, 2006-11-01) — https://www.allthingsdistributed.com/2006/11/working_backwards.html —
  antes de construir se escreve, nesta ordem, o comunicado de imprensa do produto, as perguntas frequentes, a experiência
  de quem usa e o manual. O motivo dado é a clareza e a visão comum do que se vai construir. A página não diz que o
  comunicado serve para matar a ideia; isso só aparece em resumos de terceiros, não conferidos.
- **O apetite do Shape Up (Basecamp)** — https://basecamp.com/shapeup/1.2-chapter-03 — o capítulo «Set Boundaries»
  inverte a estimativa: em vez de partir do desenho e chegar a um prazo, se fixa primeiro quanto tempo o problema
  merece (um lote pequeno de uma ou duas semanas, ou um grande de seis) e o desenho encolhe para caber. Prazo fixo,
  escopo variável.
- **O pre-mortem, de Gary Klein** (Harvard Business Review, setembro de 2007) —
  https://hbr.org/2007/09/performing-a-project-premortem — o time imagina que o projeto já fracassou e lista os
  motivos plausíveis; a técnica torna seguro dizer as dúvidas que, no planejamento, ninguém diz. Só a introdução se
  abriu (o resto é pago).
- **Critérios de desistência, de Annie Duke** (Wharton, 2023-05-30) — https://knowledge.wharton.upenn.edu/?p=28797 —
  um texto curto da autora de *Quit*: os «kill criteria» são as condições, escritas ao fixar a meta, que dão uma saída
  racional; o exemplo dela é seguir com um produto «a menos que» certas metas não se cumpram em dois meses. Ter uma
  meta já leva à escalada do compromisso (seguir quando já não serve). Que o melhor critério junta um estado e uma
  data aparece em resumos do livro, não no texto lido.
- **The Mom Test, de Rob Fitzpatrick** — https://www.momtestbook.com/ — a página do livro só diz o tema (conversas com
  clientes que dão dados verdadeiros, mesmo quando todos mentem por gentileza). As três regras conhecidas (falar da
  vida da pessoa, não da sua ideia; perguntar por fatos passados e concretos; ouvir mais do que falar) vêm só de
  resumos de terceiros: **secundária**, o livro não foi lido.
- **Fabio Akita — Competente o Suficiente** (o livro, pela página impressa): o agente acelera qualquer direção,
  inclusive a errada, e a pesquisa do primeiro dia teria poupado três de cinco dias (pp. 106–107); o agente seguiu
  pelo caminho mais longo porque ninguém disse que havia um mais curto (p. 67); entre o que faltou do lado de quem pede,
  saber a hora de largar um caminho e ver o que já existe pronto (p. 115); projeto sem usuário está morto, e os
  que ficaram de pé foram os que alguém usa (pp. 133–134).

**(b) Como se procura o que já existe**

- **GitHub — buscar repositórios** — https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories —
  os filtros que dizem se um projeto está vivo e serve: `pushed:>=AAAA-MM-DD`, `stars:>=n`, `license:apache-2.0`,
  `language:`, `topic:`, `archived:false`.
- **npm search** — https://docs.npmjs.com/cli/v11/commands/npm-search — procura no registro pelos metadados dos
  pacotes; `--json` e `--searchlimit` (20 por padrão).
- **deps.dev** — https://docs.deps.dev/ — o grafo de dependências de pacotes de Cargo, Go, Maven, npm, NuGet, PyPI e
  RubyGems, com os avisos de segurança do OSV, e uma API HTTP e gRPC. A página não fala de licenças nem do Scorecard.
- **Listas «awesome»** — https://github.com/sindresorhus/awesome — a lista das listas por tema. A página não diz o que
  uma lista precisa para entrar.
- **OpenSSF Scorecard** — https://scorecard.dev/ e https://github.com/ossf/scorecard — 18 verificações automáticas
  (entre elas Maintained, License, Security Policy, Code Review, Contributors, Vulnerabilities), cada uma de 0 a 10. Sem
  instalar nada, se lê em `scorecard.dev/viewer/?uri=github.com/<dono>/<repo>`, só para os projetos que a
  varredura semanal cobre. A verificação Maintained pergunta se o projeto tem ao menos 90 dias e atividade nesse
  período.
- **CHAOSS** — https://chaoss.community/kb/metric-time-to-first-response/ e
  https://chaoss.community/kb/metric-bus-factor/ — métricas de saúde de comunidade, projeto da Linux Foundation: o
  tempo até a primeira resposta a uma issue ou PR, e o «fator de ausência» (o antigo «bus factor»: quantas pessoas
  fazem metade das contribuições).
- **choosealicense.com** — https://choosealicense.com/licenses/ — compara as licenças por permissões, condições e
  limitações: as permissivas (MIT, Apache-2.0) pedem manter os avisos; a GPL-3.0 pede publicar o código da versão
  distribuída sob a mesma licença; a AGPL-3.0 conta o uso em rede como distribuição.
- **Lista de licenças SPDX** (versão 3.29.0, 2026-09-16) — https://spdx.org/licenses/ — o identificador curto e
  padronizado de cada licença (`MIT`, `Apache-2.0`), que se usa para nomear a licença sem ambiguidade.
- **Martin Fowler — Utility vs Strategic Dichotomy** (2010, revisto em 2016) —
  https://martinfowler.com/bliki/UtilityVsStrategicDichotomy.html — o que não diferencia (a folha de pagamento, no
  exemplo) se compra pronto e se adapta o processo ao pacote; só o que diferencia se constrói. A maior parte dos
  projetos é do primeiro tipo, e uma função pode mudar de tipo com o tempo.
- **O livro, de novo:** pedir ao agente que pesquise os programas de código aberto mais usados e escolher uma base bem
  cuidada para um fork, com a origem e a licença de cada acervo documentadas (p. 218); manter cópia própria é dívida,
  mas trocar de estratégia no meio saiu barato com o agente (p. 142).

## O que se mediu

**No Morg-laws** (`main` = `38c1b84`, árvore limpa, em 2026-11-14):

| O quê | Resultado |
|---|---|
| O que a `comecando-um-projeto` já diz | a ronda 4 (Arquitetura) traz meia frase: antes de construir, ver se já existe solução pronta (`SKILL.md:44`). Nenhuma ronda pergunta se o projeto vale a pena. |
| O que a bíblia já tirou do livro | `biblia-akita/pedidos-e-sessoes.md:13`: procurar no primeiro dia se já existe solução pronta (pp. 67, 106–107, 218), «onde aplicar: `comecando-um-projeto`». A p. 115 (quando abandonar e procurar o que já existe) não é citada nessa linha. |
| Soma das descrições das 13 skills | 7.366 caracteres, contra `TETO_DA_SOMA = 7600` (`tests/test_formato_das_skills.py:36`): folga de 234. A da `comecando-um-projeto` tem 667, a maior. |
| Linhas de um `SKILL.md` | limite de 500 (`LIMITE_DE_LINHAS`); a `comecando-um-projeto` tem 101. |
| Arquivos em `assets/` | o `tests/test_comecando_um_projeto.py` exige que cada arquivo de `assets/` seja cópia, byte a byte, de um molde de `modelos/documentos/`; um arquivo a mais reprova. |

**A lista curta** (para uma ronda com o dono; cada pergunta com a fonte e o que a resposta decide):

| # | Pergunta | De onde vem | O que a resposta decide |
|---|---|---|---|
| 1 | O que você quer fazer, numa frase sem jargão, e para quem? | Heilmeier (1); o comunicado do Working Backwards | se não cabe numa frase, **encolher** ou esclarecer antes de seguir |
| 2 | Como isso se resolve hoje, e já existe algo pronto que resolva ou se adapte? | Heilmeier (2); Fowler; o livro (pp. 67, 106–107, 218) | **adaptar** ou usar pronto, em vez de construir |
| 3 | Quem vai usar, e o que essa pessoa já fez de concreto para resolver isso? | Cagan (valor); o livro (pp. 133–134); o Mom Test (secundária) | sem ninguém que use, **desistir** ou rever para quem é |
| 4 | Quanto tempo você aceita gastar nisso, antes de saber o custo? | o apetite do Shape Up; Heilmeier (6, 7) | **encolher** o escopo para caber no apetite |
| 5 | Imagine que deu errado daqui a três meses: por quê? | o pre-mortem de Klein; Heilmeier (5); Cagan (viabilidade técnica e do negócio) | os motivos viram restrições do projeto, ou **desistir** se um não tem saída |
| 6 | O que faria você parar, e até quando se vê isso? | Annie Duke (critérios de desistência); Heilmeier (8) | se escreve o critério de parada; sem ele, **seguir** não tem fim marcado |

**O passo a passo do «já existe»**, que um agente consegue seguir:

1. Escrever em duas ou três linhas o problema e os termos de busca, a partir da resposta à pergunta 1.
2. Procurar: a busca do GitHub com `pushed:>=` (um ano para trás), `archived:false` e `license:`; o registro de pacotes
   da pilha (`npm search`, deps.dev para os outros ecossistemas); a lista «awesome» do tema; e os produtos e serviços
   prontos (uma busca na web).
3. Para cada candidato, ler sem baixar nem rodar nada: a data do último commit e da última versão, as issues abertas
   e se alguém responde (CHAOSS: tempo até a primeira resposta), quantas pessoas fazem metade do trabalho (fator de
   ausência), o Scorecard pelo visualizador quando existir, e a licença pelo identificador SPDX e pelo
   choosealicense.
4. Separar: pronto para usar como está; serve com adaptação (fork ou módulo por fora, com o custo de manter, p. 142);
   não serve, com o motivo.
5. Levar ao dono a tabela dos candidatos e a recomendação. Fica escrito no projeto o que se procurou e por que não
   serviu, para a sessão seguinte não refazer a busca.

**O que o agente vê sozinho:** datas de commit e de versão, issues e respostas, número de contribuidores, a licença
declarada, o Scorecard publicado, as dependências. **O que só o dono decide:** se a licença serve ao uso que ele vai
dar (sobretudo copyleft e AGPL num serviço em rede), se o problema é dele de verdade (utilidade ou diferencial, em
Fowler), quanto tempo aceita gastar, e se aceita manter um fork.

## O que não se verificou

- O livro de Annie Duke (*Quit*), o de Rob Fitzpatrick (*The Mom Test*) e o de Colin Bryar e Bill Carr (*Working
  Backwards*) **não foram lidos**; o que se diz deles vem das páginas citadas acima. Do Mom Test, as três regras vêm
  só de resumos de terceiros.
- Do artigo de Klein na HBR só se abriu a introdução (o resto pede assinatura).
- Que o critério de parada junte um estado e uma data é da forma do livro *Quit* segundo resumos; o texto lido da
  autora não diz isso.
- A página do Scorecard não confirma que o deps.dev mostra o Scorecard, nem documenta o endereço da API para os
  resultados (só o do selo).
- O que a lista «awesome» exige de uma lista não se leu (o guia de contribuição não abriu na página).
- O `tests/test_formato_das_skills.py` não rodou nesta máquina (falta o PyYAML no Python do sistema); a soma foi
  medida lendo a linha `description:` de cada `SKILL.md`, que é de uma linha só em todas.
- Ninguém mediu quais perguntas pesam mais num projeto feito por uma pessoa com agentes; o que a Conclusão diz disso
  é leitura das fontes.

## Conclusão

As fontes concordam no essencial: antes de construir, saber o que se quer numa frase, quem vai usar, como se resolve
hoje, quanto se aceita gastar, como pode dar errado e quando parar. As seis perguntas da tabela cabem em duas rondas de
até quatro.

Para uma pessoa com agentes, três pesam mais, pelo que as fontes dizem e não por medição: a 2 (já existe?), porque o
agente acelera a direção que lhe dão e não propõe o caminho mais curto sem que alguém o diga (o livro, pp. 67 e 107);
a 3 (quem vai usar?), porque o livro conta que só ficaram de pé os projetos com usuário (pp. 133–134); e a 6 (quando
parar?), porque começar ficou barato, e a escalada do compromisso de Duke vem justamente de já ter uma meta.

No projeto que já existe, as fontes sustentam a pergunta 6 e o «já existe» peça por peça: Duke escreve sobre seguir ou
largar o que já está em curso, e os três casos do livro (pp. 67, 107, 142) são de trocar uma parte de um projeto já
começado por algo pronto. Sobre adotar regras num projeto antigo, nenhuma fonte diz nada.
