# O ciclo de uma mudança

Uma mudança no seu projeto passa por cinco passos, sempre na mesma ordem: o plano e o seu “sim”, o commit por caminho, o hook que recusa e a correção, o bug que traz o teste, e o push, que só sai com um novo “sim”. Esta parte conta cada um com um caso real. Os hooks e as regras em si ficam para as partes seguintes.

## P18 · O plano e o “sim”

### Na prática

Antes de mexer em vários arquivos, peça o plano e leia-o. Só diga “sim” depois de lê-lo.

1. Peça ao agente um plano: o que muda, em quais arquivos, em que ordem e como cada passo se prova (P7).
2. Leia o plano e ponha-o à prova com as perguntas incômodas (P9): o que ele deixa de fora, o que acontece se parar no meio.
3. Quando houver uma decisão que é sua, o agente a pergunta, explicada, com a opção recomendada marcada. Você responde, ou escreve “R”, que aceita a recomendação.
4. Só então diga “sim”. Um “sim” vale para aquele plano: um plano novo pede outro.

Um exemplo, reescrito: o plano deste próprio manual, da primeira à segunda versão.

```
Plano, versão 1: o formato, a ferramenta do PDF, os procedimentos em páginas duplas, as fontes.
Auditoria a frio: dezenove achados.
Conferência: confere os achados e afina quatro correções.
Ronda ao dono: oito decisões, cada uma com a recomendação marcada.
Resposta: “Tudo no recomendado.”
Plano, versão 2: aplica os achados e a resposta; as decisões sem o porquê escrito vão a outra ronda.
```

O que costuma dar errado:

- Dizer “sim” a um plano que você só passou os olhos.
- Aceitar uma decisão sua sem a explicação: o agente decidiu pelo que era mais fácil para ele.
- Tratar um “sim” antigo como licença para o próximo plano.

### Por quê e fonte

Um plano ruim, a IA o executa com perfeição e mais rápido (livro *Competente o Suficiente*, de Fabio Akita, pp. 105–106). Por isso o livro manda pedir primeiro o plano, revê-lo e só então avançar, acompanhando enquanto roda (pp. 45, 78, 122). O plano em papel é barato de corrigir; o código depois dele, não.

O `AGENTS.md` traz as duas regras do começo: “plano antes de mexer” (uma mudança com vários arquivos começa por um plano e pelo “sim” do dono do projeto) e “decisão é do dono” (a decisão no meio do trabalho vai ao dono, explicada, com a recomendada marcada). O porquê escrito lá: cada palpite errado custa uma volta de retrabalho, e não se decide sozinho o que é do dono.

Onde vive no Morg-laws: o `AGENTS.md` (o núcleo) e a skill `pondo-o-plano-a-prova`, que traz as perguntas do P9.

## P19 · Commitar por caminho

### Na prática

Um commit é uma mudança com um propósito. Duas mudanças independentes são dois commits. Commitar não precisa de pedido: terminou um pedaço que funciona, commite.

```
git status --short -uall
git add -- <arquivo1> <arquivo2>
git commit -F msg -- <arquivo1> <arquivo2>
```

- Use sempre o `-uall`: sem ele, uma pasta nova aparece como uma linha só e os arquivos dentro dela ficam fora do commit.
- Nunca `git add -A` nem `git add .`: eles levam o que não é seu (P17).
- A mensagem vai num arquivo (aqui, `msg`), com `-F`. Título de até 72 caracteres, com o tipo e a área, sem ponto final; uma linha em branco; e um corpo que diz o que mudou e por quê. A mensagem é tão pública quanto o código: sem dados reais.

Um exemplo real, a mensagem de um commit do próprio repositório, abreviada:

```
test(skills): o teste dos destinos olha a tabela e o dos prefixos olha os rótulos

O teste dos sete destinos procurava cada nome no texto inteiro da skill, e por isso
continuava verde sem a linha do AGENTS.md na tabela da seção 4. Agora procura o destino
na primeira coluna da tabela dessa seção.
[...]
Dois testes novos provam os casos: a tabela sem a linha do AGENTS.md e os rótulos trocados.
```

