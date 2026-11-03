---
name: codigo-legivel
description: Diz as regras da forma do código que um agente escreve — arquivo até 500 linhas, função nova até 20, nomes únicos e pesquisáveis, nada de nome genérico, nenhum alarme calado sem motivo, nenhum teste saltado sem condição, os testes num só comando — com o porquê de cada uma e o teste pronto que a impõe em Python e em TypeScript (vitest), e como adotar esses testes num projeto que já viola, com uma linha de base que só encolhe. Usar ao escrever, partir ou rever código, quando um arquivo ou uma função crescem demais, ao escolher um nome, antes de calar um aviso do lint ou de saltar um teste, ou ao instalar os testes prontos num projeto. Não usar para provar que um trabalho funciona ou corrigir um bug (é a testes-e-provas), nem para os commits (é a git-e-commits).
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
  (`// eslint-disable-line no-console — o CLI escreve no terminal`), e a linha de base sobe no mesmo commit, à
  vista de quem revê.
- **Teste saltado:** diga quando e porquê: `test.skip(semRede, 'precisa da rede')` ou
  `@unittest.skipIf(sys.platform == "win32", "o hook só corre em sh")`. Um teste que não vai voltar apaga-se.

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
- Ligue-os ao comando único de testes, que o hook do commit e o CI chamam.

## 4. Num projeto que já viola: a linha de base

Os testes de tamanho de arquivo e de função, nomes, alarmes e testes saltados aceitam uma **linha de base**: o que
já viola fica congelado e só pode encolher; um arquivo novo nasce limpo.

1. Rode os testes uma vez com `MORG_CRIAR_LINHA_DE_BASE=1`. Cada base que falta é criada em
   `tests/linhas-de-base/<regra>.json`, com o excesso de hoje por arquivo (`{"src/a.ts": {"linhasAcima": 12}}`),
   e o teste falha até ela entrar no git.
2. Leia a base antes do `git add`: ela é a lista da dívida.
3. Daí em diante, três testes por regra: **não piora** (nenhum arquivo passa do que a base deixa), **sem folga**
   (quem corrige desce a base no mesmo commit) e **só encolhe** (a base não ganha entrada nem valor face ao último
   commit). Uma base que já existe nunca é reescrita pela variável.
4. As duas línguas usam o mesmo formato, por isso um projeto misto pode partilhar a pasta. Os moldes Python mais
   antigos têm a base dentro do arquivo: `LONGAS_ANTIGAS` no de funções e `MAXIMO_POR_TIPO` no de alarmes; o de
   nomes genéricos em Python ainda não tem base.

**Limite:** uma catraca diz «não piorou», nunca «está bem». Apagar a base num commit e criá-la de novo no seguinte
passa: só a revisão do histórico apanha isso.

## 5. Fronteira com outras skills

- **testes-e-provas:** provar que um trabalho funciona, o teste que pega o bug, depurar, auditar e o que é uma
  catraca em geral. Esta skill diz as regras da forma do código e os testes prontos que as impõem.
- **escrevendo-regras-de-agente:** onde uma regra vai (texto, skill ou barreira).
- **git-e-commits:** o comando único no hook do commit e os commits.

## Fontes

Sem fonte externa: os limites (500 linhas por arquivo, 20 por função nova) e as listas vêm da prática do projeto de
origem, onde os mesmos testes correm como catracas. A forma de cada teste está nos próprios moldes, que dizem o que
medem. Quando uma regra passar a apoiar-se numa fonte, ela entra em
[`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md).
