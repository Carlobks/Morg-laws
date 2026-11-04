// Lê o código JS/TS pela árvore do TypeScript, e não por expressões regulares: só a árvore distingue `{ data }`
// (declara `data`) de `{ data: faturasDoMes }` (declara `faturasDoMes`), e um uso de um nome da sua declaração.
// Usado pelos moldes de tamanho de função, nomes genéricos, nomes únicos e testes saltados.
import ts from 'typescript'

export const EXTENSOES_JS_E_TS = ['.ts', '.tsx', '.mts', '.cts', '.js', '.jsx', '.mjs', '.cjs']

export function eCodigoJsOuTs(caminho: string): boolean {
    return EXTENSOES_JS_E_TS.some((extensao) => caminho.toLowerCase().endsWith(extensao))
}

function tipoDoScript(caminho: string): ts.ScriptKind {
    if (/\.[jt]sx$/i.test(caminho)) return /\.tsx$/i.test(caminho) ? ts.ScriptKind.TSX : ts.ScriptKind.JSX
    return /\.[mc]?js$/i.test(caminho) ? ts.ScriptKind.JS : ts.ScriptKind.TS
}

/** A árvore de um arquivo, com os pais ligados (`no.parent`). */
export function lerArvore(caminho: string, texto: string): ts.SourceFile {
    return ts.createSourceFile(caminho, texto, ts.ScriptTarget.Latest, true, tipoDoScript(caminho))
}

/** Os nomes de uma ligação: `a`, `{ a, b: c }` → a, c; `[d, ...e]` → d, e. */
function nomesDaLigacao(ligacao: ts.BindingName): string[] {
    if (ts.isIdentifier(ligacao)) return [ligacao.text]
    return ligacao.elements.flatMap((elemento) => (ts.isOmittedExpression(elemento) ? [] : nomesDaLigacao(elemento.name)))
}

const DECLARACOES_COM_NOME: Array<(no: ts.Node) => boolean> = [
    ts.isFunctionDeclaration, ts.isClassDeclaration, ts.isInterfaceDeclaration, ts.isTypeAliasDeclaration,
    ts.isEnumDeclaration, ts.isFunctionExpression, ts.isClassExpression, ts.isMethodDeclaration,
    ts.isPropertyDeclaration, ts.isGetAccessorDeclaration, ts.isSetAccessorDeclaration,
    // Os membros de uma interface, de um tipo ou de um enum, como os campos de uma classe no Python (`data: str`,
    // `data = 1` num Enum).
    ts.isPropertySignature, ts.isMethodSignature, ts.isEnumMember,
]

/** Os nomes que este nó declara (nenhum, se não for uma declaração). */
export function nomesDeclaradosPeloNo(no: ts.Node): string[] {
    if (ts.isVariableDeclaration(no) || ts.isParameter(no)) return nomesDaLigacao(no.name)
    if (!DECLARACOES_COM_NOME.some((eDoTipo) => eDoTipo(no))) return []
    const nome = (no as ts.NamedDeclaration).name
    return nome && ts.isIdentifier(nome) ? [nome.text] : []
}

/** Todos os nomes declarados no arquivo, a qualquer nível, um por declaração. */
export function todosOsNomesDeclarados(arvore: ts.SourceFile): string[] {
    const nomes: string[] = []
    const visitar = (no: ts.Node): void => {
        nomes.push(...nomesDeclaradosPeloNo(no))
        ts.forEachChild(no, visitar)
    }
    visitar(arvore)
    return nomes
}

/** Os nomes declarados no topo do arquivo, sem repetir. */
export function nomesDoTopoTs(arvore: ts.SourceFile): Set<string> {
    const instrucoes = arvore.statements.flatMap((instrucao): ts.Node[] => (ts.isVariableStatement(instrucao)
        ? [...instrucao.declarationList.declarations] : [instrucao]))
    return new Set(instrucoes.flatMap(nomesDeclaradosPeloNo))
}

/** A linha (a partir de 1) de uma posição do texto. */
export function linhaDaPosicao(arvore: ts.SourceFile, posicao: number): number {
    return arvore.getLineAndCharacterOfPosition(posicao).line + 1
}
