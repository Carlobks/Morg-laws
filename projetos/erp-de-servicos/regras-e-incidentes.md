# Regras e incidentes

Cada regra de trabalho do projeto de origem, o incidente que a fez nascer, a barreira que a faz ser cumprida e onde ela está neste repositório. Vale o que o projeto tinha em novembro de 2026. As regras por pasta (telas, banco de dados, padrões de código) chegam numa etapa seguinte, neste mesmo arquivo.

Como ler:

- **A regra** é a frase curta que o agente lê a cada sessão; o texto integral, com o porquê, fica no projeto.
- **O incidente** traz o número que o próprio projeto escreveu ao lado da regra e o mês do commit que o trouxe. O texto exato que se pesquisou no git está na última tabela. Quando o projeto não escreveu um incidente, a linha diz «incidente não registrado».
- **A barreira** diz o que obriga a cumprir: um hook, uma permissão que pede confirmação ou recusa, uma catraca (um teste que conta uma coisa ruim e recusa que o número cresça) ou só texto.
- **No Morg-laws** liga à skill ou ao `AGENTS.md` que ensina a regra, ou diz «só no projeto» quando ela depende de um produto que não está aqui.

## As 21 regras de trabalho

| Regra | A regra | O incidente | A barreira | No Morg-laws |
|---|---|---|---|---|
| 1. Commit sem pedido, push com o sim | Commitar não precisa de pedido; push e PR precisam, a cada vez. Commits atômicos, cada um com uma alteração lógica. | 109 arquivos viveram só no disco de uma máquina, acumulados em cerca de uma semana e quatro módulos, sem histórico (julho de 2026). | Uma permissão que pede confirmação em cada forma de `git push` (12 entradas, entre Bash e PowerShell), uma que recusa `--no-verify` e `git commit -n`, e o lembrete do hook de fim de sessão para o que ficou por commitar. | [`AGENTS.md`](../../AGENTS.md) e a skill [`git-e-commits`](../../skills/git-e-commits/SKILL.md). |
| 2. O pré-commit é a rede | `tsc`, `eslint`, os testes ligados ao que mudou e as catracas correm sozinhos; se o hook recusou, corrige-se a causa. | Dos últimos 200 títulos de commit, 89 passavam de 72 caracteres, e 25 dos últimos 50 commits não tinham descrição: a regra só escrita não bastava (outubro de 2026). | Os hooks `pre-commit` e `commit-msg`, versionados numa pasta do repositório e ligados uma vez por clone; saltá-los é recusado pelas permissões. | [`AGENTS.md`](../../AGENTS.md), [`git-e-commits`](../../skills/git-e-commits/SKILL.md) e os moldes de [`modelos/git/portoes`](../../modelos/git/portoes/). |
| 3. O passivo só encolhe | O que já viola as regras não pode piorar; o arquivo novo nasce limpo; a linha de base só desce. | O registro de violações dizia «0 críticas» para a regra das 50 linhas por função, e havia 677 funções acima de 50 (outubro de 2026). | 9 catracas, cada uma com uma linha de base versionada, lida do índice do git e não do disco. | [`AGENTS.md`](../../AGENTS.md) (não piorar) e [`codigo-legivel`](../../skills/codigo-legivel/SKILL.md), na parte da linha de base. |
| 4. Nomes únicos e pesquisáveis | Todo nome novo é único no projeto e diz o que guarda; nomes genéricos como `data` ou `utils` são proibidos; antes de criar, `git grep`. | O nome `Props` se repetia 140 vezes entre os nomes de topo (outubro de 2026). | A catraca de nomes únicos e a de nomes genéricos. | [`AGENTS.md`](../../AGENTS.md) e [`codigo-legivel`](../../skills/codigo-legivel/SKILL.md). |
| 5. Bug traz teste | Um `fix` traz o teste de regressão, visto a falhar antes da correção, ou, na mensagem, uma linha de rodapé com o motivo de não haver teste. | Dos últimos 199 `fix`, 86 não traziam teste (outubro de 2026). | O `commit-msg` recusa um `fix` sem arquivo de teste e sem a linha de motivo. Ver o teste falhar antes é protocolo: o hook não o enxerga. | [`AGENTS.md`](../../AGENTS.md) (bug traz teste) e [`testes-e-provas`](../../skills/testes-e-provas/SKILL.md). |
| 6. Registro de bugs por área | O bug encontrado e não corrigido vira um arquivo numa pasta por área; o corrigido vive no próprio commit `fix`. | Os bugs ficavam na conversa. O número que o projeto mediu é do desenho: os `fix` de 30 dias tinham 15 escopos livres, e por isso a lista de áreas é fixa (outubro de 2026). | A catraca dos erros conhecidos (formato e área) e o `commit-msg`, que recusa uma linha de rodapé apontando um arquivo de bug que não vai no commit. Que um bug encontrado foi anotado é protocolo. | [`testes-e-provas`](../../skills/testes-e-provas/SKILL.md): o bug não corrigido vai para o registro do projeto, por área. |
| 7. Fontes usadas em Markdown | Toda fonte citada num `.md` entra no arquivo único de fontes, com a data da consulta e para que serviu. | 432 endereços sem registro em 108 arquivos, quando a catraca nasceu (outubro de 2026). | A catraca de fontes por registrar: um endereço novo num `.md` sem entrada no arquivo de fontes é recusado. | [`AGENTS.md`](../../AGENTS.md), nas regras deste repositório sobre fontes, e [`escrevendo-regras-de-agente`](../../skills/escrevendo-regras-de-agente/SKILL.md). |
| 8. Pesquisa registrada | A pesquisa que outra sessão vai reler vai para um arquivo próprio, com cabeçalho e cinco seções fixas. | 29 auditorias e estudos espalhados em pastas diferentes, cada um com o seu formato (outubro de 2026). | A catraca de pesquisas confere o nome, o cabeçalho, as seções e a marca de cada fonte. Que uma pesquisa feita chegou a ser escrita é protocolo. | [`AGENTS.md`](../../AGENTS.md) (`pesquisas/`) e [`escrevendo-regras-de-agente`](../../skills/escrevendo-regras-de-agente/SKILL.md). |
| 9. Uma só branch | Trabalha-se na principal, sem branches de funcionalidade nem worktrees; a pasta e o índice são compartilhados, então se commita por caminho explícito e se vê o índice à parte. | Duas sessões trabalharam o dia inteiro na mesma pasta: um push levou 27 commits em vez dos 11 que eram do autor (setembro de 2026). Em outubro, um arquivo preparado foi levado pelo commit de outra sessão durante os cerca de 25 segundos do hook. | Só texto: o hook de fim de sessão conta arquivos por commitar, mas não sabe de quem são. | [`orquestrando-sessoes`](../../skills/orquestrando-sessoes/SKILL.md) (várias sessões na mesma pasta) e [`git-e-commits`](../../skills/git-e-commits/SKILL.md). |
| 10. Sem sub-agentes | O trabalho se faz na sessão; uma leitura independente se faz numa sessão nova, que o dono vê e conduz. | Incidente não registrado. O motivo da regra: o resultado de um sub-agente chega como resumo que o dono não vê nem corrige, e corre num contexto que não leu as regras (setembro de 2026, mês em que a regra foi escrita). | Só texto: nenhum hook nem permissão cita a ferramenta de sub-agentes. | [`orquestrando-sessoes`](../../skills/orquestrando-sessoes/SKILL.md) (sub-agentes ou sessões novas: uma escolha, não uma lei). |
| 11. Changelog por fragmento | Toda mudança observável escreve um fragmento próprio, com o hash do commit no nome, no mesmo ciclo do código. | Num arquivo único de changelog, 27 commits de outra conversa apareceram por cima de um trabalho em curso (julho de 2026). | O lembrete do hook de fim de sessão, que cita a pasta dos fragmentos. O resto é texto. | [`git-e-commits`](../../skills/git-e-commits/SKILL.md) (changelog por fragmento) e os moldes de [`modelos/changelog`](../../modelos/changelog/). |
| 12. Tarefa de sistema automática | No fechamento de cada ciclo, além do fragmento, cria-se uma tarefa interna, escrita para o dono ler em três segundos. | As 3 primeiras tarefas saíram com o texto técnico do fragmento colado e ficaram ilegíveis para o dono (outubro de 2026). | Só texto: é um passo do protocolo de fechar o ciclo. | Só no projeto: depende do quadro de tarefas do produto. |
| 13. Versionamento | Só se passa à versão maior seguinte quando o dono declarar o módulo financeiro 100% concluído. | Incidente não registrado (regra de junho de 2026). | Só texto. | Só no projeto. |
| 14. Este arquivo é lido inteiro, todas as vezes | O arquivo de regras tem até 100 linhas, 160 letras por linha e 10 mil no total; o detalhe vai para outro arquivo. | Chegou a 328 KB, cerca de 82 mil tokens por sessão: 39% eram tarefas concluídas há meses, 27% uma cópia do changelog e 13% uma tabela de sessões (agosto de 2026). | A catraca do arquivo de regras recusa linhas, letras e total acima do limite, e um título de regra sem texto integral. | [`AGENTS.md`](../../AGENTS.md) (máximo de 60 linhas, conferido por hook) e [`escrevendo-regras-de-agente`](../../skills/escrevendo-regras-de-agente/SKILL.md). |
| 15. Sugestão de modelo e esforço | A linha de sugestão só aparece quando trocar de modelo compensa no bloco de trabalho seguinte inteiro. | Numa só sessão a sugestão alternou entre dois modelos em quatro sugestões seguidas, trocando a cada uma; como o cache é por modelo, a primeira resposta depois de cada troca relê a conversa inteira a preço cheio (outubro de 2026, mês da revisão da regra). | Só texto. | Só no projeto. A skill [`orquestrando-sessoes`](../../skills/orquestrando-sessoes/SKILL.md) tem uma tabela de modelo para a sessão filha, que é outra regra. |
| 16. Migração aplicada | Um arquivo de migração não prova que ela foi aplicada: confere-se no catálogo do banco vivo. | Uma migração ficou marcada como feita cerca de um mês sem a coluna existir, e o código que a usava deixou a criação de itens 100% quebrada, sem que o `tsc`, o build ou um teste acusassem (julho de 2026). | Protocolo: a consulta ao catálogo. Um hook vigia as chamadas de SQL, mas não prova que a migração foi aplicada. | [`sql-postgres`](../../skills/sql-postgres/SKILL.md) (a prova no banco) e a skill de [banco gerenciado](../../skills/supabase/SKILL.md). |
| 17. SQL auditado numa sessão nova | Todo SQL que pede o sim do dono é lido antes por uma sessão nova, com um pedido imperativo e neutro, que não adianta a conclusão. | A prova de uma migração chegou ao dono com um bloco esquecido que a fazia falhar, sem `BEGIN` e `ROLLBACK` escritos e com um gatilho que trancava as escritas numa tabela de pessoas; o dono a parou antes de correr (outubro de 2026). | As catracas de auditorias de SQL e de SQL novo (formato, categorias, `lock_timeout`, guarda de papel nas funções). Que a auditoria foi feita é protocolo. | [`orquestrando-sessoes`](../../skills/orquestrando-sessoes/SKILL.md) (mudanças de risco passam por uma auditoria a frio) e [`sql-postgres`](../../skills/sql-postgres/SKILL.md). |
| 18. Plano por fases, uma sessão por fase | A sessão principal orquestra; cada fase corre numa sessão nova, auditada e devolvida até ficar verde antes da seguinte. | Na primeira vez que se trabalhou assim (um protótipo de quadro de tarefas, num plano de mais de dez fases), a principal apanhou uma importação circular, um ícone que não existia, um array vazio que furava a memoização e dois achados médios de SQL antes de chegarem ao dono (outubro de 2026). | Só texto. | [`orquestrando-sessoes`](../../skills/orquestrando-sessoes/SKILL.md) (fases: uma de cada vez, cada uma curta). |
| 19. O nome da sessão diz o estado | O título da sessão tem três partes: o estado (quatro valores), a área em maiúsculas e o assunto; cada sessão o troca ao mudar de estado. | Mais de 40 sessões abertas num só dia, cada uma com um título de formato diferente, e o dono não sabia quais podia apagar (novembro de 2026). | Só texto. | Só no projeto. |
| 20. Não martelar a produção | Uma consulta avulsa vale à vontade; reabrir telas pesadas dezenas de vezes não; a escrita se prova dentro de `BEGIN` e `ROLLBACK`. | 6,37 GB num único dia estouraram o limite mensal do banco, e o servidor ficou inutilizável por cerca de 1h40 para quem trabalhava nele. A causa foi um ciclo de correções que verificava contra a base real (agosto de 2026). | Só texto. O provedor do banco, se o excesso se repetir no mesmo ciclo de faturamento, bloqueia tudo de uma vez. | [`sql-postgres`](../../skills/sql-postgres/SKILL.md) (não martelar o servidor). |
| 21. Portão dos 5 pontos | Não se pede push do módulo financeiro enquanto os 5 eixos (regras dos `.md`, cliques, visual, padronização, desempenho) não estiverem provados por medição. | A primeira versão da métrica de consultas sem limite contou 58 onde havia 2: um contador que exagera ensina todos a ignorar a linha (agosto de 2026). | Um comando que imprime cada eixo com o valor medido, o alvo e o veredicto, e sai com código diferente de zero se algum falhar; o eixo visual só fecha com uma pessoa. | Só no projeto. [`codigo-legivel`](../../skills/codigo-legivel/SKILL.md) tem a lição geral: uma catraca diz «não piorou», nunca «está bem». |

