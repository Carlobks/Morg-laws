// Imita o que o Next.js guarda sobre a requisição atual (cookies e cabeçalhos).
// Aqui fica só o id do usuário que fez login; os testes escolhem quem é.

let usuarioDaRequisicaoAtual: string | null = null

export function definirUsuarioDaRequisicao(usuarioId: string | null): void {
  usuarioDaRequisicaoAtual = usuarioId
}

export function lerUsuarioDaRequisicao(): string | null {
  return usuarioDaRequisicaoAtual
}
