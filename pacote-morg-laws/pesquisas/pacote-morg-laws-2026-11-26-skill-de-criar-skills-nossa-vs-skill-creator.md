---
titulo: a nossa skill de criar skills (criando-skills) é melhor ou pior que a skill-creator da Anthropic, e o que cada uma devia copiar da outra?
data: 2026-11-26
area: geral
estado: concluida
destino: nenhum (decisão do PO; entra no envio ao Morg-laws de 27-11)
---

## Veredito

**Não são concorrentes: a `criando-skills` foi escrita para correr junto com a `skill-creator`** («Use junto com `skill-creator`, que traz o
processo», `criando-skills/SKILL.md:8`). A `skill-creator` é melhor no processo de teste (avaliações, comparação com e sem a skill,
otimização da descrição com scripts). A `criando-skills` é melhor no que vem antes e no que é da casa: decidir se é mesmo uma skill,
procurar sobreposição, medir o que o modelo já faz, a língua do utilizador, as fontes e o fecho «Feito / Conferido / Não verificado».

**Recomendação ➡️ opção C: manter as duas e melhorar a nossa** com 4 correções pequenas (ver «Conclusão»). Trocar pela da Anthropic
perde as regras da casa; instalar a do link do PO (OneAway) é pior que a da Anthropic que já temos.

**Atenção ao link do PO:** `https://oneaway.io/skills/skill-creator` **não é** a skill-creator da Anthropic que está instalada. É uma
cópia num site de terceiros, sem autor nem repositório, com o fluxo antigo (`init_skill.py`, `package_skill.py`,
`references/workflows.md`) e incoerências (título «Skill Creator», `name: create-skill`). A versão instalada da Anthropic já não tem
esses ficheiros: tem avaliações, visualizador e otimizador de descrição.

## Pergunta

O PO encontrou a «skill-creator» e achou-a parecida com a nossa e mais bem organizada. Quer saber qual é melhor pelos pontos que
importam ao criar uma skill, segundo a documentação oficial, e o que cada uma devia copiar da outra. O resultado entra no envio ao
Morg-laws de sexta 27-11.

## Fontes lidas

- **A nossa, `criando-skills`** — `~/.claude/skills/synced/<id>/criando-skills/SKILL.md`, 51 linhas, de 2026-10-20 (lido agora)
- **A da Anthropic, `skill-creator`** — `~/.claude/skills/synced/<id>/skill-creator/SKILL.md`, 506 linhas, por secções (lido agora)
- **Anthropic — Skill authoring best practices** — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices (lido agora)
- **OneAway — Skill Creator** — https://oneaway.io/skills/skill-creator, pelo resumo da ferramenta de leitura (lido agora)
- **Critérios da casa** — `.claude/rules/padroes-de-codigo.md:32` e a memória `skills-da-casa-estado.md` (lido agora)
- **A página da OneAway copia a versão antiga da skill-creator do repositório `anthropics/skills`** (do conhecimento do modelo)

## O que se mediu

Notas sobre as cópias:

- A `criando-skills` tem uma segunda cópia, idêntica (`diff -rq` sem diferenças), na pasta do plugin em
  `AppData/Local/Claude-Data/.../plugin_011ada.../skills/criando-skills/`. A fonte é a sincronizada do claude.ai. **Não está no clone
  do Morg-laws** (`~/Projetos/Morg-laws/skills/` tem 15 skills, sem esta).
- A `skill-creator` lida é a que aparece como `anthropic-skills:skill-creator`. Há outra cópia mais antiga, de 485 linhas, no plugin
  oficial (`~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/`): difere em 8 ficheiros, sobretudo no formato
  dos testes (`evals/evals.json` na antiga, uma pasta por caso na nova).
- Ficheiros de apoio da `skill-creator` (não lidos todos): `agents/` (grader, comparator, analyzer: instruções para sub-agentes),
  `references/schemas.md` (430 linhas), `scripts/` (run_eval, run_loop, improve_description, aggregate_benchmark, generate_report,
  package_skill, quick_validate), `eval-viewer/` (generate_review.py, viewer.html), `assets/eval_review.html`.
- Dos critérios da casa: skills de terceiros não se instalam sem as ler e sem dor concreta (livro do Akita pp. 128–129); testar uma
  skill depende de uma sessão nova do PO, por causa da regra SEM SUB-AGENTES.

`wc -l` (51 contra 506 linhas), `diff -rq` entre as cópias (as duas `criando-skills` iguais; as duas `skill-creator` diferem em 8
ficheiros), `grep -n` das secções da `skill-creator`, e a listagem de `~/Projetos/Morg-laws/skills/`.

