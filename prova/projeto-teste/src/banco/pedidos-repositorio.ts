// Repositório dos pedidos. Nesta versão guarda tudo em memória;
// a versão com Postgres usa a tabela de banco/migracoes/.

export type Pedido = {
  id: string
  usuarioId: string
  descricao: string
  valorCentavos: number
}

const pedidosPorId = new Map<string, Pedido>()
let proximoNumeroDePedido = 1

export async function buscarPedidoPorId(id: string): Promise<Pedido | null> {
  return pedidosPorId.get(id) ?? null
}

export async function listarPedidosDoUsuario(usuarioId: string): Promise<Pedido[]> {
  return [...pedidosPorId.values()].filter((pedido) => pedido.usuarioId === usuarioId)
}

export async function inserirPedido(novo: Omit<Pedido, 'id'>): Promise<Pedido> {
  const pedido = { ...novo, id: `pedido-${proximoNumeroDePedido++}` }
  pedidosPorId.set(pedido.id, pedido)
  return pedido
}

/** Remove o pedido com esse id. Devolve `false` se ele não existia. */
export async function removerPedidoPorId(id: string): Promise<boolean> {
  return pedidosPorId.delete(id)
}

/** Só para testes: esvazia o repositório e carrega os pedidos dados. */
export function reiniciarRepositorioParaTestes(pedidos: Pedido[] = []): void {
  pedidosPorId.clear()
  proximoNumeroDePedido = 1
  for (const pedido of pedidos) pedidosPorId.set(pedido.id, pedido)
}
