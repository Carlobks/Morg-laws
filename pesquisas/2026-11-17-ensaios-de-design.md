# Ensaios às cegas das skills de design

Data: 2026-11-17.

## Pergunta

Que skills de design para agentes existem, quais valem um ensaio, e qual delas faz as melhores telas quando o mesmo
modelo recebe o mesmo pedido? A `desenhando-telas` do Morg-laws ajuda ou atrapalha? Telas de sistema (ERP, painéis)
e sites pedem as mesmas regras? E que falhas de acessibilidade se repetem nas melhores páginas, mesmo quando a pessoa
gosta delas? Este resumo existe para as skills `desenhando-telas`, `desenhando-sites` e `cuidando-da-acessibilidade`
terem onde apontar quando dizem «nos ensaios às cegas de novembro de 2026».

## Fontes

O trabalho correu de 2026-11-16 a 2026-11-17, em quatro partes: a busca e a triagem das skills, o banco de ensaio, os
ensaios com o julgamento às cegas, e a régua de acessibilidade nas páginas que ganharam. Os documentos de cada parte, as
páginas geradas, as gravações e a chave das letras ficam privados: têm o texto do dono do projeto, que julgou, e
caminhos da máquina. O que segue é um resumo com palavras próprias.

**As skills ensaiadas**, cada uma baixada inteira como texto (o `SKILL.md` e as `references/`) num commit fixo, sem
executar nada. As licenças vêm do `LICENSE` de cada repositório, aberto nesse commit quando se escreveu o plano das
skills. Cada link tem a sua entrada no `FONTES.md`.

- **`emilkowalski/skills`** — https://github.com/emilkowalski/skills/tree/64eb3deb — commit `64eb3deb`
  (2026-11-15), MIT, Emil Kowalski. Três skills: `emil-design-eng`, `apple-design` e `choreograph`.
- **`interface-design`** — https://github.com/Dammyjay93/interface-design/tree/2f9be320 — commit `2f9be320`
  (2026-06-20), MIT, Damola Akinleye.
- **`make-interfaces-feel-better`** — https://github.com/jakubkrehel/make-interfaces-feel-better/tree/1a2aa969 —
  commit `1a2aa969` (2026-11-16), MIT, Jakub Krehel.
- **`motion-design`** — https://github.com/LottieFiles/motion-design-skill/tree/f9a8a041 — commit `f9a8a041`
  (2026-05-18), MIT, LottieFiles.
- **`frontend-design`** — https://github.com/anthropics/skills/tree/e4bb5d96/skills/frontend-design — commit
  `e4bb5d96` (2026-11-16), Apache-2.0 (no `LICENSE.txt` da pasta; a raiz do repositório não declara licença).
- **`ui-animation`** — https://github.com/mblode/agent-skills/tree/7df4b7ed/skills/ui-animation — commit `7df4b7ed`
  (2026-11-14), MIT, Matthew Blode.
- **A `desenhando-telas` do próprio Morg-laws**, no commit `bce0c78a` (2026-11-14), sem a pasta `evals/`.

**A régua:** as Web Interface Guidelines da Vercel —
https://github.com/vercel-labs/web-interface-guidelines/blob/434b7f91364665f2f733b310ec54809bf8f37937/AGENTS.md —
commit `434b7f91` (2026-10-05), MIT, Vercel Labs.

**Lidas na busca e deixadas de fora** (lidas na `main` em 2026-11-16, sem commit fixo):

- **`impeccable`** — https://github.com/pbakaus/impeccable — Apache-2.0.
- **taste-skill** — https://github.com/Leonxlnx/taste-skill — MIT.
- **O catálogo skills.sh** — https://skills.sh/ — onde a busca começou, pela tabela de instalações e pela categoria
  de design.

## O que se mediu

**1. A busca: 9 skills úteis, 2 recusadas por segurança.**

- Cada skill lida foi partida em pontos, um por instrução que muda o que o agente faz. Cada ponto foi marcado como
  concreto ou vago, e como novo, igual ou contrário em relação à `desenhando-telas`. Uma tabela de valores contou
  como um ponto.
- Antes da contagem, três barreiras: segurança (o que a skill manda executar), licença (só MIT ou Apache-2.0) e
  leitura (se dá para ler inteira).
- **Recusadas na barreira de segurança:** a `impeccable` manda rodar, no início de cada sessão, um lançador que baixa
  um binário que não se pode ler e põe hooks nas configurações do agente; a taste-skill declara um hook que roda
  `node` ao fim de cada sessão e traz 153 scripts. Ficaram fora mesmo como fonte.
