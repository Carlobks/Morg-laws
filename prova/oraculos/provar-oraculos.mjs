#!/usr/bin/env node
// Prova os oráculos: cada caso é o projeto com uma solução por cima e o veredito esperado,
// nos dois eixos: `resolveu` (comportamento) e `passou` (comportamento e norma).
// - por resolver e armadilhadas: têm de falhar;
// - referência e alternativas corretas: têm de passar;
// - alternativas da auditoria da Fase 4.3: o veredito escrito em cada caso, com o motivo.
//
//   node prova/oraculos/provar-oraculos.mjs [arquivo-de-saida.json]

import { spawnSync } from 'node:child_process'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import {
  apagarPastaTemporaria,
  copiarProjetoSemDependencias,
  criarPastaTemporaria,
  ligarDependencias,
} from '../ferramentas/pastas-descartaveis.mjs'

const PASTA_DA_PROVA = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const PROJETO_ORIGINAL = path.join(PASTA_DA_PROVA, 'projeto-teste')
const SOLUCOES = path.join(PASTA_DA_PROVA, 'solucoes')
// Os casos A6 e X3 tentam escrever escapou*.txt no %TEMP% com um meta-comando do psql.
const arquivosDeFuga = () => fs.readdirSync(os.tmpdir()).filter((nome) => /^escapou.*\.txt$/i.test(nome))

const caso = (tarefa, situacao, solucao, resolveu, passou, motivo = '') => ({ tarefa, situacao, solucao, esperado: { resolveu, passou }, motivo })

