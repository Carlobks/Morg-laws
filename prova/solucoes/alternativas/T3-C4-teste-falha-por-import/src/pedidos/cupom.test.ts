import { expect, it } from 'vitest'
import { aplicarCupom } from './total'

it('o cupom de 10% baixa o preço de cada item', () => {
  const itens = aplicarCupom([{ produtoId: 'caneca', precoCentavos: 2000, quantidade: 1 }], { codigo: 'DEZ', percentual: 10 })
  expect(itens[0].precoCentavos).toBe(1800)
})
