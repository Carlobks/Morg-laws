---
name: desenhando-telas
description: Guia o desenho de telas de sistema (ERP, Kanban, painel) — que tela existe, hierarquia, resumir e abrir ao clicar, KPIs, atalhos, celular e movimento. Usar ao criar, redesenhar ou rever essas telas. Não usar para sites (é a desenhando-sites) nem para acessibilidade (é a cuidando-da-acessibilidade).
---

# Desenhando telas

**Os dados são o protagonista, e a hierarquia decide o que se vê primeiro.** Uma tela de sistema é aberta dezenas de
vezes por dia por quem trabalha nela: o que importa é achar a coisa certa num relance, agir sem procurar o botão e não
esperar pela interface. A skill descreve **papéis** («superfície de cartão», «texto de apoio»), não classes, para valer
em qualquer stack.

Onde ler o resto:

- `references/kanban-ficha-painel.md`: a receita de cada tipo de tela (o quadro, a ficha, o painel), por papéis.
- `references/movimento-no-sistema.md`: as tabelas de duração e curva, a mola e o arrasto, com a fonte de cada número.
- `references/tetos-e-fontes.md`: os tetos medidos (abas, ação primária) e de onde vem cada regra.
- `references/exemplo-tailwind.md`: um exemplo dos papéis em Tailwind, num tema escuro.

As regras novas desta versão vêm dos ensaios às cegas de novembro de 2026, em que a mesma tela de sistema foi pedida
a agentes com e sem skills de design e uma pessoa ordenou as páginas sem saber qual era qual (o resumo está na
pesquisa [`2026-11-17-ensaios-de-design.md`](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-17-ensaios-de-design.md)).
A versão anterior desta skill ficou abaixo de não usar skill nenhuma: falava de que telas existem e quase nada de como
ficam. Esta fala das duas coisas.

**O que mora em outra skill:** contraste, cor e daltonismo, alvos de toque, hover, foco, movimento reduzido e letra em
`rem` se medem com a `cuidando-da-acessibilidade`; sites e landing pages são da `desenhando-sites`; provar no navegador
que a tela funciona é da `testes-e-provas`. Esta skill decide a cara da tela e termina mandando passar a de
acessibilidade.

## 1. Antes de desenhar

Responda por escrito, em poucas linhas, antes do primeiro componente:

1. **Quem é a pessoa e o que ela veio fazer.** Não «usuários»: quem abre esta tela, em que momento do dia, e o verbo
   da tarefa (aprovar, achar o atrasado, mover para o próximo estado). O verbo decide o que vem primeiro.
2. **O tom, em palavras que dizem algo.** «Denso como uma mesa de operações», «calmo como um caderno»; nunca «limpo e
   moderno», que qualquer agente diz e não decide nada.
3. **O ponto focal.** A única coisa que tem de ganhar o olhar, dita antes de começar, e como ela ganha (tamanho, peso,
   posição, o espaço em volta).
4. **As seis perguntas da tela:**
   - Que complexidade o sistema absorve, e qual fica para a pessoa?
   - Qual é o **único** número que responde à pergunta desta tela?
   - Qual é a **única** ação principal?
   - O que se esconde, e com que **frequência medida** é usado?
   - O que se agrupa?
   - Quem vê? O que se desativa e o que se explica?
5. **As suposições de volume:** quantos registros, o nome mais longo, itens por mês. Uma tela desenhada para 10 linhas
   quebra com 300.

## 2. Decidir a tela

**Arquitetura de informação.**

- **Uma página-índice ou carrega dados ou não existe.** Com uma só filha não precisa de índice; se só repete nomes,
  apague. Um índice legítimo mostra contagens, estado ou pendências e deixa começar a tarefa ali mesmo.
- **O tipo de página decide o layout:** panorama (ler o geral), detalhe (ler uma entidade), transacional (editar).
  Largura total para tabelas; largura fixa para texto e formulários, que não se esticam.
- **Tetos medidos:** abas fixas no máximo 4; uma só ação primária; acima do teto de abas, um menu de «mais», nunca um
  carrossel. Os números e as fontes estão em `references/tetos-e-fontes.md`.
