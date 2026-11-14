# Instalar só algumas skills do Morg-laws

Data: 2026-11-14.

## Pergunta

Hoje o `npx skills add Carlobks/Morg-laws` traz as 13 skills, e quem não usa uma pilha (Supabase, por exemplo) apaga
à mão as que não quer. A ferramenta deixa escolher as skills uma a uma, listar as de um repositório sem instalar e
remover uma? O que o `skills-lock.json` guarda numa instalação parcial, e o que um `update` ou um segundo `add` fazem
com as que ficaram de fora? Uma skill do Morg-laws depende de outra? O que no manual, no molde `AGENTS.md`, nos testes
e na skill `comecando-um-projeto` fica errado quando a pessoa instala só uma parte? E como se prova o comando numa
pasta temporária?

## Fontes

Lidas em 2026-11-14. O código e a documentação da ferramenta foram lidos na tag `v1.8.1`, com o `gh api` (o arquivo
inteiro, procurado com `grep`); a versão publicada, no registro do npm com o `WebFetch`. Nada foi instalado nem
rodado. Cada link tem a sua entrada no `FONTES.md`.

- **A referência dos comandos, na 1.8.1** —
  https://github.com/vercel-labs/skills/blob/v1.8.1/docs/commands.md — as opções do `add` (`--skill`, `--list`,
  `--copy`, `-y`, `--all`), do `list`, do `update` e do `remove`; comparada linha a linha com a mesma página na tag
  `v1.7.4`.
- **O README, na 1.8.1** — https://github.com/vercel-labs/skills/blob/v1.8.1/README.md — o exemplo com `--skill`, o
  Node mínimo e a seção do hash do `skills-lock.json` (versão 2 do arquivo).
- **O código do `add`** — https://github.com/vercel-labs/skills/blob/v1.8.1/src/add.ts — como se escolhem as skills,
  quando o `-y` liga sozinho e quando a instalação copia em vez de criar links.
- **O código do `update`** — https://github.com/vercel-labs/skills/blob/v1.8.1/src/update.ts — de onde o `update` do
  projeto tira a lista do que atualizar.
- **O código do arquivo de travas** — https://github.com/vercel-labs/skills/blob/v1.8.1/src/local-lock.ts — os campos
  de cada entrada e como um `add` novo junta a sua entrada às que já existem.
- **O código do instalador** — https://github.com/vercel-labs/skills/blob/v1.8.1/src/installer.ts — a pasta canônica
  `.agents/skills/` e o modo cópia que a pula.
- **O código da telemetria** — https://github.com/vercel-labs/skills/blob/v1.8.1/src/telemetry.ts — as duas
  variáveis que a desligam.
- **As versões publicadas** — https://github.com/vercel-labs/skills/releases — as datas da 1.7.4 à 1.8.1 e as notas
  das que mexem no `remove`, no `update` e no arquivo de travas.
- **O registro do npm** — https://registry.npmjs.org/skills/latest — a versão atual e o Node exigido.
- **O próprio Morg-laws**, em `f0a1a26`: `manual/03-instalar.md`, `README.md`, o aprendizado de 2026-10-30, o molde
  `AGENTS.md` e a cópia dele na `comecando-um-projeto`, `modelos/testes/test_regras.py`, `tests/projeto_de_exemplo.py`,
  `tests/test_comecando_um_projeto.py`, as 13 `SKILL.md` com os `references/`, e os testes de teto do manual e das
  descrições.

## O que se mediu

**1. A ferramenta já escolhe uma a uma, desde antes da 1.7.4.**

- A versão atual é a **1.8.1**, de 2026-11-10 (o registro do npm e a página das versões dizem o mesmo); exige Node
  22.20 ou mais novo. Entre a testada (1.7.4, de 2026-10-19) e ela saíram a 1.7.5, a 1.7.6 e a 1.8.0.
- `--skill <nome>` (ou `-s`), repetido para várias, instala só as citadas; `--skill '*'` instala todas. Se nenhum dos
  nomes existe no repositório, termina com erro e a lista das que existem; se só alguns existem, instala esses e não
  avisa dos outros fora do modo `--json`. A opção está na tabela do `add` nas duas
  versões, sem diferença entre elas.