O arquivo de regras do projeto tem 21 regras com título em maiúsculas e a palavra regra, e 18 delas trazem o motivo curto depois do ponto médio.

## As proibições

O arquivo de regras do projeto tem uma seção de proibições, com sete linhas. Ficou de fora desta tabela a seção das empresas, que é dado do produto. Quando a proibição repete uma regra, o incidente está nela.

| Proibição | A barreira | No Morg-laws |
|---|---|---|
| `push` ou PR sem o sim do dono; saltar ou desligar os hooks; citar numa mensagem de commit a opção que os salta | Permissão que pede confirmação para cada forma de `git push`; permissão que recusa `--no-verify`, `git commit -n`, mexer na configuração do caminho dos hooks e escrever dentro da pasta interna do git | [`AGENTS.md`](../../AGENTS.md) (commit sem pedido, push com o sim; os hooks são a rede) |
| `git add -A` ou `git add .`; preparar um arquivo antes da hora; commitar trabalho de outra sessão; criar branches ou worktrees | Só texto: a lista de permissões liberadas do projeto está vazia | [`AGENTS.md`](../../AGENTS.md) (só o próprio trabalho) e [`orquestrando-sessoes`](../../skills/orquestrando-sessoes/SKILL.md) |
| Lançar sub-agentes; escrever no banco sem a skill de migração e sem o sim do dono (só uma classe de tarefas internas tem licença permanente) | Para o banco: a ferramenta de aplicar migração pede confirmação e um hook vigia as chamadas de SQL. Para sub-agentes: só texto | [`AGENTS.md`](../../AGENTS.md) (sem escrita no banco), [`sql-postgres`](../../skills/sql-postgres/SKILL.md) e [`orquestrando-sessoes`](../../skills/orquestrando-sessoes/SKILL.md) |
| Apagar uma pessoa do cadastro; filtrar por coluna de exclusão lógica em duas tabelas que não a têm; dados reais em testes ou exemplos | Só texto. Incidente não registrado | [`AGENTS.md`](../../AGENTS.md) (sem dados reais); as outras duas são do produto |
| `any`; uma lista de ícones banidos; re-exports ou constantes de valor num arquivo `'use server'` | Os ícones: um hook de interface que avisa depois de escrever. `any`: o eslint recusa-o no código do sistema (os testes ficam de fora), no `pre-commit`; a catraca das exceções ao alarme conta quem o cala. `'use server'`: só o build acusa, o `tsc` não. Incidente não registrado | [`nextjs-react`](../../skills/nextjs-react/SKILL.md) (arquivo `'use server'`) e [`codigo-legivel`](../../skills/codigo-legivel/SKILL.md); os ícones são do produto |
| Subir para a versão maior por iniciativa própria; reintroduzir uma tela retirada por decisão do dono; martelar a produção com ciclos ou retentativas | Só texto | [`sql-postgres`](../../skills/sql-postgres/SKILL.md) (não martelar); o resto é do produto |
| Ler os arquivos de ambiente ou a pasta dos backups do banco; rodar um download que se executa direto no shell; mudar as próprias permissões | Permissões que recusam a leitura dessas pastas, os comandos de download com execução e a edição do arquivo de permissões (36 entradas de recusa no total). Incidente não registrado | [`AGENTS.md`](../../AGENTS.md) (sem segredos) |

