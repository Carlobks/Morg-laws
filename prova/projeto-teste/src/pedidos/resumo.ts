import { calcularPartesDoTotal, calcularSubtotal, type Carrinho } from './total'

export type ResumoDoCarrinho = {
  subtotalSemCupomCentavos: number
  descontoCentavos: number
  freteCentavos: number
  totalCentavos: number
}

/** O que a tela do carrinho mostra antes de confirmar o pedido. */
export function montarResumoDoCarrinho(carrinho: Carrinho): ResumoDoCarrinho {
  const subtotalSemCupomCentavos = calcularSubtotal(carrinho.itens)
  const partes = calcularPartesDoTotal(carrinho)
  return {
    subtotalSemCupomCentavos,
    descontoCentavos: subtotalSemCupomCentavos - partes.subtotalCentavos,
    freteCentavos: partes.freteCentavos,
    totalCentavos: partes.totalCentavos,
  }
}
