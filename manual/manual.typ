// O molde de página do manual de uso: não é conteúdo. Lê as partes em Markdown, põe a página, os pares e o colofão.
// A página, as letras, os títulos, os pares e as notas estão em `manual/molde/`. Gerar o PDF, da raiz do repositório (o mesmo
// comando em sh e no PowerShell):
//   typst compile --root . --font-path manual/fontes --ignore-system-fonts --input commit="$(git describe --always --dirty)" manual/manual.typ manual/manual.pdf
#import "@preview/cmarker:0.1.10"
#import "molde/pagina.typ": *
#import "molde/pares.typ": *
#import "molde/titulos.typ": *
#import "molde/notas.typ": *

#let partes = ("00-antes-de-comecar", "01-o-que-e-o-morg-laws", "02-preparar-o-computador", "03-instalar", "04-pedir", "05-sessoes",
  "06-o-ciclo-de-uma-mudanca", "07-as-regras", "08-como-se-garante", "09-quando-da-errado", "10-glossario",
  "11-pedidos-prontos", "12-como-este-manual-foi-feito")
// O Typst não sabe se um arquivo existe: cada fase acrescenta aqui a parte que escreveu (as outras não partem a compilação).
#let escritas = ("00-antes-de-comecar", "01-o-que-e-o-morg-laws", "02-preparar-o-computador", "03-instalar", "04-pedir", "05-sessoes",
  "06-o-ciclo-de-uma-mudanca", "07-as-regras", "08-como-se-garante", "09-quando-da-errado", "10-glossario", "11-pedidos-prontos", "12-como-este-manual-foi-feito")

#let commit = sys.inputs.at("commit", default: none)
#let escopo-do-markdown = (marca-de-par: marca-de-par)

#set document(title: nome-da-obra + ": " + lower(subtitulo-da-obra))
#show: configura
#show: regras-das-notas
#show: regras-dos-titulos
#show: regras-dos-pares

// O rosto e a página de créditos: o rosto sem número, o verso com o que o livro deve às letras e ao commit.
#sem-cabecalho-aqui()
#v(91pt)
#align(center)[
  #text(font: fonte-titulos, weight: "semibold", size: 27pt, fill: tinta)[#nome-da-obra]
  #v(14pt)
  #fio()
  #v(17pt)
  #text(font: fonte-titulos, size: 12pt, fill: cinza-escuro)[#subtitulo-da-obra]
]
#pagebreak()
#sem-cabecalho-aqui()
#set par(first-line-indent: 0pt)
#set text(size: 9pt)
#v(1fr)
*Créditos.* Gerado em #datetime.today().display("[day]/[month]/[year]")#if commit != none [ a partir do commit #raw(commit)].

Corpo em Source Serif 4 e títulos em Source Sans 3, de Adobe (SIL Open Font License 1.1, em `manual/fontes/`). Código em
DejaVu Sans Mono (licença Bitstream Vera, vem com o Typst). Composto com o Typst (Apache-2.0). As artes e as figuras são
desenho vetorial do agente, em Typst e SVG, sem imagem feita por IA.
#pagebreak()
#set par(first-line-indent: 12.6pt)
#set text(size: 10.5pt)
#sumario()

#for parte in partes.filter(p => p in escritas) {
  cmarker.render(read(parte + ".md"), h1-level: 2, scope: escopo-do-markdown)
  fecha-o-par()
}

#confere-os-pares()
#confere-as-partes()
#vai-para("even")
#sem-cabecalho-aqui()
#set par(first-line-indent: 0pt, justify: false)
#set text(size: 9pt)
#v(1fr)
*Colofão.* #nome-da-obra, #lower(subtitulo-da-obra). Gerado em #datetime.today().display("[day]/[month]/[year]")#if commit != none [ a partir do commit #raw(commit)].

Corpo em Source Serif 4 e títulos em Source Sans 3, de Adobe (SIL Open Font License 1.1, em `manual/fontes/`). Código em
DejaVu Sans Mono (licença Bitstream Vera, vem com o Typst). As artes e as figuras são desenho vetorial do agente, em Typst e
SVG, sem imagem feita por IA. Composto com o Typst (Apache-2.0).
