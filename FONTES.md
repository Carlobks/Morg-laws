# Fontes

Toda fonte citada no repositório entra aqui, com a data em que foi lida e o que ela sustenta.
Fonte secundária leva a marca *(secundária)* até ser conferida na original.

## Entrega de regras a agentes

- **Claude Code — memória, CLAUDE.md, AGENTS.md e imports** — https://code.claude.com/docs/en/memory — lido em 2026-10-29.
  Sustenta: CLAUDE.md com menos de 200 linhas; imports não economizam contexto; com CLAUDE.md e AGENTS.md juntos, o Claude lê só o CLAUDE.md.
  Relido em 2026-11-06 (a seção do tamanho e a do `CLAUDE.md` de subpasta que perde o fim). Sustenta também: o limite dos arquivos que carregam sob demanda (`CLAUDE.md` de subpasta, regras com `paths`) conta-se em caracteres, depende da janela de contexto e vale desde o Claude Code v2.1.309; do arquivo que passa dele, o Claude recebe só o começo; a página manda contar com `wc -m` (usado em `skills/escrevendo-regras-de-agente/` §4).
  Relido em 2026-11-08. Sustenta também: o `CLAUDE.md` de uma subpasta carrega quando o Claude lê, escreve ou edita outro arquivo dela; o `AGENTS.md` de uma subpasta, sem nenhum `CLAUDE.md` próprio, carrega quando o Claude abre lá um arquivo com o Read (por isso as cópias dos moldes dentro de uma skill não se chamam `AGENTS.md` nem `CLAUDE.md`).
- **Claude Code — skills** — https://code.claude.com/docs/en/skills — lido em 2026-10-29.
  Relido em 2026-11-08 (a seção das descrições cortadas e a dos sinais «<» e «>»). Sustenta: o orçamento da lista das skills é 1 % da janela do modelo; a lista leva sempre todos os nomes e, quando transborda, tira primeiro as descrições das skills menos invocadas; cada entrada é cortada em 1.536 caracteres; «<» e «>» numa descrição aparecem como `&lt;` e `&gt;`. Fundamenta o teto de 7.600 caracteres para a soma das descrições, em `tests/test_formato_das_skills.py`.
  Sustenta: só a descrição da skill carrega no início; o corpo carrega quando é usada.
  Relido em 2026-11-08 (os primeiros 100.000 de 118.986 caracteres). Sustenta também: `/nome-da-skill` no começo da mensagem chama a skill e o resto do texto chega como argumentos; o Claude também abre a skill sozinho pela descrição; ao compactar, o Claude Code anexa de novo a chamada mais recente de cada skill, com os primeiros 5.000 tokens dela, num orçamento comum de 25.000, e as mais antigas podem sair inteiras; o `SKILL.md` fica abaixo de 500 linhas.
- **Claude Code — marketplace de plugins** — https://code.claude.com/docs/en/plugin-marketplaces — lido em 2026-10-29 e relido em 2026-11-07 (a página «Create a marketplace»).
  Sustenta: um marketplace é um repositório com `.claude-plugin/marketplace.json`; quem o usa registra-o com `claude plugin marketplace add <owner>/<repo>` e instala com `claude plugin install <plugin>@<marketplace>`.
- **Agent Skills (padrão aberto)** — https://agentskills.io — citado pela documentação do Claude Code, 2026-10-29.
- **Vercel — skills CLI** — https://vercel.com/docs/agent-resources/skills — 2026-10-29 *(secundária: lido via busca)*.
- **AAIF — Measuring AGENTS.md: what five runs show** — https://aaif.io/blog/measuring-agents-md-what-five-runs-show-that-one-doesn-t — lido em 2026-10-29.
  Sustenta: o AGENTS.md é orientação, não barreira. Com um AGENTS.md curto (12 linhas), o agente foi mais rápido e gastou menos (um repositório, um agente, 2 tarefas, 5 corridas com e sem). O estudo **não** compara arquivos curtos com longos, e o autor chama-lhe «one data point». Conferido de novo em 2026-10-30.
- **Evaluating AGENTS.md (arXiv 2602.11988)** — https://arxiv.org/abs/2602.11988 — resumo lido em 2026-10-30.
  Sustenta: os arquivos de contexto «do not generally improve task success rates» e sobem o custo de inferência em mais de 20%, em média. O resumo não fala do tamanho dos arquivos, e a página não mostra a afiliação dos autores.
- **agents.md** — https://agents.md — lido em 2026-10-30 (numa auditoria independente). Sustenta: o formato é mantido pela Agentic AI Foundation, sob a Linux Foundation, e a página lista 23 ferramentas que o leem.
- **Claude Code — hooks** — https://code.claude.com/docs/en/hooks — lido em 2026-11-01 (a primeira parte da página) e, em 2026-11-02, as seções do `PreCompact`, do `PostCompact`, do `SessionStart` e do `InstructionsLoaded` e as linhas que citam `compact`, na versão em texto (o mesmo endereço com `.md`); não a página inteira. Sustenta: o `PreToolUse` decide com `permissionDecision` (`allow`, `deny`, `ask`, `defer`) e o `ask` passa a decisão ao usuário; sair com 2 «Blocks the tool call», com o motivo no stderr; `onFailure` aceita `continue` ou `block` (desde o Claude Code v2.1.295); o `CLAUDE_PROJECT_DIR` é a pasta onde a sessão começou e não muda com a sessão. Que as regras `ask` do `settings.json` não perguntam no modo automático foi **medido** num projeto real, não está na página (usado na skill `auditoria-de-seguranca` e em `modelos/claude/`).
  Sustenta também, para a compactação (`pesquisas/2026-11-02-hooks-de-compactacao.md`): o `PreCompact` roda antes e pode barrar; o `PostCompact` roda depois, recebe o resumo e não decide nada; o `SessionStart` volta a rodar com a origem `compact`; o `InstructionsLoaded` avisa com o motivo `compact` quando os arquivos de instruções voltam a carregar.
- **Agent Skills — especificação** — https://agentskills.io/specification — lido em 2026-11-02 (as seções do `name` e do `description` e as linhas com limites). Sustenta: `name` de 1 a 64 caracteres, só minúsculas, algarismos e hífens, sem hífen no começo, no fim ou repetido, igual ao nome da pasta; `description` de 1 a 1024 caracteres; corpo abaixo de 500 linhas (usado em `skills/passando-o-trabalho/`).
  Relido em 2026-11-08. Sustenta também: o `name` sem hífen duplo e igual ao nome da pasta; o corpo carrega inteiro quando a skill ativa (menos de 5.000 tokens recomendados); as pastas opcionais `references/` (documentação que o agente lê quando precisa) e `assets/` (moldes de documento e outros recursos estáticos).
- **Codex — skills** — https://developers.openai.com/codex/skills — lido em 2026-11-02, a página inteira (o endereço redireciona para `learn.chatgpt.com`). Sustenta: o Codex segue o padrão Agent Skills, começa só com o nome, a descrição e o caminho de cada skill e procura-as em `.agents/skills` (da pasta atual até a raiz do repositório) e em `~/.agents/skills`.
  Relido em 2026-11-08 (o endereço redireciona para `learn.chatgpt.com/docs/build-skills`). Sustenta também: no CLI e na extensão chama-se uma skill com `/skills` ou digitando `$`; o Codex escolhe a skill pela descrição, e `allow_implicit_invocation: false` em `agents/openai.yaml` desliga isso (o `$skill` continua valendo); a lista inicial de skills usa no máximo 2 % da janela do modelo, ou 8.000 caracteres se a janela não é conhecida, e as descrições são encurtadas primeiro (depois disso o Codex pode deixar skills de fora, com um aviso; o orçamento sobe com `skills.max_context_tokens`). Fundamenta o teto de 7.600 caracteres para a soma das descrições.