- `--list` (ou `-l`) mostra as skills do repositório, cada uma com a descrição, e sai sem instalar.
- Sem `--skill`, num terminal, a ferramenta abre uma lista para marcar as que se quer. Com `-y` não há lista: entram
  **todas**. O comando do P1 de hoje (`-a claude-code -y`) instala, portanto, as 13.
- Quando a ferramenta percebe que roda dentro de um agente de código, ela liga o `-y` sozinha. Isso já estava na 1.7.4.
  Pedir ao agente que rode o comando sem `--skill` traz todas, sem lista.
- Com um único agente (`-a claude-code`), o modo padrão é **cópia** direto em `.claude/skills/`, sem a pasta canônica.
  Com dois agentes de pastas diferentes (`-a claude-code -a codex`), o padrão é uma cópia em `.agents/skills/` e links
  simbólicos na pasta de cada agente. Lido no código; a prova é que mostra.
- `skills remove <nome>` tira a skill da pasta e do arquivo de travas; `remove --all` só remove as que o arquivo de
  travas registra (desde a 1.8.0). `skills list` compara a pasta com as travas e marca cada skill como acompanhada,
  modificada, sem trava ou faltando (desde a 1.7.5).
- O `skills-lock.json` (versão 2 desde a 1.8.0; a 1.8.x converte o da versão 1 ao ler) tem uma entrada por skill
  instalada: a origem, o tipo, o caminho da `SKILL.md` no repositório, um hash do conteúdo e, quando foi cópia por
  escolha, o modo. Um segundo `add` **junta** a entrada nova às que já existem. O `update` do projeto percorre só as
  entradas do arquivo: **não traz** as skills que ficaram de fora, nem uma skill nova que o Morg-laws publique depois.
- A 1.8.x aceita fixar a origem numa tag ou num commit (`dono/repo@v1.2.3`). O Morg-laws não tem tags.
- A telemetria vai para o `skills.sh` e desliga com `DISABLE_TELEMETRY` ou `DO_NOT_TRACK`.

**2. As skills se citam, mas nenhuma quebra sem a outra.**

Contei, em cada `SKILL.md` e nos `references/` (sem os `evals/`), as menções ao nome de outra das 13. Quase todas
são do tipo «para isso, é a outra skill», que só apontam o caminho. As que pesam:

- `supabase` → `sql-postgres` (4 vezes; a abertura diz que vale junto com ela). É o único par que a própria skill
  manda usar junto.
- `sql-postgres` → `supabase` (3) e `auditoria-de-seguranca` → `supabase` (2): mandam o detalhe do Supabase para a
  skill dele. Sem ela, quem não usa Supabase não perde nada.
- `comecando-um-projeto` → `pondo-o-plano-a-prova` (5): para um projeto que já tem documentos, o pedido vai para a
  outra. E o molde `AGENTS.md` que ela escreve cita as 13.
- `testes-e-provas` → `git-e-commits` (4) e `codigo-legivel` (2); `orquestrando-sessoes` ↔ `passando-o-trabalho` (4 e
  2).

Pela descrição de cada uma, quatro são de pilha: `supabase`, `sql-postgres` e `nextjs-react` (nomeiam a tecnologia) e
`desenhando-telas` (sistemas com muitos dados, como ERPs e painéis). As outras nove servem a qualquer projeto. Um
conjunto mínimo possível seria as nove gerais, com `supabase` sempre junto de `sql-postgres`.

**3. O que fica errado com uma instalação parcial.**

