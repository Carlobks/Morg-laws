# <N>.ª verificação contra as regras — <AAAA-MM-DD>

Leitura independente, numa sessão nova, do ramo `<ramo>` em `<hash>`. As contagens abaixo foram fechadas e
commitadas **antes** de ler a verificação anterior, o plano e o handoff (lida antes, a anterior vira a resposta
esperada). A comparação com a anterior está no fim, escrita depois.

**Fontes das regras:** <o AGENTS.md/CLAUDE.md, as skills, outros>. **Não se aplicam:** <o quê e porquê>.

**Veredictos:** cumprida · em parte (falta uma parte, ou só existe em texto quando podia ter máquina) · falha ·
por validar (não se mede a partir do repositório) · não se aplica.

## Contagens

| Veredicto | Regras |
|---|---|
| Cumprida | <n> |
| Em parte | <n> |
| Falha | <n> |
| Por validar | <n> |
| Não se aplica | <n> |
| **Total** | **<n>** |

Contei de novo a tabela abaixo antes de gravar.

## Provas rodadas

| Comando | Saída |
|---|---|
| `<comando de testes>` | `<resumo da saída>` · saída 0 |
| `gitleaks git --redact .` | `<n> commits scanned` · `no leaks found` |
| Sondas aos hooks do agente (JSON de exemplo no stdin) | <resultado de cada uma> |

## Tabela das regras

| # | Regra | Veredicto | Prova (arquivo:linha ou comando) | O que falta |
|---|---|---|---|---|
| N1 | <regra> | <veredicto> | <prova> | <falta, ou —> |

## Achados por gravidade (para o dono decidir; nada foi corrigido)

**Alto:** <…> · **Médio:** <…> · **Baixo:** <…>

## O que não se verificou

- <o que só se mede na máquina do dono, com uma pessoa, ou fora do repositório>

## Comparação com a anterior

<Escrita depois de commitar as contagens: o que melhorou, o que piorou, o que esta viu e a anterior não.>
