---
titulo: o Morg-laws impede que uma sessão-filha receba contexto a mais, e como deve a mãe montar o briefing?
data: 2026-11-19
area: geral
estado: concluida
destino: nenhum
---

## Pergunta

O PO perguntou duas coisas, depois de a filha «7.ª correção do plano (T1 a T10)» bater no teto da ferramenta Read:

1. O Morg-laws pode ajudar a impedir que uma sessão-filha receba um contexto grande demais? Com que regra, skill ou
   hook, e onde?
2. Como deve a sessão-mãe enviar o contexto a uma filha, para que vá organizado e só com o que ela precisa?

O briefing da filha mandava ler a 6.ª auditoria toda e **reescrever de raiz** o plano
`modelo-de-mudanca/acesso-do-agente-a-bd/plano-fechar-acesso-do-agente-a-bd.md` (revisão 7, commit `3d41f525`),
mais a página e um ficheiro de arquivo novo. Esta pesquisa é só de leitura: não muda skills, hooks, `CLAUDE.md`,
`.claude/` nem o Morg-laws. O PO verifica-a antes de qualquer mudança.

## Fontes lidas

- **Claude Code — Tools reference, secção «Large files»** — https://code.claude.com/docs/en/tools-reference (lido agora)
- **Claude Code — Environment variables, `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`** — https://code.claude.com/docs/en/env-vars (lido agora)
- **Morg-laws, `skills/orquestrando-sessoes/SKILL.md`** — clone em `C:\Users\Usuario\Projetos\Morg-laws`, commit `7b4c228` (lido agora)
- **Morg-laws, o hook e o teste de tamanho** — `modelos/claude/hooks/limite_de_linhas.py` e `modelos/testes/test_tamanho_dos_arquivos.py` (lido agora)
- **Morg-laws, os moldes e o manual** — `modelos/documentos/plano.md`, `modelos/README.md`, `AGENTS.md`, `manual/05-sessoes.md` (lido agora)
- **Morg-laws, `skills/passando-o-trabalho/SKILL.md`** — só a regra do tamanho do handoff (lido agora)
- **ERP, a skill e a adoção** — `.claude/skills/orquestrando-sessoes/SKILL.md`, `docs/adocao-do-morg-laws.md`, `.context/HANDOFF-adocao-do-morg-laws.md` (lido agora)
- **ERP, as medições** — `scripts/catracas/medir-tamanho-de-ficheiro.mjs`, os `.context/BRIEF-*.md`, o histórico do plano no git e o transcript da filha por `list_events` (lido agora)

## O que se mediu

### 1. O teto da ferramenta Read (documentação oficial, 2026-11-19)

- Uma chamada Read devolve **no máximo 25 000 tokens** (muda-se com `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`) e recusa
  um ficheiro inteiro acima de **256 KB**.
- O comportamento muda com a forma da leitura, e é isto que explica o incidente:
  - **o ficheiro inteiro** acima do teto chega como `PARTIAL view`: a primeira página, com aviso e o `offset` seguinte;
  - **uma leitura com `offset`/`limit`** acima do teto **dá erro** («exceeds maximum allowed tokens»).
- O `allow_large: true` (v2.1.296 ou mais nova) lê tudo de uma vez, medido pela janela que sobra. Não resolve o
  problema do PO: põe o ficheiro inteiro no contexto.

Prova nesta sessão: um Read do plano sem `offset` devolveu as linhas 1–420 com o aviso
`PARTIAL view … (72600 tokens, cap 25000)`. O plano inteiro custa, pela própria ferramenta, **72 600 tokens**:
2,2 bytes por token neste ficheiro (português com acentos e tabelas largas). Os números de tokens abaixo usam esta
razão; é uma estimativa medida num ficheiro só.

### 2. O incidente: o que se pediu e onde rebentou

