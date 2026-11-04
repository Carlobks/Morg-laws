---
name: codigo-legivel
description: Diz as regras da forma do código que um agente escreve — arquivo até 500 linhas, função nova até 20, nomes únicos e pesquisáveis, nada de nome genérico, nenhum alarme calado sem motivo, nenhum teste saltado sem condição, os testes num só comando — com o porquê de cada uma e o teste pronto que a impõe em Python e em TypeScript (vitest), e como adotar esses testes num projeto que já viola, com uma linha de base que só encolhe. Usar quando um arquivo ou uma função crescem demais ou é preciso parti-los, ao escolher um nome, antes de calar um aviso do lint ou de saltar um teste, ou ao instalar os testes prontos num projeto. Não usar para provar que um trabalho funciona ou corrigir um bug (é a testes-e-provas), nem para os commits (é a git-e-commits).
---

# Código legível

O agente lê o código para o mudar. Arquivo grande, função longa e nome genérico fazem-no ler de mais, editar o
lugar errado ou repetir o que já existe. Cada regra abaixo tem o porquê e o teste pronto que a impõe: texto é
conselho, e o que tem de ser cumprido vira teste.

## 1. As regras

| Regra | Porquê | Teste em Python | Teste em TypeScript |
|---|---|---|---|
| **Arquivo até 500 linhas** | Um arquivo grande mistura responsabilidades, e o agente lê-o inteiro para mudar uma linha | [`test_tamanho_dos_arquivos.py`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes/test_tamanho_dos_arquivos.py) | [`tamanho-de-arquivo.test.ts`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes-ts/tamanho-de-arquivo.test.ts) |
| **Função nova até 20 linhas** | Uma função curta faz uma coisa só; a mudança acerta à primeira e o teste dela é pequeno | [`test_tamanho_das_funcoes.py`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes/test_tamanho_das_funcoes.py) | [`tamanho-de-funcao.test.ts`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes-ts/tamanho-de-funcao.test.ts) |
| **Nada de nome genérico** (`data`, `utils`, `helper`, `info`, `dados`…) | Não diz o que guarda e dá dezenas de resultados no `grep` | [`test_nomes.py`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes/test_nomes.py) | [`nomes-genericos.test.ts`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes-ts/nomes-genericos.test.ts) |
| **Nomes únicos** (de topo e de arquivo) | Duas funções `calcular` ou dois `pedido.ts`: o agente edita o errado | [`test_nomes_unicos.py`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes/test_nomes_unicos.py) | [`nomes-unicos.test.ts`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes-ts/nomes-unicos.test.ts) |
| **Nenhum alarme calado sem motivo** (`noqa`, `eslint-disable`, `@ts-expect-error`…) | Um alarme calado sem motivo esconde o seguinte | [`test_alarmes.py`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes/test_alarmes.py) | [`alarmes.test.ts`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes-ts/alarmes.test.ts) |
| **Nenhum teste saltado sem condição** (nem `.only`) | Um teste saltado para sempre deixa de proteger, e ninguém volta a ele | [`test_testes_saltados.py`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes/test_testes_saltados.py) | [`testes-saltados.test.ts`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes-ts/testes-saltados.test.ts) |
| **Testes num só comando** | Quem não sabe como rodar tudo roda só uma parte; o hook do commit e o CI chamam o mesmo comando | `COMANDO_DOS_TESTES` do [`pre-commit`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/git/hooks/pre-commit) | o mesmo (`npx vitest run`) |

As duas línguas têm os mesmos limites e as mesmas listas, e um teste do Morg-laws corre a mesma pasta de casos
pelos dois moldes de cada regra e exige o mesmo veredito.

## 2. Como cumprir cada uma

- **Arquivo grande:** divida por responsabilidade (o cálculo, a leitura, a tela), não por tamanho. Encolher um
  arquivo antigo é sempre permitido.
- **Função longa:** conta-se da linha onde começa à linha onde fecha, com as linhas em branco e os comentários
  (os decoradores não). Extraia os passos com nomes que dizem o quê. Num teste, o `it` conta, como um método; o
  `describe` não, como uma classe.
