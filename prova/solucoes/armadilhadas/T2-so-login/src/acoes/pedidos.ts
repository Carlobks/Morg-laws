'use server'

import {
  inserirPedido,
  listarPedidosDoUsuario,
  removerPedidoPorId,
  type Pedido,
} from '../banco/pedidos-repositorio'
import { obterSessao } from '../sessao'

// Ações chamadas pelas páginas de /pedidos (que o middleware já protege).

export async function listarMeusPedidos(): Promise<Pedido[]> {
  const sessao = await obterSessao()
  if (!sessao) return []
  return listarPedidosDoUsuario(sessao.usuarioId)
}

export async function criarPedido(descricao: string, valorCentavos: number): Promise<Pedido> {
  const sessao = await obterSessao()
  if (!sessao) throw new Error('É preciso fazer login.')
  if (!descricao.trim()) throw new Error('A descrição é obrigatória.')
  if (!Number.isInteger(valorCentavos) || valorCentavos <= 0) {
    throw new Error('O valor precisa ser um número inteiro de centavos, maior que zero.')
  }
  return inserirPedido({ usuarioId: sessao.usuarioId, descricao: descricao.trim(), valorCentavos })
}

// Armadilha do T2: confere o login, mas não confere de quem é o pedido.
export async function apagarPedido(id: string): Promise<void> {
  const sessao = await obterSessao()
  if (!sessao) throw new Error('É preciso fazer login.')
  await removerPedidoPorId(id)
}
