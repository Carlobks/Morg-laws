# Pedir

Como pedir o que você quer, de um jeito que o agente consiga entregar. São quatro passos: o molde do pedido, o oráculo que diz se ficou certo, o caso em que nada disso é preciso e a conversa de perguntas que põe um plano grande à prova antes de começar.

## P6 · As quatro partes de um pedido

### Na prática

Um pedido que o agente entrega bem diz quatro coisas: o que você quer, como (em linhas gerais), o que você não quer e como
vai saber que ficou certo.

O molde:

```
O que quero: <o resultado, numa frase>
Como: <o caminho em linhas gerais; se achar melhor outro, diga antes de começar>
O que não quero: <o que fica de fora, o que não se mexe>
Como vou saber que ficou certo: <o que eu consigo ver ou rodar>
```

Um exemplo preenchido, o pedido de um manual de uso:

```
O que quero: um manual de uso para quem está começando com agentes de código, que explique como instalar e como pedir.
Como: Markdown no repositório e um PDF gerado dele, com uma página para o que fazer e outra para o porquê. Se achar melhor
outro caminho, diga antes de começar.
O que não quero: nada copiado de livros ou de terceiros, nenhum dado pessoal, e nada publicado antes de eu dizer sim.
Como vou saber que ficou certo: os testes passam, o PDF compila e cada trecho tem a sua fonte.
```

O que costuma dar errado:

- A terceira parte fica em branco. É a que mais vale e a mais esquecida.
- O critério de pronto é “fica bom”. O agente não consegue conferir isso, e você também não.
- O pedido deixa de fora o que só você sabe: o combinado de ontem, o arquivo que não se mexe, o prazo.

### Por quê e fonte

O agente não adivinha o que ficou na sua cabeça. Cada parte que falta vira um palpite dele, e cada palpite errado custa
uma volta de retrabalho. A parte do que você não quer evita o erro mais caro, o de ele fazer a mais. A do critério de pronto
transforma “acho que está bom” em algo que se confere.