- **Nome genérico:** troque pelo que a coisa guarda (`const { data: faturasDoMes } = …`, `pedido_pago`). Vale para
  variáveis, parâmetros, funções, classes, arquivos e pastas. Um nome composto que diz o quê (`bar_helper.py`, o
  ajudante da barra) não é genérico.
- **Nome repetido:** antes de criar, `git grep -n "<nome>"`. Ficam de fora o que a língua impõe (`__init__`,
  `main`, `__x__`) e os nomes de uma interface comum de propósito, que o projeto lista no bloco «Ajuste ao projeto»
  (no Next.js, `page.tsx` e `GET`).
- **Alarme:** corrija o que ele aponta. Se não der, o motivo vai na mesma linha, depois de « — »
  (`// eslint-disable-line no-console — o CLI escreve no terminal`). A contagem por tipo, no projeto inteiro, não
  sobe: um alarme novo justificado sobe a linha de base e leva a linha `Alarme-novo: <motivo>` na mensagem do
  commit. O commit-msg confere-a na máquina e o CI de novo, commit a commit (sem os merges: numa PR, o merge de
  teste não a traz e não é acusado; e uma base apagada num commit e recriada mais alta no seguinte conta contra a
  última conhecida); nas duas línguas é a mesma regra.
  Mudar um alarme de arquivo não sobe nada.