### A comparação, ponto a ponto

Critérios da documentação oficial (a «best practices» acima). `cs` = `criando-skills/SKILL.md`; `sc` = `skill-creator/SKILL.md`.

| Critério (doc oficial) | A nossa (`cs`) | A Anthropic (`sc`) | Melhor |
|---|---|---|---|
| **Descrição: o quê + quando, 3.ª pessoa, ≤1024** | Diz o quê, quando e «Não usar…»; regra escrita (`cs:21`) | Diz o quê e quando (`sc:3`); manda descrição «insistente» contra o subdisparo (`sc:67`) | **Nossa**: tem a regra e o «Não usar» |
| **Quando não usar** | Obrigatório no fim da descrição (`cs:3`, `cs:21`) | Não existe na descrição nem como regra | **Nossa** (a doc não o exige; é regra da casa) |
| **Nome (≤64, minúsculas, sem claude/anthropic, gerúndio)** | Limites escritos (`cs:20`); o nome já é gerúndio | Só «Skill identifier» (`sc:66`) | **Nossa** |
| **Tamanho (<500 linhas)** | Remete para a `sc` e mede antes de entregar (`cs:23`, `cs:45`); ela própria tem 51 | <500 linhas, hierarquia se se aproximar (`sc:90`, `sc:96`); ela tem 506, acima do próprio limite | Empate na regra; a **nossa** cumpre |
| **Estrutura de pastas** | Não fala (`scripts/`, `references/`) | Anatomia com `scripts/`, `references/`, `assets/` (`sc:73-84`) e organização por domínio (`sc:100-109`) | **Anthropic** |
| **Revelação progressiva** | Não fala | Três níveis, índice em referências >300 linhas (`sc:86-98`). A doc pede índice a partir de 100 e referências a **um** nível | **Anthropic** (falta-lhe o «um nível») |
| **Scripts** | Só «teste o código e o SQL que entram» (`cs:29`) | Scripts para trabalho repetido; se os testes reescrevem o mesmo script, junta-o (`sc:325`) | **Anthropic** |
| **Antes de escrever: é mesmo skill? já existe?** | Lugar certo: CLAUDE.md, skill, conector ou memória; vizinhas que se sobrepõem (`cs:14-15`) | Entrevista e pesquisa (`sc:47-60`), sem estas duas perguntas | **Nossa** |
| **Medir o modelo sem a skill antes de escrever** | Sim, 2–3 pedidos reais antes (`cs:16`) — é o «Build evaluations first» da doc | Linha de base só depois do rascunho (`sc:185-202`) | **Nossa** (bate com a doc) |
| **Testar se funciona** | Formato de testes antigo (`evals/evals.json`, `cs:35`); com e sem a skill em «agentes independentes» (`cs:37`) | Uma pasta por caso, legível pelo `claude plugin eval` (`sc:145-160`); com e sem a skill em sub-agentes, avaliador, benchmark e visualizador (`sc:185-260`) | **Anthropic** (a nossa ficou no formato que ela já chama antigo, `sc:160`) |
| **Testar se dispara** | `trigger-eval.json` com quase-acertos; diz que o teste de gatilho é simulado (`cs:36`, `cs:38`) | ~20 consultas, divide 60/40 treino/teste, 3 corridas por consulta, escolhe pela nota de teste (`sc:358-415`); precisa de `claude -p` (`sc:453`) | **Anthropic** no método; **nossa** na honestidade sobre o limite |
| **Modelos testados** | Haiku, Sonnet e Opus (`cs:38`) | Não pede | **Nossa** (é o que a doc pede) |
| **Iteração** | «Corrija só o que os testes mostrarem» (`cs:39`) | Ciclo completo: ler o retorno, generalizar, não sobreajustar (`sc:313-345`) | **Anthropic** |
| **Língua do utilizador** | Mesma língua na descrição e no corpo: a do utilizador (`cs:22`) | Adapta o jargão ao utilizador (`sc:32-41`), mas é escrita em inglês | **Nossa** |
| **Informação que envelhece / caminhos fixos** | Proíbe caminhos de máquina e versões; «a confirmar» (`cs:22`) | Não fala | **Nossa** (bate com a doc, «Avoid time-sensitive information») |
| **Fontes e factos** | Doc oficial lida, separar lido de sabido, tema legal manda ao profissional (`cs:27-31`) | Não fala | **Nossa** |
| **Segurança** | Ler o SKILL.md e todos os scripts antes de instalar (`cs:31`) | Sem malware nem surpresas (`sc:111-113`) | Complementares |
| **Entrega e fecho** | Pelo cartão `propose_skills` (`cs:43`); fecho Feito/Conferido/Não verificado (`cs:46`) | `.skill` empacotado, se houver ferramenta (`sc:429`) | **Nossa** no fecho; a entrega só vale no claude.ai |

