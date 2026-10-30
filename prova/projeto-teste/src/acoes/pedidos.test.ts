import { beforeEach, describe, expect, it } from 'vitest'
import { reiniciarRepositorioParaTestes } from '../banco/pedidos-repositorio'
import { definirUsuarioDaRequisicao } from '../infra/requisicao-simulada'
import { criarPedido, listarMeusPedidos } from './pedidos'

const USUARIO_UM = 'usuario-teste-1'
const USUARIO_DOIS = 'usuario-teste-2'

describe('ações dos pedidos', () => {
  beforeEach(() => {
    reiniciarRepositorioParaTestes()
    definirUsuarioDaRequisicao(null)
  })

  it('cria o pedido em nome de quem tem login', async () => {
    definirUsuarioDaRequisicao(USUARIO_UM)
    const pedido = await criarPedido('Caneca azul', 3500)
    expect(pedido.usuarioId).toBe(USUARIO_UM)
  })

  it('recusa criar sem login', async () => {
    await expect(criarPedido('Caneca azul', 3500)).rejects.toThrow()
  })

  it('lista só os pedidos de quem tem login', async () => {
    definirUsuarioDaRequisicao(USUARIO_UM)
    await criarPedido('Caneca azul', 3500)
    definirUsuarioDaRequisicao(USUARIO_DOIS)
    await criarPedido('Prato fundo', 2200)
    const meus = await listarMeusPedidos()
    expect(meus.map((pedido) => pedido.descricao)).toEqual(['Prato fundo'])
  })
})
