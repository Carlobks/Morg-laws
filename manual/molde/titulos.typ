// Os títulos: a abertura do capítulo, a página de parte com as duas artes, as seções e o sumário.
// Níveis: 1 = a parte (só nas partes novas), 2 = o capítulo (o `#` do Markdown), 3 = a seção (`##`), 4 = o lado do par (`###`).
#import "pagina.typ": *
#import "pares.typ": vai-para

#let contador-de-parte = counter("parte")
#let contador-de-capitulo = counter("capitulo")
#let romano(n) = numbering("I", n)
#let fio(largura: 32pt) = line(length: largura, stroke: 0.6pt + cinza-claro)
#let sem-recuo = par.with(first-line-indent: 0pt, justify: false)

#let regras-dos-titulos(livro) = {
  // A abertura: o título fica escondido no lugar (para o sumário e o cabeçalho o acharem) e o desenho é este.
  show heading.where(level: 2): it => {
    let peca = sem-numero(texto-de(it.body))
    pagebreak(weak: true)
    sem-cabecalho-aqui()
    if not peca { contador-de-capitulo.step() }
    counter(footnote).update(0)
    counter(figure.where(kind: image)).update(0)
    hide(box(height: 0pt, it))
    v(81.3pt)
    if not peca {
      context sem-recuo(text(font: fonte-titulos, weight: "light", size: 30pt, fill: cinza-claro)[#contador-de-capitulo.get().first()])
      v(16.2pt - 0.67em)
    }
    sem-recuo(leading: 0.4em, text(font: fonte-titulos, weight: "semibold", size: 19pt, fill: tinta, it.body))
    v(26pt)
    fio()
    v(39pt)
  }
  show heading.where(level: 3): set text(font: fonte-titulos, weight: "semibold", size: 12pt, fill: tinta)
  show heading.where(level: 3): set block(above: 22pt, below: 10pt)
  show heading.where(level: 4): set text(font: fonte-titulos, weight: "semibold", style: "italic", size: 10.5pt, fill: tinta)
  show heading.where(level: 4): set block(above: 14pt, below: 8pt)
  show heading: set par(first-line-indent: 0pt, justify: false)
  livro
}

// A parte: a página par com a arte A inteira, depois a página da parte, com a arte B no terço de cima, o rótulo, o fio e o título.
// O capítulo anterior tem de acabar numa página ímpar, senão a arte A teria uma página em branco antes.
// As artes chegam como `image(...)` já montadas por quem chama (o caminho do SVG vale a partir do arquivo de quem chama).
#let marca-do-fim = <fim-antes-da-parte>
#let pagina-de-parte(titulo, arte-a: none, arte-b: none) = {
  [#metadata(none) #marca-do-fim]
  vai-para("even")
  contador-de-parte.step()
  sem-cabecalho-aqui()
  [#metadata("arte-a") <arte-da-parte>]
  if arte-a != none { box(width: 100%, height: 100%, arte-a) }
  pagebreak()
  sem-cabecalho-aqui()
  place(hide(heading(level: 1, outlined: true, numbering: none, titulo)))
  if arte-b != none { v(8pt); align(center, arte-b); v(15pt) } else { v(153pt) }
  align(center, {
    context text(font: fonte-titulos, size: 8.5pt, tracking: 0.3em, fill: cinza-escuro, upper[Parte #romano(contador-de-parte.get().first())])
    v(33pt)
    fio()
    v(29.3pt)
    sem-recuo(text(font: fonte-titulos, weight: "semibold", size: 21pt, fill: tinta, titulo))
  })
}

#let confere-as-partes() = context {
  let fins = query(marca-do-fim).map(m => m.location().page())
  let artes = query(<arte-da-parte>).map(m => m.location().page())
  for (fim, arte) in fins.zip(artes) {
    if arte != fim + 1 { panic("a arte da parte está na página " + str(arte) + " e o capítulo anterior acaba na " + str(fim) + ": ajuste o capítulo para acabar numa página ímpar") }
  }
}

// As linhas do sumário: a parte como faixa e o capítulo com o número, o pontilhado e a página.
#let com-link(destino, conteudo) = if destino == none { conteudo } else { link(destino, conteudo) }
#let linha-de-parte(numero, titulo, destino: none) = {
  set par(first-line-indent: 0pt, justify: false, leading: 0.5em)
  v(16pt, weak: true)
  com-link(destino, text(font: fonte-titulos, size: 7.5pt, tracking: 0.18em, fill: cinza-escuro, upper[Parte #romano(numero) · #titulo]))
  v(5pt, weak: true)
}
#let linha-de-capitulo(numero, titulo, pagina, destino: none) = {
  set par(first-line-indent: 0pt, justify: false)
  com-link(destino, grid(columns: (20pt, auto, 1fr, auto), column-gutter: 4pt, row-gutter: 6pt,
    text(font: fonte-titulos, fill: cinza-claro)[#numero], titulo, box(width: 100%, repeat(text(fill: cinza-claro)[.], gap: 2pt)), [#pagina]))
}

// O sumário: as partes como faixa e os capítulos numerados; nenhuma seção interna. O número é o da página do título.
#let sumario(linhas: none) = {
  vai-para("odd")
  sem-cabecalho-aqui()
  v(40pt)
  sem-recuo(text(font: fonte-titulos, weight: "semibold", size: 19pt, fill: tinta)[Sumário])
  v(10pt)
  show link: set text(fill: tinta)
  show outline.entry.where(level: 1): it => linha-de-parte(contador-de-parte.at(it.element.location()).first(), it.element.body, destino: it.element.location())
  show outline.entry.where(level: 2): it => {
    linha-de-capitulo(numero-do-capitulo(it.element),it.element.body, it.page(), destino: it.element.location())
  }
  if linhas != none { linhas } else { outline(title: none, depth: 2) }
}
