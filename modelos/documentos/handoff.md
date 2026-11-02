# Handoff: <assunto>

Para retomar numa sessão nova. Confirme o estado no repositório (`git log --oneline`) antes de confiar neste
arquivo. Vive em `.context/HANDOFF-<assunto>.md` e atualiza-se no commit que fecha cada fase (skill
`orquestrando-sessoes`). O `tests/test_docs_indices.py` exige as seções abaixo e confere cada hash citado.

## Objetivo

<O que se quer e onde está o plano.>

## Estado verificado (<AAAA-MM-DD>, ramo `<ramo>`)

| Fase | Commits | O que ficou |
|---|---|---|
| F1 | `<hash>` | <resultado medido> |

## Decisões e porquê

Do dono (perguntadas, com a recomendação):
- **<decisão>:** <o porquê>.

Técnicas (tomadas durante as fases, com o motivo medido):
- **<decisão>:** <o porquê, com o número que a sustenta>.

## Descartado

- <abordagem>: <porque não serviu>, para a sessão seguinte não a tentar de novo.

## Próximos passos

1. <o que falta, na ordem>.

**Cuidados:** <armadilhas que a sessão seguinte vai encontrar>.
