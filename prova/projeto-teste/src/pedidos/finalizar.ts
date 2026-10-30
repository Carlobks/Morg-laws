import { montarResumoDoCarrinho, type ResumoDoCarrinho } from './resumo'
import { calcularTotal, type Carrinho } from './total'

export type CompraFinalizada = {
  /** O que o cliente viu na última tela. */
  resumo: ResumoDoCarrinho
  /** O que vai para o meio de pagamento. */
  valorCobradoCentavos: number
}

export function finalizarCompra(carrinho: Carrinho): CompraFinalizada {
  const resumo = montarResumoDoCarrinho(carrinho)
  const valorCobradoCentavos = calcularTotal(carrinho)
  return { resumo, valorCobradoCentavos }
}