| O quê | Bytes | Linhas | Tokens (estim.) |
|---|---:|---:|---:|
| Plano, revisão 7 (`3d41f525`) | 160 013 | 1 437 | 72 600 (medido pela Read) |
| 6.ª auditoria (`.context/AUDITORIA-6-…-2026-11-19.md`) | 19 170 | 228 | ~8 700 |
| Leitura que rebentou: linhas 421–1018 do plano | 58 284 | 598 | ~26 400 (erro: 26 379) |
| Plano reescrito pela filha (no disco, por commitar) | 123 776 | — | ~56 000 |
| Arquivo novo das revisões (no disco, por commitar) | 104 966 | — | ~48 000 |

- O transcript da filha mostra a sequência `Read`, `Bash`, quatro `Read`, «A ler o resto do plano (linhas 1019 em
  diante)» e mais `Read`. O `list_events` não mostra os parâmetros; a leitura que deu o erro é a das linhas 421–1018,
  porque é o único pedaço cujo tamanho bate com os 26 379 tokens (58 284 bytes ÷ 2,2). **A filha já lia por partes**:
  o que falhou foi o tamanho da parte, não a falta de método.
- O erro em si custou uma chamada. O problema maior é o **volume** da tarefa: só para ler o plano e a auditoria vão
  ~81 mil tokens; reescrever o plano e escrever o arquivo põe outros ~104 mil na conversa (o texto de cada `Write`
  fica no contexto). São **~185 mil tokens**, acima dos ~150 mil em que o Morg-laws manda compactar, antes de contar
  as leituras da página HTML e as respostas.
- **Porque o plano chegou aqui:** cresceu de 24 KB para 160 KB em 7 revisões e 4 dias, sempre por camadas (cada revisão
  juntou um parágrafo no topo, uma tabela na §7 e notas «leia-se» por cima do texto antigo):

| Commit | Bytes |
|---|---:|
| `65267009` (o plano) | 24 354 |
| `7499f161` (revisão 2) | 43 579 |
| `fc01eff1` (revisão 3) | 58 145 |
| `45086fcc` (revisão 4) | 84 472 |
| `bbc8cfe2` (revisão 5) | 110 722 |
| `53c3444b` (revisão 6) | 133 437 |
| `3d41f525` (revisão 7) | 160 013 |

- Por secção, na revisão 7: a F10 tem **44 715** bytes sozinha (421 linhas), a §7 (as tabelas das revisões) 27 098,
  o cabeçalho e as §1–3 23 785, as fases retiradas 10 976; cada uma das outras fases fica entre 1,2 e 7 KB. A linha
  mais longa tem 840 caracteres. Uma fase cabe numa leitura; o plano inteiro não.
- Não é caso único: a mesma mensagem de erro aparece nos transcripts de **13 sessões** do ERP (procura em
  `search_session_transcripts`, com as arquivadas), de 25 115 a 50 623 tokens por leitura.

### 3. Quantos ficheiros passam do teto

Limiar: 55 000 bytes, que neste tipo de texto são ~25 mil tokens (`find … -printf '%s'`, 2026-11-19):

| Pasta | `.md` acima de 55 KB | Total de `.md` |
|---|---:|---:|
| `modelo-de-mudanca/` | 9 | 108 |
| `docs/` | 10 | 258 |
| `.claude/skills/` | 1 | 37 |
| `.context/` (handoffs e briefings) | 0 | 116 |

- Em `modelo-de-mudanca/`, de 124 a 56 KB: o plano do acesso à BD, `tarefas-categorias/fidelidade-final.md`, o
  arquivo novo das revisões (ele próprio já passa do teto), `fila-de-commits/plano-fila-de-commits.md`,
  `tarefas-categorias/desenho.md`, `excecoes-do-npm-audit/plano-excecoes-com-prazo.md`,
  `financeiro/plano-contas-a-pagar.md`, `versionar/plano-versionar-pelas-categorias.md` e
  `tarefas-categorias/plano-fase-1.md`.
- Os 11 `BRIEF-*.md` vão de 3,2 a 26 KB: os briefings comuns cabem todos numa leitura. O maior é
  `BRIEF-plano-d-uma-tarefa-por-sessao.md` (25 964 bytes). O de acesso à BD tem 3 364.

### 4. O que o Morg-laws já diz (clone, commit `7b4c228`)