- **Claude — Agent Skills, visão geral da plataforma** — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview — lido em 2026-11-08, a página inteira. Sustenta: o `name` com até 64 caracteres, só minúsculas, algarismos e hífens, sem marcas XML e sem as palavras reservadas `anthropic` e `claude`; a `description` não vazia, com até 1.024 caracteres e sem marcas XML (a base do `tests/test_formato_das_skills.py`).
- **Claude Code — app de desktop** — https://code.claude.com/docs/en/desktop — lido em 2026-11-08 (os primeiros 100.000 de 221.007 caracteres). Sustenta: na app de desktop renomeia-se uma sessão abrindo-a e clicando no título dela, na barra do título, ou pedindo ao Claude que a renomeie ou arquive (a base do item do título das sessões em `skills/orquestrando-sessoes/`).
- **skills (a ferramenta do `npx skills add`)** — https://github.com/vercel-labs/skills — lido em 2026-11-02: o começo do README, `docs/agents.md` (procura por Codex e Claude Code) e os formatos de origem em `docs/commands.md`. Sustenta: instala para o Claude Code em `.claude/skills/` e para o Codex em `.agents/skills/`, escolhe os agentes com `-a` e aceita uma pasta local como origem.

## Compactação da conversa

Lidas em 2026-11-02 para a skill `passando-o-trabalho`; o que se leu de cada uma está em `pesquisas/2026-11-02-compactacao-claude-code-e-codex.md`.

- **Claude Code — comandos** — https://code.claude.com/docs/en/commands — Sustenta: `/compact` aceita instruções de foco para o resumo; `/autocompact` muda o tamanho da janela de compactação automática; `/context` mostra o que ocupa a janela.
  Relido em 2026-11-08. Sustenta também: `/rename [nome]` muda o nome da sessão e mostra-o na barra do prompt; sem nome, gera um a partir da conversa; vale também no modo não interativo (`-p`); o nome tem no máximo 200 caracteres.
- **Claude Code — janela de contexto** — https://code.claude.com/docs/en/context-window — Sustenta: o que volta depois de compactar (CLAUDE.md da raiz, regras sem `paths:`, descrições das skills, até cinco arquivos lidos ou editados, o corpo das skills cortado em 5 mil tokens a guardar o começo) e que compactar com um foco antes da automática guarda o que se escolhe.
- **Claude Code — como funciona** — https://code.claude.com/docs/en/how-claude-code-works — Sustenta: a compactação automática perto do limite pode perder instruções do começo da conversa; uma seção «Compact instructions» no CLAUDE.md ou um `/compact` com foco controlam o que fica.
- **Claude Code — glossário** — https://code.claude.com/docs/en/glossary — Sustenta: o CLAUDE.md da raiz sobrevive à compactação e é relido do disco; instruções dadas só na conversa podem perder-se.
- **Claude Code — configuração do modelo** — https://code.claude.com/docs/en/model-config — Sustenta: sem configurar, a automática dispara no limite do modelo (com exceções por modelo); a janela de compactação vai de 100 mil a 1 milhão de tokens.
- **Claude Code — referência das configurações** — https://code.claude.com/docs/en/settings-reference — Sustenta: a compactação por inatividade (conversa longa parada há cerca de uma hora) e as chaves `idleCompaction` e `autoCompactEnabled`.
- **Claude Code — custos** — https://code.claude.com/docs/en/costs — Sustenta: a seção «Compact instructions» no CLAUDE.md; compactar um contexto grande é ele próprio um pedido grande.
  Relido em 2026-11-06 (as seções «Reduce token usage» e «Why usage climbs in a long session»), para `pesquisas/2026-11-05-linha-de-base-do-uso.md`. Sustenta também: o custo cresce com o tamanho do contexto; a primeira mensagem depois de uma pausa maior que a vida da cache reprocessa o contexto inteiro; uma mensagem de outra sessão, entregue a uma sessão parada, vira um turno novo que manda o contexto inteiro; num plano de API ou de nuvem, o gasto alto costuma vir de sessões longas nunca limpas e do Opus deixado como padrão.
- **Codex — comandos** — https://developers.openai.com/codex/cli/slash-commands — o endereço redireciona para `learn.chatgpt.com`. Sustenta: o `/compact` pede confirmação e troca os turnos antigos por um resumo; a página não documenta argumentos; o `/recap` resume sem liberar contexto.
  Relido em 2026-11-08 (a página para onde redireciona, `learn.chatgpt.com/docs/developer-commands?surface=cli`, na parte depois dos primeiros 100.000 caracteres). Sustenta também: `/rename <nome>` dá um nome à conversa salva, e `/rename` sozinho abre o pedido do nome; a transcrição não muda. A página não diz se a extensão ou a aplicação têm outra forma.
- **Codex — referência da configuração** — https://developers.openai.com/codex/config-reference — o endereço redireciona para `learn.chatgpt.com`. Sustenta: `compact_prompt` troca o prompt da compactação; `model_auto_compact_token_limit` e `model_post_turn_compact_threshold_percent` decidem quando compacta sozinho, sem valor recomendado.

## Git e contas

- **Git Credential Manager — várias contas** — https://github.com/git-ecosystem/git-credential-manager/blob/main/docs/multiple-users.md — lido em 2026-10-29.
  Sustenta: o usuário no endereço do repositório escolhe a conta só para aquele repositório.

- **Git — `lockfile.c` (mensagem do `index.lock`)** — https://github.com/git/git/blob/master/lockfile.c — lido em 2026-10-29.
  Sustenta: o git não manda apagar o lock; só diz que outro processo pode estar a correr ou que o lock pode estar velho.
- **Pro Git — 2.6 Tagging** — https://git-scm.com/book/en/v2/Git-Basics-Tagging — lido em 2026-10-31 (no projeto de origem). Sustenta: a tag anotada guarda autor, data e mensagem; usada para marcar cada versão (`modelos/changelog/`).
- **Git — `git` (opções globais)** — https://git-scm.com/docs/git — lido em 2026-11-02. Sustenta: as opções entre o `git` e o subcomando (`-C <caminho>` e `-c <nome>=<valor>` com o valor à parte; `--git-dir=`, `--work-tree=`, `--no-pager`/`-P` e outras), que o `perguntar_antes.py` pula para achar o `push`.
- **GitHub CLI — `gh api`** — https://cli.github.com/manual/gh_api — lido em 2026-11-02. Sustenta: «The default HTTP request method is GET normally and POST if any parameters were added»; os parâmetros vêm de `-f`/`--raw-field` e `-F`/`--field`, o corpo de `--input`, e o método muda com `-X`/`--method` (usado no `perguntar_antes.py`).

## Changelog e versões

Lidas em 2026-10-31 no projeto de origem, onde sustentaram a decisão escrita (ADR) do changelog por fragmentos e da versão SemVer.

- **Keep a Changelog 1.1.0** — https://keepachangelog.com/en/1.1.0/ — Sustenta: as seis categorias e a ordem (Added, Changed, Deprecated, Removed, Fixed, Security, aqui em português) e um changelog escrito para pessoas, com a versão e a data.
- **towncrier** (tutorial) — https://towncrier.readthedocs.io/en/stable/tutorial.html — Sustenta: um arquivo por mudança, juntado e apagado na hora do lançamento. Só a ideia: o modelo `juntar_changelog.py` não usa o towncrier (biblioteca padrão apenas). Relido em 2026-11-06: o nome do fragmento junta o número da issue e o tipo, e a compilação apaga os fragmentos com `git rm` (a ideia do arquivo por bug em `skills/git-e-commits/` §6).
- **GitLab — How we solved GitLab's CHANGELOG conflict crisis** (2018) — https://about.gitlab.com/blog/2018/07/03/solving-gitlabs-changelog-conflict-crisis/ — lido em 2026-11-06. Sustenta: com um `CHANGELOG` único, os pedidos de merge abertos ao mesmo tempo colidiam no mesmo lugar; a solução foi um arquivo por mudança numa pasta, compilado por um script no lançamento. Texto de um fornecedor, sem números (usado em `skills/git-e-commits/` §6).
- **Semantic Versioning 2.0.0** — https://semver.org/lang/pt-BR/ — Sustenta: MAIOR.MENOR.CORREÇÃO; o MAIOR sobe com uma mudança incompatível; no 0.y.z tudo pode mudar; os metadados de compilação (`+…`) não contam na comparação.
- **CalVer** — https://calver.org/ — Sustenta a alternativa descartada: a versão pela data não diz a quem usa se uma atualização quebra algo.

## Segurança

- **React — Critical Security Vulnerability in React Server Components (CVE-2025-55182)** — https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components — lido em 2026-10-30.
  Sustenta: CVSS 10.0; versões 19.0, 19.1.0, 19.1.1 e 19.2.0 afetadas; vulnerabilidades novas acrescentadas depois.