- **Teste saltado:** diga quando e porquê. No vitest: `it.skipIf(semRede)(…)`, ou, dentro do teste,
  `contexto.skip(semRede, 'precisa da rede')` ou `if (semRede) contexto.skip('precisa da rede')`. **Não** use
  `test.skip(semRede, '…')` nem as opções `{ skip: true }` ou `{ only: true }` do teste: no vitest o 1.º argumento
  de `test.skip` é o nome do teste, e ele salta sempre
  ([API do vitest](https://vitest.dev/api/test)); é a forma do Playwright. No Python:
  `@unittest.skipIf(sys.platform == "win32", "o hook só corre em sh")`, ou o `skipTest` dentro de um `if` ou de um
  `except ImportError`. Um teste que não vai voltar apaga-se.

## 3. Instalar os testes prontos

- **Python:** copie a pasta [`modelos/testes`](https://github.com/Carlobks/Morg-laws/tree/main/modelos/testes) para
  `tests/` do projeto (os moldes usam o
  [`carregar_por_caminho.py`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes/carregar_por_caminho.py)
  e o [`linha_de_base.py`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes/linha_de_base.py) dela) e
  ajuste o bloco
  «Ajuste ao projeto» do início de cada um. Rodam com `python -m unittest discover -s tests`.
- **TypeScript:** copie a pasta [`modelos/testes-ts`](https://github.com/Carlobks/Morg-laws/tree/main/modelos/testes-ts)
  para `tests/catracas/` do projeto. Precisam do `vitest` e do `typescript` (para ler o código pela árvore) e rodam
  com `npx vitest run`.
- Os testes leem o **índice do git**: um arquivo novo conta depois do `git add`, e o trabalho a meio de outra
  sessão na mesma pasta não trava o commit desta.
- Ligue-os ao comando único de testes, que o hook do commit e o CI chamam. No CI de um projeto TypeScript, o
  [molde de CI](https://github.com/Carlobks/Morg-laws/blob/main/modelos/github/workflows/ci.yml) fixa o Node pelo
  arquivo .nvmrc do projeto, instala o lockfile com `npm ci` e corre o `npm audit`.
- A linha `Alarme-novo:` na máquina é conferida pelo
  [`mensagem_commit.py`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/git/portoes/mensagem_commit.py),
  no hook `commit-msg`. Um projeto que copia só os testes prontos não o tem, e a marca só é conferida no CI.

## 4. Num projeto que já viola: a linha de base

Os seis testes, nas duas línguas, aceitam uma **linha de base**: o que já viola fica congelado e só pode encolher;
um arquivo novo nasce limpo.

1. Rode os testes uma vez com `MORG_CRIAR_LINHA_DE_BASE=1`. Cada base que falta é criada em
   `tests/linhas-de-base/<regra>.json`, com o excesso de hoje por arquivo (`{"src/a.ts": {"linhasAcima": 12}}`; a
   dos alarmes conta por tipo, em `{"*": {"eslint-disable": 3}}`), e o teste falha até ela entrar no git. Num
   projeto com as duas línguas, as bases são as mesmas: corra a variável numa língua, faça `git add`, corra na
   outra (ela junta as métricas que faltam) e faça `git add` de novo.
2. Leia a base antes do `git add`: ela é a lista da dívida.
3. Daí em diante, três testes por regra: **não piora** (nenhum arquivo passa do que a base deixa), **sem folga**
   (quem corrige desce a base no mesmo commit) e **só encolhe** (a base não ganha entrada nem valor face à base de
   comparação). Uma base já commitada nunca é reescrita pela variável.
4. **No CI e numa PR**, o índice é o próprio commit: a variável `MORG_BASE_DE_COMPARACAO` diz com que commit
   comparar (a ponta anterior do ramo de destino) e o checkout precisa de `fetch-depth: 0`. O molde do CI do
   Morg-laws já as tem. Sem isto, um commit feito sem os hooks (no site do GitHub, por exemplo) subiria a base.
   Quando a base de comparação não é um commit que o git conheça (o push de um ramo novo, cujo «antes» são 40
   zeros, um push forçado, um nome errado), o «só encolhe» **salta**, com o motivo escrito: nesse push não compara.

**Limites conhecidos:**
- Uma catraca diz «não piorou», nunca «está bem».
- Apagar a base e criá-la de novo: o commit que a apaga com o código ainda a violar falha no «não piora», e no CI
  os dois commits no mesmo push são apanhados. Só passa com o primeiro feito sem os hooks e os dois enviados em
  pushes separados; aí só a revisão do histórico o apanha.
- Num projeto TypeScript com um `index.ts` por pasta, junte `index` aos nomes impostos dos nomes únicos (nas duas
  línguas), ou os `index.ts` reprovam todos.
- Mudar de caminho um arquivo que está na base (`git mv`) conta como entrada nova: corrija-o antes, ou faça um
  commit só da base, revisto.
- Casos que as duas línguas deixam passar por igual, contra a regra escrita: um arquivo com as linhas separadas só
  por `\r`; um alarme num `.mts`, `.cts` ou `.cjs` (fora das extensões, que o projeto pode alargar); um
  `import … as data`; uma condição constante (`skipIf(True, "x")`, `it.skipIf(true)`). Só no Python,
  `pytestmark = pytest.mark.skip`; só no TypeScript, uma função longa passada a um `describe` no código de produção.
  E um caso certo que as duas recusam: um `.skip(…)` de outra coisa num arquivo de teste (`leitor.skip(3)`).
- No TypeScript, as opções `{ skip }` e `{ only }` de um teste por um caminho que a árvore não mostra passam: numa
  variável (`const opcoes = { skip: true }; it('a', opcoes, …)`), espalhadas (`{ ...{ skip: true } }`) ou depois de
  um `.each` (`it.each([1])('a', { skip: true }, …)`).

## 5. Fronteira com outras skills

- **testes-e-provas:** provar que um trabalho funciona, o teste que pega o bug, depurar, auditar e o que é uma
  catraca em geral. Esta skill diz as regras da forma do código e os seis testes prontos que as impõem, com a
  linha de base deles. Escrever uma tela ou uma rota não é forma do código: só se abre esta quando o arquivo, a
  função, um nome, um alarme ou um teste saltado estão em causa.
- **escrevendo-regras-de-agente:** onde uma regra vai (texto, skill ou barreira).
- **git-e-commits:** o comando único no hook do commit e os commits.

## Fontes

Os limites (500 linhas por arquivo, 20 por função nova) e as listas vêm da prática do projeto de origem, onde os
mesmos testes correm como catracas. A forma de saltar um teste no vitest vem da
[API do vitest](https://vitest.dev/api/test). A forma de cada teste está nos próprios moldes, que dizem o que medem.
As fontes estão em [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#testes-prontos-vitest).
