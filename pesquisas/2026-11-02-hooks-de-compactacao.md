# Hooks em volta da compactação no Claude Code

Data: 2026-11-02.

## Pergunta

Quando o Claude Code compacta a conversa, que hooks disparam, o que cada um recebe e o que cada um pode fazer?
A resposta diz onde uma passagem de trabalho pode guardar o estado antes de a conversa encolher e por onde esse
estado pode voltar ao agente depois.

## Fontes

- **Claude Code — hooks** — https://code.claude.com/docs/en/hooks — lidas em 2026-11-02 as seções dos quatro
  eventos e as linhas que citam `compact`, na versão em texto da página (o mesmo endereço terminado em `.md`); não
  a página inteira. Entrada no `FONTES.md`.

## O que se mediu

Tudo abaixo foi **lido** na página, não executado. Os quatro pontos de contato com a compactação:

| Evento | Quando | O que recebe, além dos campos comuns | O que pode fazer |
|---|---|---|---|
| `PreCompact` | Antes de compactar. O filtro (`matcher`) é `manual` (o `/compact`) ou `auto` (a janela de compactação automática e a compactação por inatividade). | `trigger` e `custom_instructions`: o texto que a pessoa deu ao `/compact`, ou nulo; no `auto` é sempre nulo. | Barrar a compactação: código de saída 2 ou `"decision": "block"`. No `manual`, a pessoa vê o stderr. Os campos `systemMessage` e `continue` são descartados. |
| `PostCompact` | Depois de compactar, com os mesmos dois filtros. | `trigger` e `compact_summary`, o resumo que a compactação gerou. | Nada sobre o resultado: não tem controle de decisão. Serve para efeitos à parte, como registrar o resumo ou atualizar um estado fora da conversa. O stderr vai só para a pessoa. |
| `SessionStart` | Volta a disparar depois da compactação, com a origem (`source` e filtro) `compact`. | `source` e campos opcionais (`model` e outros). | Pôr texto no contexto do agente: `additionalContext` no JSON, ou texto simples no stdout. Só aceita hooks `command` e `mcp_tool`; os `mcp_tool`, que não rodam na abertura da sessão, rodam neste disparo. |
| `InstructionsLoaded` | Quando o `CLAUDE.md` ou os arquivos de `.claude/rules/` voltam a carregar depois da compactação, com o motivo (`load_reason`) `compact`. | `file_path`, `memory_type`, `load_reason` e outros. | Só observar: roda em segundo plano, sem a sessão esperar, não barra nem muda nada, e o JSON que devolve é descartado. |

Três detalhes que mudam o desenho de um hook:

- **Barrar a compactação automática nem sempre é inofensivo.** Se ela foi preventiva, a conversa só segue sem
  compactar. Se ela veio para recuperar de um erro de limite de contexto que a API já devolveu, o pedido em curso
  falha com esse erro.
- **O `AGENTS.md` lido direto não avisa.** O `InstructionsLoaded` não dispara quando o Claude Code lê o `AGENTS.md`
  pelo ajuste de instruções do projeto; dispara quando um `CLAUDE.md` o importa (motivo `include`) ou é um link
  simbólico para ele.
- Um `SessionStart` assíncrono que devolve o mesmo texto de antes é pulado, salvo depois de uma compactação ou de um
  `/clear`, quando o texto volta a ser entregue.

## O que não se verificou

- Nenhum dos quatro hooks foi executado: não há medição num projeto, só a leitura da página.
- A página não foi lida de ponta a ponta: as três ausências abaixo valem para as seções lidas e para as linhas que
  citam `compact`.
- A ordem entre o `PostCompact`, o `SessionStart` com `compact` e o `InstructionsLoaded` com `compact` não está
  escrita nesse trecho. Não se sabe se o `PostCompact` termina antes de o `SessionStart` rodar.
- Onde fica o `additionalContext` do `SessionStart` em relação ao resumo da compactação: o trecho lido não diz.
- O trecho lido não dá a versão do Claude Code a partir da qual estes eventos existem.
- A página própria da compactação e o comportamento de outros agentes (Codex e outros) ficam para a fase seguinte
  (a da skill de passagem de trabalho), que junta essas pesquisas a esta.

## Conclusão

Para uma passagem de trabalho que sobreviva à compactação:

1. **Guardar** o estado no `PreCompact` (antes de a conversa encolher) ou no `PostCompact` (já com o resumo em
   `compact_summary`). Nenhum dos dois põe texto no contexto do agente.
2. **Devolver** o estado ao agente pelo `SessionStart` com o filtro `compact`: dos quatro, é o único com um campo
   para isso (`additionalContext`).
3. **Não barrar** no `PreCompact` por padrão: na compactação automática perto do limite, barrar faz o pedido falhar.
4. O `InstructionsLoaded` com `compact` serve só para registrar que as regras voltaram a carregar; e não vê o
   `AGENTS.md` lido direto.

O que esta pesquisa não mediu (a ordem dos eventos e o lugar do texto devolvido) tem de ser provado num projeto
antes de virar regra.