| Onde | O que diz | Teria travado o incidente? |
|---|---|---|
| `skills/orquestrando-sessoes/SKILL.md:33-43`, «Uma leitura longa: uma parte de cada vez» | Ler uma parte inteira (saber antes o tamanho; se veio cortada, ler o resto), escrever logo a nota dela em disco, só depois abrir a seguinte. **Uma leitura grande divide-se em duas sessões**, com o limite do projeto de origem de **6 partes ou ~60 mil tokens** (l. 40). O plano da fase diz o método de leitura (l. 41) | Sim, em parte: 81 mil tokens só de leitura passam dos 60 mil, e a tarefa ter-se-ia partido. Não fala da escrita |
| `skills/orquestrando-sessoes/SKILL.md:48` | Uma fase cabe numa sessão curta, abaixo dos ~150 mil tokens; a que não cabe parte-se no plano, antes de começar | Sim, se alguém medisse: ~185 mil não cabem. Mas não diz **quem** mede nem **como** |
| `skills/orquestrando-sessoes/SKILL.md:58` | O pedido da filha leva o objetivo, os ficheiros, o que já se descartou, como se prova e o modelo | Não: não pede a secção, as linhas nem o tamanho |
| `modelos/claude/hooks/limite_de_linhas.py:13-16,41` | Hook PreToolUse (Write/Edit) que recusa um ficheiro acima de **500 linhas** que cresça; a lista de extensões **inclui `.md`** | Sim, indiretamente: o plano não passaria das 500 linhas sem se partir. As edições pela shell escapam (l. 4) |
| `modelos/testes/test_tamanho_dos_arquivos.py:18-21` | O mesmo limite de 500 linhas, com `.md`, para todos os ficheiros do git, com linha de base | O mesmo, e apanha a shell |
| `modelos/documentos/plano.md` | O molde do plano: contexto, decisões, fora do escopo, passos (uma linha por fase), prova | Um plano neste molde não leva as revisões dentro |
| `skills/passando-o-trabalho/SKILL.md:82` | O handoff tem menos de 150 linhas | Não se aplica ao plano |

**O que falta no Morg-laws:**

- Nenhum texto diz que **a mãe mede** o que manda ler e escrever **antes** de abrir a filha. O limite de 60 mil existe,
  mas fica do lado de quem lê, que só o descobre a meio.
- A **escrita** não conta em lado nenhum. Uma reescrita custa o ficheiro duas vezes (ler e escrever).
- O teto de 25 mil tokens por leitura e a diferença entre a página parcial e o erro com `offset`/`limit` não estão
  escritos. A regra «saber antes o tamanho» (l. 37) não diz como (`wc -c`, `grep -n '^#'`).
- O limite de tamanho é em **linhas**. Num `.md` com linhas de 840 caracteres, 500 linhas tanto podem ser 20 KB como
  100 KB. Neste plano, por acaso, 500 linhas são ~55 KB, ou seja, perto do teto da Read.
- Não há regra para um plano que cresce por revisões: onde vão as tabelas «achado → onde ficou», as fases retiradas e
  as notas de cada revisão.

### 5. O que o ERP adotou e o que ficou de fora

- A `orquestrando-sessoes` do ERP tem as fases, a orquestradora magra e o modelo pela tarefa, e diz na l. 32 «Cada fase
  vai para uma sessão nova com o briefing, a secção da fase e **só o contexto de que precisa**». É o princípio certo,
  sem medida nem forma.
- **Não tem** a secção «Uma leitura longa: uma parte de cada vez» do Morg-laws (`grep` por «leitura longa» e «parte de
  cada vez» em `.claude/skills/`: nenhuma ocorrência nesta skill).
- O `limite_de_linhas.py` **não foi portado** (`docs/adocao-do-morg-laws.md:83`: «o ERP já tem a catraca de tamanho de
  ficheiro»). Mas a catraca do ERP só mede código (`scripts/catracas/medir-tamanho-de-ficheiro.mjs:11`,
  `\.(ts|tsx|mts|mjs|js|jsx)$`) e deixa fora `modelo-de-mudanca/` e `docs/` (l. 14). Os `.md` de plano ficaram, por isso,
  sem nenhum limite: a parte do Morg-laws que os cobria perdeu-se na adoção.

