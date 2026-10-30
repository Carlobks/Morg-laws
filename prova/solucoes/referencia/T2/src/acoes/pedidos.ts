'use server'

import {
  buscarPedidoPorId,
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

// Uma ação do servidor é um endpoint público: o middleware não corre para ela,
// por isso a sessão e a posse são conferidas aqui dentro.
export async function apagarPedido(id: string): Promise<void> {
  const sessao = await obterSessao()
  if (!sessao) throw new Error('É preciso fazer login.')
  const pedido = await buscarPedidoPorId(id)
  if (!pedido || pedido.usuarioId !== sessao.usuarioId) {
    throw new Error('Pedido não encontrado.')
  }
  await removerPedidoPorId(id)
}
