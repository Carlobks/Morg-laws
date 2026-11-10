# O que é o Morg-laws

## O que é e para que serve

O Morg-laws é um repositório público de regras, skills e modelos para quem trabalha com agentes de código, como o Claude Code e o Codex. Uma skill é uma pasta com instruções sobre um assunto (como commitar, como dividir o trabalho entre sessões, como mexer num banco de dados); o agente lê só a descrição dela no começo e abre o resto quando o assunto aparece, e o Codex segue o mesmo padrão, segundo a [documentação de skills do Codex](https://developers.openai.com/codex/skills). As regras ficam no `AGENTS.md`, um arquivo curto que o agente lê inteiro em todo turno, num [formato aberto, mantido em comum por várias ferramentas](https://agents.md).

Serve para três coisas. Dar ao agente o combinado do projeto, para você não repetir tudo em cada conversa. Trocar o conselho por barreira: o que tem de ser cumprido vira hook, teste ou CI, e não só um texto que o agente pode esquecer. E guardar o porquê de cada regra, com a fonte, para que você possa discordar com conhecimento de causa.

## De onde veio

Tudo saiu de um sistema web de gestão feito para duas empresas de serviços, conduzido por uma pessoa que não escreve o código: pede, aprova e confere, e os agentes propõem e implementam. Cada regra nasceu de algo que deu errado nesse projeto, e o catálogo `projetos/` conta isso sem o nome da empresa, sem nomes de pessoas e sem trechos de código, no [catálogo do projeto de origem](https://github.com/Carlobks/Morg-laws/blob/main/projetos/erp-de-servicos/README.md). O repositório é anonimizado de propósito: o que entra num repositório público não sai mais.

## O que tem cada pasta

A tabela completa está no [README do repositório](https://github.com/Carlobks/Morg-laws/blob/main/README.md). Em resumo, na raiz:

- `AGENTS.md`: o núcleo das regras e o índice de quando ler cada skill. É o que o agente lê primeiro. O `CLAUDE.md` ao lado só aponta para ele, com a linha `@AGENTS.md`.
- `skills/`: as skills, uma pasta por assunto, cada uma com um `SKILL.md`.
- `modelos/`: arquivos prontos para copiar para o seu projeto, como os hooks do Claude Code, os hooks do git, os testes das regras e o CI. É daqui que vêm as barreiras.
- `biblia-akita/`: o resumo, com palavras próprias, do livro *Competente o Suficiente*, de Fabio Akita, com a página de cada conselho.
- `manual/`: este manual, em Markdown, de onde sai o PDF.
- `aprendizados/`: notas datadas sobre ferramentas e erros que custaram caro.
- `pesquisas/`: as pesquisas feitas para o repositório, uma por arquivo.
- `projetos/`: o catálogo do projeto de origem, anonimizado.
- `prova/`: o método que foi preparado para medir as regras, com a ressalva da seção seguinte.
- `tests/` e `scripts/`: os testes do próprio repositório e o comando que os roda.
- `.github/` e `.githooks/`: os formulários de issue, o CI e os portões do git do próprio repositório.
- `FONTES.md`: todas as fontes usadas, com a data em que foram lidas.

## A prova é o uso real

Este manual não diz que as regras foram medidas, porque não foram. A medição paga que o repositório chegou a preparar, na pasta `prova/`, nunca correu: o autor decidiu que a validação seria o uso real em outros projetos, e o próprio `prova/README.md` avisa que nenhum resultado dali pode ser apresentado como medido. O que existe é o uso diário no projeto de origem, e as [medições do uso daquele projeto antes das regras](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-05-linha-de-base-do-uso.md), que descrevem como o trabalho era e servem de ponto de partida para uma segunda medição.

Há também o que a pesquisa externa diz, e é menos animador. Um estudo sobre arquivos de contexto como o `AGENTS.md` conclui que eles em geral não melhoram a taxa de tarefas resolvidas e aumentam o custo em mais de 20% em média ([o estudo no arXiv](https://arxiv.org/abs/2602.11988)). Outro, de cinco corridas num só repositório, achou que um `AGENTS.md` curto, de 12 linhas, deixou o agente mais rápido e mais barato, e o próprio autor o chama de um único ponto de dados ([AAIF, cinco corridas](https://aaif.io/blog/measuring-agents-md-what-five-runs-show-that-one-doesn-t)). Por isso o `AGENTS.md` daqui é curto e o texto longo vive nas skills, que só abrem quando precisam.

O que vai mostrar se as regras servem são as **issues**: quem as usa num projeto e vê uma delas falhar, ou ver o agente fazer o contrário do que ela diz, abre uma e conta.

## Como reportar um erro

Entre pelos formulários do [New issue](https://github.com/Carlobks/Morg-laws/issues/new/choose). Há um para um problema numa regra (ela disse uma coisa e aconteceu outra), um para uma sugestão e um para uma correção de fonte, quando um resumo da `biblia-akita/` não bate com a página do livro. Cada formulário pede a prova, e esta é a parte que mais ajuda: o que você pediu, o que aconteceu e o que esperava.

O repositório é público, e a issue também. Não ponha nomes de empresas, de projetos ou de pessoas, e-mails, chaves nem caminhos da sua máquina: troque por um papel (“o dono”, “projeto X”). Um problema de segurança não vai numa issue: use o aviso privado descrito na [política de segurança](https://github.com/Carlobks/Morg-laws/blob/main/.github/SECURITY.md). Se o erro for deste manual, use o mesmo caminho, dizendo qual parte e qual frase.
