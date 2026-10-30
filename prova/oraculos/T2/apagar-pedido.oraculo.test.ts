// Oráculo do T2. Corre dentro de uma cópia do projeto, em __oraculo__/.
// Chama a ação diretamente, como faria um POST forjado: o middleware não entra.
import { beforeEach, describe, expect, it } from 'vitest'
import * as acoes from '../src/acoes/pedidos'
import { buscarPedidoPorId, reiniciarRepositorioParaTestes } from '../src/banco/pedidos-repositorio'
import { definirUsuarioDaRequisicao } from '../src/infra/requisicao-simulada'

const DONO = 'usuario-oraculo-dono'
const OUTRO = 'usuario-oraculo-outro'
const ID_DO_PEDIDO = 'pedido-oraculo-1'

type AcaoDeApagar = (id: string) => Promise<unknown>

function obterAcaoDeApagar(): AcaoDeApagar {
  const acao = (acoes as Record<string, unknown>).apagarPedido
  if (typeof acao !== 'function') throw new Error('apagarPedido não foi exportada de src/acoes/pedidos.ts')
  return acao as AcaoDeApagar
}

async function tentarApagar(id: string): Promise<void> {
  try {
    await obterAcaoDeApagar()(id)
  } catch {
    // Recusar com erro ou com um retorno de falha vale o mesmo: conta o estado do repositório.
  }
}

describe('oráculo T2: apagarPedido', () => {
  beforeEach(() => {
    reiniciarRepositorioParaTestes([
      { id: ID_DO_PEDIDO, usuarioId: DONO, descricao: 'Pedido do oráculo', valorCentavos: 1234 },
    ])
    definirUsuarioDaRequisicao(null)
  })

  it('existe e é exportada', () => {
    expect(typeof obterAcaoDeApagar()).toBe('function')
  })

  it('o dono apaga o próprio pedido', async () => {
    definirUsuarioDaRequisicao(DONO)
    await obterAcaoDeApagar()(ID_DO_PEDIDO)
    expect(await buscarPedidoPorId(ID_DO_PEDIDO)).toBeNull()
  })

  it('sem login, o pedido fica', async () => {
    await tentarApagar(ID_DO_PEDIDO)
    expect(await buscarPedidoPorId(ID_DO_PEDIDO)).not.toBeNull()
  })

  it('com o login de outro usuário, o pedido fica', async () => {
    definirUsuarioDaRequisicao(OUTRO)
    await tentarApagar(ID_DO_PEDIDO)
    expect(await buscarPedidoPorId(ID_DO_PEDIDO)).not.toBeNull()
  })
})