- **A navegação nomeia a tarefa, não a tabela** («Pagamentos», não «Eventos de cobrança»), e **as abas levam
  contagens** («Fornecedores (3) · Contratos (12)»).
- **A moldura do sistema não se repete no módulo:** a navegação de topo é uma só.
- **A densidade é do público.** Quem usa a tela o dia inteiro quer mais dados por tela. «Na dúvida, tira» vale para a
  moldura (bordas, ornamentos); dados só se cortam com medição.

**Permissões à vista.** A ação sem permissão fica desativada, com o motivo em texto visível (um `title` não aparece
num botão desativado nem numa tela de toque). A navegação sem permissão, ou vazia, fica visível e explica por quê.

**Botões.**

- Três níveis: **fantasma** (ação solta, com borda), **ferramenta** (age no contêiner onde está, sem borda, com
  rótulo escrito) e **chip** (um valor escolhido).
- **Botão faz, link vai.** Rótulo = verbo + resultado, em uma a três palavras («Gerar contrato», «Marcar como pago»),
  nunca «OK» ou «Confirmar» sozinhos. **Arquivar** (volta atrás) não é **Excluir** (some de vez).
- **Uma principal**, de uma cor que não é a dos valores na mesma tela (se o dinheiro é verde, a ação não é verde).
  Secundária neutra com borda; destrutiva na cor de erro; desativada com o motivo.
- A principal fica **onde a tarefa acaba** (no fim do modal, à direita). O destrutivo pede confirmação e, se for
  irreversível, a pessoa escreve o identificador antes.

**Componentes.**

- **Reutilize antes de criar:** o botão, o diálogo e o menu do projeto antes de um novo; um primitivo pronto e
  acessível antes de escrever o comportamento à mão. Uma variante nova é uma inconsistência nova.
- **Editar fica no cabeçalho do bloco que edita**; um campo editável novo entra no formulário que já existe.
- **Modais** usam portal, prendem o foco, fecham com Esc e avisam antes de descartar alterações.
- **Um interruptor grava na hora.** O que espera por «Salvar» usa botões de opção ou caixa de seleção, e os dois tipos
  não se misturam na mesma tela.
- **Camadas** com uma escala fixa (conteúdo, barra fixa, ícones globais, modal, sobre-modal, confirmação); antes de
  subir o `z-index`, veja se a camada está num portal.

## 3. Menos informação, com hierarquia

Foi o defeito que apareceu em todas as fichas dos ensaios: tudo à vista, nada em destaque. Mostrar tudo não é ser
completo; é deixar a pessoa fazer o trabalho de escolher.

- **Cartões-resumo que abrem ao clicar.** A ficha e o painel mostram, em cada bloco, só o essencial (3 a 5 linhas é o
  nosso ponto de partida, a calibrar) e abrem o resto ao clicar: num painel lateral, numa gaveta ou numa aba com
  contagem («Anexos · 9»). O que se esconde **sempre mostra um resumo**, nunca uma seta muda.
- **Corte pela frequência medida, não pela importância percebida.** Se a pessoa comum abre mais da metade dos blocos
  recolhidos, recolher custa mais do que poupa.
- **Sinal de risco nunca se esconde:** vencido, em falta, bloqueado, por pagar.
- **A entrada (o topo da ficha):** o nome em tamanho grande, ar suficiente em volta e **uma só coisa em destaque à
  direita** (o estado, o saldo, o próximo prazo). Duas coisas em destaque são nenhuma.
- **O que precisa de atenção tem um bloco próprio**, perto do topo, com a cor do estado e um ícone diferente para cada
  tipo de pendência. É o bloco que a pessoa procura primeiro; não o dilua entre os outros.
- **Um estado de alerta diz-se com pouca cor e um ícone**: um ponto ou uma borda fina na cor do estado e o ícone ao
  lado do texto, não o cartão inteiro pintado de vermelho.