- **Next.js — Security Advisory CVE-2025-66478** — https://nextjs.org/blog/CVE-2025-66478 — 2026-10-30 *(secundária: lida via busca)*.
- **Vercel — React2Shell Security Bulletin** — https://vercel.com/kb/bulletin/react2shell — 2026-10-30 *(secundária: lida via busca)*. Sustenta: atualizar é a única correção completa.
- **Vercel — Postmortem on Next.js middleware bypass (CVE-2025-29927)** — https://vercel.com/blog/postmortem-on-next-js-middleware-bypass — lido em 2026-10-30.
  Sustenta: o cabeçalho `x-middleware-subrequest` saltava o middleware em apps com servidor próprio; o middleware não deve ser a única proteção das rotas.

- **gitleaks** (licença MIT) — https://github.com/gitleaks/gitleaks — lido em 2026-10-30.
  Sustenta: `gitleaks git --log-opts=…` verifica um intervalo de commits; sai com 0 sem vazamentos e com 1 quando acha (usado em `modelos/pre-push`).
- **gitleaks-action** — https://github.com/gitleaks/gitleaks-action — lido em 2026-10-30. Sustenta: a chave `GITLEAKS_LICENSE` é «required for organizations, not required for user accounts». Desde 2026-11-01 o CI deste repositório não usa a action: roda o binário.
- **gitleaks 8.30.1 — versão publicada** — https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1 — conferida em 2026-10-31 no projeto de origem. Sustenta: o arquivo
  https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz e o sha256 escrito nos workflows (`.github/workflows/seguranca.yml`, `modelos/github/workflows/ci.yml`).
- **GitHub — Secure use reference (GitHub Actions)** — https://docs.github.com/en/actions/reference/security/secure-use — lido em 2026-11-01. Sustenta: «Pin references to actions to a commit SHA», porque uma tag pode ser movida ou apagada por quem ganhar acesso ao repositório da action; o `GITHUB_TOKEN` com as permissões mínimas, só leitura por padrão; evitar o `pull_request_target` quando não é necessário (usado nos workflows e em `modelos/testes/test_ci.py`).
- **npm audit** — https://docs.npmjs.com/cli/v11/commands/npm-audit — lido em 2026-10-30. Sustenta: `--audit-level` decide a partir de que gravidade o comando falha, sem filtrar o relatório; exige um lockfile.
- **OSV-Scanner — saída e códigos de saída** — https://google.github.io/osv-scanner/output/ — lido em 2026-10-30. Sustenta: sai com 1 quando há qualquer vulnerabilidade e com 128 quando não acha pacotes; não documenta um limiar de gravidade.

## Banco de dados (PostgreSQL, Supabase, PostgREST)

Lidas em 2026-10-30 numa auditoria independente das skills `sql-postgres` e `supabase`; cada trecho que elas sustentam foi depois provado num PostgreSQL 18.3 descartável.

- **PostgreSQL 18 — Row Security Policies** — https://www.postgresql.org/docs/18/ddl-rowsecurity.html — Sustenta: o `USING` filtra sem erro e só o `WITH CHECK` dá erro; superusuário e `BYPASSRLS` passam sempre; o dono passa, salvo `FORCE ROW LEVEL SECURITY`.
- **PostgreSQL 18 — CREATE FUNCTION** («Writing SECURITY DEFINER Functions Safely») — https://www.postgresql.org/docs/18/sql-createfunction.html — Sustenta: uma `SECURITY DEFINER` sem `search_path` seguro pode ser desviada por uma tabela temporária.
- **PostgreSQL 18 — CREATE VIEW** — https://www.postgresql.org/docs/18/sql-createview.html — Sustenta: por padrão, a vista aplica as políticas do dono; `security_invoker` muda isso.
- **PostgreSQL 18 — information_schema.columns** — https://www.postgresql.org/docs/18/infoschema-columns.html — Sustenta: só aparecem as colunas a que o usuário atual tem acesso.
- **PostgreSQL 18 — Sequence Manipulation Functions** — https://www.postgresql.org/docs/18/functions-sequence.html — Sustenta: `nextval` e `setval` não se desfazem com o `ROLLBACK`.
- **PostgreSQL 18 — Enumerated Types** — https://www.postgresql.org/docs/18/datatype-enum.html — Sustenta: os valores de um `ENUM` seguem a ordem da declaração (o `ADD VALUE` aceita `BEFORE`/`AFTER`); acrescentar e renomear existem, remover e reordenar não.
- **PostgreSQL 18 — ALTER TYPE** — https://www.postgresql.org/docs/18/sql-altertype.html — Sustenta: `ADD VALUE` e `RENAME VALUE`; o valor novo só se usa depois do commit.
- **PostgreSQL 18 — ALTER TABLE** — https://www.postgresql.org/docs/18/sql-altertable.html — Sustenta: o `ACCESS EXCLUSIVE` por padrão, o `DEFAULT` volátil que reescreve a tabela, o `NOT VALID` e o `VALIDATE CONSTRAINT`; o dono desliga os gatilhos com `DISABLE TRIGGER`, e no modo `replica` (`session_replication_role`) só disparam os `ENABLE ALWAYS`.
- **PostgreSQL 18 — SET** — https://www.postgresql.org/docs/18/sql-set.html — Sustenta: o `SET LOCAL` fora de uma transação só dá um aviso e não tem efeito.
- **PostgreSQL 18 — Client Connection Defaults** (`search_path`) — https://www.postgresql.org/docs/18/runtime-config-client.html — Sustenta: o esquema temporário, se não está no caminho, é pesquisado primeiro para tabelas, e nunca para funções nem operadores.
- **PostgreSQL 18 — Privileges** — https://www.postgresql.org/docs/18/ddl-priv.html — Sustenta: o `MAINTAIN` (desde o 17) permite `VACUUM`, `ANALYZE`, `CLUSTER`, `REINDEX` e `LOCK TABLE`.
- **Supabase — Row Level Security** — https://supabase.com/docs/guides/database/postgres/row-level-security — Sustenta: `search_path` vazio nas `SECURITY DEFINER`; tabela exposta sem RLS aberta a quem tem grant; vistas passam por cima do RLS; o dono `postgres` tem `bypassrls`; `raw_user_meta_data` editável pelo usuário; regras de desempenho das políticas.
- **Supabase — Securing your API** — https://supabase.com/docs/guides/api/securing-your-api — Sustenta: os privilégios por padrão do `public`, que mudam conforme a data de criação do projeto.
- **Supabase — Server-Side Auth for Next.js** — https://supabase.com/docs/guides/auth/server-side/nextjs — Sustenta: no servidor, não confiar no `getSession()`.
- **Supabase — Testing Overview** — https://supabase.com/docs/guides/local-development/testing/overview — Sustenta: definir o `sub` do usuário antes das asserções.
- **PostgREST — Errors** — https://docs.postgrest.org/en/stable/references/errors.html — Sustenta: o `PGRST204` é coluna do payload; o `42501` chega como HTTP 401 ou 403.

## Interface e acessibilidade

- **WCAG 2.2 — Contrast (Minimum), 1.4.3** — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — lido em 2026-10-30.
  Sustenta: 4,5:1 para texto normal e 3:1 para texto grande, que é ≥ 18 pt (≈ 24 px) ou ≥ 14 pt em negrito (≈ 18,5 px).