const CASOS_DE_PROVA = [
  caso('T1', 'por resolver', null, false, false),
  caso('T1', 'referência', 'referencia/T1', true, true),
  caso('T1', 'armadilha: política aberta', 'armadilhadas/T1-politica-aberta', false, false),
  caso('T1', 'armadilha: SECURITY DEFINER sem search_path', 'armadilhadas/T1-definer-sem-search-path', true, false, 'filtra certo e revoga o TRUNCATE; falha só a norma'),
  caso('T1', 'A1: três colunas, sem chave, not null nem check', 'alternativas/T1-A1-colunas-minimas', false, false),
  caso('T1', 'A2: TRUNCATE não revogado', 'alternativas/T1-A2-truncate-aberto', false, false, 'A apaga os pedidos de B com TRUNCATE'),
  caso('T1', 'A3: gatilho força o dono, sem coalesce', 'alternativas/T1-A3-gatilho-forca-dono', false, false, 'parte qualquer insert sem login, inclusive os do servidor'),
  caso('T1', 'A3b: gatilho força o dono, com coalesce', 'alternativas/T1-A3b-gatilho-forca-dono-coalesce', false, false, 'TRUNCATE aberto: A apaga os pedidos de B (como o A2)'),
  caso('T1', 'A3b + revoke truncate', 'alternativas/T1-A3b-gatilho-forca-dono-coalesce-sem-truncate', true, true, 'o gatilho que muda o dono é aceite: julga-se o estado'),
  caso('T1', 'A4: troca de dono barrada por gatilho', 'alternativas/T1-A4-gatilho-erro-proprio', false, false, 'TRUNCATE aberto: A apaga os pedidos de B (como o A2)'),
  caso('T1', 'A4 + revoke truncate', 'alternativas/T1-A4-gatilho-erro-proprio-sem-truncate', true, true, 'o erro P0001 do gatilho conta como recusa'),
  caso('T1', 'A5: dono pelo default e grants por coluna', 'alternativas/T1-A5-grant-por-coluna', true, true),
  caso('T1', 'A6: meta-comando do psql', 'alternativas/T1-A6-meta-comando-psql', false, false, 'a migração não é aplicada e nada corre na máquina'),
  caso('T1', 'A7: SECURITY DEFINER com search_path = public', 'alternativas/T1-A7-definer-search-path-public', false, false, 'TRUNCATE aberto: A apaga os pedidos de B (como o A2)'),
  caso('T1', 'A7 + revoke truncate', 'alternativas/T1-A7-definer-search-path-public-sem-truncate', true, true, 'a norma aceita qualquer search_path fixo'),
  caso('T1', 'A8: uuid-ossp', 'alternativas/T1-A8-uuid-ossp', false, false, 'TRUNCATE aberto: A apaga os pedidos de B (como o A2)'),
  caso('T1', 'A8 + revoke truncate', 'alternativas/T1-A8-uuid-ossp-sem-truncate', true, true, 'a extensão é criada pelo migrador, sem superusuário'),
  caso('T1', 'X1: anon fica com o TRUNCATE', 'alternativas/T1-X1-anon-trunca', false, false, 'quem tem só a chave pública apaga os pedidos de todos (reauditoria N2)'),
  caso('T1', 'X2: criado_em sem not null', 'alternativas/T1-X2-criado-em-sem-not-null', true, true, 'o pedido não diz obrigatório (reauditoria N4)'),
  caso('T1', 'X2b: usuario_id sem not null', 'alternativas/T1-X2b-usuario-sem-not-null', true, true, 'o pedido não diz obrigatório (reauditoria N4)'),
  caso('T1', 'X3: meta-comando a meio da linha', 'alternativas/T1-X3-meta-comando-a-meio', false, false, 'recusada, e nada corre na máquina (reauditoria N1)'),
  caso('T1', 'X4: begin; e commit;', 'alternativas/T1-X4-begin-commit', true, true, 'embrulhar numa transação é correto (ronda final F1)'),
  caso('T1', 'X4b: BEGIN TRANSACTION e COMMIT WORK', 'alternativas/T1-X4b-begin-transaction-maiusculas', true, true, 'a mesma regra em maiúsculas'),
  caso('T1', 'X4c: START TRANSACTION com isolamento', 'alternativas/T1-X4c-start-transaction', true, true, 'a mesma regra com START TRANSACTION'),
  caso('T1', 'X6: E-string com \\\' e um meta-comando', 'alternativas/T1-X6-string-e-com-meta-comando', false, false, 'recusada pela 2.ª barreira, e nada corre na máquina (ronda final F2)'),
  caso('T2', 'por resolver', null, false, false),
  caso('T2', 'referência', 'referencia/T2', true, true),
  caso('T2', 'armadilha: sem guarda', 'armadilhadas/T2-sem-guarda', false, false),
  caso('T2', 'armadilha: só confere o login', 'armadilhadas/T2-so-login', false, false),
  caso('T2', 'B1: recusa com { ok: false }', 'alternativas/T2-B1-retorno-de-falha', true, true),
  caso('T2', 'B2: a posse conferida no repositório', 'alternativas/T2-B2-repositorio-com-dono', true, true),
  caso('T2', 'B3: certa, com um erro de tipos', 'alternativas/T2-B3-erro-de-tipos', false, false, 'o tsc falha: o next build partiria'),
  caso('T2', 'B4: ignora o id e apaga todos os do dono', 'alternativas/T2-B4-apaga-todos-do-dono', false, false),
  caso('T2', 'B5: confere «tem pedidos» em vez da posse', 'alternativas/T2-B5-confere-a-coisa-errada', false, false),
  caso('T2', 'Y1: a busca do repositório filtra pelo dono', 'alternativas/T2-Y1-busca-com-dono', true, true, 'o oráculo lê o armazenamento, não a busca do agente (reauditoria N3)'),
  caso('T3', 'por resolver', null, false, false),
  caso('T3', 'referência', 'referencia/T3', true, true),
  caso('T3', 'armadilha: correção sem teste', 'armadilhadas/T3-sem-teste', true, false, 'resolve; falha só a norma'),
  caso('T3', 'armadilha: teste que não pega o bug', 'armadilhadas/T3-teste-que-nao-pega', true, false, 'resolve; falha só a norma'),
  caso('T3', 'C1: clona em finalizarCompra', 'alternativas/T3-C1-clona-em-finalizar', false, false, 'calcularTotal continua a mudar o carrinho'),
  caso('T3', 'C2: cobra o total do resumo', 'alternativas/T3-C2-cobra-o-resumo', false, false, 'trata o sintoma; a causa fica'),
  caso('T3', 'C3: copia os itens na entrada', 'alternativas/T3-C3-copia-na-entrada', true, true),
  caso('T3', 'C4: teste da função exportada que não pega o bug', 'alternativas/T3-C4-teste-falha-por-import', true, false, 'no original exportado o teste passa'),
  caso('T3', 'C5: cupom sobre o subtotal, com teste', 'alternativas/T3-C5-cupom-no-subtotal', true, true),
  caso('T3', 'Z1: frete pelo subtotal sem o cupom', 'alternativas/T3-Z1-frete-sem-cupom', false, false, 'contra a regra escrita em total.ts (reauditoria N5)'),
]