## O mapa das lições

O projeto guarda, além das regras, um arquivo de lições técnicas. Medido em novembro de 2026, ele tem 45 títulos (15 de seção e 30 de lição). Desses, 9 são as categorias, 2 não são lições (o índice e o registro de sessões) e 4 lições ficam fora das categorias, o que dá **34 lições**. Aqui entra só o mapa: cada lição, com palavras próprias, e onde o tema está publicado neste repositório. Nada foi copiado, e os aprendizados novos ficam para outra fase.

Das 34, 29 têm o tema publicado (uma só em parte) e 5 não estão publicadas.

| Lição | Onde está no Morg-laws |
|---|---|
| Edição em massa de arquivos pode corromper sem avisar | [ambiente e ferramentas](../../aprendizados/2026-10-30-ambiente-e-ferramentas.md) |
| Depois de uma edição que devolve avisos, conferir o resultado | Não publicada |
| Ao mover um arquivo, deixar um re-export no lugar antigo | [organização de código](../../aprendizados/2026-10-30-organizacao-de-codigo.md) |
| Tipos compartilhados numa pasta própria | [organização de código](../../aprendizados/2026-10-30-organizacao-de-codigo.md) (organização por tipo) |
| Ações de servidor numa pasta própria | [organização de código](../../aprendizados/2026-10-30-organizacao-de-codigo.md) (organização por tipo) |
| `export *` proibido num arquivo `'use server'` | [`nextjs-react`](../../skills/nextjs-react/SKILL.md) |
| `key={index}` proibido em listas que mudam | [`nextjs-react`](../../skills/nextjs-react/SKILL.md) |
| Bibliotecas de ícones em `optimizePackageImports` | [`nextjs-react`](../../skills/nextjs-react/SKILL.md) |
| Recarregar uma lista não pode ligar o «carregando» | Em parte: [`nextjs-react`](../../skills/nextjs-react/SKILL.md) (o «carregando» só na primeira carga) |
| Consultas em lote no lugar de uma consulta por item num laço | [`sql-postgres`](../../skills/sql-postgres/SKILL.md) e a skill de [banco gerenciado](../../skills/supabase/SKILL.md) |
| `revalidatePath` e `revalidateTag` num helper central | [`nextjs-react`](../../skills/nextjs-react/SKILL.md) |
| Operações independentes em paralelo | [organização de código](../../aprendizados/2026-10-30-organizacao-de-codigo.md) |
| O CI não toca a rede | [`testes-e-provas`](../../skills/testes-e-provas/SKILL.md) |
| Rodar os testes depois de cada lote de decomposição | Não publicada |
| O cliente do banco usa o tipo gerado | A skill de [banco gerenciado](../../skills/supabase/SKILL.md) |
| Zero `any`, cada exceção justificada | [TypeScript](../../aprendizados/2026-10-30-typescript.md) |
| Função com no máximo 50 linhas (hoje 20) | [TypeScript](../../aprendizados/2026-10-30-typescript.md) (limites de tamanho) |
| A data de hoje no servidor vem de uma função única | [datas e validação](../../aprendizados/2026-10-30-datas-e-validacao.md) |
| Criar a data dentro do validador de um schema é permitido | Não publicada |
| Formatação de datas com o locale fixo | [datas e validação](../../aprendizados/2026-10-30-datas-e-validacao.md) |
| Componente que faz tudo vira orquestrador | [organização de código](../../aprendizados/2026-10-30-organizacao-de-codigo.md) |
| Ação de servidor que faz tudo vira estrela | [organização de código](../../aprendizados/2026-10-30-organizacao-de-codigo.md) |
| Checklist de decomposição segura | Não publicada |
| Heredoc do PowerShell corrompe arquivos | [ambiente e ferramentas](../../aprendizados/2026-10-30-ambiente-e-ferramentas.md) |
| `useParams()` devolve mais do que uma string | [TypeScript](../../aprendizados/2026-10-30-typescript.md) |
| `as const` só em literais | [TypeScript](../../aprendizados/2026-10-30-typescript.md) |
| Derivar o tipo do parâmetro da função que consome o dado | [TypeScript](../../aprendizados/2026-10-30-typescript.md) |
| Ícones com muitos apelidos quebram em runtime no Turbopack | [ambiente e ferramentas](../../aprendizados/2026-10-30-ambiente-e-ferramentas.md) |
| Criar usuários do login pela interface administrativa do serviço, nunca por inserção direta na tabela | Não publicada |
| No servidor, a sessão vem dos cookies | A skill de [banco gerenciado](../../skills/supabase/SKILL.md) |
| O código não referencia colunas de migrações não aplicadas | [`sql-postgres`](../../skills/sql-postgres/SKILL.md) e a skill de [banco gerenciado](../../skills/supabase/SKILL.md) |
| Variáveis de ambiente públicas do Next.js só com acesso estático | [`nextjs-react`](../../skills/nextjs-react/SKILL.md) |
| Sem as setas nativas de `<input type="number">` | [`nextjs-react`](../../skills/nextjs-react/SKILL.md) |
| Sem `_prefixo` para calar uma prop não usada | [`nextjs-react`](../../skills/nextjs-react/SKILL.md) |