| Onde | O que diz hoje | O que fica errado |
|---|---|---|
| `manual/03-instalar.md:14` | O comando com `-a claude-code -y`, sem `--skill`. | Traz as 13; não ensina a escolher. |
| `manual/03-instalar.md:17` e `:34` | Testado na 1.7.4, em 2026-10-30. | A versão atual é a 1.8.1; o teste ficou velho. |
| `manual/03-instalar.md:36` | Instalar muitas é barato, e cada uma não usada é leitura a mais. | Continua certo, mas não diz como evitar as de pilha. |
| `README.md:27` e `:30` | O comando sem `-a` nem `--skill`. | Num terminal abre a lista; dentro de um agente traz as 13. |
| `modelos/documentos/AGENTS.md:41-53` | O índice cita as 13; a linha `:53` junta as três de pilha numa linha só. | O projeto parcial tem de apagar linhas, e dividir a `:53` se instalou só uma das três. |
| `skills/comecando-um-projeto/assets/molde-AGENTS.md:41` | Cópia igual do molde. | O mesmo. |
| `skills/comecando-um-projeto/SKILL.md:59` | Escreve o `AGENTS.md` do molde, com o resto «como está». | Escreve o índice das 13, mesmo que só algumas estejam instaladas. |
| `modelos/testes/test_regras.py:130-139` | O conjunto das skills entre crases no índice tem de ser igual ao das pastas em `.claude/skills/`, e as chaves do `skills-lock.json` iguais às pastas. | Passa com uma parte **se** o índice citar só as instaladas. Com o molde como está, reprova. Quem apaga uma pasta à mão (o jeito de hoje) também reprova na `:139`, porque a trava ainda a tem: o certo é remover com `skills remove`. |
| `tests/projeto_de_exemplo.py:14-15` | Instala todas, porque o índice do molde cita todas. | Nenhum teste cobre um projeto com só uma parte. |
| `aprendizados/2026-10-30-instalacao-das-skills.md:7` e `:11` | 10 skills, `skills@latest`, versão 1.7.4. | Fato do passado; não fala de `--skill`. |
| `AGENTS.md:51` (o da raiz) e `prova/README.md:83` | Citam o comando ou a cópia inteira. | Só citam; mudam se o comando mudar. |
| `tests/test_comecando_um_projeto.py:55` e `:138` | O README tem de ter `npx skills add` antes da seção da primeira mensagem. | Nada, enquanto o texto continuar no README. |

**4. Os tetos.** A parte `03` do manual tem 1.972 palavras de prosa para um teto de 3.450; no P1, «Na prática» tem 123
de 250 e «Por quê e fonte» 203 de 400 (contadas com o `verificador_do_manual.py`; os blocos de código não contam). A
soma das descrições das 13 skills é 7.366 para o `TETO_DA_SOMA` de 7.600 (folga de 234); o
`test_formato_das_skills.py` passa (23 testes, OK, no ambiente virtual da casa, que tem o PyYAML).

## O que não se verificou

- Nada foi rodado: o comportamento do `--skill`, do `-y`, do modo cópia, do `update` e do `remove` vem do código e da
  documentação da 1.8.1. Só a prova numa pasta temporária confirma.
- Onde a 1.8.1 grava o hash quando instala em modo cópia, sem a pasta canônica: a seção do hash fala de
  `.agents/skills/`, e o código do instalador pula essa pasta na cópia.
- Se a instalação de projeto lê ou escreve algo na pasta pessoal (uma trava global, a última escolha de agentes).
- Se o sufixo `@` de fixar um commit convive com o `@` que também nomeia uma skill.
- Quais variáveis de ambiente fazem a ferramenta achar que roda dentro de um agente: ela usa um pacote à parte, que
  não li.
- A página do pacote no site do npm: li o registro, não a página.

## Conclusão

A ferramenta já resolve a escolha: `--list` mostra as 13 e `--skill` instala só as citadas, nas duas versões. O que
falta é do Morg-laws: o P1 e o README mandam um comando que traz todas, o índice do molde `AGENTS.md` cita as 13, a
`comecando-um-projeto` o escreve inteiro, e o teste do molde reprova quando o índice e a pasta divergem. Nenhuma skill
para de funcionar sem outra; o único par que se pede junto é `supabase` com `sql-postgres`. Quem já instalou tudo
remove as que não quer com `skills remove`, e não apagando a pasta, para a trava acompanhar. A prova numa pasta
temporária, com a versão fixada, fecha o que aqui só se leu.