### 6. As opções

| # | Opção | Prós | Contras | Custo |
|---|---|---|---|---|
| A | **Teto no briefing:** antes de abrir a filha, a mãe mede com `wc -c` o que manda ler e escrever, soma, e parte a tarefa se passar de um orçamento (por exemplo 60 mil tokens de leitura, a regra do Morg-laws, ou ~130 KB de leitura e escrita juntas) | Ataca a causa (a mãe decide o tamanho); usa o número que o Morg-laws já tem; nenhuma ferramenta nova | Só texto: depende de a mãe se lembrar; a razão bytes/token varia | Baixo: um parágrafo na `orquestrando-sessoes` |
| B | **A filha lê por secções:** `grep -n '^#'` para os títulos, depois `Read` com `offset`/`limit` de uma secção de cada vez, abaixo de ~50 KB por chamada | Acaba com o erro; o Morg-laws já tem o texto (§2, l. 33-43) para copiar | Não reduz o volume: ler tudo em fatias continua a encher a janela | Muito baixo: adotar a secção que falta |
| C | **Partir os planos grandes:** um índice curto (o molde `modelos/documentos/plano.md`) e um ficheiro por fase; as revisões e as tabelas da §7 num arquivo à parte | Cada filha lê o índice, o briefing e a sua fase (1–45 KB em vez de 160); a auditoria de uma fase lê só essa fase | Uma revisão que toque em várias fases mexe em vários ficheiros; ligações a manter; é preciso decidir quando partir | Médio por plano; 9 planos acima do teto hoje. O arquivo de 105 KB que a D26 criou também passa do teto e precisaria do mesmo |
| D | **Catraca de tamanho para os `.md` de plano**, em **bytes** (não linhas), com linha de base e «só encolhe», como as outras catracas do ERP | Barreira de máquina: apanha a shell e todas as sessões; impede que o próximo plano cresça por camadas | Os 9 planos de hoje entram na linha de base (não encolhem sozinhos); um teto mal escolhido parte planos pequenos; mexe em `scripts/` e nos testes | Médio: um `medir-…` novo, testes e a linha de base |
| D' | O mesmo, como **hook** PreToolUse (Write/Edit), à maneira do `limite_de_linhas.py` | Avisa no momento da escrita, antes do commit | Não apanha a shell; mais um hook | Médio |
| E | **Modelo de briefing «só o que precisa»** na `orquestrando-sessoes`: cada ficheiro a ler com a **secção, as linhas e o tamanho medido**; o que **não** ler; o que se escreve; o orçamento; como se prova; o modelo; o fim | Torna o tamanho visível à mãe ao escrever e à filha ao ler; organiza o briefing | Só texto; um briefing mais longo de escrever | Baixo |
| F | Um hook no `start_session` que lê o briefing, acha os caminhos e soma os tamanhos | Mediria sozinho, sem depender da mãe | **Não verificado** que os hooks do Claude Code vejam as ferramentas da app (`mcp__ccd_session__*`); achar caminhos num texto livre é frágil | Alto, e incerto |

Nenhuma das opções resolve sozinha: B tira o erro mas não o volume; A e E dependem de texto; C e D tratam o tamanho do
plano mas não o pedido de «reescrever tudo» numa sessão.

### 7. Como seria o briefing (resposta à pergunta 2)

Um briefing que caberia no orçamento, escrito para a 7.ª correção do incidente:

- **Objetivo:** fechar os achados T1 a T10 nas fases vivas do plano, com as D24 a D26.
- **Ler, por esta ordem (medido pela mãe):** o briefing comum (3,4 KB); a 6.ª auditoria (19 KB, inteira); do plano,
  só a §2 e as fases que os achados citam, pelas linhas do `grep -n '^#'` (por exemplo F1b, l. 325-397, 7 KB).