- **WCAG 2.2 — Target Size (Minimum), 2.5.8** — https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — lido em 2026-10-30. Sustenta: alvo ≥ 24 × 24 px (AA).
- **Apple HIG — Accessibility** — https://developer.apple.com/design/human-interface-guidelines/accessibility — lido em 2026-10-30. Sustenta: controles de 44 × 44 pt (padrão) e 28 × 28 pt (mínimo) em iOS e iPadOS.
- **Apple HIG — Tab bars** — https://developer.apple.com/design/human-interface-guidelines/tab-bars — lido em 2026-10-30. Sustenta: menos abas navegam melhor; aba "Mais"; lista personalizável com 5 ou menos. **Não** traz um teto de 6.
- **Material Design 3 — Tabs** — https://m3.material.io/components/tabs/guidelines — lido em 2026-10-30. Sustenta: não mais de 4 abas fixas.
- **WCAG 2.2 — Use of Color, 1.4.1** — https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html — citada desde 2026-10-30 em `skills/desenhando-telas/references/tetos-e-fontes.md` *(secundária: não relida; a skill cita-a de memória)*.
- **Nielsen Norman Group — 10 Usability Heuristics** — https://www.nngroup.com/articles/ten-usability-heuristics/ — citada desde 2026-10-30 no mesmo arquivo (heurística 8) *(secundária: não relida)*.
- **Nielsen Norman Group — Tabs, Used Right** — https://www.nngroup.com/articles/tabs-used-right/ — citada desde 2026-10-30 no mesmo arquivo *(secundária: não relida)*.
- **Microsoft Dynamics 365 — Workspace form pattern** — https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/user-interface/workspace-form-pattern — citada desde 2026-10-30 no mesmo arquivo *(secundária: veio de uma pesquisa anterior, não relida)*.
- **SAP Fiori — When to use which floorplan** — https://www.sap.com/design-system/fiori-design-web/v1-136/page-types/floorplans/when-to-use-which-floorplan — citada desde 2026-10-30 no mesmo arquivo *(secundária: veio de uma pesquisa anterior, não relida)*.
- **Nielsen Norman Group — The Principle of Common Region** — https://www.nngroup.com/articles/common-region/ — lido em 2026-11-06. Sustenta: o que está dentro de uma fronteira (borda ou fundo) lê-se como um grupo, com mais força do que a proximidade; agrupar só com espaço deixa a tela mais simples; bordas e caixas a mais são ruído (usado em `skills/desenhando-telas/` §5).
- **Nielsen Norman Group — Proximity Principle in Visual Design** — https://www.nngroup.com/articles/gestalt-proximity/ — lido em 2026-11-06. Sustenta: o rótulo fica perto do seu campo, com uma margem maior antes do par seguinte; o que está afastado lê-se como menos relacionado e pode passar despercebido (usado em `skills/desenhando-telas/` §5).
- **Innovaccer Design System — Key Value Pair** — https://design.innovaccer.com/components/keyValuePair/usage/ — lido em 2026-11-06. Sustenta: em contentores estreitos (≈ 200 px) o rótulo vai por cima do valor; em médios (≈ 400 px) fica à esquerda, com ≈ 40 % da largura, e o valor à direita (usado em `skills/desenhando-telas/` §5).
- **Nielsen Norman Group — Toggle-Switch Guidelines** — https://www.nngroup.com/articles/toggle-switch-guidelines/ — lido em 2026-11-06. Sustenta: o interruptor tem efeito imediato, sem "Salvar"; quando isso não é possível, usam-se botões de opção ou uma caixa de seleção; os controles de efeito imediato não se misturam com os que esperam por um botão (usado em `skills/desenhando-telas/` §10).
- **Apple HIG — Toggles** — https://developer.apple.com/design/human-interface-guidelines/toggles — lido em 2026-11-06 (pela versão em dados da página, porque a página não devolve o texto sem JavaScript). Sustenta: no macOS, mais de duas opções exclusivas pedem botões de opção, que aparecem em grupos de 2 a 5, e com mais de cerca de cinco opções usa-se um menu suspenso (*pop-up button*); no iOS, o interruptor só numa linha de lista; o estado não depende só da cor (usado em `skills/desenhando-telas/` §10).
- Os demais (Rams, Tesler e os tetos por confirmar do Oracle Redwood, sem link) estão em `skills/desenhando-telas/references/tetos-e-fontes.md`.

## Relatório de erros

Lidas em 2026-10-31 no projeto de origem, para os campos do formulário `modelos/github/ISSUE_TEMPLATE/erro.yml`.

- **Mozilla — Bug writing guidelines** — https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html — Sustenta: resumo curto, passos numerados para reproduzir, resultado esperado e resultado obtido, cada um à parte.
- **OpenTelemetry — convenções semânticas das exceções** — https://opentelemetry.io/docs/specs/semconv/exceptions/exceptions-logs/ — Sustenta: o que um registro de exceção leva (tipo, mensagem, pilha de chamadas).
- **GitHub — sintaxe dos formulários de issue** — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms — Sustenta: `name`, `description`, `title`, `labels` e `body` com campos `input`, `textarea` e `markdown`, e o `validations: required`.
  Relido em 2026-11-08, para `pesquisas/2026-11-08-modelos-de-issue-e-de-pr.md`. Sustenta também: as chaves de topo permitidas são `name`, `description`, `body`, `assignees`, `labels`, `title`, `type` e `projects`; `name`, `description` e `body` são obrigatórias; o `name` não pode repetir o de outro modelo, nem o de um modelo em Markdown; uma etiqueta que não existe no repositório não é posta na issue; a sintaxe está em *public preview* e pode mudar. A página manda o arquivo começar por `name`, `description` e `body`, mas o exemplo completo dela escreve `title`, `labels`, `projects`, `assignees` e `type` antes do `body`.
- **Python — `faulthandler`** — https://docs.python.org/3/library/faulthandler.html — Sustenta: despeja a pilha de chamadas quando o processo quebra numa falha fatal; foi ele que revelou o erro do `restype` em `aprendizados/2026-11-01-python.md`.

## Testes e decisões

- **Node.js 24 — Test runner** (cobertura) — https://nodejs.org/docs/latest-v24.x/api/test.html — lido em 2026-10-23 no projeto de origem. Sustenta: os comentários `node:coverage disable`/`enable` e `ignore next` (`aprendizados/2026-11-01-testes.md`).
- **Pester — code coverage** — https://pester.dev/docs/usage/code-coverage — lido em 2026-10-23 no projeto de origem. O comportamento dos mocks filtrados do Pester 6 em `aprendizados/2026-11-01-testes.md` foi **medido**, não lido.
- **Martin Fowler — Humble Object** — https://martinfowler.com/bliki/HumbleObject.html — lido em 2026-10-23 no projeto de origem. Sustenta: deixar a cola com o sistema fina e sem lógica, para o resto ser testável (a cobertura a 100 % dos modelos).
- **Michael Nygard — Documenting Architecture Decisions** — https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions — lido em 2026-10-23 no projeto de origem. Sustenta: o formato contexto, decisão, consequências e as decisões numeradas que não se reutilizam (`modelos/documentos/adr.md`).
  Relido em 2026-11-08. Sustenta também: as cinco partes (título, contexto, decisão, estado, consequências); números seguidos que nunca se reutilizam; a decisão revertida fica no lugar, marcada como substituída, com a referência à nova; uma ou duas páginas; merece uma ADR a decisão que afeta a estrutura, as características não funcionais, as dependências, as interfaces ou as técnicas de construção.

## Testes prontos (vitest)

Lidas em 2026-11-04 para os moldes de `modelos/testes-ts/` e a skill `codigo-legivel`.

- **Vitest — Test API** — https://vitest.dev/api/test — Sustenta: o 1.º argumento de `test.skip` é o nome do teste (`test.skip('skipped test', …)`), por isso `test.skip(condição, 'motivo')` pula sempre; `test.skipIf(condição)` pula quando a condição é verdadeira e `test.runIf` é o contrário; `test.each` e `test.only`; no contexto do teste, `context.skip(condição, mensagem)`, com os dois argumentos opcionais.
- **Node.js — lista das versões** — https://nodejs.org/dist/index.json — Sustenta: a 24 mais nova com pelo menos duas semanas (a 24.22.1, de 2026-10-20, uma versão de segurança), fixada em `tests/exemplo-ts/.nvmrc`.

## Código morto

Lidas em 2026-11-06 para `pesquisas/2026-11-03-codigo-morto.md`. As páginas não dizem a versão do knip a que se
referem; nesse dia, a publicada no npm era a 6.44.1 (de 2026-10-31).

