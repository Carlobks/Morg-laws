# Fontes

Toda fonte citada no repositório entra aqui, com a data em que foi lida e o que ela sustenta.
Fonte secundária leva a marca *(secundária)* até ser conferida na original.

## Entrega de regras a agentes

- **Claude Code — memória, CLAUDE.md, AGENTS.md e imports** — https://code.claude.com/docs/en/memory — lido em 2026-10-29.
  Sustenta: CLAUDE.md com menos de 200 linhas; imports não economizam contexto; com CLAUDE.md e AGENTS.md juntos, o Claude lê só o CLAUDE.md.
  Relido em 2026-11-06 (a seção do tamanho e a do `CLAUDE.md` de subpasta que perde o fim). Sustenta também: o limite dos arquivos que carregam sob demanda (`CLAUDE.md` de subpasta, regras com `paths`) conta-se em caracteres, depende da janela de contexto e vale desde o Claude Code v2.1.309; do arquivo que passa dele, o Claude recebe só o começo; a página manda contar com `wc -m` (usado em `skills/escrevendo-regras-de-agente/` §4).
- **Claude Code — skills** — https://code.claude.com/docs/en/skills — lido em 2026-10-29.
  Sustenta: só a descrição da skill carrega no início; o corpo carrega quando é usada.
- **Claude Code — marketplace de plugins** — https://code.claude.com/docs/en/plugin-marketplaces — lido em 2026-10-29.
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
- **Codex — skills** — https://developers.openai.com/codex/skills — lido em 2026-11-02, a página inteira (o endereço redireciona para `learn.chatgpt.com`). Sustenta: o Codex segue o padrão Agent Skills, começa só com o nome, a descrição e o caminho de cada skill e procura-as em `.agents/skills` (da pasta atual até a raiz do repositório) e em `~/.agents/skills`.
- **skills (a ferramenta do `npx skills add`)** — https://github.com/vercel-labs/skills — lido em 2026-11-02: o começo do README, `docs/agents.md` (procura por Codex e Claude Code) e os formatos de origem em `docs/commands.md`. Sustenta: instala para o Claude Code em `.claude/skills/` e para o Codex em `.agents/skills/`, escolhe os agentes com `-a` e aceita uma pasta local como origem.

## Compactação da conversa

Lidas em 2026-11-02 para a skill `passando-o-trabalho`; o que se leu de cada uma está em `pesquisas/2026-11-02-compactacao-claude-code-e-codex.md`.

- **Claude Code — comandos** — https://code.claude.com/docs/en/commands — Sustenta: `/compact` aceita instruções de foco para o resumo; `/autocompact` muda o tamanho da janela de compactação automática; `/context` mostra o que ocupa a janela.
- **Claude Code — janela de contexto** — https://code.claude.com/docs/en/context-window — Sustenta: o que volta depois de compactar (CLAUDE.md da raiz, regras sem `paths:`, descrições das skills, até cinco arquivos lidos ou editados, o corpo das skills cortado em 5 mil tokens a guardar o começo) e que compactar com um foco antes da automática guarda o que se escolhe.
- **Claude Code — como funciona** — https://code.claude.com/docs/en/how-claude-code-works — Sustenta: a compactação automática perto do limite pode perder instruções do começo da conversa; uma seção «Compact instructions» no CLAUDE.md ou um `/compact` com foco controlam o que fica.
- **Claude Code — glossário** — https://code.claude.com/docs/en/glossary — Sustenta: o CLAUDE.md da raiz sobrevive à compactação e é relido do disco; instruções dadas só na conversa podem perder-se.
- **Claude Code — configuração do modelo** — https://code.claude.com/docs/en/model-config — Sustenta: sem configurar, a automática dispara no limite do modelo (com exceções por modelo); a janela de compactação vai de 100 mil a 1 milhão de tokens.
- **Claude Code — referência das configurações** — https://code.claude.com/docs/en/settings-reference — Sustenta: a compactação por inatividade (conversa longa parada há cerca de uma hora) e as chaves `idleCompaction` e `autoCompactEnabled`.
- **Claude Code — custos** — https://code.claude.com/docs/en/costs — Sustenta: a seção «Compact instructions» no CLAUDE.md; compactar um contexto grande é ele próprio um pedido grande.
- **Codex — comandos** — https://developers.openai.com/codex/cli/slash-commands — o endereço redireciona para `learn.chatgpt.com`. Sustenta: o `/compact` pede confirmação e troca os turnos antigos por um resumo; a página não documenta argumentos; o `/recap` resume sem liberar contexto.
- **Codex — referência da configuração** — https://developers.openai.com/codex/config-reference — o endereço redireciona para `learn.chatgpt.com`. Sustenta: `compact_prompt` troca o prompt da compactação; `model_auto_compact_token_limit` e `model_post_turn_compact_threshold_percent` decidem quando compacta sozinho, sem valor recomendado.

