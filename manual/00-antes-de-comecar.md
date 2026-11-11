# Antes de começar

> **Aviso.** Este manual é o achado próprio de um não profissional, não uma crítica a ninguém. Quem o escreve está aprendendo, e o que está aqui é o que ele usa num projeto real, não um padrão da área.

## Quem escreveu isto

Eu sou o Carlobks, estou na casa dos vinte e escrevo este manual para compartilhar o que ando vivendo: o sonho de poder criar o que vem na minha cabeça. Sou um júnior que nunca trabalhou na área. Fiz o SENAI e tive o prazer de ter um professor incrível, o Cenora. Desde lá venho apaixonado por criar, porque foi ali que fiz o meu primeiro site, sobre o criador da franquia Zelda. Lembro de ficar horas só trocando a posição das imagens, e quando adicionei JavaScript ao site fiquei louco: passava o mouse pelos ícones e eles reagiam. Sempre quis fazer um jogo ou algo assim, mas era realmente algo enorme. Desde fevereiro de 2026 caí de cabeça nas IAs que escrevem código e quero aprender a lógica por trás delas. Escrevi o manual para mim e para qualquer pessoa que ainda não sabe usar agentes: um guia prático para ler, ou imprimir e ter sempre à mão, com o que o Morg-laws já aplica desde o início.

O agente de código fez o rascunho do texto e conferiu as fontes. O que é decisão, escolha ou gosto é meu. A história inteira, de como cheguei até aqui, fica para outro livro: aqui o manual é só prático. Não há aqui o nome civil de ninguém nem dado pessoal, só o nome Carlobks, e é assim porque o repositório é público. O mesmo tom do aviso do topo está na [pesquisa da linha de base do uso](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-05-linha-de-base-do-uso.md), que também é o achado de um não profissional. A intenção é esta: tudo o que eu conseguir melhorar, vou colocando aqui no manual, para qualquer pessoa, de um jeito prático e simples.

## Como ler este manual

O manual tem partes numeradas, de `00` a `11`. Cada parte é um arquivo em `manual/`, e o PDF junta todas. Os procedimentos, os “faça assim”, vêm em páginas duplas: na página da esquerda, **Na prática**, com o molde, um exemplo preenchido e o que costuma dar errado; na da direita, **Por quê e fonte**, com a teoria, a fonte e onde aquilo vive no Morg-laws. Você pode ler só a esquerda e fazer. Quando quiser saber por que, vira a página.

**Se você tem pressa:** leia a parte `02-instalar.md`, que põe tudo para funcionar, e depois a `03-pedir.md`, que ensina a pedir. O resto você consulta quando precisar. A parte `01-o-que-e-o-morg-laws.md` explica o que você acabou de instalar, e a `08-quando-da-errado.md` serve para o dia em que algo falhar.

Você vai ver a expressão “as vozes da cabeça de Carlobks”. É uma brincadeira dele: quando uma escolha é do autor e não de uma fonte, o manual diz isso assim, com a data em que ele decidiu, e diz também o porquê. Se um porquê não estiver escrito, o manual não cita a decisão. Assim você sempre sabe o que é fato de uma fonte e o que é preferência de uma pessoa.

Uma última combinação sobre a escrita: as páginas do livro que o manual cita são as impressas, e nada do livro é copiado, só resumido com palavras próprias. A fonte de cada parte vem no fim dela, em link ou em página. O livro que inspirou este formato é o *Competente o Suficiente*, de Fabio Akita, e o [resumo dele que o repositório guarda](https://github.com/Carlobks/Morg-laws/blob/main/biblia-akita/README.md) mostra de onde vem cada conselho.

## Para qual ferramenta é

O manual é sobre o Claude Code, que o autor usa quase todo dia. Ele deve servir também para o Codex, que segue o mesmo padrão de skills, como diz a [documentação de skills do Codex](https://developers.openai.com/codex/skills). Mas o autor ainda não usou o Codex: onde o manual diz como algo funciona nele, vem da documentação, não da prática. Os passos que dependem do Claude Code dizem isso no lugar: os hooks do agente e o `settings.json` (P3), as sessões filhas, os títulos e os avisos entre sessões (P11, P12, P14) e a compactação (P10). Os hooks do git, os testes e o CI não dependem do agente. Se você usa o Codex e algo não bater, abra uma issue (a parte `01-o-que-e-o-morg-laws.md` mostra como).

## O que este manual não promete

As regras do Morg-laws saíram de um projeto real, em uso, e a prova delas é o uso real em outros projetos e as issues que voltam para o repositório. As regras não foram medidas, e nenhum texto aqui diz o contrário. O método de prova existe no repositório, na pasta `prova/`, para quem quiser rodar. Quem quiser os números do uso que originou as regras lê a [pesquisa da linha de base](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-05-linha-de-base-do-uso.md), que também é achado de um não profissional.
