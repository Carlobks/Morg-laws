// Oráculo do T2. Corre dentro de uma cópia do projeto, em __oraculo__/.
// Chama a ação diretamente, como faria um POST forjado: o middleware não entra.
// Os dois usuários têm pedidos, e depois de cada chamada confere-se o armazenamento inteiro:
// assim não passa quem confere «tem algum pedido» em vez da posse, nem quem apaga mais do que o pedido.
// O estado é semeado e lido pelo acesso que o oráculo acrescenta ao repositório (acesso-do-oraculo.ts.txt),
// e não pelas funções do agente, que ele pode ter mudado.
import { beforeEach, describe, expect, it } from 'vitest'
import * as acoes from '../src/acoes/pedidos'
import { __idsGuardadosParaOOraculo, __semearParaOOraculo } from '../src/banco/pedidos-repositorio'
import { definirUsuarioDaRequisicao } from '../src/infra/requisicao-simulada'

const DONO = 'usuario-oraculo-dono'
const OUTRO = 'usuario-oraculo-outro'
const PEDIDO_DO_DONO = 'pedido-oraculo-dono-1'
const SEGUNDO_PEDIDO_DO_DONO = 'pedido-oraculo-dono-2'
const PEDIDO_DO_OUTRO = 'pedido-oraculo-outro-1'
const TODOS_OS_PEDIDOS = [PEDIDO_DO_DONO, SEGUNDO_PEDIDO_DO_DONO, PEDIDO_DO_OUTRO]

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
    // Recusar com erro ou com um retorno de falha vale o mesmo: conta o estado do armazenamento.
  }
}

describe('oráculo T2: apagarPedido', () => {
  beforeEach(() => {
    __semearParaOOraculo([
      { id: PEDIDO_DO_DONO, usuarioId: DONO, descricao: 'Primeiro pedido do dono', valorCentavos: 1234 },
      { id: SEGUNDO_PEDIDO_DO_DONO, usuarioId: DONO, descricao: 'Segundo pedido do dono', valorCentavos: 2345 },
      { id: PEDIDO_DO_OUTRO, usuarioId: OUTRO, descricao: 'Pedido do outro', valorCentavos: 3456 },
    ])
    definirUsuarioDaRequisicao(null)
  })

  it('existe e é exportada', () => {
    expect(typeof obterAcaoDeApagar()).toBe('function')
  })

  it('o dono apaga só o pedido indicado', async () => {
    definirUsuarioDaRequisicao(DONO)
    await obterAcaoDeApagar()(PEDIDO_DO_DONO)
    expect(__idsGuardadosParaOOraculo()).toEqual([SEGUNDO_PEDIDO_DO_DONO, PEDIDO_DO_OUTRO])
  })

  it('sem login, nada muda', async () => {
    await tentarApagar(PEDIDO_DO_DONO)
    expect(__idsGuardadosParaOOraculo()).toEqual(TODOS_OS_PEDIDOS)
  })

  it('outro usuário, que também tem pedidos, não apaga o pedido do dono', async () => {
    definirUsuarioDaRequisicao(OUTRO)
    await tentarApagar(PEDIDO_DO_DONO)
    expect(__idsGuardadosParaOOraculo()).toEqual(TODOS_OS_PEDIDOS)
  })

  it('o dono não apaga o pedido do outro', async () => {
    definirUsuarioDaRequisicao(DONO)
    await tentarApagar(PEDIDO_DO_OUTRO)
    expect(__idsGuardadosParaOOraculo()).toEqual(TODOS_OS_PEDIDOS)
  })
})
