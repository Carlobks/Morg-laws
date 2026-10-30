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

describe('cupom de 10%', () => {
  it('aplica o desconto a mais de um item', () => {
    const total = calcularTotal({
      itens: [
        { produtoId: 'chaleira', precoCentavos: 5000, quantidade: 2 },
        { produtoId: 'caneca', precoCentavos: 1999, quantidade: 1 },
      ],
      cupom: { codigo: 'DEZ', percentual: 10 },
    })
    expect(total).toBe(10799)
  })
})