## Git e contas

- **Git Credential Manager — várias contas** — https://github.com/git-ecosystem/git-credential-manager/blob/main/docs/multiple-users.md — lido em 2026-10-29.
  Sustenta: o usuário no endereço do repositório escolhe a conta só para aquele repositório.

- **Git — `lockfile.c` (mensagem do `index.lock`)** — https://github.com/git/git/blob/master/lockfile.c — lido em 2026-10-29.
  Sustenta: o git não manda apagar o lock; só diz que outro processo pode estar a correr ou que o lock pode estar velho.
- **Pro Git — 2.6 Tagging** — https://git-scm.com/book/en/v2/Git-Basics-Tagging — lido em 2026-10-31 (no projeto de origem). Sustenta: a tag anotada guarda autor, data e mensagem; usada para marcar cada versão (`modelos/changelog/`).
- **Git — `git` (opções globais)** — https://git-scm.com/docs/git — lido em 2026-11-02. Sustenta: as opções entre o `git` e o subcomando (`-C <caminho>` e `-c <nome>=<valor>` com o valor à parte; `--git-dir=`, `--work-tree=`, `--no-pager`/`-P` e outras), que o `perguntar_antes.py` salta para achar o `push`.
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
- **PostgreSQL 18 — CREATE VIEW** — https://www.postgresql.org/docs/18/sql-createview.html — Sustenta: por omissão, a vista aplica as políticas do dono; `security_invoker` muda isso.
- **PostgreSQL 18 — information_schema.columns** — https://www.postgresql.org/docs/18/infoschema-columns.html — Sustenta: só aparecem as colunas a que o usuário atual tem acesso.
- **PostgreSQL 18 — Sequence Manipulation Functions** — https://www.postgresql.org/docs/18/functions-sequence.html — Sustenta: `nextval` e `setval` não se desfazem com o `ROLLBACK`.
- **PostgreSQL 18 — Enumerated Types** — https://www.postgresql.org/docs/18/datatype-enum.html — Sustenta: os valores de um `ENUM` seguem a ordem da declaração (o `ADD VALUE` aceita `BEFORE`/`AFTER`); acrescentar e renomear existem, remover e reordenar não.
- **PostgreSQL 18 — ALTER TYPE** — https://www.postgresql.org/docs/18/sql-altertype.html — Sustenta: `ADD VALUE` e `RENAME VALUE`; o valor novo só se usa depois do commit.
- **PostgreSQL 18 — ALTER TABLE** — https://www.postgresql.org/docs/18/sql-altertable.html — Sustenta: o `ACCESS EXCLUSIVE` por omissão, o `DEFAULT` volátil que reescreve a tabela, o `NOT VALID` e o `VALIDATE CONSTRAINT`; o dono desliga os gatilhos com `DISABLE TRIGGER`, e no modo `replica` (`session_replication_role`) só disparam os `ENABLE ALWAYS`.
- **PostgreSQL 18 — SET** — https://www.postgresql.org/docs/18/sql-set.html — Sustenta: o `SET LOCAL` fora de uma transação só dá um aviso e não tem efeito.
- **PostgreSQL 18 — Client Connection Defaults** (`search_path`) — https://www.postgresql.org/docs/18/runtime-config-client.html — Sustenta: o esquema temporário, se não está no caminho, é pesquisado primeiro para tabelas, e nunca para funções nem operadores.
- **PostgreSQL 18 — Privileges** — https://www.postgresql.org/docs/18/ddl-priv.html — Sustenta: o `MAINTAIN` (desde o 17) permite `VACUUM`, `ANALYZE`, `CLUSTER`, `REINDEX` e `LOCK TABLE`.
- **Supabase — Row Level Security** — https://supabase.com/docs/guides/database/postgres/row-level-security — Sustenta: `search_path` vazio nas `SECURITY DEFINER`; tabela exposta sem RLS aberta a quem tem grant; vistas passam por cima do RLS; o dono `postgres` tem `bypassrls`; `raw_user_meta_data` editável pelo usuário; regras de desempenho das políticas.
- **Supabase — Securing your API** — https://supabase.com/docs/guides/api/securing-your-api — Sustenta: os privilégios por omissão do `public`, que mudam conforme a data de criação do projeto.
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
- Os demais (Rams, Tesler e os tetos por confirmar do Oracle Redwood, sem link) estão em `skills/desenhando-telas/references/tetos-e-fontes.md`.