**Onde cada uma é melhor, e porquê.** A Anthropic ganha no **como se prova**: tem scripts, formato de teste estável e um otimizador
de descrição com separação treino/teste, que evita o sobreajuste. A nossa ganha no **o quê e porquê**: obriga a decidir se é skill,
a procurar sobreposição (o problema real do ERP, com muitas skills da casa e o `skill-guard`), a medir antes, a escrever na língua do PO
e a dizer o que não se verificou. A doc oficial dá razão à nossa em três pontos que a `skill-creator` não segue: avaliações antes de
escrever, testar em três modelos e não pôr informação que envelhece.

### Custo e risco de cada opção

| Opção | Custo | Risco |
|---|---|---|
| **A. Manter a nossa como está** | Zero | Os testes ficam num formato que a Anthropic já chama antigo; manda usar «agentes independentes», o que o `CLAUDE.md` do ERP proíbe |
| **B. Trocar pela da Anthropic** | Perder as regras da casa (lugar certo, sobreposição, língua, fontes, fecho) | Em inglês; o teste e a comparação às cegas dependem de **sub-agentes** (`sc:185`, `sc:350`), proibidos no ERP; o otimizador precisa do `claude -p` e de Python; 506 linhas carregadas em cada uso |
| **C. ➡️ Manter as duas e corrigir a nossa** | ~1 hora: 4 mudanças na `criando-skills`, testadas numa sessão nova | Baixo. A `skill-creator` continua a vir da Anthropic e muda sem aviso: a nossa deve remeter para ela, não copiá-la |
| **D. Instalar a do link (OneAway)** | Ler o SKILL.md e os scripts todos (`padroes-de-codigo.md:32`) | Origem desconhecida, versão antiga e incoerente; não resolve dor nenhuma que a instalada não resolva |

## O que não se verificou

- **Não se correu nenhuma das duas** num caso real: a comparação é do texto, não do resultado. Provar exigiria uma sessão nova do PO.
- Não se leram os scripts, os `agents/*.md` nem o `references/schemas.md` da `skill-creator` (só os nomes e o tamanho).
- Não se confirmou que a página da OneAway copia a versão antiga do repositório `anthropics/skills` (vem do conhecimento do modelo).
- Não se leu a página «Skills» do Claude Code (`code.claude.com/docs/en/skills`), que pode ter campos do frontmatter (por exemplo,
  impedir o disparo automático) que nenhuma das duas cobre.
- Não se testou se o `claude plugin eval` existe na versão do Claude Code instalada aqui.

## Conclusão

**Recomendação ➡️ C: manter as duas, com a `criando-skills` como camada da casa por cima da `skill-creator`, e corrigir na nossa:**

1. **Formato dos testes:** trocar `evals/evals.json` (`cs:35`) por «uma pasta por caso em `evals/`, no formato da `skill-creator`
   (ler o `references/schemas.md` dela)», para não fixar um formato que ela já mudou.
2. **Sem sub-agentes:** onde diz «agentes independentes» (`cs:37`), dizer «numa sessão nova, sem a skill e com ela; se o ambiente
   proíbe sub-agentes, a comparação às cegas e o benchmark da `skill-creator` ficam de fora».
3. **Revelação progressiva e scripts:** uma linha a mandar a `scripts/` e `references/` da `skill-creator`, mais o que a doc pede e
   ela não diz: referências a **um** nível do `SKILL.md` e índice a partir de 100 linhas.
4. **Entrega:** o cartão `propose_skills` (`cs:43`) só existe no claude.ai; no Claude Code a entrega é o ficheiro na pasta de skills
   do projeto ou no Morg-laws, pela fila de commits.

**O que a `skill-creator` devia copiar da nossa** (não se manda à Anthropic, mas serve ao Morg-laws): o «Não usar…» na descrição, a
pergunta «é mesmo skill?», a procura de sobreposição, medir antes de escrever, testar em três modelos, a língua do utilizador e o
fecho com o que não se verificou.

**Decisões do PO:**

- **D1.** Opção C (recomendada), A, B ou D?
- **D2.** Se C: as 4 correções fazem-se antes do envio de sexta 27-11 (com teste numa sessão nova) ou ficam como tarefa para depois?
- **D3.** A `criando-skills` entra no Morg-laws? Hoje não está lá; só vive na sincronização do claude.ai.