- **Um número protagonista** por tela ou por bloco, grande, com `tabular-nums`. O resto é apoio.
- **Letra:** a escala sai de uma razão (≈ 1,2 para telas densas, ≈ 1,25 para as comuns), não do olho. A hierarquia vem
  primeiro do peso e da cor, depois do tamanho: num tamanho só cabem três níveis (valor 600, rótulo 500, meta 400).
  Nada de pesos finos. O título de uma seção nunca é menor nem mais apagado do que o texto dentro dela.

## 4. Grade e equilíbrio

- **KPIs numa grade de 3 × 2, agrupados por categoria**, e não numa linha que ocupa a largura toda. A linha só serve
  quando os gráficos são o foco da tela e os números são apoio.
- **Cartões vizinhos com a mesma altura**, alinhados em grade: ao descer, a pessoa lê por categorias, linha a linha.
- **Nenhum cartão sobra sozinho a esticar a página.** Um bloco alto e estreito (uma lista longa numa coluna) parte o
  equilíbrio da tela. As listas longas (histórico, últimos movimentos) vão para baixo, na largura toda, com poucas
  linhas e um «ver tudo».
- **Sem espaço vazio sem razão**, no cabeçalho e dentro dos cartões. O cabeçalho usa a faixa de cima para o que ajuda
  a trabalhar: as teclas, o filtro ativo, a contagem. Um cartão meio vazio ao lado de um cheio pede outra grade.
- **Proximidade:** o espaço entre seções é pelo menos o dobro do maior espaço dentro delas. Separe primeiro por espaço;
  a linha vem depois.
- **Densidade decidida em px e mantida:** 12 a 16 px de padding é bancada de trabalho; 24 px é folheto. Escolha uma e
  repita-a em toda a tela.
- **Rótulo e valor:** numa coluna estreita (≈ 200 px) o rótulo vai por cima do valor; lado a lado só num contêiner
  mais largo (≈ 400 px).

## 5. A lateral que segue o scroll

O bloco do que precisa de atenção, ou a ação principal da tela, pode viver numa coluna lateral com
`position: sticky` que acompanha o scroll enquanto o resto do painel rola. Foi a peça mais elogiada nos ensaios do
painel. Ela pode ter **duas animações**:

- **A entrada ao abrir a tela**, uma vez, junto com o resto do painel (seção 9).
- **O movimento enquanto acompanha o scroll:** em vez de ficar colada seca, chega à nova posição com uma transição
  curta (≤ 300 ms, valor nosso, a calibrar) feita só com `transform`. Nunca atrasa a leitura, nunca cobre conteúdo, e
  com o movimento reduzido fica só o `position: sticky`, sem animação.

É **a única coisa da tela de sistema que se mexe com o scroll**. O conteúdo nunca espera pelo scroll para aparecer:
num produto que se rola dezenas de vezes por sessão, aparecer tarde lê-se como lentidão.

No celular a lateral deixa de ser lateral: vira um bloco no topo, recolhido, com o resumo («3 pendências») e a
contagem por tipo (valor nosso).

**A lateral de detalhe** (a que abre ao clicar num cartão do quadro ou numa linha da lista) foi onde mais se errou nos
ensaios. Ela se organiza por grupos, separados por linhas finas e por fundos de tom um pouco diferente; tem o «Mover
para» com os estados em fila (seção 6); e o teclado funciona dentro dela como no resto.

## 6. Teclado

Nos ensaios, todas as telas tinham atalhos e quase nenhuma dizia como começar a usá-los. Atalho que não aparece é
como se não existisse.

- **Uma legenda de teclas sempre à vista**, no cabeçalho ou no rodapé, nunca escondida num canto ou atrás de um «?».
  Ela diz **como começar** («Tab para entrar no quadro»), não só as teclas de dentro.
- **O modelo do teclado de mover**, que é o que funcionou: Tab entra no quadro; as setas andam entre os cartões;
  **espaço pega o cartão, as setas o movem, espaço o solta, Esc cancela** e devolve o cartão ao lugar. Diga com uma
  região viva o que aconteceu («Movido para Em revisão, posição 2»).
- **O teclado funciona também dentro das laterais e dos diálogos:** Tab percorre os campos e os botões deles, Esc fecha
  e devolve o foco ao cartão de onde veio.