## Relatório de erros

Lidas em 2026-10-31 no projeto de origem, para os campos do formulário `modelos/github/ISSUE_TEMPLATE/erro.yml`.

- **Mozilla — Bug writing guidelines** — https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html — Sustenta: resumo curto, passos numerados para reproduzir, resultado esperado e resultado obtido, cada um à parte.
- **OpenTelemetry — convenções semânticas das exceções** — https://opentelemetry.io/docs/specs/semconv/exceptions/exceptions-logs/ — Sustenta: o que um registro de exceção leva (tipo, mensagem, pilha de chamadas).
- **GitHub — sintaxe dos formulários de issue** — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms — Sustenta: `name`, `description`, `title`, `labels` e `body` com campos `input`, `textarea` e `markdown`, e o `validations: required`.
- **Python — `faulthandler`** — https://docs.python.org/3/library/faulthandler.html — Sustenta: despeja a pilha de chamadas quando o processo quebra numa falha fatal; foi ele que revelou o erro do `restype` em `aprendizados/2026-11-01-python.md`.

## Testes e decisões

- **Node.js 24 — Test runner** (cobertura) — https://nodejs.org/docs/latest-v24.x/api/test.html — lido em 2026-10-23 no projeto de origem. Sustenta: os comentários `node:coverage disable`/`enable` e `ignore next` (`aprendizados/2026-11-01-testes.md`).
- **Pester — code coverage** — https://pester.dev/docs/usage/code-coverage — lido em 2026-10-23 no projeto de origem. O comportamento dos mocks filtrados do Pester 6 em `aprendizados/2026-11-01-testes.md` foi **medido**, não lido.
- **Martin Fowler — Humble Object** — https://martinfowler.com/bliki/HumbleObject.html — lido em 2026-10-23 no projeto de origem. Sustenta: deixar a cola com o sistema fina e sem lógica, para o resto ser testável (a cobertura a 100 % dos modelos).
- **Michael Nygard — Documenting Architecture Decisions** — https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions — lido em 2026-10-23 no projeto de origem. Sustenta: o formato contexto, decisão, consequências e as decisões numeradas que não se reutilizam (`modelos/documentos/adr.md`).

## Testes prontos (vitest)

Lidas em 2026-11-04 para os moldes de `modelos/testes-ts/` e a skill `codigo-legivel`.

- **Vitest — Test API** — https://vitest.dev/api/test — Sustenta: o 1.º argumento de `test.skip` é o nome do teste (`test.skip('skipped test', …)`), por isso `test.skip(condição, 'motivo')` salta sempre; `test.skipIf(condição)` salta quando a condição é verdadeira e `test.runIf` é o contrário; `test.each` e `test.only`; no contexto do teste, `context.skip(condição, mensagem)`, com os dois argumentos opcionais.
- **Node.js — lista das versões** — https://nodejs.org/dist/index.json — Sustenta: a 24 mais nova com pelo menos duas semanas (a 24.22.1, de 2026-10-20, uma versão de segurança), fixada em `tests/exemplo-ts/.nvmrc`.

