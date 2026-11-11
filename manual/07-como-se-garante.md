# Como se garante

A parte 06 disse o que cada regra manda. Esta diz como o Morg-laws faz uma regra ser cumprida mesmo quando o agente a esquece ou escolhe outro caminho. A resposta é uma só, repetida em três lugares: o que tem de ser cumprido deixa de ser texto e vira uma barreira de máquina, que recusa em vez de pedir. Aqui estão as três camadas, o que cada arquivo pronto recusa, as catracas que seguram a dívida de um projeto que já viola e o jeito de ligar tudo, sem repetir os passos do procedimento P3 da parte 02.

## Texto vira barreira

O `AGENTS.md` termina o núcleo com a regra “Texto vira barreira”: o texto é conselho, e o que tem de ser cumprido vira hook, teste ou CI. O porquê escrito é curto: regra só escrita não se cumpre. Um agente lê o `AGENTS.md` em todo turno e mesmo assim esquece, porque a regra concorre com o pedido que ele acabou de receber. Um hook não concorre com nada: quando roda, a resposta dele é um código de saída. Onde cada hook não chega, esta parte diz mais abaixo.

A pergunta que decide o que vira barreira está na seção 6 da skill [`escrevendo-regras-de-agente`](https://github.com/Carlobks/Morg-laws/blob/main/skills/escrevendo-regras-de-agente/SKILL.md). Em resumo, se pergunta o que acontece se o agente a ignorar: se acontece pouco, a regra fica como texto; se acontece muito (um vazamento, um dado apagado, a produção fora do ar), ela vira barreira. O mapa de cada regra e da barreira que a obriga, ou do motivo de ficar em texto, tem um molde pronto, `modelos/documentos/regras-e-barreiras.md`, e o teste `test_regras.py` confere que cada regra do `AGENTS.md` tem a sua linha nesse mapa. Nem toda regra grave tem barreira: no mapa, a escrita no banco de produção fica em texto, porque nenhuma máquina sabe se houve o “sim” do dono.

## As três camadas

Cada camada olha para um momento diferente, e uma cobre o que a outra deixa passar.

1. **Os hooks do agente** olham o que o agente tenta fazer: um comando, uma escrita de arquivo. Vivem em `modelos/claude/hooks/` e se ligam no `modelos/claude/settings.json`. Só valem no Claude Code, mas pegam o erro antes de ele acontecer.
2. **Os hooks do git** olham o commit e o push, de quem for: do agente, de uma pessoa ou de outra ferramenta. Vivem em `modelos/git/hooks/`, com a lógica em `modelos/git/portoes/`.
3. **O CI** roda o mesmo comando de testes numa máquina limpa, a cada push, e não depende da configuração da máquina de quem commita. Vive em `modelos/github/workflows/ci.yml`.

A fonte da forma geral é a skill [`escrevendo-regras-de-agente`](https://github.com/Carlobks/Morg-laws/blob/main/skills/escrevendo-regras-de-agente/SKILL.md), e a lista completa dos arquivos, com o destino de cada um, está em [`modelos/README.md`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/README.md).

## Os hooks do agente

São quatro scripts em Python, só com a biblioteca padrão, e um `settings.json` que os liga ao Claude Code. Os três primeiros olham comandos de shell; o quarto olha escritas de arquivo.

- **`guarda_do_git.py`** recusa o que contorna os hooks do git: `--no-verify`, mudar o `core.hooksPath`, `git add -A`, `commit -a`, um commit sem caminhos, uma mensagem com `-m` de várias linhas e o `git stash`. É a regra “Os hooks são a rede” e o “Nunca” dos commits alheios, em forma de máquina.
- **`bloquear_segredos.py`** recusa ler segredos pela shell, porque o `deny` das permissões só cobre a ferramenta Read, e recusa `curl … | sh`. É o “Nunca” dos segredos.
- **`perguntar_antes.py`** não recusa: pergunta. Antes de um push, de tudo o que escreve no GitHub (PR, issue, comentário, versão), de instalações e de mudanças nas regras do agente, ele pede o “sim” do dono, também quando uma regra `ask` das permissões não perguntaria. Num projeto real, um `git push` saiu sem pergunta no modo automático, embora a documentação diga que as regras `ask` perguntam também ali ([modos de permissão](https://code.claude.com/docs/en/permission-modes)); o hook não depende de qual dos dois vale na sua versão.
- **`limite_de_linhas.py`** recusa que um arquivo de código passe de 500 linhas e cresça. Só bloqueia se passar do limite e crescer: encolher um arquivo antigo e grande é sempre permitido.

As permissões do `settings.json` têm três colunas. O `deny` tira do alcance do agente o que ele não deve usar, como `.env`, chaves e a pasta da lista negra. O `ask` pergunta antes de um push ou de uma instalação. O `allow` libera o que é só leitura. O livro manda tirar do alcance do agente o que ele não deve usar (pp. 164–165). O `settings.json` ainda desliga o modo que pula as permissões e põe `onFailure: block` em cada hook, de modo que um hook que falha também bloqueia, e não deixa passar.

Os hooks do agente só olham o que o agente tenta. Uma edição feita pela shell escapa do `limite_de_linhas.py`, e um commit feito à mão não passa por nenhum deles. Para isso existe a camada seguinte. A fonte é a seção sobre hooks do [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md) e a skill [`auditoria-de-seguranca`](https://github.com/Carlobks/Morg-laws/blob/main/skills/auditoria-de-seguranca/SKILL.md).

## Os hooks do git

São três hooks em `sh` (o Git para Windows traz um), que chamam scripts em Python em `modelos/git/portoes/`.

O `pre-commit` roda antes de o commit existir e confere a identidade do autor, a lista negra e o comando único de testes, que você define em `COMANDO_DOS_TESTES`. O `commit-msg` confere o formato da mensagem e passa a mensagem pela mesma lista negra, porque a mensagem de um commit também é pública. O formato tem cinco marcas que liberam uma recusa com o motivo escrito: `Sem-teste:` para um `fix` sem teste de regressão, `Teste-mudado:` para um teste alterado, `Sem-changelog:` para uma mudança sem fragmento, `Alarme-novo:` para deixar subir a contagem de alarmes calados e `Changelog-corrigido:` para mudar uma versão já lançada do `CHANGELOG.md`. O `pre-push` mostra o que vai sair, roda o gitleaks sobre os commits que vão sair e roda o `npm audit` com linha de base em cada pasta com `package-lock.json`. Há também uma versão do `pre-push` só em `sh`, sem Python, em `modelos/pre-push`: vai para o mesmo `.githooks/pre-push`, no lugar da outra, e precisa da marca de executável.

A parte 05 mostra o que o aluno vê quando um deles recusa (P20). A fonte de cada hook é a seção “Os hooks são a rede” da skill [`git-e-commits`](https://github.com/Carlobks/Morg-laws/blob/main/skills/git-e-commits/SKILL.md).

## O CI

O molde `modelos/github/workflows/ci.yml` roda, numa máquina limpa e a cada push, o mesmo comando de testes do `pre-commit`, com todo o histórico, para a linha de base poder ser comparada com a do ramo de destino. Roda também o gitleaks em todo o histórico, com o binário baixado de uma versão fixa e o hash conferido, e as actions fixadas por hash de commit, com a versão em comentário.

O CI existe porque os hooks locais podem ser pulados de verdade: quem commita de outra máquina, ou desliga a configuração, os evita. O CI é a última rede, fora da máquina de quem commita, mas não da mão de quem faz push: cada push roda o `ci.yml` do próprio commit ([workflows do GitHub](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows)), e quem muda o arquivo muda o CI. Por isso uma mudança no `ci.yml` se revê como uma mudança de código. Um teste pronto, `test_ci.py`, confere o próprio arquivo do CI: actions fixadas por hash, token só de leitura e nada baixado direto para uma shell. A fonte é a skill [`auditoria-de-seguranca`](https://github.com/Carlobks/Morg-laws/blob/main/skills/auditoria-de-seguranca/SKILL.md).

## Os testes prontos

Os testes prontos vivem em `modelos/testes/`, em Python, e têm uma versão em TypeScript em `modelos/testes-ts/`, para rodar com o `vitest`. Cada um transforma uma regra em um teste que falha. Agrupados pelo que guardam:

**Tamanho.** `test_tamanho_dos_arquivos.py` recusa arquivo de código com mais de 500 linhas, em todas as línguas, o mesmo limite do hook `limite_de_linhas.py`. `test_tamanho_das_funcoes.py` recusa função Python com mais de 20 linhas, contada como no TypeScript. As vozes da cabeça de Carlobks (decisão de 2026-11-02): função nova até 20 linhas. Porquê: uma função curta faz uma coisa só, a mudança acerta de primeira e o teste dela é pequeno (seção 1 da skill [`codigo-legivel`](https://github.com/Carlobks/Morg-laws/blob/main/skills/codigo-legivel/SKILL.md)). Outra decisão de Carlobks (2026-11-03): arquivo até 500 linhas. Porquê: um arquivo grande mistura responsabilidades, e o agente o lê inteiro para mudar uma linha. O arquivo de regras tem outro teto. No seu projeto, o `test_regras.py` recusa mais de 100 linhas, somando o `AGENTS.md` e o `CLAUDE.md`, porque os dois são lidos inteiros em todo turno ([`test_regras.py`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/testes/test_regras.py)). O Morg-laws usa 60 no próprio `AGENTS.md` ([`pre-commit`](https://github.com/Carlobks/Morg-laws/blob/main/.githooks/pre-commit)), mas é o 100 que vale para você. Os números vêm da prática do projeto de origem, e não de uma norma.

**Nomes.** `test_nomes.py` recusa arquivo, pasta ou identificador com nome genérico solto, como `data`, `utils` ou `helper`. `test_nomes_unicos.py` recusa dois nomes de topo iguais no Python e dois arquivos de código com o mesmo nome. É a regra “Nomes únicos e pesquisáveis”.

**Alarmes.** `test_alarmes.py` recusa um alarme calado sem o motivo na mesma linha, e recusa que a contagem de cada tipo suba no projeto inteiro, salvo com a marca `Alarme-novo:` no commit. O livro dá a razão: uma exceção a um alarme só vale com a razão escrita (p. 165). `test_testes_saltados.py` recusa um teste pulado sem condição ou sem motivo escrito.

**Dados pessoais.** `test_dados_pessoais.py` recusa caminhos de pastas pessoais, e-mails pessoais, termos da lista negra e os números de documento que o projeto ligar. É o “Nunca” dos dados reais.

**Permissões e CI.** `test_permissoes.py` confere as três colunas, o modo que pula as permissões desligado e os hooks ligados com `onFailure: block`. `test_ci.py`, acima, confere o CI.

**Regras e documentos.** `test_regras.py` confere o arquivo de regras: cada regra com motivo e com linha no mapa das barreiras, caminhos citados que existem e o índice das skills igual ao instalado. `test_docs_indices.py` confere os índices dos documentos, as decisões seguidas, a pesquisa com data e os handoffs com hashes que existem. `test_fins_de_linha.py` confere LF no git.

A fonte de todos é a skill [`codigo-legivel`](https://github.com/Carlobks/Morg-laws/blob/main/skills/codigo-legivel/SKILL.md), com a lista de cada um e como instalar, e a [`testes-e-provas`](https://github.com/Carlobks/Morg-laws/blob/main/skills/testes-e-provas/SKILL.md).

## As catracas

Um projeto que já viola uma regra não consegue ligar o teste dela: a primeira corrida falharia em tudo. A catraca resolve isso. Uma catraca é uma linha de base que só encolhe: o que já viola fica congelado numa lista, o que não está nela tem de nascer limpo, e quem corrige uma violação a tira da lista no mesmo commit. A lista não pode subir nem ficar com folga: se uma violação foi corrigida e continua listada, o teste falha, para a lista não esconder uma melhora.

O motor é `modelos/testes/linha_de_base.py`, e os seis testes de tamanho, de nomes, de alarmes e de testes pulados o usam. Cada linha de base vive num arquivo em `tests/linhas-de-base/` do projeto. Para criar a primeira, rode os testes uma vez com a variável `MORG_CRIAR_LINHA_DE_BASE=1`, leia o que ficou congelado e adicione os arquivos ao commit. No CI, a lista é comparada com a do ramo de destino, dada pela variável `MORG_BASE_DE_COMPARACAO`, porque senão alguém poderia “encolher” a lista alterando só o arquivo dela. Os moldes em TypeScript têm o mesmo formato, e leem o código pela árvore do `typescript`.

O próprio Morg-laws usa uma catraca para as entradas antigas do `FONTES.md` que ainda não têm data ou “Sustenta”: `tests/linhas-de-base/fontes.json`, que só pode encolher. Quem corrige uma entrada a tira dali no mesmo commit, e o teste falha se ela ficar. O mecanismo e o cuidado de ler a linha de base antes de congelá-la estão na seção 4 da skill [`codigo-legivel`](https://github.com/Carlobks/Morg-laws/blob/main/skills/codigo-legivel/SKILL.md) e na seção 6 da [`testes-e-provas`](https://github.com/Carlobks/Morg-laws/blob/main/skills/testes-e-provas/SKILL.md). Uma catraca diz “não piorou”, nunca “está bem”.

## O próprio Morg-laws como exemplo

O repositório que você está lendo usa as três camadas. O `.githooks/pre-commit` confere a identidade, a lista negra do nome do autor, das linhas adicionadas e dos nomes dos arquivos, e roda os testes que impedem dados pessoais no catálogo e neste manual. O `.githooks/commit-msg` passa a mensagem pela lista negra. O CI tem dois arquivos: `.github/workflows/seguranca.yml`, que roda o gitleaks em todo o histórico, confere que o `AGENTS.md` tem no máximo 60 linhas e roda a suíte de testes, e `.github/workflows/links.yml`, que usa o lychee para conferir os links externos dos arquivos `.md`.

O Morg-laws é público, por isso a lista negra é o que mais pesa nele. Ela fica fora do repositório, e o hook mostra só as linhas do commit que casaram, no seu terminal, nunca a lista inteira. Os arquivos estão em [`.githooks/`](https://github.com/Carlobks/Morg-laws/tree/main/.githooks) e em [`.github/workflows/`](https://github.com/Carlobks/Morg-laws/tree/main/.github/workflows).

## Os passos técnicos

O procedimento P3 da parte 02 liga o mínimo: copiar, dar a marca de executável, ligar o `core.hooksPath` e definir o comando de testes. O “Como instalar” de [`modelos/README.md`](https://github.com/Carlobks/Morg-laws/blob/main/modelos/README.md) manda mais algumas coisas, e é nelas que um projeto real costuma tropeçar.

1. **A identidade.** Use um e-mail só deste repositório, no formato `noreply` do GitHub, com `git config --local`, para o seu e-mail pessoal não ficar público em cada commit.
2. **A lista negra.** Guarde-a fora do repositório, um termo por linha, e aponte para ela com a configuração `morg.listaNegra` do git. A pasta que o molde usa já está no `deny` e no `bloquear_segredos.py`; se usar outra, ajuste os dois.
3. **O ajuste ao projeto.** Defina `COMANDO_DOS_TESTES` no `pre-commit`, `TESTE` e `PUBLICADO` no `mensagem_commit.py` e o bloco “Ajuste ao projeto” no início de cada teste. Uma parte cuja pasta não existe é pulada, e não falha.
4. **Um projeto em TypeScript.** Copie `modelos/testes-ts/` para `tests/catracas/`, instale o `vitest` e o `typescript` com as versões fixadas no `package-lock.json`, fixe o Node num `.nvmrc` e ponha `npx vitest run` no comando único.
5. **O Python dos hooks.** Os hooks usam a variável `MORG_PY`, ou `py` no Windows, ou `python3`, sempre com `-I`. Os hooks do agente só travam se falharem com o Claude Code na versão 2.1.295 ou mais nova; numa versão antiga o campo `onFailure` é ignorado, e um hook que não inicia deixa passar.
6. **Só sessões, sem sub-agentes (opção).** Acrescente `"Agent"` ao `deny` do `.claude/settings.json` e ponha `SO_SESSOES = True` no `test_permissoes.py`. O nome da ferramenta sozinho a tira do contexto do agente. O molde vem sem esta linha, porque é uma escolha.
7. **Pedir uma sonda.** Antes de confiar numa barreira, peça ao agente uma ação que ela deve recusar, como um commit com `--no-verify`, e veja a recusa. O método está na seção 8 da skill [`auditoria-de-seguranca`](https://github.com/Carlobks/Morg-laws/blob/main/skills/auditoria-de-seguranca/SKILL.md).