- **«Mover para» com os estados em fila**, como alternativa ao arrastar: uma lista dos estados na ordem do fluxo, com o
  atual marcado, por clique e por teclado. É a alternativa que o celular usa (seção 8).
- Atalhos de navegação (números para trocar de vista, `/` para a busca) também entram na legenda.

## 7. Cor e superfícies no sistema

- **Superfícies sólidas são o padrão do sistema**, não uma proibição geral: o que passa por trás de um fundo
  translúcido apaga a hierarquia de uma tela cheia de dados. Transparência só no fundo atrás do modal e em estados.
- **Fronteira entre superfícies de pelo menos 1,2:1**, pelo fundo **ou** pela borda (no tema escuro, quase sempre pela
  borda). O erro é fundo fraco e borda fraca ao mesmo tempo, e borda semitransparente, que muda com o que está atrás.
- **Uma estratégia de profundidade, só ela:** bordas, ou sombras suaves, ou degraus de fundo. Não misture.
- **Orçamento de bordas:** borda no que se edita, nos contêineres de topo e no botão fantasma. Uma lista vive num só
  contêiner com divisórias, nunca uma caixa por item.
- **Distribuição ≈ 60/30/10:** uma superfície neutra dominante, um tom secundário e cerca de 10 % de acento. Uma cor de
  acento só; a cor comunica (estado, ação, identidade), e cor sem motivo é ruído.
- **No tema escuro, a cor é pouca e só onde importa.** No escuro qualquer cor ganha destaque: um quadro com uma cor por
  coluna, por etiqueta e por pessoa vira confusão. Neutros para a estrutura e cor forte só no estado e na ação.
- **Nada de listras, barras cinzentas nem padrões decorativos** no fundo ou nos cartões. Gradiente só se disser alguma
  coisa.
- **Ícones diferentes por tipo** (de documento, de pendência, de estado), do mesmo conjunto e do mesmo traço. O traço
  acompanha o peso do texto ao lado: 1,5 px ao lado de texto 400, 2 px ao lado de 500–600.
- **Números e palavras alinhados ao centro da linha** em filtros, etiquetas e abas com contagem; `tabular-nums` em todo
  número que se compara.
- Estado ou identidade, a cor como único sinal e o contraste se conferem na `cuidando-da-acessibilidade`.

## 8. Celular

Nos ensaios, nenhum quadro funcionou no celular. Uma tela de sistema que só funciona a 1440 px não está pronta.

- **O quadro abaixo de 768 px mostra uma coluna de cada vez**, com abas de estado no topo (cada uma com a contagem e
  pelo menos 44 px de altura) e o «Mover para» como ação do cartão em vez do arrastar (valor e forma nossos, a partir
  dos ensaios).
- **Cada coluna do quadro rola sozinha**, no computador e no celular; o cabeçalho da coluna fica parado.
- **A grade de 3 × 2 vira 2 × 3 ou uma coluna;** a lateral vira o bloco recolhido no topo (seção 5).
- **Todo alvo com pelo menos 44 px no toque.** Abas, ações dentro de cartões e botões só de ícone foram os que mais
  falharam; meça a caixa com a `cuidando-da-acessibilidade`.
- **Nada principal depende de hover:** no toque não há hover.
- Tabelas largas: as colunas de apoio saem primeiro, ou a linha vira um cartão; nunca a página inteira com scroll de
  lado.

## 9. Movimento no sistema

**A frequência decide se anima.** Os **atalhos** usados centenas de vezes por dia (abrir a paleta de comandos, trocar
de vista, navegar numa lista) não animam: animação ali deixa o sistema lento. **Mover um cartão anima, pelo mouse e
pelo teclado:** é a confirmação de que o cartão foi para onde a pessoa queria, e foi o movimento mais elogiado dos
ensaios. O que se usa poucas vezes (um modal, uma gaveta, a entrada do painel) tem animação normal.

- **Durações:** pressão 100–160 ms, tooltip 125–200 ms, menu 150–250 ms, modal e gaveta 200–500 ms. **A interface de
  sistema fica abaixo de 300 ms**; modais e gavetas são a exceção. As tabelas estão em
  `references/movimento-no-sistema.md`.
