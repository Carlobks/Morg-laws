# Páginas duplas num manual técnico

Escrita com palavras próprias; nada das fontes foi copiado. As páginas foram relidas em 2026-11-09 com o `WebFetch`; o
PDF do STOP é uma imagem digitalizada e não voltou a ser lido, por isso o ponto 4 vale pela leitura anterior.

## Pergunta

Num manual prático impresso de 6 × 9,6 polegadas, vale a pena pôr a prática na página da esquerda (o molde, um exemplo
preenchido, o que costuma dar errado) e a teoria na da direita (o porquê, a fonte e onde a coisa vive no Morg-laws)?
Já existem livros feitos assim, o que se aprende com eles, quanto custa montar isso no Typst ou no CSS de impressão e,
se não servir, qual é a forma mais simples que guarda a ideia?

## Fontes

Lidas em 2026-11-09.

- **Hughes Aircraft, «Sequential Thematic Organization of Publications (STOP)»**, de J. R. Tracey, D. E. Rugh e
  W. S. Starkey, janeiro de 1965, na reimpressão do *Journal of Computer Documentation* (agosto de 1999, vol. 23,
  n.º 3) — https://faculty.washington.edu/farkas/TC510-Fall2011/TraceySTOPReport-DF-Ann.pdf — lidas as páginas 4 a 9
  da reimpressão (folha de rosto, sumário, «The STOP Technique at a Glance» e «Concept of the Topical Module»). É a
  fonte primária, digitalizada como imagem; o arquivo do curso traz anotações de um leitor por cima.
- **Folger Shakespeare Library, «About the Folger Shakespeare»** —
  https://www.folger.edu/about-us/what-we-do/about-the-folger-shakespeare/ — a página da própria editora.
- **Folgerpedia, «New Folger Library Shakespeare editions»** —
  https://folgerpedia.folger.edu/New_Folger_Library_Shakespeare_editions — o wiki da própria biblioteca.
- **Loeb Classical Library (Wikipedia)** — https://en.wikipedia.org/wiki/Loeb_Classical_Library — *(secundária:
  as páginas da editora, `hup.harvard.edu` e `loebclassics.com`, responderam vazio ou 403)*.
- **A Pattern Language, a anatomia de um padrão** — https://designmatrix.com/pl/anatomy.html — *(secundária: o livro
  de 1977 não foi aberto; o site oficial, https://www.patternlanguage.com/, só descreve as três partes do livro)*.
- **Typst, `page`** — https://typst.app/docs/reference/layout/page/ — e **Typst, `pagebreak`** —
  https://typst.app/docs/reference/layout/pagebreak/ — e **Typst, `footnote`** —
  https://typst.app/docs/reference/model/footnote/ (lida na conferência da auditoria do plano).
- **MDN, `@page`** — https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@page — e **Chrome for
  Developers, «Add content to the margins of web pages when printed using CSS»** (30-10-2024) —
  https://developer.chrome.com/blog/print-margins.
- **WeasyPrint, «API Reference», seção «Supported Features»** —
  https://doc.courtbouillon.org/weasyprint/stable/api_reference.html.
- **WeasyPrint, «First Steps», instalação** —
  https://doc.courtbouillon.org/weasyprint/stable/first_steps.html.

## O que se mediu

1. **Folger.** As duas páginas da biblioteca dizem que as notas ficam na página em frente ao texto que explicam.
   Nenhuma das duas diz de que lado. Os anúncios de livreiros dizem que a peça vai à direita e as notas à esquerda,
   mas isso não foi conferido num exemplar. A página dupla aqui é um **auxílio de leitura**: as duas páginas falam das
   mesmas linhas, uma é o texto e a outra explica palavras.
2. **Loeb.** A fonte secundária diz que o original grego ou latino fica à esquerda e a tradução à direita. É o mesmo texto duas vezes, em duas línguas; também é auxílio de leitura, não de
   ensino.
3. **A Pattern Language.** Pela fonte secundária, cada padrão segue sempre a mesma ordem: uma visualização
   (opcional), o resumo do problema, a análise, a solução, que começa por «Therefore» («portanto»), e os padrões que
   vêm depois dele. A mesma página diz que o livro **não** tem o elemento de contexto que outras linguagens de padrões
   usam. Corre em texto seguido, sem página dupla. Serve de modelo para a **ordem fixa** de cada tópico, não para
   o desenho da folha.