O que costuma dar errado:

- Uma mensagem que diz só o quê (“ajusta o teste”) e não porquê.
- Um arquivo preparado com a versão errada: o commit por caminho grava o que está no disco.
- Dois assuntos num commit só, que depois ninguém desfaz.

### Por quê e fonte

O commit é o único lugar onde o trabalho fica a salvo: num projeto real, 109 arquivos viveram só no disco de uma máquina até alguém notar ([o que se mediu no projeto de origem](https://github.com/Carlobks/Morg-laws/blob/main/projetos/erp-de-servicos/o-que-se-mediu.md)). O Git é a rede, com commits pequenos e o envio na mão de uma pessoa (livro *Competente o Suficiente*, de Fabio Akita, pp. 230, 382), e as entregas pequenas e frequentes andam junto com a estabilidade (pp. 286–288, 291–292). O porquê escrito na mensagem é o que a pessoa que ler o histórico não tem como adivinhar. O `git add` é o que põe um arquivo novo no git: sem ele, o commit por caminho recusa. Num arquivo que o git já acompanha, o commit por caminho grava o que está no disco, e o hook do git vê só esses caminhos.

O commit por caminho existe por causa da pasta compartilhada: o aviso de arquivos por commitar conta arquivos, e não donos. E uma mudança que quem usa nota leva um fragmento próprio no changelog, em vez de um arquivo único que colide quando várias sessões escrevem ao mesmo tempo (o texto do GitLab, na seção [“Changelog e versões” do `FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#changelog-e-versões)).

Onde vive no Morg-laws: a skill `git-e-commits`, seções “Como commitar” e “Changelog por fragmento”. A regra “commit sem pedido, push com o sim” está no `AGENTS.md`.

## P20 · Quando o hook recusa

### Na prática

Um hook é um programa que roda antes do commit (`pre-commit`) ou confere a mensagem (`commit-msg`), e pode recusar. Quando recusar:

1. Leia a saída inteira: ela diz o que falhou e onde.
2. Corrija a causa: o erro de tipo, o teste, a linha comprida, o dado que não podia estar ali.
3. Adicione os arquivos corrigidos ao índice e commite de novo. O commit recusado não existiu; não há o que desfazer.
4. Se o hook estiver errado, corrija o hook, num commit próprio. Não o contorne.

Nunca use `--no-verify`, nunca desligue o hook e nunca cite na mensagem a opção que o pula.

Um exemplo, reescrito: o relatório de uma série de correções.

```
O que deu errado: três commits da série ficaram com um portão vermelho no meio.
O portão mede o índice do git, e eu rodava os portões antes de adicionar os arquivos
ao índice: cada corrida media o commit anterior. Descobri na corrida do terceiro,
que reprovou, e commitei assim mesmo, porque o hook do commit não roda esse teste.
Corrigi num commit novo, sem amend.
Daí em diante: adicionar os caminhos ao índice, rodar os portões, só então commitar.
```

Aqui o hook não recusou: o teste vermelho era de um portão que se roda à mão. Com um portão vermelho também não se commita.

O que costuma dar errado:

- Rodar os portões antes de adicionar os arquivos ao índice.
- Commitar com um portão vermelho porque “o hook não pegou”.
- Refazer um commit já publicado em vez de fazer um novo.

### Por quê e fonte

Pulado, o hook deixa passar o erro: ele é a rede, e uma rede com um buraco só se nota quando algo cai. O livro de Fabio Akita manda passar cada commit pela mesma bateria: estilo, dependências, análise estática e testes (pp. 408–409). Hook recusou, se corrige a causa; o texto que só aconselha não é cumprido, e o que tem de valer sempre vira hook ou teste.

O exemplo mostra outra lição: o portão que você roda à mão e o hook do commit podem conferir coisas diferentes. Rodar os dois, na ordem certa, evita depender de sorte.

O histórico já publicado não se reescreve para esconder o erro: isso muda os hashes de todos. A saída é um commit novo.

Onde vive no Morg-laws: a seção “Os hooks são a rede” da skill `git-e-commits`, a seção “Quando algo dá errado” da mesma skill e o `AGENTS.md` (“os hooks são a rede”).

## P21 · Bug traz teste

### Na prática

Um `fix` traz o teste que pega o bug, visto falhando antes da correção. O passo a passo:

1. Reproduza o bug num teste novo e rode-o: ele tem de falhar, pelo motivo certo.
2. Corrija o código e rode o teste de novo: ele passa.
3. Commite o teste e a correção juntos, com o porquê na mensagem.
4. Quando não há como testar, escreva no corpo do commit a linha `Sem-teste: <motivo concreto>`. Um hook pode exigi-la.

Um exemplo real: um `fix` do próprio repositório, com o nome do arquivo trocado por uma descrição.

```
fix(hooks): o pre-commit recusa quando o teste do catálogo falta no disco

Sem o arquivo do teste do catálogo, o unittest acha 0 testes, e em Python 3.11 ou
anterior sai com 0: o commit passava sem a barreira. Agora o passo confere o arquivo
antes e recusa com uma mensagem.
```

O commit levou a correção no hook e um teste novo: ele apaga o arquivo do disco, prepara uma linha limpa e confere que o commit é recusado, com a mensagem certa.

O que costuma dar errado:

- Escrever o teste depois da correção e nunca o ver falhar: ele pode passar por qualquer motivo.
- Corrigir sem teste e sem o `Sem-teste:`: o mesmo bug volta.
- Mudar um teste que existia só para ele passar.

### Por quê e fonte

Um teste que nunca falhou não prova nada. O livro de Fabio Akita manda prender cada bug com um teste e só juntar com tudo verde (pp. 80–81), e lembra que um programa vazio tem de reprovar: os controles negativos (pp. 423–424). Num projeto real, 86 de 199 commits de correção não tinham teste antes dessa regra ([o que se mediu no projeto de origem](https://github.com/Carlobks/Morg-laws/blob/main/projetos/erp-de-servicos/o-que-se-mediu.md)).

Onde vive no Morg-laws: a seção “Correção sem teste tem de dizer porquê” da skill `git-e-commits` e a seção “Bug tem teste” da skill `testes-e-provas`. O `AGENTS.md` traz a regra “bug traz teste”.

## P22 · Push só com o “sim”

### Na prática

Commitar não precisa de pedido; o push precisa, a cada vez. Um “sim” de antes não vale para o push seguinte.

Antes de pedir o “sim”, confira, no fim da fase:

1. o diff dos commits novos, contra o que o pedido mandava;
2. a suíte inteira, com a saída;
3. o scanner de segredos (o `gitleaks`) sobre os commits por enviar;
4. a lista negra sobre os arquivos novos;
5. a lista dos arquivos de todos os commits por enviar.

Peça ao agente cada uma, com a saída. O `pre-push` roda o gitleaks de novo no envio, mas aí o “sim” já foi dado.

Só então pergunte. Um exemplo, reescrito, o fim de uma fase:

```
Conferido, sem reauditoria: o diff, a suíte, o catálogo, o gitleaks e a lista negra.
Posso fazer o push dos commits da fase?
➡️ sim · ainda não
```

O que costuma dar errado:

- Pedir o “sim” sem ter conferido o diff e a suíte.
- Tratar o “sim” da fase anterior como valendo para esta.
- Fazer o push porque “era só um commit pequeno”.

### Por quê e fonte

O push publica no momento em que sai: o que entra num repositório público não sai mais, e um segredo publicado se roda ou se revoga, nunca se esconde. Por isso o “sim” é do dono, a cada vez. O livro de Fabio Akita manda ver a lista de arquivos de todos os commits por enviar antes do push (p. 386) e lembra que o envio é feito na mão de uma pessoa (pp. 230, 382).

A conferência é de uma sessão que não escreveu o trabalho, e não da filha que o escreveu: quem escreveu lê o que quis dizer (P15). A orquestradora lê só o resultado dela (P14).

Onde vive no Morg-laws: o `AGENTS.md`, regra “commit sem pedido, push com o sim”, e a seção “Quando commitar e quando pedir” da skill `git-e-commits`.
