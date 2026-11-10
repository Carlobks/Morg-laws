# Pedir

Como pedir o que você quer, de um jeito que o agente consiga entregar.

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
- O critério de pronto é «fica bom». O agente não consegue conferir isso, e você também não.
- O pedido deixa de fora o que só você sabe: o combinado de ontem, o arquivo que não se mexe, o prazo.

### Por quê e fonte

O agente não adivinha o que ficou na sua cabeça. Cada parte que falta vira um palpite dele, e cada palpite errado custa
uma volta de retrabalho. A parte do que você não quer evita o erro mais caro, o de ele fazer a mais. A do critério de pronto
transforma «acho que está bom» em algo que se confere.

A mesma ideia aparece no guia de boas práticas do Claude Code, que pede ao agente um jeito de verificar o próprio trabalho
([boas práticas do Claude Code](https://code.claude.com/docs/en/best-practices)), e no livro *Competente o Suficiente*,
de Fabio Akita: o pedido importante não sai sem o que fica de fora e o critério de pronto (pp. 118, 120–121).

Onde vive no Morg-laws: a skill `pondo-o-plano-a-prova` pergunta pelas quatro partes antes de um pedido grande começar.