- **As nove que passaram deram todas «muito útil»**, de 21 a 86 pontos novos e concretos cada uma. Nenhuma repetia
  outra em 80 % ou mais; a mais parecida (a `ui-animation`) tinha 38 % dos pontos novos iguais aos de uma skill do Emil
  Kowalski.
- **O critério não separou:** a `desenhando-telas` quase não falava de movimento, de gestos nem de sites, e qualquer
  skill razoável dessas áreas passava o limite. A escolha veio dos casos que cada uma cobre e da parecença entre elas,
  não da nota.
- Antes dos ensaios já se via um desvio: quatro skills punham as animações de interface abaixo de 300 ms e não
  animavam o que se usa o dia todo; a `desenhando-telas` aceitava até 500 ms.

**2. O banco de ensaio: os 5 casos e o isolamento.**

| Caso | O que se pediu | Os pontos difíceis de propósito |
|---|---|---|
| C1 Kanban | 5 colunas e 42 cartões; arrastar entre colunas e dentro delas, abrir o cartão, mover pelo teclado | um título de 123 letras e outro de 3, cartões sem responsável, prazos vencidos, cartões bloqueados |
| C2 Ficha de funcionário | uma pessoa, 12 documentos, 10 eventos, 3 formações; editar a ficha | um nome de 47 letras, documentos a vencer, um vencido |
| C3 Painel de entrada | 6 indicadores em 3 períodos, gráficos semanais e mensais, avisos, atividade recente | a semana corrente pela metade, valores com centavos, sem biblioteca de gráficos |
| C4 Site de empresa de serviços | serviços, números, etapas, obras, depoimentos, perguntas, formulário de orçamento | sem fotos; 4 campos obrigatórios |
| C5 Site de psicóloga | áreas, etapas, formatos, valores, perguntas, formulário | sem fotos; a pergunta sobre crise fácil de achar; sem depoimentos de pacientes |

- **O mesmo para todas:** o mesmo pedido, palavra por palavra; dados inventados; a saída num único `index.html`,
  sem build nem servidor; cores, letra, espaço e movimento livres; «a primeira versão é a que conta», sem segunda
  rodada. Nos ensaios com skill, uma só linha a mais, no topo, mandava carregar a skill.
- **O mesmo modelo:** Claude Opus 5.5, esforço `medium`, em todos.
- **Uma sessão nova por ensaio, numa pasta nova, fora de qualquer projeto**, sem `CLAUDE.md` nem `AGENTS.md`
  acima dela. Um `settings.json` na pasta recusava as skills e as ferramentas de design que vêm com o Claude Code, a
  busca na web, os sub-agentes, os conectores e a leitura das pastas de projeto. Testado antes: com ele, as ferramentas
  recusadas somem da lista e uma skill de design embutida devolve «bloqueada»; a skill da pasta carrega. Os nomes das
  skills bloqueadas continuam na lista que o modelo vê.
- **A prova depois de cada ensaio:** um script lia o transcript e conferia que só a skill do ensaio foi carregada,
  que nenhum `SKILL.md` foi lido à mão e que nenhuma ferramenta tocou em pasta proibida.
- **A gravação:** um Chromium sem janela seguia o mesmo roteiro em cada página do caso e saíam capturas (computador e
  celular), um vídeo do movimento e os valores lidos da página (por exemplo, os cartões de cada coluna antes e depois
  do arrasto).
- **O julgamento às cegas:** as versões de cada caso receberam letras sorteadas e a chave ficou guardada à parte. O
  dono viu todas lado a lado, ordenou-as e disse por quê; a chave só foi aberta depois dos 5 casos.
- **A skill da Vercel não concorreu:** ela só revê e busca as regras na internet a cada uso. Virou a régua.

**3. O resultado: a nota de cada skill.**

A nota de um caso vai de 1 (a primeira) a 0 (a última): (n − posição) / (n − 1). No C1 só houve 1.ª e 2.ª.

| Skill | C1 | C2 | C3 | C4 | C5 | Média de C2 a C5 |
|---|---|---|---|---|---|---|
| `motion-design` | — | — | — | 2.ª (0,88) | **1.ª** (1,00) | 0,94 (só sites) |
| `interface-design` | sem posição | **1.ª** (1,00) | 3.ª (0,67) | — | — | 0,83 (só ERP) |
| `apple-design` | **1.ª** | — | — | **1.ª** (1,00) | 4.ª (0,57) | 0,79 |
| `make-interfaces-feel-better` | sem posição | 2.ª (0,80) | 4.ª (0,50) | 3.ª (0,75) | 2.ª (0,86) | 0,73 |
| `ui-animation` | sem posição | 5.ª (0,20) | 2.ª (0,83) | 4.ª (0,63) | 3.ª (0,71) | 0,59 |
| `emil-design-eng` | sem posição | 4.ª (0,40) | **1.ª** (1,00) | 8.ª (0,13) | 7.ª (0,14) | 0,42 |
| sem skill | 2.ª | 3.ª (0,60) | 5.ª (0,33) | 6.ª (0,38) | 6.ª (0,29) | 0,40 |
| `choreograph` | — | — | 7.ª (0,00) | 5.ª (0,50) | — | 0,25 |
| `frontend-design` | — | — | — | 9.ª (0,00) | 5.ª (0,43) | 0,21 |
| `desenhando-telas` | sem posição | 6.ª, última (0,00) | 6.ª (0,17) | 7.ª (0,25) | 8.ª, última (0,00) | **0,10** |