- **knip — página inicial** — https://knip.dev — Sustenta: o knip acha dependências, exports e arquivos sem uso; a página não fala de ramos dentro de um arquivo.
- **knip — modo de produção** — https://knip.dev/features/production-mode — Sustenta: como os testes importam o código de produção, um arquivo pode parecer usado sem o ser; o `--production` deixa de fora os testes e as *stories* e conta só as entradas marcadas com `!` e as de produção dos plugins.
- **knip — plugins** — https://knip.dev/explanations/plugins — Sustenta: os arquivos de configuração em JavaScript ou TypeScript são carregados dinamicamente (executados) para ler o que exportam, e também se analisam como entradas.
- **knip — arquivos de entrada** — https://knip.dev/explanations/entry-files — Sustenta: as entradas por padrão (`index`, `main`, `cli`), as que os plugins e o `package.json` acrescentam, e que um `entry` próprio substitui as de padrão em vez de se somar.
- **knip — plugin do Next.js** — https://knip.dev/reference/plugins/next — Sustenta: `app/**/route` (e `page`, `layout`, o `middleware`, o `proxy` e o `instrumentation`) são entradas por padrão; o plugin carrega o `next.config`.
- **knip — configuração** — https://knip.dev/reference/configuration — Sustenta: por padrão, os exports sem uso das entradas não se acusam (`includeEntryExports` liga-o, salvo nas entradas dos plugins, como as rotas do Next.js); o `ignoreExportsUsedInFile` cala os exports usados só no próprio arquivo. A página não fala de `export default`.
- **knip — tratar os achados** — https://knip.dev/guides/handling-issues — Sustenta: o caminho calculado de um `import()` não se resolve e o montado com *template string* pode ser ignorado, o que dá falsos positivos (corrige-se declarando a entrada); esconder um achado não é resolvê-lo.
- **knip — problemas conhecidos** — https://knip.dev/reference/known-issues — Sustenta: uma configuração que não carrega para o knip com erro; a variável de ambiente que falta é uma das causas, e a página sugere carregar o `.env` para o knip.

## Uso e custo de agentes

Lidas em 2026-11-06; as primeiras entradas para `pesquisas/2026-11-05-linha-de-base-do-uso.md`, e a das permissões depois, para a fase das lacunas. A página dos custos do Claude Code está na seção «Compactação da conversa», com o que sustenta aqui.

- **Claude Code — boas práticas** — https://code.claude.com/docs/en/best-practices — Sustenta: cada pedido manda a conversa inteira, então uma sessão que juntou várias tarefas relê todas em cada turno; o `/clear` entre tarefas sem relação não custa nada; numa assinatura a cache dura cerca de uma hora, e uma sessão nova sai mais barata quando o histórico não faz falta; o Sonnet custa menos no trabalho de rotina e o Haiku serve para sub-agentes de tarefas simples; cada sub-agente faz os próprios pedidos, que contam no mesmo uso.
- **Claude Code — permissões** — https://code.claude.com/docs/en/permissions — lido em 2026-11-06.
  Sustenta: pela regra geral (seção «Match all uses of a tool»), o nome de uma ferramenta sozinho, sem parênteses, casa com todos os usos dela, e um `deny` com o nome sozinho tira a ferramenta do contexto do agente (vale para todas as ferramentas menos a `EndConversation`, seção «Manage permissions»); a seção «Agent (subagents)» mostra só a forma com parênteses, `Agent(Explore)`, que nega um sub-agente só; as regras avaliam-se na ordem `deny`, `ask`, `allow`, e a primeira que casa decide, sem que uma regra `allow` mais específica abra exceção a um `deny`; e uma ferramenta negada num nível não pode ser liberada por nenhum outro (seção «Settings precedence») (usado em `modelos/README.md`, passo 8, e em `skills/orquestrando-sessoes/` seção 1).
- **Anthropic — Building effective agents** (2024-12-19) — https://www.anthropic.com/engineering/building-effective-agents — Sustenta: começar pela solução mais simples e só acrescentar passos ou agentes quando isso melhora o resultado de forma medida, porque um sistema com agentes troca latência e custo por desempenho.
- **Anthropic — How we built our multi-agent research system** (2025-06-13) — https://www.anthropic.com/engineering/multi-agent-research-system — Sustenta: um agente gasta cerca de 4 vezes os tokens de uma conversa, e um sistema com vários agentes cerca de 15 vezes; só compensa quando a tarefa vale esse custo, e a maior parte das tarefas de código, que pedem contexto compartilhado, não é um bom caso hoje.

## Inspirações (nada copiado)

- **Matt Pocock — skill "grill-me"** (licença MIT) — https://github.com/mattpocock/skills — consultado em 2026-10-29.
  Inspirou a ideia de interrogar o dono antes de executar. A skill `pondo-o-plano-a-prova` foi escrita do zero, com estrutura própria.
- **OWASP Cheat Sheet Series** (CC BY-SA 4.0) — https://cheatsheetseries.owasp.org/ — referência de segurança. Indica-se só por link; o conteúdo não se copia, porque a licença ShareAlike não combina com a CC BY 4.0 deste repositório.

## Livros e autores

