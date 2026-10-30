import { beforeEach, describe, expect, it } from 'vitest'
import { buscarPedidoPorId, reiniciarRepositorioParaTestes } from '../banco/pedidos-repositorio'
import { definirUsuarioDaRequisicao } from '../infra/requisicao-simulada'
import { apagarPedido } from './pedidos'

const DONO = 'usuario-teste-1'
const OUTRO = 'usuario-teste-2'

describe('apagarPedido', () => {
  beforeEach(() => {
    reiniciarRepositorioParaTestes([
      { id: 'pedido-1', usuarioId: DONO, descricao: 'Caneca azul', valorCentavos: 3500 },
    ])
  })

  it('o dono apaga o próprio pedido', async () => {
    definirUsuarioDaRequisicao(DONO)
    await apagarPedido('pedido-1')
    expect(await buscarPedidoPorId('pedido-1')).toBeNull()
  })

  it('sem login, recusa e o pedido fica', async () => {
    definirUsuarioDaRequisicao(null)
    await expect(apagarPedido('pedido-1')).rejects.toThrow()
    expect(await buscarPedidoPorId('pedido-1')).not.toBeNull()
  })

  it('outro usuário não apaga o pedido alheio', async () => {
    definirUsuarioDaRequisicao(OUTRO)
    await expect(apagarPedido('pedido-1')).rejects.toThrow()
    expect(await buscarPedidoPorId('pedido-1')).not.toBeNull()
  })
})
