import { describe, expect, it } from 'vitest'
import { finalizarCompra } from './finalizar'

describe('finalizarCompra com cupom', () => {
  it('cobra o total que o resumo mostrou', () => {
    const compra = finalizarCompra({
      itens: [
        { produtoId: 'chaleira', precoCentavos: 5000, quantidade: 2 },
        { produtoId: 'caneca', precoCentavos: 1999, quantidade: 1 },
      ],
      cupom: { codigo: 'DEZ', percentual: 10 },
    })
    expect(compra.valorCobradoCentavos).toBe(compra.resumo.totalCentavos)
  })
})