- **Fabio Akita — Competente o Suficiente** (livro). Citado pela página impressa.
  - A pasta `biblia-akita/` resume, com palavras nossas e um arquivo por tema, os conselhos do livro, cada um com a página. Nenhum trecho foi copiado: antes de cada commit, um script local confere que nenhuma sequência de 8 palavras dos resumos é igual ao livro, que nunca entra no repositório.
  - pp. 128–129: skills e ferramentas de terceiros só com leitura completa e uma dor concreta (usado em `escrevendo-regras-de-agente`).
  - p. 165: modelos esconderam uma biblioteca vulnerável numa lista de exceções (usado em `codigo-legivel`, `auditoria-de-seguranca` e `escrevendo-regras-de-agente`).
  - pp. 30–32, 124 e 411: a janela cheia custa dinheiro, tempo e atenção; o resumo da compactação perde o detalhe e o agente volta a propor o que já se descartou; a atenção cai à medida que a janela enche; uma sessão longa se enche de tentativas antigas (usado em `passando-o-trabalho`; o livro não dá nenhum limiar para compactar).
  - pp. 118, 120–121: pôr no pedido um esforço à medida do que está em jogo e não mandar um pedido importante sem o que fica de fora e o critério de pronto (usado em `pondo-o-plano-a-prova`).
  - pp. 322–323: escrever o que faria mudar a conclusão em critérios que alguém de fora consiga medir (base do oráculo em `pondo-o-plano-a-prova`).
  - pp. 16, 43–46: cada ferramenta, MCP e skill instalada gasta tokens antes da primeira palavra (usado em `escrevendo-regras-de-agente`).
  - pp. 19, 29–31: o contexto é relido a cada mensagem e enchê-lo custa dinheiro, tempo e precisão (usado em `passando-o-trabalho`).
  - pp. 19, 319: o modelo não guarda nada da conversa; o que se lembra guarda-se fora (usado em `passando-o-trabalho`).
  - pp. 19, 38–39: numa conversa longa, um resumo conferido e recomeçar numa conversa limpa (usado em `passando-o-trabalho`).
  - p. 21: o agente não decide sozinho uma regra de negócio ou legal (usado em `pondo-o-plano-a-prova`).
  - p. 21: «nenhuma falha encontrada» não é garantia (usado em `auditoria-de-seguranca`).
  - pp. 21, 69, 158: o agente só acha as falhas que se manda procurar (usado em `auditoria-de-seguranca`).
  - pp. 31, 33, 124: o tamanho do arquivo de regras pesa: é relido e pago a cada mensagem e o meio do contexto se perde (usado em `escrevendo-regras-de-agente`).
  - pp. 31–33: na compactação, o início da conversa encolhe e o motivo de uma decisão antiga se perde (usado em `passando-o-trabalho`).
  - p. 32: não aceitar a explicação do agente sobre uma decisão passada sem a fonte (usado em `testes-e-provas` (em parte) e `comecando-um-projeto`).
  - pp. 32–33, 36: decisão importante não fica só na conversa: vai para um arquivo de decisões (usado em `passando-o-trabalho`).
  - p. 35: não transformar cada falha numa regra; muitas são passageiras (usado em `escrevendo-regras-de-agente`).
  - pp. 36, 323–324, 392–397: a memória em arquivos seus, num formato aberto, e um documento de estado para mudar de agente (usado em `passando-o-trabalho`).
  - pp. 36–37: os documentos numa pasta, em arquivos curtos, um por assunto (usado em `comecando-um-projeto`).
  - pp. 43, 50, 112–114: um juiz de fora que diga se o agente acertou, e os meios de executar e de medir (usado em `testes-e-provas`).
  - pp. 45, 155, 159–161, 311–312: escolher o modelo pelo preço, pelo tempo e pela ferramenta, e testar a combinação (usado em `orquestrando-sessoes` (em parte)).
  - pp. 45, 78, 122: pedir primeiro o plano, revê-lo e só então avançar, acompanhando enquanto roda (usado em `pondo-o-plano-a-prova` e `orquestrando-sessoes` (em parte)).
  - p. 47: o «pronto» do agente e o trabalho certo são coisas diferentes (usado em `testes-e-provas` e `git-e-commits` (em parte)).
  - pp. 48, 416: auditar a própria auditoria e desconfiar dos testes quando o resultado sai mau (usado em `testes-e-provas`).
  - pp. 49, 153–155, 210: orquestra de agentes só para lotes independentes; custa mais tokens e coordenação (usado em `orquestrando-sessoes`).
  - pp. 49, 156: mais de um revisor, com modelos e ferramentas diferentes (usado em `orquestrando-sessoes`).
  - pp. 52–54, 56: não pedir validação com uma pergunta que já traz a resposta (usado em `orquestrando-sessoes`).
  - pp. 56, 58: citar só o material dado e pedir pontos fortes e fracos em vez de um veredito (usado em `orquestrando-sessoes` (em parte)).
  - pp. 57, 150–151: a fonte primária decide, não a maioria dos modelos (usado em `orquestrando-sessoes`).
  - pp. 64, 126: escrever o arquivo de regras no primeiro dia, com a arquitetura e as convenções (usado em `escrevendo-regras-de-agente` (em parte) e `comecando-um-projeto`).
  - pp. 67, 105, 411: para arejar, trocar de agente ou de sessão (usado em `passando-o-trabalho`).
  - pp. 67, 106–107, 218: antes de construir do zero, procurar uma solução pronta e bem mantida (usado em `comecando-um-projeto`).
  - pp. 67, 108–110, 171–172, 410–411: ao depurar: reproduzir, achar o commit que estragou, uma variável de cada vez (usado em `testes-e-provas`).
  - pp. 69, 241, 248–249, 427–428: uma funcionalidade pequena por vez, com testes; migrações grandes devagar, uma parte de cada vez (usado em `git-e-commits` (em parte) e `testes-e-provas` (em parte)).
  - pp. 80–81: começar pelo teste, prender cada bug com um teste e só juntar com tudo verde (usado em `testes-e-provas` e `git-e-commits`).
  - p. 81: testes escritos pelo agente junto com o código pesam mais, não menos (usado em `testes-e-provas` (em parte)).
  - pp. 81, 156, 231–232, 239: duas auditorias independentes, a segunda sem ler a primeira (usado em `orquestrando-sessoes`).
  - pp. 89–90: auditorias com perguntas concretas, e não «revê a segurança» (usado em `auditoria-de-seguranca`).
  - pp. 90, 191–192, 304, 424: testar o objetivo final; o que só aparece na tela confere-se na tela (usado em `testes-e-provas`).
  - p. 92: um plano só se aprova com as perguntas incômodas (e se parar a meio, se os dados corromperem) (usado em `pondo-o-plano-a-prova` (em parte)).
  - pp. 94, 99: juntar as regras repetidas num só lugar, porque duas instruções sobre o mesmo assunto se contradizem (usado em `escrevendo-regras-de-agente`).
  - pp. 96–97: para começar um sistema para outra pessoa, partir das palavras dela (usado em `pondo-o-plano-a-prova` (em parte) e `comecando-um-projeto`).
  - p. 99: perguntar se o «zero» de um relatório foi medido ou só não encontrado (usado em `testes-e-provas` (em parte)).
  - p. 105: parar e repensar quando cada ajuste quebra outra coisa (usado em `testes-e-provas` (em parte)).
  - pp. 105–106: a IA executa um plano ruim com perfeição, e mais rápido (usado em `pondo-o-plano-a-prova` (em parte)).
  - p. 114: medir onde está o custo em vez de o adivinhar (usado em `testes-e-provas` (em parte)).
  - pp. 124–125, 243–244: código para um leitor com pressa: arquivos e funções pequenos, nomes que o grep acha, verificação automática (usado em `codigo-legivel`).
  - pp. 125–126: os testes rodam com um só comando e uma saída previsível (usado em `codigo-legivel`).
  - p. 126: regras curtas, diretas e em forma de ordem, porque o arquivo é relido a cada pedido (usado em `escrevendo-regras-de-agente`).
  - pp. 126, 387: o arquivo de regras é o prompt de sistema que se escreve e uma das três gavetas da memória (usado em `escrevendo-regras-de-agente` (em parte)).
  - p. 127: o trecho típico do arquivo de regras: arquivos pequenos, nomes únicos, bug com teste, testes num comando (usado em `codigo-legivel` e `testes-e-provas`).
  - pp. 127, 129: uma contribuição não se aprova pela descrição de quem a escreveu: audita-se o código (usado em `orquestrando-sessoes` (em parte)).
  - pp. 127, 247–248: numa contribuição de fora, auditar o código; a decisão é de uma pessoa (usado em `orquestrando-sessoes` (em parte)).
  - pp. 127–129: cada regra nasce de um erro vivido; uma linha nova quando o mesmo deslize se repete (usado em `escrevendo-regras-de-agente`).
  - pp. 128–129, 239: ler tudo antes de instalar uma skill de terceiros; de preferência, escrever a sua (usado em `escrevendo-regras-de-agente`).
  - pp. 128–129, 412–413: poucas skills, todas em uso; a que ficou encostada é dívida (usado em `escrevendo-regras-de-agente`).
  - pp. 130, 323: registrar por escrito o trabalho fora do código: pesquisa, decisão, alternativa descartada (usado em `passando-o-trabalho` e `escrevendo-regras-de-agente`).
  - pp. 133–134, 294: quem usa de verdade é a revisão mais forte, com a mudança pequena atrás de um interruptor (usado em `nextjs-react`).
  - pp. 135–136: não liberar para todos o que ficou pronto rápido e passa nos testes (usado em `nextjs-react`).
  - p. 137: as assinaturas custavam menos que o token avulso; um modelo barato pode baixar a qualidade (usado em `orquestrando-sessoes` (em parte)).
  - p. 153: contar testes diz pouco: ver o que cada um verifica (usado em `testes-e-provas`).
  - p. 157: «tudo feito» só com a prova de cada exigência (usado em `testes-e-provas`).
  - pp. 160–161: perguntar porquê quando uma mudança altera um teste existente para ele passar (usado em `git-e-commits`).
  - pp. 164–165: tirar do alcance do agente o que ele não deve usar (usado em `auditoria-de-seguranca`).
  - p. 165: exceção a um alarme só com a razão escrita (usado em `codigo-legivel`).
  - pp. 165–167: perguntar quem escreveu a verificação (usado em `testes-e-provas` (em parte)).
  - pp. 172, 252, 276–277: dizer o alcance e os limites do que se provou (usado em `testes-e-provas`).
  - p. 178: o que não foi medido escreve-se «não medido», nunca «zero» (usado em `testes-e-provas` (em parte)).
  - pp. 191–193: o modelo pode dizer que os testes passaram sem os ter rodado (usado em `testes-e-provas`).
  - p. 211: não pôr a própria conclusão no pedido de pesquisa: concordar com ela é eco (usado em `orquestrando-sessoes`).
  - p. 218: registrar a origem e a licença dos dados e acervos de terceiros (usado em `escrevendo-regras-de-agente` (em parte)).
  - pp. 218–219: na tela, a informação de que a pessoa precisa para agir, não o número interno (usado em `desenhando-telas` (em parte)).
  - pp. 222, 224: operação destrutiva em lote só depois de ver a contagem do que se protege e do que se apaga (usado em `sql-postgres`).
  - pp. 223–224: pedir a outro agente que execute e confira o procedimento que o primeiro escreveu (usado em `orquestrando-sessoes` (em parte)).
  - pp. 226–227: conferir o estado na origem, contando, e não pelo que a ferramenta diz (usado em `testes-e-provas` e `sql-postgres`).
  - p. 227: o agente trabalha com as permissões de quem o abriu (usado em `auditoria-de-seguranca` (em parte)).
  - pp. 228, 386: o modo que pula todas as permissões só dentro de uma sandbox (usado em `auditoria-de-seguranca`).
  - pp. 230, 382: o Git como rede: commits pequenos, cópia remota e o envio na mão de uma pessoa (usado em `git-e-commits`).
  - pp. 230–231: ler o que a proteção promete; cada camada precisa de quem a audite (usado em `auditoria-de-seguranca`).
  - pp. 232, 253: o que uma auditoria achou: um atalho de teste esquecido e uma senha em variáveis de ambiente (usado em `auditoria-de-seguranca` (em parte)).
  - pp. 234–235, 386–387: os agentes longe da produção; as mudanças como receitas versionadas que uma pessoa promove (usado em `sql-postgres` (em parte)).
  - p. 236: decisão que destrói algo: outra pessoa ou outra sessão olha o plano antes (usado em `orquestrando-sessoes`).
  - pp. 242–243, 262: o endurecimento pede-se por escrito e confere-se; comandos negados de início (usado em `auditoria-de-seguranca` (em parte)).
  - pp. 245–246: conferir cada afirmação de um relatório do agente antes de o mandar a terceiros (usado em `orquestrando-sessoes`).
  - pp. 285–287: antes de entregar uma ferramenta, saber o objetivo, o número que muda e o que tem de continuar funcionando (usado em `pondo-o-plano-a-prova`).
  - pp. 286–288, 291–292: entregas pequenas e frequentes; velocidade e estabilidade andam juntas (usado em `git-e-commits` (em parte)).
  - pp. 319, 323: o agente não aprende com a sessão; o que não se guarda evapora (usado em `passando-o-trabalho`).
  - p. 324: trocar de fornecedor de modelo, mas guardar consigo a memória e o processo (usado em `passando-o-trabalho` (em parte)).
  - pp. 336, 344: dois números que não batem: dizer o que cada um conta; entre o resumo e a fonte, vale a fonte (usado em `testes-e-provas`).
  - p. 357: a explicação do agente sobre como verificou não é prova (usado em `testes-e-provas`).
  - p. 385: permissões em três colunas: pode sem perguntar, pergunta antes, nunca (usado em `auditoria-de-seguranca` (em parte)).
  - p. 386: antes do push, ver a lista de arquivos de todos os commits por enviar (usado em `auditoria-de-seguranca` (em parte)).
  - p. 387: três gavetas: as regras, as decisões e pesquisas no git, e a passagem de turno de cada sessão (usado em `passando-o-trabalho` e `escrevendo-regras-de-agente` (em parte)).
  - p. 389: não deixar o agente ler o .env; a configuração do projeto só aperta a jaula (usado em `auditoria-de-seguranca`).
  - p. 397: um curl | sh só depois de conferir a soma de verificação (usado em `auditoria-de-seguranca` (em parte)).
  - pp. 408–409: cada commit pela mesma bateria: estilo, dependências, análise estática e testes (usado em `auditoria-de-seguranca`).
  - pp. 423–424: controles negativos: um programa vazio tem de reprovar (usado em `testes-e-provas`).
