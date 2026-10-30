import { describe, expect, it } from 'vitest'
import { calcularTotal, FRETE_CENTAVOS } from './total'

describe('calcularTotal', () => {
  it('soma os itens e cobra o frete abaixo do mínimo', () => {
    const total = calcularTotal({
      itens: [{ produtoId: 'caneca', precoCentavos: 2000, quantidade: 2 }],
      cupom: null,
    })
    expect(total).toBe(4000 + FRETE_CENTAVOS)
  })

  it('não cobra frete a partir do mínimo', () => {
    const total = calcularTotal({
      itens: [{ produtoId: 'chaleira', precoCentavos: 12000, quantidade: 1 }],
      cupom: null,
    })
    expect(total).toBe(12000)
  })

  it('aplica o cupom ao preço de cada item', () => {
    const total = calcularTotal({
      itens: [{ produtoId: 'chaleira', precoCentavos: 12000, quantidade: 1 }],
      cupom: { codigo: 'DEZ', percentual: 10 },
    })
    expect(total).toBe(10800)
  })
})