## Código morto

Lidas em 2026-11-06 para `pesquisas/2026-11-03-codigo-morto.md`. As páginas não dizem a versão do knip a que se
referem; nesse dia, a publicada no npm era a 6.44.1 (de 2026-10-31).

- **knip — página inicial** — https://knip.dev — Sustenta: o knip acha dependências, exports e arquivos sem uso; a página não fala de ramos dentro de um arquivo.
- **knip — modo de produção** — https://knip.dev/features/production-mode — Sustenta: como os testes importam o código de produção, um arquivo pode parecer usado sem o ser; o `--production` deixa de fora os testes e as *stories* e conta só as entradas marcadas com `!` e as de produção dos plugins.
- **knip — plugins** — https://knip.dev/explanations/plugins — Sustenta: os arquivos de configuração em JavaScript ou TypeScript são carregados dinamicamente (executados) para ler o que exportam, e também se analisam como entradas.
- **knip — arquivos de entrada** — https://knip.dev/explanations/entry-files — Sustenta: as entradas por omissão (`index`, `main`, `cli`), as que os plugins e o `package.json` acrescentam, e que um `entry` próprio substitui as de omissão em vez de se somar.
- **knip — plugin do Next.js** — https://knip.dev/reference/plugins/next — Sustenta: `app/**/route` (e `page`, `layout`, o `middleware`, o `proxy` e o `instrumentation`) são entradas por omissão; o plugin carrega o `next.config`.
- **knip — configuração** — https://knip.dev/reference/configuration — Sustenta: por omissão, os exports sem uso das entradas não se acusam (`includeEntryExports` liga-o); o `ignoreExportsUsedInFile` cala os exports usados só no próprio arquivo. A página não fala de `export default`.
- **knip — tratar os achados** — https://knip.dev/guides/handling-issues — Sustenta: o caminho calculado de um `import()` não se resolve e o montado com *template string* pode ser ignorado, o que dá falsos positivos (corrige-se declarando a entrada); esconder um achado não é resolvê-lo.
- **knip — problemas conhecidos** — https://knip.dev/reference/known-issues — Sustenta: uma configuração que não carrega para o knip com erro; a variável de ambiente que falta é uma das causas, e a página sugere carregar o `.env` para o knip.

## Inspirações (nada copiado)

- **Matt Pocock — skill "grill-me"** (licença MIT) — https://github.com/mattpocock/skills — consultado em 2026-10-29.
  Inspirou a ideia de interrogar o dono antes de executar. A skill `pondo-o-plano-a-prova` foi escrita do zero, com estrutura própria.
- **OWASP Cheat Sheet Series** (CC BY-SA 4.0) — https://cheatsheetseries.owasp.org/ — referência de segurança. Indica-se só por link; o conteúdo não se copia, porque a licença ShareAlike não combina com a CC BY 4.0 deste repositório.

## Livros e autores

- **Fabio Akita — Competente o Suficiente** (livro). Citado pela página impressa.
  - A pasta `biblia-akita/` resume, com palavras nossas e um arquivo por tema, os conselhos do livro, cada um com a página. Nenhum trecho foi copiado: antes de cada commit, um script local confere que nenhuma sequência de 8 palavras dos resumos é igual ao livro, que nunca entra no repositório.
  - pp. 128–129: skills e ferramentas de terceiros só com leitura completa e uma dor concreta (usado em `escrevendo-regras-de-agente`).
  - p. 165: modelos esconderam uma biblioteca vulnerável numa lista de exceções (base de "sem silenciar alarme").
  - pp. 30–32, 124 e 411: a janela cheia custa dinheiro, tempo e atenção; o resumo da compactação perde o detalhe e o agente volta a propor o que já se descartou; a atenção cai à medida que a janela enche; uma sessão longa se enche de tentativas antigas (usado em `passando-o-trabalho`; o livro não dá nenhuma percentagem para compactar).
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