- **Fabio Akita — blog** — https://akitaonrails.com — lido em 2026-11-04. Sustenta: o índice dos artigos, por mês, de onde saíram os endereços e as datas de publicação da `biblia-akita/leituras.md`.

## Artigos que o livro recomenda

Lidas em 2026-11-04, para a `biblia-akita/leituras.md`. São as fontes originais que o livro aponta na secção «Fontes» (pp. 434–455). Cada entrada diz o título e o que o artigo sustenta, com palavras nossas.

- **Por que as LLMs não te dão o resultado esperado** (2026-04-15) — https://akitaonrails.com/2026/04/15/como-falar-com-o-claude-code-efetivamente/ — Sustenta: o pedido em partes (objetivo, o que não se quer, como validar, contexto) e a conversa que continua durante o trabalho.
- **Clean Code pra Agentes de IA** (2026-04-20) — https://akitaonrails.com/2026/04/20/clean-code-para-agentes-de-ia/ — Sustenta: arquivos e funções pequenos, nomes distintos, tipos explícitos, testes que o agente roda sozinho, e as regras no arquivo de instruções.
- **Como me precaver pros meus agentes não apagarem minhas coisas?** (2026-07-11) — https://akitaonrails.com/2026/07/11/como-me-precaver-pros-meus-agentes-nao-apagarem-minhas-coisas/ — Sustenta: jaula, snapshots automáticos e backup externo com retenção, para que um engano seja recuperável.
- **Dicas e Toolkit de IA do Akita: ai-jail, ai-memory, ai-usagebar** (2026-05-24) — https://akitaonrails.com/2026/05/24/dicas-e-toolkit-de-ia-do-akita-ai-jail-ai-memory-ai-usagebar/ — Sustenta: poucas ferramentas, testes, CI, refatoração, deploy automático, cercas de segurança e decisões registradas no git.
- **Desastre no meu NAS! Como quase perdi 90 TB de dados** (2026-10-06) — https://akitaonrails.com/2026/10/06/desastre-no-meu-nas-como-quase-perdi-90-tb-de-dados/ — Sustenta: RAID (espelho ou paridade) não é backup; duas paridades com discos grandes; uma cópia fora de casa.
- **Por que LLMs vão falhar na Sua Empresa?** (2026-06-24) — https://akitaonrails.com/2026/06/24/por-que-llms-vao-falhar-na-sua-empresa/ — Sustenta: ciclos curtos entre decidir, fazer, testar e rever, em vez de somar IA ao processo antigo.
- **Parem de inventar desculpas e façam mais deploy!** (2026-09-22) — https://akitaonrails.com/2026/09/22/parem-de-inventar-desculpas-e-facam-mais-deploy-a-premissa-mudou/ — Sustenta: entregas mais frequentes, só com testes, CI, voltar atrás, observação e ambiente de testes já montados.
- **O código fonte do Claude Code vazou. O que achamos dentro.** (2026-03-31) — https://akitaonrails.com/2026/03/31/codigo-fonte-do-claude-code-vazou-o-que-achamos-dentro/ — Sustenta: as verificações de um processo de publicação e os limites de leitura e de resultados que o arquivo de instruções deve ter em conta.
- **Vibe Code: Do Zero à Produção em 6 DIAS** (2026-02-16) — https://akitaonrails.com/2026/02/16/vibe-code-do-zero-a-producao-em-6-dias-the-m-akita-chronicles/ — Sustenta: plano antes do código, testes, CI e commits pequenos, com a pessoa nos papéis de produto, liderança técnica e qualidade.
- **Testes de Integração em MonoRepo** (2026-02-20) — https://akitaonrails.com/2026/02/20/testes-de-integracao-em-monorepo-bastidores-do-the-m-akita-chronicles/ — Sustenta: os dublês não apanham a quebra do contrato entre aplicações; testar o caminho inteiro e controlar o custo das chamadas pagas.
- **Software Nunca Está 'Pronto'** (2026-03-01) — https://akitaonrails.com/2026/03/01/software-nunca-esta-pronto-4-projetos-a-vida-pos-deploy-e-por-que-one-shot-prompt-e-mito/ — Sustenta: a melhoria por voltas depois do deploy, com testes, CI e entregas pequenas.
- **Como Driveclub e shadPS4 Quase Derrotaram a IA e a Mim: Como Aprender** (2026-04-23) — https://akitaonrails.com/2026/04/23/driveclub-shadps4-e-ia-como-aprender/ — Sustenta: a causa antes do remendo, e aprender um assunto novo por etapas.
- **LLM Benchmark: Devo usar o que tem nota maior?** (2026-07-19) — https://akitaonrails.com/2026/07/19/llm-benchmark-devo-usar-o-que-tem-nota-maior/ — Sustenta: o ranking lido como grupos e a escolha pelo custo, pela velocidade e pela ferramenta, com um teste próprio.
- **Novo LLM Benchmark v4: retestando TODOS os principais LLMs (Parte 1)** (2026-09-15) — https://akitaonrails.com/2026/09/15/novo-llm-benchmark-v4-retestando-todos-llms-parte-1/ — Sustenta: cada nota vale só para o método que a gerou; testar no próprio problema.
- **Ensinando a questionar notícias | Frank Investigator** (2026-03-27) — https://akitaonrails.com/2026/03/27/ensinando-a-questionar-noticias-frank-investigator/ — Sustenta: comparar fontes, procurar a primária e preferir perguntas estruturadas às abertas.
- **Hot take: Harness, Loop Engineering, Graph Engineering são Bullshit** (2026-08-18) — https://akitaonrails.com/2026/08/18/hot-take-harness-loop-engineering-graph-engineering-sao-bullshit/ — Sustenta: a base da engenharia de software em vez de cursos de moda, e o conhecimento do projeto guardado no projeto.
- **Você é um idiota se acredita nas propagandas enganosas da OpenAI, Anthropic, NVIDIA** (2026-09-09) — https://akitaonrails.com/2026/09/09/propagandas-enganosas-da-openai-anthropic-nvidia/ — Sustenta: perguntar quem lucra com um anúncio e exigir provas que se possam conferir.