## Os textos pesquisados

Cada mês acima é o do primeiro commit que traz o texto da segunda coluna. O comando é `git log -S"<texto>" --date=short --format=%ad -- <arquivo> | tail -1 | cut -c1-7`. O «arquivo de regras» é o mesmo `CLAUDE.md` de `o-que-se-mediu.md`; o «arquivo integral» guarda o texto inteiro de cada regra e só existe desde setembro de 2026. Os textos estão como o projeto os escreveu. O que se conferiu foi a linha que o commit acrescenta, e o número em si não foi recontado.

| Regra | Texto pesquisado | Arquivo | Mês |
|---|---|---|---|
| 1 | `109 ficheiros por commitar` | de regras | julho de 2026 |
| 2 | `89 dos últimos 200` | integral | outubro de 2026 |
| 3 | `677 funções` | integral | outubro de 2026 |
| 4 | ``Props` 140`` | integral | outubro de 2026 |
| 5 | `86 de 199` | de regras | outubro de 2026 |
| 6 | `15 âmbitos livres` | integral | outubro de 2026 |
| 7 | `432 URLs por registar` | integral | outubro de 2026 |
| 8 | `29 auditorias e estudos` | integral | outubro de 2026 |
| 9 | `levou **27 commits**` | de regras | setembro de 2026 |
| 9 | `estagiei um fragmento e commitei no mesmo comando` | integral | outubro de 2026 |
| 10 | `não se lançam sub-agentes` | de regras | setembro de 2026 |
| 11 | `27 commits de outra conversa` | de regras | julho de 2026 |
| 12 | `nas primeiras 3 tarefas` | integral | outubro de 2026 |
| 13 | `is 100% finished` | de regras | junho de 2026 |
| 14 | `328 KB` | de regras | agosto de 2026 |
| 15 | `a sugestão saltou` | integral | outubro de 2026 |
| 16 | `durante ~1 mês` | de regras | julho de 2026 |
| 17 | `um bloco esquecido` | integral | outubro de 2026 |
| 18 | `apanhou uma importação circular` | integral | outubro de 2026 |
| 19 | `mais de 40 sessões` | integral | novembro de 2026 |
| 20 | `6,37 GB` e `1h40` | de regras | agosto de 2026 |
| 21 | `58 onde havia 2` | de regras | agosto de 2026 |
