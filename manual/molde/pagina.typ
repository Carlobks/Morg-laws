// A página e as letras: as medidas do livro de referência (432 × 648 pt, margem de 54 pt, corpo a 10,5 pt), em Source Serif 4,
// os cabeçalhos e os títulos em Source Sans 3 e o código em DejaVu Sans Mono (vem com o Typst).
#let tinta = rgb("#1b2238")
#let cinza-claro = rgb("#8a8f98")
#let cinza-escuro = rgb("#4a5060")
#let fonte-corpo = "Source Serif 4"
#let fonte-titulos = "Source Sans 3"
#let fonte-codigo = "DejaVu Sans Mono"
// A entrelinha é a que põe as linhas de base a 13,5 pt uma da outra (medido com `pdftotext -bbox`).
#let entrelinha = 0.62em

// O nome da obra, num só lugar: o rosto, o cabeçalho par, o título do PDF e o colofão leem estas três variáveis.
#let nome-da-obra = "Morg-laws"
#let subtitulo-da-obra = "Manual de uso"
#let cabecalho-par = nome-da-obra + " · " + subtitulo-da-obra

// Uma página que leva esta marca fica sem cabeçalho: a abertura, a página de parte, a arte e a página em branco.
#let sem-cabecalho-aqui() = [#metadata(none) <sem-cabecalho>]

// Os textos de um título (que pode ter ênfase) como texto simples.
#let texto-de(c) = {
  if type(c) == str { c }
  else if c.has("text") { c.text }
  else if c.has("children") { c.children.map(texto-de).join() }
  else if c.has("body") { texto-de(c.body) }
  else if c == [ ] { " " }
  else { "" }
}

// As peças sem número (o Prefácio, os apêndices, as Notas…): abrem como um capítulo, sem o algarismo e sem gastar o contador.
#let sem-numero(texto) = texto.starts-with("Apêndice") or texto in ("Prefácio", "Como ler este manual", "Posfácio", "Notas", "Referências", "Glossário")

// O número de um capítulo (o `h` achado por `query`): o contador lido no lugar do título ainda não tem o passo da abertura, que vem depois.
#let numero-do-capitulo(h) = if sem-numero(texto-de(h.body)) { none } else { counter("capitulo").at(h.location()).first() + 1 }

// Cabeçalho: na página par, o número e o nome do livro; na ímpar, o título curto do capítulo e o número.
#let cabecalho() = context {
  let pagina = here().page()
  if query(<sem-cabecalho>).any(m => m.location().page() == pagina) { return none }
  let capitulos = query(selector(heading.where(level: 2)).before(here()))
  let estilo(c) = text(font: fonte-titulos, size: 7.5pt, tracking: 0.12em, fill: cinza-escuro, upper(c))
  if calc.even(pagina) {
    estilo[#pagina #h(1.2em) #cabecalho-par]
  } else if capitulos.len() > 0 {
    let curto = texto-de(capitulos.last().body).split(",").first()
    align(right, estilo[#curto #h(1.2em) #pagina])
  }
}

// As letras, as margens e o que vale em todo o livro.
#let configura(livro) = {
  set page(width: 432pt, height: 648pt, margin: 54pt, header-ascent: 15pt, header: cabecalho(), footer: none, numbering: "1")
  set text(font: fonte-corpo, size: 10.5pt, lang: "pt", region: "BR", hyphenate: true)
  set par(justify: true, leading: entrelinha, spacing: entrelinha, first-line-indent: 12.6pt)
  show link: set text(fill: rgb("#1f4e79"))
  show raw: set text(font: fonte-codigo, size: 7.4pt)
  show raw.where(block: true): it => block(width: 100%, fill: rgb("#f3f3f3"), inset: (x: 8pt, y: 6pt), radius: 3pt, breakable: false, {
    set par(first-line-indent: 0pt, justify: false)
    it
  })
  // O destaque: uma barra de 1,6 pt à esquerda e a letra do corpo a 11 pt, sem itálico.
  show quote.where(block: true): it => block(width: 100%, inset: (left: 11.5pt, y: 3pt), stroke: (left: 1.6pt + tinta), {
    set par(first-line-indent: 0pt, justify: false)
    text(size: 11pt, fill: tinta, style: "normal", it.body)
  })
  // As figuras: legenda «Figura N.M», numerada por capítulo.
  show figure.caption: set text(font: fonte-titulos, size: 8.5pt, fill: cinza-escuro)
  set figure(supplement: "Figura", numbering: n => context [#counter("capitulo").get().first().#n])
  livro
}
