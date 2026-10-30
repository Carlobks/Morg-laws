# Morg-laws

Regras, boas práticas e aprendizados para trabalhar com agentes de IA no código
(Claude Code, Codex, Cursor, Copilot e outros). Tudo saiu do dia a dia de um sistema real em produção:
o que deu errado, a regra que nasceu disso e a fonte que a sustenta.

## O que tem aqui

| Pasta | O que guarda |
|---|---|
| `AGENTS.md` | O núcleo das regras e o índice. É o que o agente lê primeiro. |
| `skills/` | Regras por assunto (SQL, Supabase, Next.js, segurança, sessões…). O agente só abre o que o projeto usa. |
| `biblia-akita/` | Resumo, com palavras nossas, do livro *Competente o Suficiente*, de Fabio Akita, com capítulo e página. |
| `aprendizados/` | Notas datadas sobre bibliotecas, ferramentas e erros que custaram caro. |
| `modelos/` | Arquivos prontos para copiar: o hook `pre-push` (segredos com gitleaks e bibliotecas com `npm audit`, com linha de base). |
| `FONTES.md` | Todas as fontes usadas, com a data em que foram lidas. |

O repositório está em construção: as pastas aparecem conforme as fases avançam.

## Como usar num projeto

```bash
npx skills add Carlobks/Morg-laws
```

(em construção: o comando funciona quando a primeira skill for publicada)

## Para quem contribui

Ative os hooks depois de clonar:

```bash
git config core.hooksPath .githooks
```

O `pre-commit` recusa commits com e-mail que não seja o noreply do GitHub e com AGENTS.md acima de 60 linhas.
Ele também procura nomes e dados sensíveis numa lista que fica **fora** do repositório
(`git config morg.listaNegra <arquivo>`); sem essa lista, só avisa. No GitHub, o `gitleaks` procura segredos em todo push.

## Licença

Texto sob [CC BY 4.0](LICENSE): pode copiar e adaptar, citando a origem.