- **A `desenhando-telas` ficou abaixo do «sem skill» nos quatro casos ordenados:** ter a skill deu telas piores do
  que não ter nenhuma.
- **A mais constante foi a `make-interfaces-feel-better`:** na metade de cima nos quatro casos, em ERP e em sites.
- **ERP e sites ganham com skills diferentes:** no ERP, a `interface-design`, a `apple-design` (no Kanban) e a
  `emil-design-eng` (só no painel); nos sites, a `motion-design` e a `apple-design`. Por isso viraram duas skills, uma
  de telas de sistema e outra de sites.
- **As mais instaladas decepcionaram:** a `emil-design-eng` foi a melhor só no painel e das últimas nos sites; a
  `frontend-design` foi a última no site da empresa.

**4. O que o julgamento ensinou, caso a caso** (resumo do que o dono escreveu, com palavras nossas):

- **Kanban:** todas tinham atalhos de teclado, mas só uma dizia como começar a usá-los; atalho que não aparece é
  como se não existisse. As sete deixaram cada coluna rolar sozinha, o que agradou. No tema escuro, cor demais
  confunde; cor forte só onde importa. O painel lateral do cartão foi onde houve mais problemas: separar com linhas
  finas e fundos de tom diferente, mostrar os estados em fila para mover o cartão, e o teclado tem de funcionar
  também ali. O movimento ao mover cartões pesou mais do que o resto. Um cartão bloqueado se marca com pouca cor e um
  ícone. Listras decorativas, não. **O celular falhou nas sete.**
- **Ficha de funcionário:** a melhor entrada tem o nome em destaque, espaço de sobra e uma só coisa realçada ao lado.
  O que precisa de atenção ganha um bloco próprio, com a cor certa. Ícones diferentes por tipo de documento; cartões
  alinhados na mesma altura, para se ler por categoria; um cartão que sobra sozinho e estica a página é erro. **Todas
  falharam pelo mesmo motivo:** informação demais e hierarquia de menos. O certo era mostrar um resumo e abrir o resto
  ao clicar, ou usar abas.
- **Painel de entrada:** indicadores numa grade de 3 × 2, agrupados por tema, e não numa linha que ocupa a largura
  toda. Nenhum cartão alto e estreito que quebre a página; a atividade recente vai embaixo, na horizontal. O que
  precisa de atenção numa lateral que acompanha a rolagem, com animação ao entrar e ao acompanhar. Gráficos que
  realçam o item sob o mouse e apagam o resto. Atalhos à vista, nunca num canto. Sem espaço vazio sem motivo. A ordem
  das animações de entrada bateu com a ordem geral.
- **Sites (os dois):** o dono não gostou de nenhum no geral. Faltou uma capa forte; faltaram textos que surgem com a
  rolagem ao longo da página toda, que foi o que mais pesou; sobrou texto e espaço vazio entre as seções. Valeram
  pontos: destacar um dos serviços, o formulário de orçamento em duas colunas (poucas informações de um lado, os
  campos do outro), o cabeçalho translúcido com o fundo desfocado, cada ideia num cartão curto com um ícone, e a ação
  principal numa lateral que acompanha a rolagem.
- **Dois choques com as regras lidas:** o movimento com a rolagem na página toda vai contra a `frontend-design` (um
  só momento de movimento por página) e a `ui-animation` (revelar ao rolar só em poucos lugares); o vidro translúcido
  ia contra a `desenhando-telas`. A saída foi separar: nos sites valem os dois, no ERP o movimento é curto e as
  superfícies são sólidas.

**5. A régua: as falhas que se repetem.**

A régua rodou nas duas primeiras páginas de cada caso (10 páginas), lidas só pela letra, antes de abrir a chave.
Entraram 38 regras das diretrizes da Vercel que se provam numa página parada: com Tab de verdade, com
`prefers-reduced-motion` emulado, com um envio de formulário vazio, em 1440, 390 e 320 px de largura.

