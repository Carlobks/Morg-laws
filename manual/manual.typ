// O molde de página do manual de uso: não é conteúdo. Lê as partes em Markdown, põe a página, os pares e o colofão.
// Gerar o PDF, da raiz do repositório (o mesmo comando em sh e no PowerShell):
//   typst compile --root . --font-path manual/fontes --ignore-system-fonts --input commit="$(git describe --always --dirty)" manual/manual.typ manual/manual.pdf
#import "@preview/cmarker:0.1.10"

#let partes = ("00-antes-de-comecar", "01-o-que-e-o-morg-laws", "02-instalar", "03-pedir", "04-sessoes",
  "05-o-ciclo-de-uma-mudanca", "06-as-regras", "07-como-se-garante", "08-quando-da-errado", "09-glossario",
  "10-pedidos-prontos", "11-como-este-manual-foi-feito")
// O Typst não sabe se um arquivo existe: cada fase acrescenta aqui a parte que escreveu (as outras não partem a compilação).
#let escritas = ("00-antes-de-comecar", "03-pedir")

#let fonte-corpo = "Libertinus Serif"
#let fonte-titulos = "Stardos Stencil"
#let commit = sys.inputs.at("commit", default: none)

#set document(title: "Morg-laws: manual de uso")
#set page(width: 6in, height: 9.6in, binding: left,
  margin: (inside: 0.9in, outside: 0.6in, top: 0.7in, bottom: 0.8in))
#set text(font: fonte-corpo, size: 10.5pt, lang: "pt", region: "BR")
#set par(justify: true, leading: 0.62em)
#show heading: set text(font: fonte-titulos, weight: "bold")
#show raw: set text(size: 8.5pt)
#show link: set text(fill: rgb("#1f4e79"))

// A página em branco que a paridade pede sai sem número (a capa também, mais abaixo).
#let quebra(..argumentos) = { set page(numbering: none); pagebreak(..argumentos) }

// --- Os pares: a prática na página par, a teoria na ímpar seguinte, cada lado numa página só ---
#let marca(tipo, nome) = [#metadata((tipo: tipo, nome: nome)) <marca-do-par>]
#let par-aberto = state("par-aberto", none)
#let texto-de(c) = {
  if type(c) == str { c }
  else if c.has("text") { c.text }
  else if c.has("children") { c.children.map(texto-de).join() }
  else if c.has("body") { texto-de(c.body) }
  else if c == [ ] { " " }
  else { "" }
}
#let texto-do(titulo) = texto-de(titulo.body)

#let fecha-o-par() = context {
  let nome = par-aberto.get()
  if nome != none { marca("fim-teoria", nome); par-aberto.update(none) }
}

#show heading: it => {
  let texto = texto-do(it)
  if it.level <= 2 { fecha-o-par() }
  if it.level == 2 and texto.match(regex("^P\d+\b")) != none {
    quebra(to: "even")
    par-aberto.update(texto)
    marca("ini-pratica", texto)
  } else if it.level == 3 and texto == "Por quê e fonte" {
    context {
      if par-aberto.get() == none { panic("«Por quê e fonte» fora de um par: falta o «## P<n>» antes dela") }
      marca("fim-pratica", par-aberto.get())
    }
    quebra(to: "odd", weak: true)
    context marca("ini-teoria", par-aberto.get())
  }
  it
}

#let confere-os-pares() = context {
  let achadas = query(<marca-do-par>).map(m => (m.value, m.location().page()))
  let nomes = achadas.map(a => a.at(0).nome).dedup()
  for nome in nomes {
    let de(tipo) = achadas.find(a => a.at(0).nome == nome and a.at(0).tipo == tipo)
    let (ini-p, fim-p, ini-t, fim-t) = ("ini-pratica", "fim-pratica", "ini-teoria", "fim-teoria").map(tipo => {
      let achada = de(tipo)
      if achada == none { panic("o par «" + nome + "» não tem a marca «" + tipo + "»") }
      achada.at(1)
    })
    if ini-p != fim-p { panic("o par «" + nome + "»: a prática não cabe numa página só (começa na " + str(ini-p) + ", acaba na " + str(fim-p) + ")") }
    if calc.odd(ini-p) { panic("o par «" + nome + "»: a prática começa numa página ímpar, a " + str(ini-p)) }
    if ini-t != fim-t or ini-t != fim-p + 1 { panic("o par «" + nome + "»: a teoria não cabe na página ímpar seguinte (começa na " + str(ini-t) + ", acaba na " + str(fim-t) + ")") }
  }
}

// --- O sumário, as partes e o colofão ---
#align(center + horizon)[
  #text(font: fonte-titulos, size: 26pt, weight: "bold")[Morg-laws]
  #v(0.4em)
  #text(size: 14pt)[Manual de uso]
]
#quebra(to: "odd")
#set page(numbering: "1")
#outline(title: "Sumário", depth: 2)

#for parte in partes.filter(p => p in escritas) {
  quebra(to: "odd", weak: true)
  cmarker.render(read(parte + ".md"))
  fecha-o-par()
}

#confere-os-pares()

#quebra(to: "even", weak: true)
#v(1fr)
#set text(size: 9pt)
#set par(justify: false)
*Colofão.* Gerado em #datetime.today().display("[day]/[month]/[year]")#if commit != none [ a partir do commit #raw(commit)].

Corpo em #fonte-corpo (SIL Open Font License 1.1, vem com o Typst). Títulos em #fonte-titulos, de Vernon Adams
(SIL Open Font License 1.1, em `manual/fontes/`). Código em DejaVu Sans Mono (licença Bitstream Vera, vem com o Typst).
Composto com o Typst (Apache-2.0).
