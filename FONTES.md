# Fontes

Toda fonte citada no repositório entra aqui, com a data em que foi lida e o que ela sustenta.
Fonte secundária leva a marca *(secundária)* até ser conferida na original.

## Entrega de regras a agentes

- **Claude Code — memória, CLAUDE.md, AGENTS.md e imports** — https://code.claude.com/docs/en/memory — lido em 2026-10-29.
  Sustenta: CLAUDE.md com menos de 200 linhas; imports não economizam contexto; com CLAUDE.md e AGENTS.md juntos, o Claude lê só o CLAUDE.md.
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
- **Claude Code — hooks** — https://code.claude.com/docs/en/hooks — lido em 2026-11-01 (a primeira parte da página) e inteiro em 2026-11-02, na versão em texto (o mesmo endereço com `.md`). Sustenta: o `PreToolUse` decide com `permissionDecision` (`allow`, `deny`, `ask`, `defer`) e o `ask` passa a decisão ao usuário; sair com 2 «Blocks the tool call», com o motivo no stderr; `onFailure` aceita `continue` ou `block` (desde o Claude Code v2.1.295); o `CLAUDE_PROJECT_DIR` é a pasta onde a sessão começou e não muda com a sessão. Que as regras `ask` do `settings.json` não perguntam no modo automático foi **medido** num projeto real, não está na página (usado na skill `auditoria-de-seguranca` e em `modelos/claude/`).
  Sustenta também, para a compactação (`pesquisas/2026-11-02-hooks-de-compactacao.md`): o `PreCompact` roda antes e pode barrar; o `PostCompact` roda depois, recebe o resumo e não decide nada; o `SessionStart` volta a rodar com a origem `compact`; o `InstructionsLoaded` avisa com o motivo `compact` quando os arquivos de instruções voltam a carregar.

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
- **towncrier** (tutorial) — https://towncrier.readthedocs.io/en/stable/tutorial.html — Sustenta: um arquivo por mudança, juntado e apagado na hora do lançamento. Só a ideia: o modelo `juntar_changelog.py` não usa o towncrier (biblioteca padrão apenas).
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

## Inspirações (nada copiado)

- **Matt Pocock — skill "grill-me"** (licença MIT) — https://github.com/mattpocock/skills — consultado em 2026-10-29.
  Inspirou a ideia de interrogar o dono antes de executar. A skill `pondo-o-plano-a-prova` foi escrita do zero, com estrutura própria.
- **OWASP Cheat Sheet Series** (CC BY-SA 4.0) — https://cheatsheetseries.owasp.org/ — referência de segurança. Indica-se só por link; o conteúdo não se copia, porque a licença ShareAlike não combina com a CC BY 4.0 deste repositório.

## Livros e autores

- **Fabio Akita — Competente o Suficiente** (livro). Citado por capítulo e página.
  - pp. 128–129: skills e ferramentas de terceiros só com leitura completa e uma dor concreta (usado em `escrevendo-regras-de-agente`).
  - p. 165: modelos esconderam uma biblioteca vulnerável numa lista de exceções (base de "sem silenciar alarme").
- **Fabio Akita — blog** — https://akitaonrails.com