| Regra | Falhou em | O que se viu |
|---|:-:|---|
| `scroll-margin-top` nas âncoras, com cabeçalho fixo | 4 de 4 sites | o título da seção pode ficar sob o cabeçalho |
| Alvo de toque ≥ 44 px no celular | 9 de 10 | abas, botões de ação e atalhos com 28 a 39 px de altura |
| Contraste de texto ≥ 4,5:1 | 9 de 10 | texto secundário (códigos, datas, legendas) de 11 a 13 px em cinzas entre 3,2:1 e 4,4:1 |
| `touch-action: manipulation` | 8 de 10 | quase ninguém declara |
| `<meta name="theme-color">` | 6 de 10 | as 6 telas de sistema; os 4 sites tinham |
| `text-wrap: balance` nos títulos | 6 de 10 | |
| Animar propriedades de layout | 5 de 10 | o acordeão das perguntas anima a altura; o link de pular para o conteúdo anima `top` |
| `aria-hidden` em SVG decorativo | 5 de 10 | logotipos, setas e ilustrações sem o atributo |
| `tabular-nums` nos números | 5 de 10 | telefones, anos, preços e horas de listas; nos indicadores e nas tabelas estava certo |
| Estados vazio e de erro previstos | 4 de 10 | painéis e Kanban só com o caminho feliz |
| `spellcheck` desligado no e-mail | 3 de 4 com e-mail | |
| Alvo ≥ 24 px | 3 de 10 | links de telefone com 21 a 23 px; botões de 20 px de largura |

- **Nenhuma das 10 falhou** em: foco visível em cada alvo, `outline: none` sem substituto, tudo alcançável pelo
  teclado, foco escondido sob elemento fixo, zoom bloqueado, `prefers-reduced-motion`, `transition: all`, `<title>`, nome acessível em botões só de
  ícone, hierarquia de títulos, reticências e aspas curvas. Isso o modelo já faz sozinho; a skill não precisa
  repetir.
- **A régua não segue o gosto.** Cruzando a ordem do julgamento com as notas, a primeira do painel (a
  `emil-design-eng`) teve 7 falhas de regras obrigatórias e a segunda (a `ui-animation`) 3; a primeira da ficha (a
  `interface-design`) teve 9, empatada com a mais alta das 10. A menor foi 3; a maior, 9.

## O que não se verificou

- **Um ensaio por skill e por caso.** A mesma skill pode sair melhor ou pior em outra tentativa: uma ou duas posições
  de diferença não provam nada. Só as diferenças grandes e repetidas valem (a `desenhando-telas` no fim; a
  `make-interfaces-feel-better` sempre em cima).
- **Um só juiz**, que é também quem vai usar as skills. O gosto dele está nas regras que saírem daqui.
- **Os pedidos dos sites pesaram em todas:** uma página só e nenhuma foto. A estrutura igual e a capa fraca vieram em
  parte do pedido, não das skills.
- **No Kanban** só houve 1.ª e 2.ª; o resto ficou em comentários.
- **Não se ensaiou em celular de verdade:** o celular foi emulado no Chromium, a 390 px.
- **A régua mediu o contraste pelo WCAG 2, aproximado;** a Vercel prefere o APCA, que não se implementou. Ela não
  distingue um estado de transição de um estado final. Menus móveis dos sites e o painel de crise da psicóloga não
  foram abertos.
- **A régua leu só 10 páginas**, as duas melhores de cada caso; as outras não se mediram.
- **A busca contou os pontos uma vez, uma pessoa só.** Das 9 classificadas, algumas não foram lidas inteiras na busca
  (as referências da `ui-animation` e da `motion-design`); nos ensaios foram inteiras.
- **As licenças** não foram reabertas para este resumo: vêm da leitura feita no commit fixo para o plano das skills.
  É uma leitura, não um parecer jurídico.
- **O custo de cada ensaio** não entra aqui.

## Conclusão

A `desenhando-telas` como estava piorava as telas: ficou abaixo de não usar skill nenhuma. As vencedoras de ERP não
são as dos sites, por isso o trabalho segue em três skills: uma de telas de sistema (com base na
`interface-design`, na `apple-design`, na `make-interfaces-feel-better` e na `emil-design-eng`), uma de sites (com
base na `motion-design`, na `apple-design`, na `make-interfaces-feel-better`, na `frontend-design` e na receita de
rolagem da `ui-animation`) e uma de acessibilidade, feita da parte da `desenhando-telas` que se mede. O que mais pesou
no julgamento foi a hierarquia (resumir e abrir ao clicar), os atalhos à vista, o equilíbrio da grade e, nos sites, o
movimento com a rolagem e uma capa forte. A régua mostra que as páginas preferidas também falham em alvos de toque,
contraste e âncoras sob o cabeçalho fixo: a skill de acessibilidade deve tratar disso com limites que se medem, sem
proibir o que o gosto pediu.
