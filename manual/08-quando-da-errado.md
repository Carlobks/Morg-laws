# Quando dá errado

Duas falhas aparecem cedo e se repetem: o agente diz “pronto” sem mostrar nada, e o agente esquece o que ficou combinado ou volta ao que já falhou. Esta parte diz o que pedir em cada caso.

## P23 · O agente diz “pronto” sem prova

### Na prática

“Pronto”, “funciona” e “passou” são frases. Antes de aceitá-las, peça a prova do tipo certo:

1. Para código: o comando e a saída dele, como o teste e o verificador de tipos.
2. Para o que se vê: a tela, em captura, ou você mesmo a abre e olha.
3. Para o que está num banco: a consulta e o resultado.
4. Em todos os casos, a lista do que não se verificou. “Os testes passam; não olhei no celular” é um relatório honesto.

Se a prova não vem, ou vem só em palavras, não aceite. Peça: “rode de novo e cole a saída”. Um resumo com números também se confere: peça que contem de novo antes de mostrá-lo.

Se a saída mostra uma falha e cada ajuste do agente quebra outra coisa, pare. Peça um plano novo (P18) em vez de mais um ajuste.

Um exemplo, reescrito, de uma pergunta e da resposta que a prova pede:

```
Você: o que você provou, e o que não?
Agente: rodei os testes: 501 passaram, com cobertura de 100%. A saída está acima.
Não rodei o PDF inteiro, e não olhei as páginas no leitor.
```

O que costuma dar errado:

- Aceitar “os testes passam” sem ver a saída.
- Aceitar um “nenhum erro” sem perguntar se foi procurado direito.
- Deixar passar um relatório sem a lista do que não se verificou.

### Por quê e fonte

Um modelo pode dizer que os testes passaram sem tê-los rodado, e uma resposta errada costuma parecer perfeita: “parece certo” e “está certo” são degraus diferentes (livro *Competente o Suficiente*, de Fabio Akita, pp. 191–193). O texto bonito não prova nada, e só o comando e a saída o separam do certo.

O livro também manda perguntar se um relatório com zero achados contou o que procurou ou apenas não encontrou nada (p. 99). E manda parar e repensar quando cada ajuste quebra outra coisa (p. 105): continuar a pedir “mais um ajuste” gasta tempo e piora o que estava bom.

Cada afirmação de que algo funciona leva o comando e a saída, a captura da tela ou o resultado da consulta, e diz sempre o que não se verificou; um resumo que o agente escreveu também se confere, porque números de cabeça erram. Isso está na seção “Provar medindo” da skill `testes-e-provas`. A mesma skill traz o bug que traz teste, visto falhando antes (P21). Para pedir o critério de “pronto” antes do trabalho, ver o P7.

Onde vive no Morg-laws: a skill `testes-e-provas`, seções “Provar medindo”, “Bug tem teste” e “O que só uma pessoa prova”.

## P24 · O agente esquece o combinado ou repete o que já falhou

### Na prática

Quase sempre a causa é uma conversa longa: o resumo perdeu o motivo de uma decisão, e o agente propõe de novo o que você já descartou. O que fazer:

1. Veja se o combinado está num arquivo: o handoff (P16). Se não está, grave-o agora, com a seção “Descartado”.
2. Peça um resumo do que se decidiu e do que se descartou. Antes de seguir, confira-o contra o arquivo e contra o `git log`.
3. Recomece numa conversa limpa: uma sessão nova que lê o handoff inteiro e confere com o `git status -s`. Quando compactar e quando abrir outra sessão, ver o P10.
4. Escreva o que já falhou, com o motivo. O agente só evita o que lê.

Se o agente insiste na mesma “solução” depois de duas voltas, não peça a terceira: troque de sessão.

Um exemplo, reescrito, de uma linha do “Descartado”:

```
## Descartado
- Fixar o modelo no `settings.json` → vale para todas as sessões → o modelo vai no pedido (P12).
```

O que costuma dar errado:

- Escrever só o que se decidiu e deixar de fora o que se descartou.
- Aceitar o resumo do agente sem conferir.
- Insistir na mesma conversa porque “já está quase lá”.

### Por quê e fonte

O resumo de uma compactação é escrito pelo próprio modelo, com a janela cheia, e perde justamente o que faz falta para continuar: caminhos, nomes, erros literais e o que já se tentou sem sucesso. Por isso a skill `passando-o-trabalho` põe esse estado num arquivo, no git, antes de compactar ou de parar. O livro de Fabio Akita diz que o resumo da compactação perde o detalhe e que o agente volta a propor o que já se descartou, e que uma sessão longa se enche de tentativas antigas (pp. 30–32). Para uma conversa longa, o livro manda repetir o que importa, pedir um resumo, conferi-lo e recomeçar numa conversa limpa com ele (pp. 19, 38–39).

A documentação do Claude Code confirma o risco: a compactação automática, perto do limite, pode perder instruções do começo da conversa ([como o Claude Code funciona](https://code.claude.com/docs/en/how-claude-code-works)). O que vive num arquivo do projeto sobrevive e é relido do disco; o que foi dito só na conversa pode se perder ([glossário do Claude Code](https://code.claude.com/docs/en/glossary)).

O porquê do handoff no git e do “Descartado” está no P16, e o do momento de compactar, no P10: não se repete aqui.

Onde vive no Morg-laws: a skill `passando-o-trabalho`, seções “Compactar” e “Retomar”, com o comando de compactação e a mensagem de retomada prontos.
