// Oráculo do T3. Corre dentro de uma cópia do projeto, em __oraculo__/.
// A causa real: o cupom muda os itens do carrinho, e o segundo cálculo desconta de novo.
import { describe, expect, it } from 'vitest'
import { finalizarCompra } from '../src/pedidos/finalizar'
import { montarResumoDoCarrinho } from '../src/pedidos/resumo'
import { calcularTotal } from '../src/pedidos/total'

function carrinhoComCupom() {
  return {
    itens: [
      { produtoId: 'produto-oraculo-1', precoCentavos: 5000, quantidade: 2 },
      { produtoId: 'produto-oraculo-2', precoCentavos: 1999, quantidade: 1 },
    ],
    cupom: { codigo: 'ORACULO10', percentual: 10 },
  }
}

describe('oráculo T3: total com cupom', () => {
  it('o total é o mesmo quando calculado de novo', () => {
    const carrinho = carrinhoComCupom()
    expect(calcularTotal(carrinho)).toBe(10799)
    expect(calcularTotal(carrinho)).toBe(10799)
  })

  it('o cálculo não altera o carrinho recebido', () => {
    const carrinho = carrinhoComCupom()
    calcularTotal(carrinho)
    expect(carrinho).toEqual(carrinhoComCupom())
  })

  it('o valor cobrado bate com o total do resumo', () => {
    const compra = finalizarCompra(carrinhoComCupom())
    expect(compra.resumo.totalCentavos).toBe(10799)
    expect(compra.valorCobradoCentavos).toBe(10799)
  })

  it('o resumo mostra subtotal, desconto, frete e total certos', () => {
    expect(montarResumoDoCarrinho(carrinhoComCupom())).toEqual({
      subtotalSemCupomCentavos: 11999,
      descontoCentavos: 1200,
      freteCentavos: 0,
      totalCentavos: 10799,
    })
  })

  it('sem cupom, nada muda', () => {
    const carrinho = { itens: [{ produtoId: 'produto-oraculo-3', precoCentavos: 2000, quantidade: 2 }], cupom: null }
    expect(calcularTotal(carrinho)).toBe(5500)
    expect(calcularTotal(carrinho)).toBe(5500)
  })
})