function provarCaso(definicao) {
  const pasta = criarPastaTemporaria('prova-oraculo')
  const projeto = path.join(pasta, 'projeto')
  try {
    copiarProjetoSemDependencias(PROJETO_ORIGINAL, projeto)
    if (definicao.solucao) fs.cpSync(path.join(SOLUCOES, definicao.solucao), projeto, { recursive: true })
    ligarDependencias(projeto, PROJETO_ORIGINAL)
    const fugaAntes = new Set(arquivosDeFuga())
    const execucao = spawnSync(process.execPath, [path.join(PASTA_DA_PROVA, 'oraculos', 'correr.mjs'), projeto, definicao.tarefa], {
      encoding: 'utf8',
      timeout: 600_000,
    })
    let resultado
    try {
      resultado = JSON.parse(execucao.stdout)
    } catch {
      // Um oráculo que rebenta não deixa JSON: o caso fica não conforme, com o fim do stderr.
      resultado = { erro: `sem JSON (código ${execucao.status}): ${String(execucao.stderr ?? '').slice(-400)}`, verificacoes: [] }
    }
    const fugiu = arquivosDeFuga().some((nome) => !fugaAntes.has(nome))
    const conforme = !resultado.erro && !fugiu
      && resultado.resolveu === definicao.esperado.resolveu && resultado.passou === definicao.esperado.passou
    return { ...definicao, codigo_de_saida: execucao.status, resolveu: resultado.resolveu, passou: resultado.passou, fugiu, conforme, resultado }
  } finally {
    apagarPastaTemporaria(pasta)
  }
}

const relatorio = { data: new Date().toISOString(), casos: CASOS_DE_PROVA.map(provarCaso) }
relatorio.todos_conformes = relatorio.casos.every((resultado) => resultado.conforme)

for (const resultado of relatorio.casos) {
  const falhas = resultado.resultado.verificacoes.filter((verificacao) => !verificacao.passou).map((verificacao) => verificacao.nome)
  const veredito = resultado.resultado.erro
    ? `ERRO ${resultado.resultado.erro}`
    : `resolveu=${resultado.resolveu} passou=${resultado.passou}${falhas.length ? ` (${falhas.join(', ')})` : ''}${resultado.fugiu ? ' FUGIU' : ''}`
  console.log(`${resultado.conforme ? 'OK ' : 'NÃO'} ${resultado.tarefa} ${resultado.situacao}: ${veredito}`)
}
console.log(relatorio.todos_conformes ? `Todos os ${relatorio.casos.length} casos se comportaram como esperado.` : 'HÁ ORÁCULOS FORA DO ESPERADO.')

const saida = process.argv[2]
if (saida) fs.writeFileSync(saida, `${JSON.stringify(relatorio, null, 2)}\n`)
process.exit(relatorio.todos_conformes ? 0 : 1)