4. **STOP (Hughes, 1965).** É o precedente que mais se parece com o caso: documentos **técnicos** (propostas e
   relatórios) partidos em módulos de **duas páginas em frente**, um tema por módulo, com título que diz o tema e uma
   frase-tese logo abaixo. No modelo típico, o texto vai à esquerda e as figuras à direita; se não houver figura, o
   texto continua no outro lado. O relatório conta cerca de 500 palavras por página de 8,5 × 11 pol. (até 1.000 por
   tema sem figura), diz que um tema que não enche o módulo deixa espaço em branco, e que o limite de duas páginas
   obriga o autor a não se esticar além do ponto. Diz também que, desde 1962, 120 propostas e relatórios já tinham sido
   feitos assim. Esse número é dos autores do método, não de uma medição independente.
5. **Typst.** A página `page` dá a largura e a altura livres (6in e 9.6in servem), as margens `inside` e `outside`
   para o lado da lombada, o parâmetro `binding` e o cabeçalho e o rodapé por página. A `pagebreak` tem
   `to: "even"` e `to: "odd"`, que põem a página seguinte num número par ou ímpar, com uma página vazia no meio se
   precisar. Com a página 1 à direita, uma página par fica sempre à esquerda: é o que segura um par prática/teoria.
6. **CSS de impressão.** O `@page` aceita `size` e os seletores `:left` e `:right`. Pela MDN, só `margin`,
   `page-orientation` e `size` estão em algum navegador (a página não diz versões). É o artigo do Chrome, de
   30-10-2024, que diz que as caixas de margem chegaram ao Chrome 131. O mesmo artigo põe as notas de rodapé e o `target-counter()` (o número da página no sumário) em «possibilidades futuras».
   O WeasyPrint, que não é navegador, diz suportar tudo do rascunho Paged Media, `:left` e `:right`, notas de rodapé,
   `target-counter()` e marcadores do PDF.
7. **Medido no PDF do livro de referência, com o `pdfinfo`:** 432 × 691,2 pt, 503 páginas, gerado pelo Typst 0.15.1.

## O que não se verificou

- Não se abriu nenhum exemplar Folger nem Loeb; o lado esquerdo ou direito vem de terceiros.
- O livro *A Pattern Language* não foi lido; a ordem dos padrões vem de uma fonte secundária.
- Do STOP foram lidas 6 páginas da reimpressão; as partes sobre leitores e avaliadores (pp. 44–48 do original) e as
  objeções ao método (apêndice) não foram lidas.
- Não se instalou o Typst nem o WeasyPrint: o custo abaixo é estimado pela documentação, não por um protótipo.
- Quantas palavras cabem numa página de 6 × 9,6 pol. depende da fonte e do corpo; o número só sai do primeiro par
  montado.
- Não se encontrou nenhum manual técnico de software feito todo em pares prática/teoria. O STOP é de propostas e
  relatórios de engenharia.

## Conclusão

**A ideia serve, mas só para os procedimentos.** O que se parece com ela é o STOP, e não a Folger ou a Loeb: aquelas
põem o mesmo texto ou as notas dele em frente, para quem lê devagar; o STOP põe um tema inteiro por módulo de duas
páginas, que é o que um manual de campo pede (abrir no procedimento e ter tudo à vista). O que o STOP ensina e o plano
leva:

- **um procedimento por par**, com o título que diz a tarefa e uma frase-tese em cima da página da esquerda;
- **um teto de palavras por lado**, conferido por teste, porque um par que transborda deixa de ser par;
- **o espaço em branco é aceitável**; o par nunca se estica para a página seguinte;
- **a ordem fixa dentro de cada lado**, como nos padrões de *A Pattern Language* (na prática: o molde, o exemplo e o que costuma
  dar errado; na teoria: o porquê, a fonte e onde vive).

As partes que são referência (as regras, as barreiras e as catracas, o glossário) correm em texto seguido: forçá-las
em pares só gera páginas em branco.

**Custo.** No Typst parece baixo, pela documentação: um `pagebreak(to: "even")` antes de cada prática, um
`pagebreak(to: "odd", weak: true)` antes da teoria, uma marca no fim de cada lado e uma conferência que falha a
compilação se a prática não começar e acabar na mesma página par, ou se a teoria não começar e acabar na ímpar
seguinte (conferir só o início deixaria passar uma teoria que transborda). Notas de rodapé nos pares ficam de fora: a
doc do `footnote` diz que uma nota pode partir-se entre páginas. Nada disto foi corrido: prova-se no primeiro par
montado. No CSS de
impressão, os pares pedem o WeasyPrint (os navegadores ainda não dão notas de rodapé nem o número da página no
sumário), que no Windows sai como executável à parte, ou pelo `pip` com o Pango do MSYS2.

**A forma mais simples, se o par não couber ou não servir:** um procedimento por seção, em texto seguido, sempre na
mesma ordem — primeiro «Na prática», depois «Por quê e fonte» —, com o mesmo teste de que nenhum par fica sem fonte.
É exatamente como o Markdown já fica; só se perde o desenho da folha.
