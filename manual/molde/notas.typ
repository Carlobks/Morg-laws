// As notas: o `cmarker` lê `texto[^nome]` e `[^nome]: conteúdo` e emite a nota nativa do Typst. A área do pé fica escondida e
// sem espaço reservado (a página com notas tem as mesmas linhas que a sem notas); a lista «Notas» vai no fim do livro,
// com um subtítulo por capítulo e a numeração recomeçada em cada um (o contador volta a zero na abertura de cada capítulo).
#import "pagina.typ": *

#let regras-das-notas(livro) = {
  set footnote.entry(separator: none, clearance: 0pt, gap: 0pt)
  show footnote.entry: none
  set footnote(numbering: "1")
  show footnote: set text(font: fonte-titulos, weight: "semibold")
  livro
}

// A segunda chamada da mesma nota chega como `footnote(<rótulo>)`: reconhece-se por o corpo ser um rótulo e não entra na lista.
#let lista-de-notas() = context {
  let notas = query(footnote).filter(n => type(n.body) != label)
  let capitulos = query(selector(heading.where(level: 2)))
  let atual = none
  set par(first-line-indent: 0pt, justify: true, leading: 0.5em, spacing: 0.5em)
  set text(size: 9pt)
  for nota in notas {
    let deste = query(selector(heading.where(level: 2)).before(nota.location())).last()
    if atual != deste.location() {
      atual = deste.location()
      v(12pt, weak: true)
      let titulo = texto-de(deste.body)
      let numero = numero-do-capitulo(deste)
      text(font: fonte-titulos, weight: "semibold", size: 10.5pt, fill: tinta, if numero == none { titulo } else { [#numero · #titulo] })
      v(4pt)
    }
    let numero = counter(footnote).at(nota.location()).first()
    grid(columns: (18pt, 1fr), text(font: fonte-titulos, fill: cinza-escuro)[#numero.], nota.body)
    v(0.3em)
  }
}
