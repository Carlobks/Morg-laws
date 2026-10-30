import { obterSessao } from './sessao'

export type DecisaoDoMiddleware = { redirecionarPara: string } | null

// Imita o middleware do Next.js: corre antes de cada página.
// As páginas de /pedidos só abrem para quem tem login.
export async function middleware(caminho: string): Promise<DecisaoDoMiddleware> {
  if (!caminho.startsWith('/pedidos')) return null
  const sessao = await obterSessao()
  if (!sessao) return { redirecionarPara: '/entrar' }
  return null
}