- **Curva de saída forte** (`cubic-bezier(0.23, 1, 0.32, 1)`) para entrar e responder; nunca `ease-in`, que atrasa o
  primeiro quadro, o momento em que a pessoa está olhando.
- **Nada cresce do zero:** começa em `scale(0.95)` com opacidade 0. O popover nasce do botão que o abriu; o modal fica
  centrado.
- **Pressão:** `scale(0.96)` ou `scale(0.97)` no `:active`, nunca abaixo de 0,95.
- **Mover cartões:**
  - o cartão segue o ponteiro 1:1 e respeita o ponto onde foi pego (não pula para o centro);
  - ao soltar, ele vai ao lugar e os vizinhos abrem e fecham o espaço com uma mola sem ressalto (amortecimento 1,0,
    resposta de 0,3 a 0,4 s), que parte da velocidade do gesto em vez de recomeçar do zero;
  - o vizinho que dá lugar se mexe junto, não depois;
  - pelo teclado, o cartão desliza para a posição nova com a mesma curva, curto.
- **Gráficos com destaque ao passar o mouse:** o elemento sob o ponteiro fica aceso e os outros se apagam um pouco;
  com o teclado, o mesmo no foco.
- **A entrada do painel conta.** Ao abrir, os blocos entram escalonados, 30–80 ms entre um e outro e o grupo inteiro
  abaixo de cerca de 300 ms, na ordem da importância. **Uma entrada por contêiner:** se o bloco entra, o que está dentro
  dele já está lá. Ninguém espera a animação para clicar.
- **Transição de página sem `transform`:** só opacidade e cor. Um `transform` num antepassado cria um novo contexto e
  quebra os elementos `fixed` e `sticky` (a lateral da seção 5) e o arrastar.
- **Só `transform` e `opacity`** nos elementos que se mexem, com as propriedades nomeadas na transição (nunca
  `transition: all`).
- **Com o movimento reduzido sobram a opacidade e a cor, ou nada** (os limites estão na `cuidando-da-acessibilidade`):
  o cartão aparece no lugar novo, a lateral fica só `sticky`, a entrada do painel é um esmaecer ou nada.
- **Uma animação se verifica pelo que pinta** (o valor resolvido ou os pixels entre quadros), não pela variável que a
  alimenta. Reveja o movimento em câmera lenta (10 % da velocidade, pelas ferramentas do navegador) antes de entregar.

## 10. Estados

Cada bloco de dados tem os quatro desenhados, não só o caminho feliz: **a carregar** (o esqueleto com a forma do
conteúdo, sem pular quando chega), **vazio** (o que significa e a ação para sair dele), **erro** (o que houve e o que
fazer, sem esvaziar o resto da tela) e **com dados**. Nos ensaios, 4 de 10 telas só tinham o caminho feliz.

Os controles têm os seus: normal, hover, pressionado, foco, desativado (com motivo) e, quando grava, «gravando» no
próprio controle.

## 11. Como trabalhar

1. **Escreva a seção 1** (pessoa, tarefa, tom, ponto focal, volume) e o plano da grade antes do código.
2. **Construa com os papéis e os tokens do projeto;** valor solto (`#fff`, `gray-200`, `px-4` repetido) é sinal de que
   falta um token ou um componente.
3. **Tire captura a 1440 px e a 390 px** quando houver navegador, e critique antes de mostrar: o ponto focal ganha?
   Algum cartão sobra? A lateral vira bloco no celular? A legenda de teclas aparece sem rolar?
4. **O teste da troca:** troque, de cabeça, a letra e o layout pelos mais comuns. Onde não mudaria nada, foi o padrão
   que decidiu, não você; volte a essa parte.
5. **O teste de semicerrar os olhos:** com a vista turva, a hierarquia ainda se lê e nada grita aos olhos.
6. **Reveja o movimento a 10 % da velocidade** e o teclado de ponta a ponta (entrar, mover, cancelar, abrir a lateral,
   sair dela).
7. **No fim, passe a `cuidando-da-acessibilidade`** e diga o que não se verificou.