A mesma ideia aparece no guia de boas práticas do Claude Code, que pede ao agente um jeito de verificar o próprio trabalho
([boas práticas do Claude Code](https://code.claude.com/docs/en/best-practices)), e no livro *Competente o Suficiente*,
de Fabio Akita: o pedido importante não sai sem o que fica de fora e o critério de pronto (pp. 118, 120–121).

Onde vive no Morg-laws: a skill `pondo-o-plano-a-prova` pergunta, antes de um pedido grande começar, por cinco lacunas: três são o que você quer, o que fica de fora e como saber que ficou certo; as outras duas são o que não tem volta e quem decide.

## P7 · O oráculo

### Na prática

O oráculo é a conferência que você escreve antes de começar e que diz se o resultado está certo, sem dizer como se faz. O agente roda cada linha antes e depois da mudança e relata linha a linha.

O molde:

```
Oráculo
- Dado <a situação>, quando <a pessoa faz X>, então <o que ela vê ou o estado que fica>.
- Continua igual: <o que não se mexe>, conferido por <tela, comando, número>.
```

Um exemplo. O catálogo do projeto de origem descreve assim o fim de uma tarefa da equipe:

```
2. A tarefa tem um responsável e um estado, e o quadro mostra o que está parado.
3. Ao concluir, a tarefa passa à coluna das concluídas e, passado um tempo, ao histórico.
```

Do passo 3 sai este oráculo:

```
Oráculo
- Dado uma tarefa em andamento com responsável, quando a pessoa a conclui, então ela aparece na coluna das concluídas e deixa de aparecer entre as paradas.
- Continua igual: o responsável da tarefa, conferido na própria tarefa depois de concluída.
```

O que costuma dar errado:

- Escrever o mecanismo (“a função grava tal coluna”). Diga o que a pessoa vê.
- Esquecer o “Continua igual”. Ponha ao menos uma linha dele.
- Uma linha do “depois” que já passa antes da mudança. Ela não prova nada: volte e pergunte.

### Por quê e fonte

Sem oráculo, o “pronto” do agente é uma opinião. Com ele, cada linha vira uma conferência, e as duas espécies têm regras opostas. A linha do “depois” tem de falhar antes da mudança; se já passa, não prova nada sobre ela. A linha “Continua igual” tem de passar antes e depois; se já falha antes, o ponto de partida não é o que você descreveu. Se o resultado não cabe no oráculo, não se reescreve o oráculo para passar: o agente volta a você.

O oráculo julga o resultado, não o mecanismo. A skill conta que, no banco de provas do repositório, um oráculo que exigia um código de erro específico reprovou soluções corretas, e oráculos que não conferiam tudo o que o pedido dizia aprovaram soluções erradas ([banco de provas](https://github.com/Carlobks/Morg-laws/blob/main/prova/README.md)). Por isso se cobre também o que não se mexe.

A ideia de escrever, antes, o que faria mudar a conclusão, em critérios que alguém de fora consiga conferir, é do livro *Competente o Suficiente*, de Fabio Akita (pp. 322–323).

Onde vive no Morg-laws: a seção “O oráculo” da skill `pondo-o-plano-a-prova`, que traz o molde e o jeito de o agente o usar. O exemplo acima vem do [catálogo do projeto de origem](https://github.com/Carlobks/Morg-laws/blob/main/projetos/erp-de-servicos/modulos-e-fluxos.md).

## P8 · A tarefa pequena

### Na prática

Nem todo pedido merece perguntas e oráculo. Se as três coisas abaixo forem verdade, é uma tarefa pequena: peça, o agente faz e diz o que fez.

1. Mexe num só lugar.
2. Dá para desfazer.
3. O próprio pedido já diz o resultado.

Um exemplo que a skill dá:

```
Troca o texto do botão para Salvar.
```

Se alguma das três falhar, o pedido deixou de ser pequeno: peça a versão elaborada, com as perguntas e o oráculo (P7 e P9). Sinais disso: o pedido mexe numa tela ou no que a pessoa já faz, toca em mais de um lugar ou em mais de três arquivos, tem um ponto sem volta (dados, produção, algo publicado, dinheiro) ou chega sem dizer o resultado esperado.

Para a tarefa pequena, peça que o relatório termine com uma linha que diga a verdade:

```
Oráculo: nenhum (tarefa pequena: um só lugar, reversível, resultado dito no pedido).
```

O que costuma dar errado:

- Chamar de pequeno o que mexe em dinheiro, em dados ou numa tela inteira.
- Ficar sem dizer como se conferiu. “Sem oráculo” não é “sem conferir”: o agente ainda diz o que viu.

### Por quê e fonte

Pergunta demais e oráculo demais numa troca de botão custam mais do que o erro que evitam. O esforço deve ser proporcional ao que está em jogo, e é essa a conta que separa a tarefa pequena da elaborada. O livro *Competente o Suficiente*, de Fabio Akita, defende pôr no pedido um esforço à medida do que está em jogo (pp. 118, 120–121).

Esta é uma escolha de Carlobks, e a skill a registra: as vozes da cabeça de Carlobks (decisão de 2026-11-08) dizem que a tarefa pequena dispensa o oráculo e as perguntas. Porquê: a [skill `pondo-o-plano-a-prova`](https://github.com/Carlobks/Morg-laws/blob/main/skills/pondo-o-plano-a-prova/SKILL.md) dispensa a tarefa pequena e clara de perguntas e de oráculo, e liga o esforço ao que está em jogo, com a fonte no livro.

A linha “Oráculo: nenhum” é uma sugestão deste manual, não uma regra do repositório: o `AGENTS.md` e a skill não a exigem. Ela existe para o relatório não calar o que ficou sem conferência.

Onde vive no Morg-laws: a seção “Quando o pedido é uma mudança” da skill `pondo-o-plano-a-prova`, que diz quando pedir a versão elaborada e quando dispensá-la.

## P9 · Pôr o plano à prova

### Na prática

Para um pedido grande, antes de o agente executar, peça que ele o ponha à prova: que faça perguntas até não haver o que adivinhar. Diga, por exemplo:

```
Antes de começar, ponha este plano à prova: faça perguntas em rondas de no máximo quatro, com opções e a recomendada marcada com ➡️.
```

Como a conversa segue:

1. O agente lê primeiro o que pode ler e só pergunta o que depende de você.
2. Cada ronda tem até quatro perguntas, e cada uma traz opções e uma marcada com ➡️, com o porquê numa frase.
3. Você responde com o que quiser. Para aceitar a recomendação, uma palavra basta, por exemplo “R”.
4. No fim, o agente entrega um resumo curto: objetivo, o que fica de fora, a prova de pronto, os pontos sem volta e quem decide o quê. Você o confirma antes de começar.

Um exemplo. Uma ronda sobre o formato deste manual aconteceu na conversa, e só o resumo ficou escrito. Deste resumo se vê o jeito de cada ponto:

```
Formato: o Markdown é a única fonte, e só o PDF sai dele. Quem escolheu: Carlobks, porque o HTML e o site fogem do escopo por agora.
Onde vive: uma pasta, um arquivo por parte. Quem escolheu: a recomendação, aceita.
Página: o tamanho do PDF do livro de referência. Quem escolheu: Carlobks, para imprimir este igual ao livro.
```

O resumo guarda o ponto, a escolha e quem escolheu: a recomendação ou outra coisa.

O que costuma dar errado:

- Responder “R” a uma pergunta que pede um texto seu. Nesse caso, escreva o texto.
- Deixar o agente perguntar o que ele mesmo poderia ler no código.
- Continuar perguntando depois de tudo respondido. Diga “chega”.

### Por quê e fonte

Um plano ruim é executado com perfeição, e mais rápido (livro *Competente o Suficiente*, de Fabio Akita, pp. 105–106). As perguntas incômodas, do tipo “e se…?”, são as que tornam o resultado confiável, e o agente não as faz sozinho (p. 92), e pedir primeiro o plano, revê-lo e só então avançar poupa o retrabalho (pp. 45, 78, 122).

As regras da conversa são da skill `pondo-o-plano-a-prova`: rondas curtas, opções concretas com uma recomendada, o termo técnico explicado dentro da pergunta, e parar quando as lacunas têm resposta, porque cada ronda custa a sua atenção. Não faça ao agente uma pergunta que já traz a resposta (pp. 52–54): ele tende a concordar.

A ideia de interrogar o dono antes de executar foi inspirada na skill “grill-me”, de [Matt Pocock](https://github.com/mattpocock/skills); a skill do repositório foi escrita do zero.

Onde vive no Morg-laws: as seções “Como perguntar”, “Quando parar” e “O que entregar no fim” da skill `pondo-o-plano-a-prova`.