## CI e links vivos

Lidas em 2026-11-07 para o workflow `links` (`.github/workflows/links.yml`) e o `lychee.toml`, com o `gh api` na tag indicada ou, nas páginas do GitHub e do Claude Code, com o `WebFetch`.

- **lychee — README (v0.24.2)** — https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/README.md — Sustenta: as opções `--cache`, `--max-cache-age` (padrão 1d), `--max-retries` (3), `--retry-wait-time` (1), `--max-concurrency` (128), `--host-concurrency` (10), `--host-request-interval` (50ms), `--timeout` (20), `--accept` (padrão `100..=103,200..=299`; a lista dada substitui-a) e `--exclude`; as saídas 0, 1, 2 e 3; o `GITHUB_TOKEN` contra a cota do github.com.
- **lychee — `lychee.example.toml` (v0.24.2)** — https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/lychee.example.toml — Sustenta: os nomes das chaves do arquivo de configuração (`exclude`, `scheme`, `accept`, `cache`, `max_cache_age`, `max_retries`, `retry_wait_time`, `timeout`, `max_concurrency`, `host_concurrency`, `host_request_interval`, `no_progress`).
- **lychee — `filter/mod.rs` (v0.24.2)** — https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/lychee-lib/src/filter/mod.rs — Sustenta: os domínios de exemplo (`example.com`, `.org`, `.net` e `.edu`), os fins `.test`, `.example`, `.invalid` e `.localhost`, o `twitter.com` e os falsos positivos que o lychee isenta antes dos `exclude`.
- **lychee-action — README e `action.yml` (v2.9.0)** — https://github.com/lycheeverse/lychee-action/blob/v2.9.0/action.yml (README: https://github.com/lycheeverse/lychee-action/blob/v2.9.0/README.md) — Sustenta: a receita da cache com `restore` e `save` separados; o `action.yml` baixa o binário com `curl -sfLO` sem conferir o sha256, que é o motivo de se usar o binário oficial.
- **GitHub Docs — eventos que disparam workflows** — https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows — Sustenta: os agendados correm no último commit da `main`, podem atrasar no começo de cada hora e desligam-se num repositório público ao fim de 60 dias sem atividade; o aviso a quem mexeu por último no `cron`; o `GITHUB_TOKEN` só lê nas PRs vindas de forks.
- **GitHub Docs — cache de dependências** — https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching — Sustenta: uma cache não se reescreve; o `restore-keys`; uma PR lê a cache da base e a que cria fica só para ela; a remoção ao fim de 7 dias sem uso; o limite de 10 GB.

## Modelos de issue e de PR (GitHub)

Lidas em 2026-11-08 com o `WebFetch`, para `pesquisas/2026-11-08-modelos-de-issue-e-de-pr.md`. A página da sintaxe dos formulários de issue está na seção «Relatório de erros», com o que ela sustenta aqui.

- **GitHub Docs — sintaxe do esquema dos formulários** — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema — Sustenta: os seis tipos de campo (`markdown`, `textarea`, `input`, `dropdown`, `checkboxes`, `upload`) e as chaves de `attributes` e de `validations` de cada um, entre elas o `min_length` em `input` e `textarea` e o `accept` no `upload`; o `id` só com letras, algarismos, `-` e `_`, único no formulário e sem uso no `markdown`; o bloco `markdown` serve de contexto e não é enviado; o `required` só vale em repositório público; o `render` põe a resposta num bloco de código; as `options` do `dropdown` não podem ser vazias nem repetidas; o `default` é o índice de uma opção, e com ele não pode haver a opção «None» nem «n/a»; o `min_length` é um inteiro não negativo; cada caixa do `checkboxes` leva `label`.
- **GitHub Docs — configurar os modelos de issue** — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository — Sustenta: o `config.yml` fica em `.github/ISSUE_TEMPLATE` e só vale depois de chegar à branch padrão; leva `blank_issues_enabled` e `contact_links` (cada link com `name`, `url` e `about`); com `false`, quem tem o papel Read ou Triage vê apenas os modelos, e quem tem Write, Maintain ou Admin continua vendo a issue em branco, marcada «Maintainers only»; a ordem do seletor é alfabética, com os `.yml` antes dos `.md`, e controla-se com um número na frente do nome do arquivo, com o zero à esquerda só a partir de 10 modelos; um formulário com `name` de 3 caracteres ou menos não aparece no seletor.
- **GitHub Docs — sobre os modelos de issue e de PR** — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates — Sustenta: o modelo em Markdown só orienta, e o formulário mostra campos e permite marcar os obrigatórios; os modelos de issue ficam em `.github/ISSUE_TEMPLATE` e os de PR na raiz, em `docs` ou em `.github`, sempre na branch padrão; `.md` para o modelo de issue e `.yml` para o formulário; para o perfil da comunidade os modelos de issue levam `name` e `description` (no `.yml`).
- **GitHub Docs — o modelo de pull request** — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository — Sustenta: o `pull_request_template.md` fica na raiz, em `docs` ou em `.github`; vários modelos vão numa pasta `PULL_REQUEST_TEMPLATE` e escolhem-se com o parâmetro `template`; um modelo só aparece sozinho no corpo da PR; só vale depois de chegar à branch padrão.
- **GitHub Docs — arquivos de saúde da comunidade** — https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file — Sustenta: o `SECURITY.md` pode ficar em `.github`, na raiz ou em `docs`, e o GitHub o procura nesta ordem; os modelos de issue e o `config.yml` ficam em `.github/ISSUE_TEMPLATE`.
- **GitHub Docs — política de segurança** — https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository — Sustenta: a política diz como reportar uma vulnerabilidade e quais versões têm suporte, e cria-se pela aba «Security and quality», em «Security policy». A página **não** diz onde fica o arquivo (isso vem da página dos arquivos de saúde da comunidade).
- **GitHub Docs — ligar o aviso privado num repositório** — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configuring-private-vulnerability-reporting-for-a-repository — Sustenta: o dono ou o administrador de um repositório público liga-o em Settings → Advanced Security → Private vulnerability reporting → Enable; com ele ligado, aparece o botão «Report a vulnerability»; recebem o aviso os administradores e os gerentes de segurança que seguem o repositório com All Activity ou com Custom e Security alerts, se as notificações deles deixarem; o formulário próprio `VULNERABILITY_REPORT.yml` em `.github` é opcional.
- **GitHub Docs — reportar em privado** — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately — Sustenta: os passos de quem reporta (aba «Security and quality», «Report a vulnerability», preencher, «Submit report»); a página não diz se a opção some ou fica desabilitada quando o aviso está desligado, e manda então seguir a política de segurança ou abrir uma issue pedindo um contato.
- **GitHub Docs — divulgação coordenada** — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/about-coordinated-disclosure-of-security-vulnerabilities — Sustenta: o aviso privado entrega os detalhes em privado aos mantenedores; sem política de segurança, abre-se uma issue pedindo um contato, sem nenhum detalhe do problema, porque ela fica pública na hora (a base do formulário «Pedir um contato de segurança»).
- **GitHub Docs — criar uma issue** — https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue — Sustenta: os parâmetros de URL (`template`, `title`, `labels`, `body` e outros) e o preenchimento dos campos de um formulário pela URL; com parâmetros inválidos ou sem a permissão, a resposta é 404. Usado nos links `template=` do `biblia-akita/README.md` e do `SECURITY.md`.
- **GitHub Docs — erros comuns de validação dos formulários** — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/common-validation-errors-when-creating-issue-forms — Sustenta: a lista de 21 erros (contados na página em 2026-11-08), entre eles o `body` vazio ou sem campo que não seja `markdown`, os `label`s repetidos ou parecidos demais, as opções repetidas, com `None` ou com booleanos, as chaves proibidas e as palavras proibidas nos rótulos (só «password» é dada como exemplo), o texto vazio ou só com espaços no topo e nos rótulos, e o rótulo de uma caixa repetido com o de outro campo; a página diz que os erros aparecem ao criar, salvar ou ver o formulário, sem dizer onde.