**Beleza não é evidência.** Uma tela se valida com uma pessoa real ou com um número medido (uma captura lida, uma
caixa medida), nunca com um «parece limpo».

## 12. Precedência

**Se o projeto tem uma doutrina de design própria, ela vence onde divergir** desta skill: durações, a escala de
pressão, o interruptor de movimento, um padrão de fundo da marca. Esta skill preenche o que a doutrina não diz. Quando
as duas divergem, siga a do projeto e diga a divergência no relatório, para o dono decidir se a doutrina muda.

## 13. Segurança acima da estética

- Uma decisão de design nunca muda dados sozinha; a validação é no servidor, e o botão fica desativado enquanto a ação
  corre.
- **Sem dados reais** (nomes, documentos, contas bancárias) em exemplos, placeholders, demos ou testes.

## 14. Lista de verificação

- [ ] Pessoa, verbo, tom, ponto focal e suposições de volume escritos antes do código?
- [ ] Uma ação principal, distinguida pelo estilo, com verbo + resultado? Botão faz, link vai? Destrutivo com atrito?
- [ ] A página-índice carrega dados? O layout segue o tipo de página? Abas ≤ 4, com contagem?
- [ ] Permissões: ação desativada com motivo visível; navegação visível e explicada?
- [ ] Os blocos mostram um resumo e abrem o resto ao clicar? Nenhum sinal de risco escondido?
- [ ] A entrada tem o nome em destaque e uma só coisa à direita? O que precisa de atenção tem bloco próprio, com ícone
  por tipo?
- [ ] KPIs em grade 3 × 2 (ou 2 × 3 no celular), agrupados, e não numa linha só?
- [ ] Cartões vizinhos com a mesma altura? Nenhum cartão alto e estreito sozinho? Listas longas embaixo, na largura toda?
- [ ] Sem espaço vazio sem razão no cabeçalho e nos cartões? Espaço entre seções ≥ 2× o de dentro?
- [ ] A lateral `sticky` só anima com `transform`, ≤ 300 ms, e fica parada com o movimento reduzido? Vira bloco no
  celular?
- [ ] **A barra lateral de detalhe:** grupos separados por linhas finas e tons de fundo, «Mover para» com os estados em
  fila, teclado funcionando dentro dela e Esc devolvendo o foco?
- [ ] Legenda de teclas à vista ao carregar, dizendo como começar? Espaço, setas, espaço e Esc movem e cancelam?
- [ ] Superfícies sólidas? Fronteira ≥ 1,2:1? Uma estratégia de profundidade? Um acento só? Nenhum padrão decorativo?
- [ ] No escuro, cor só no estado e na ação? Ícones diferentes por tipo, com o traço do peso do texto?
- [ ] O quadro funciona a 390 px (uma coluna, abas com contagem, «Mover para»)? Cada coluna rola sozinha?
- [ ] Atalhos sem animação; mover cartão com animação curta; tudo abaixo de 300 ms fora modais e gavetas?
- [ ] Saída forte, nada de `ease-in`, nada de `scale(0)`, pressão entre 0,96 e 0,97?
- [ ] Entrada do painel escalonada 30–80 ms, uma por contêiner? Transição de página sem `transform`?
- [ ] Só `transform` e `opacity` animados, sem `transition: all`? Com o movimento reduzido sobram a opacidade e a cor?
- [ ] Estados a carregar, vazio e erro desenhados em cada bloco?
- [ ] Capturas a 1440 e a 390 px criticadas? Teste da troca e de semicerrar feitos?
- [ ] A `cuidando-da-acessibilidade` passou, e o que não se verificou está dito?

## Fontes

Cada regra com a sua fonte e o commit fixo está em `references/tetos-e-fontes.md`; as fontes, com o titular de cada
uma, em [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#interface-e-acessibilidade). Nada
foi copiado: as regras das skills de terceiros (`interface-design`, `apple-design`, `emil-design-eng`, `choreograph`,
`make-interfaces-feel-better`, todas MIT) estão escritas com palavras nossas. A página do livro *Competente o
Suficiente*, de Fabio Akita, que a skill usa em parte, está em
[`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#livros-e-autores).
