import { lerUsuarioDaRequisicao } from './infra/requisicao-simulada'

export type Sessao = {
  usuarioId: string
}

/** Devolve a sessão de quem fez a requisição, ou `null` se não houver login. */
export async function obterSessao(): Promise<Sessao | null> {
  const usuarioId = lerUsuarioDaRequisicao()
  if (!usuarioId) return null
  return { usuarioId }
}
