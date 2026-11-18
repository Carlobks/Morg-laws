// Os pares: a prática na página par, a teoria na ímpar seguinte, cada lado numa página só.
// O par reconhece-se por dois gatilhos: o marcador invisível `marca-de-par()` que vem antes do `##` (o das partes novas; só anuncia,
// a quebra de página é do título, depois de fechar o par anterior)
// e o `## P<n>` que as partes de hoje ainda trazem. O lado direito chama-se «Por quê» (ou, nas partes de hoje, «Por quê e fonte»).
#import "pagina.typ": sem-cabecalho-aqui, texto-de

#let marca(tipo, nome) = [#metadata((tipo: tipo, nome: nome)) <marca-do-par>]
#let par-aberto = state("par-aberto", none)
#let par-anunciado = state("par-anunciado", false)

// Vai para a próxima página do lado pedido ("even" ou "odd"); a página em branco que a paridade pede sai sem cabeçalho.
#let vai-para(lado) = {
  set page(header: none)
  pagebreak(to: lado, weak: true)
}

#let marca-de-par() = par-anunciado.update(true)

#let fecha-o-par() = context {
  let nome = par-aberto.get()
  if nome != none { marca("fim-teoria", nome); par-aberto.update(none) }
}

// As regras dos títulos que abrem e fecham um par (níveis 3 e 4: os `##` e `###` do Markdown, com o capítulo no nível 2).
#let regras-dos-pares(livro) = {
  show heading: it => {
    let texto = texto-de(it.body)
    if it.level <= 3 { fecha-o-par() }
    if it.level == 3 {
      context {
        let anunciado = par-anunciado.get()
        if anunciado or texto.match(regex("^P\d+\b")) != none {
          vai-para("even")
          par-anunciado.update(false)
          par-aberto.update(texto)
          marca("ini-pratica", texto)
        }
      }
    } else if it.level == 4 and texto in ("Por quê", "Por quê e fonte") {
      context {
        if par-aberto.get() == none { panic("«" + texto + "» fora de um par: falta o marcador ou o «## P<n>» antes dela") }
        marca("fim-pratica", par-aberto.get())
      }
      vai-para("odd")
      context marca("ini-teoria", par-aberto.get())
    }
    it
  }
  livro
}

// Cada lado do par cabe numa página só, a prática começa numa par e a teoria é a ímpar seguinte: senão a compilação para.
// Com `--input diagnostico=1` a compilação não para: imprime no fim a lista de todos os pares que não cabem (só para medir).
#let confere-os-pares() = context {
  // A marca do fim de um lado, quando cai no alto de uma página (o título seguinte empurrou-a), vale pela página anterior.
  let pagina-da(m) = {
    let lugar = m.location().position()
    if m.value.tipo.starts-with("fim") and lugar.y <= 56pt { lugar.page - 1 } else { lugar.page }
  }
  let achadas = query(<marca-do-par>).map(m => (m.value, pagina-da(m)))
  let nomes = achadas.map(a => a.at(0).nome).dedup()
  let erros = ()
  for nome in nomes {
    let de(tipo) = achadas.find(a => a.at(0).nome == nome and a.at(0).tipo == tipo)
    let (ini-p, fim-p, ini-t, fim-t) = ("ini-pratica", "fim-pratica", "ini-teoria", "fim-teoria").map(tipo => {
      let achada = de(tipo)
      if achada == none { panic("o par «" + nome + "» não tem a marca «" + tipo + "»") }
      achada.at(1)
    })
    if ini-p != fim-p { erros.push("o par «" + nome + "»: a prática não cabe numa página só (começa na " + str(ini-p) + ", acaba na " + str(fim-p) + ")") }
    if calc.odd(ini-p) { erros.push("o par «" + nome + "»: a prática começa numa página ímpar, a " + str(ini-p)) }
    if ini-t != fim-t or ini-t != fim-p + 1 { erros.push("o par «" + nome + "»: a teoria não cabe na página ímpar seguinte (começa na " + str(ini-t) + ", acaba na " + str(fim-t) + ")") }
  }
  if sys.inputs.at("diagnostico", default: none) == none { for erro in erros { panic(erro) } }
  else { for erro in erros [DIAGNOSTICO #erro \ ] }
}
