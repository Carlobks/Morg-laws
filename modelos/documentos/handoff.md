# Handoff: <assunto>

Para retomar numa sessão nova. Confirme o estado no repositório (`git status -s` e `git log --oneline`) antes de
confiar neste arquivo. Vive em `.context/HANDOFF-<assunto>.md` e é commitado sozinho, pelo caminho, a cada
compactação e no fecho de cada fase, salvo se a pasta estiver ignorada (skill `passando-o-trabalho`, seção 3). O
`tests/test_docs_indices.py` exige as seções abaixo e confere cada hash citado. Menos de 150 linhas; seção vazia
leva "nenhum".

## Objetivo

- Principal: <o que se quer, numa linha, e onde está o plano>.
- Passo em curso: <o passo exato>.

## Estado verificado (<AAAA-MM-DD>, ramo `<ramo>`)

| Fase | Commits | O que ficou |
|---|---|---|
| F1 | `<hash>` | <resultado medido> |

Arquivos (do `git status -s`):

| Arquivo | Status | O que mudou |
|---|---|---|
| `<caminho>` | <M, A, D ou ??> | <funções, linhas> |

Testes (a última execução real, ou "não executado nesta sessão"):

- `<comando>`: passa.
- `<comando>`: falha com

  ```
  <o erro literal, só as linhas que importam>
  ```

## Decisões e porquê

Do dono (perguntadas, com a recomendação):
- **<decisão>:** <o porquê>.

Técnicas (tomadas durante as fases, com o motivo medido):
- **<decisão>:** <o porquê, com o número que a sustenta>.

## Descartado

Não repetir sem um fato novo:
- <o que se tentou> → <o que aconteceu, com o erro> → <porque se largou>.

## Próximos passos

1. <o que falta, executável sem perguntar: arquivo, função, comando>.

**Cuidados:** <armadilhas que a sessão seguinte vai encontrar>.