- **Não ler:** a §7, as fases retiradas, a F10 (44 KB), salvo um achado que a cite.
- **Escrever:** só as secções tocadas, com `Edit`; a passagem dos registos para o arquivo (D26) numa filha à parte.
- **Orçamento:** leitura + escrita até ~60 mil tokens; se a soma medida passar, a mãe parte antes de abrir.
- **Prova, modelo e fim:** como hoje.

Com a D26 («reescrever limpo»), a forma que cabe é **duas filhas**: uma que move os registos para o arquivo, sem mudar
o texto, e outra que reescreve as fases vivas a partir do índice já limpo. Partir assim é a regra do Morg-laws
(«a que não cabe parte-se no plano, antes de começar», l. 48), aplicada pela mãe.

## O que não se verificou

- Os parâmetros exatos da leitura que deu o erro: o `list_events` só mostra «(called Read)». As linhas 421–1018
  deduzem-se do tamanho (58 284 bytes, ~26 400 tokens contra os 26 379 do erro).
- A razão 2,2 bytes por token mediu-se num ficheiro só. Outros textos (código, inglês) dão outra razão.
- Os ~185 mil tokens da filha são uma soma estimada, não o `/context` dela; não se mandou mensagem à filha, que ainda
  trabalha.
- Se os hooks PreToolUse do Claude Code apanham as ferramentas da app (`mcp__ccd_session__start_session`): não se
  testou (opção F).
- Das `pesquisas/` do Morg-laws só se leu a lista dos nomes: nenhuma trata do tamanho do contexto de uma filha. Os
  bastidores privados não se abriram.
- Não se mediu quantas das 13 sessões com o erro tinham um briefing a pedir o ficheiro inteiro.

## Conclusão

**Pergunta 1.** Sim, em parte. O Morg-laws já tem três peças que, juntas, teriam travado este caso: a «leitura longa»
com o limite de ~60 mil tokens por sessão (`skills/orquestrando-sessoes/SKILL.md:33-43`), a fase abaixo dos ~150 mil
(l. 48) e o limite de tamanho que inclui os `.md` (`modelos/claude/hooks/limite_de_linhas.py`,
`modelos/testes/test_tamanho_dos_arquivos.py`). O ERP adotou a segunda e deixou cair a primeira e a terceira: a
catraca do ERP não mede `.md` nem `modelo-de-mudanca/`. O que falta nos dois lados é a mãe **medir** antes de abrir,
contar a **escrita**, e medir em **bytes**, não em linhas.

**Pergunta 2.** A mãe manda caminhos com a secção e o tamanho medido, diz o que não ler, soma leitura e escrita contra
um orçamento e parte a tarefa antes de abrir a filha quando a soma passa.

**Recomendação (a decidir pelo PO):** A + B + E já, porque são texto na `orquestrando-sessoes` e custam pouco; D a
seguir, como catraca em bytes com linha de base, para que nenhum plano novo volte a crescer por camadas; C só para os
planos que voltem a ser tocados, a começar pelo do acesso à BD e pelo arquivo novo, sem partir os 9 de uma vez. F não.
Devolver ao Morg-laws o que falta lá (medir antes, contar a escrita, bytes, o comportamento da Read).

**Decisões do PO:**

1. Adotar no ERP a secção «Uma leitura longa» do Morg-laws, com o limite de ~60 mil tokens, ou outro número?
2. O orçamento do briefing: conta só a leitura (como o Morg-laws) ou leitura e escrita? Que número?
3. A catraca de tamanho dos `.md`: sim ou não; em bytes ou em linhas; que teto (por exemplo 50 KB); que pastas
   (`modelo-de-mudanca/`, `.context/`, `docs/`); como catraca, como hook, ou os dois?
4. Partir os planos grandes: só ao tocá-los, ou os 9 já? E na forma índice + um ficheiro por fase?
5. A 7.ª correção em curso: deixá-la acabar como está, ou, nas correções seguintes deste plano, partir em duas filhas
   (mover os registos; reescrever as fases)?
6. Levar o que falta ao Morg-laws (numa sessão própria, depois desta verificação)?
