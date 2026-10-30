// Regras do total do carrinho. Todos os valores em centavos.

export type ItemDoCarrinho = {
  produtoId: string
  precoCentavos: number
  quantidade: number
}

export type Cupom = {
  codigo: string
  /** Desconto em percentagem, de 1 a 100, aplicado ao preço de cada item. */
  percentual: number
}

export type Carrinho = {
  itens: ItemDoCarrinho[]
  cupom: Cupom | null
}

export const FRETE_CENTAVOS = 1500
/** O frete é grátis quando o subtotal, já com o cupom, chega a este valor. */
export const FRETE_GRATIS_A_PARTIR_DE_CENTAVOS = 10000

// Devolve itens novos: mudar os do carrinho fazia o cupom valer duas vezes
// quando o total era calculado de novo (resumo e depois cobrança).
function aplicarCupom(itens: ItemDoCarrinho[], cupom: Cupom | null): ItemDoCarrinho[] {
  if (!cupom) return itens
  return itens.map((item) => ({
    ...item,
    precoCentavos: Math.round((item.precoCentavos * (100 - cupom.percentual)) / 100),
  }))
}

export function calcularSubtotal(itens: ItemDoCarrinho[]): number {
  return itens.reduce((soma, item) => soma + item.precoCentavos * item.quantidade, 0)
}

export function calcularFrete(subtotalCentavos: number): number {
  return subtotalCentavos >= FRETE_GRATIS_A_PARTIR_DE_CENTAVOS ? 0 : FRETE_CENTAVOS
}

export type PartesDoTotal = {
  /** Subtotal dos itens, já com o cupom. */
  subtotalCentavos: number
  freteCentavos: number
  totalCentavos: number
}

export function calcularPartesDoTotal(carrinho: Carrinho): PartesDoTotal {
  const itens = aplicarCupom(carrinho.itens, carrinho.cupom)
  const subtotalCentavos = calcularSubtotal(itens)
  const freteCentavos = calcularFrete(subtotalCentavos)
  return { subtotalCentavos, freteCentavos, totalCentavos: subtotalCentavos + freteCentavos }
}

/** Total a pagar: itens com o cupom aplicado, mais o frete. */
export function calcularTotal(carrinho: Carrinho): number {
  return calcularPartesDoTotal(carrinho).totalCentavos
}
