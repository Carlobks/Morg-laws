---
name: git-e-commits
description: Guia como o agente commita e fecha um ciclo de trabalho — commits atômicos por caminho, mensagens com o porquê, hooks que não se saltam, a marca obrigatória em commits de correção sem teste, o changelog por fragmento e o que conferir antes de pedir o push. Usar ao commitar, ao escrever uma mensagem de commit, quando um hook recusa um commit, ao terminar um bloco de trabalho com arquivos por commitar, ou antes de pedir push ou PR. Não usar para coordenar várias sessões na mesma pasta (é a orquestrando-sessoes) nem para decidir que testes escrever (é a testes-e-provas).
---

# Git e commits

O commit é o único lugar onde o trabalho fica a salvo. Num projeto real, 109 arquivos viveram só no disco de uma máquina até alguém notar. Esta skill diz como commitar sem perder trabalho e sem levar o trabalho de outros.

## 1. Quando commitar e quando pedir

- **Commitar não precisa de pedido.** Terminou um pedaço que funciona: commite.
- **Push e PR precisam do "sim" do dono do projeto**, a cada vez. Um "sim" de antes não vale para o push seguinte.
- O commit é **atômico**: uma mudança com um propósito. Duas mudanças independentes são dois commits.

## 2. Como commitar

```bash
git status --short -uall          # -uall: mostra cada arquivo das pastas novas
git add -- <arquivo1> <arquivo2>  # por caminho, nunca -A nem .
git commit -F msg.txt -- <arquivo1> <arquivo2>
```

- **Por caminho, sempre.** Sem `-uall`, uma pasta nova aparece como uma linha só, e os arquivos dentro dela ficam fora do commit sem ninguém notar.
- **Mensagem num arquivo** (`-F`), não por heredoc nem por `-m` com várias linhas: no Windows, o heredoc corrompe o texto.
- **Formato:** título com até 72 caracteres, tipo e área (`fix(login): …`, `docs(regras): …`), sem ponto final. Linha em branco. Corpo com **o que mudou e porquê**.
- **Nada de dados reais** na mensagem: ela é tão pública quanto o código.
- **Clone novo, identidade local:** `git config --local user.email <noreply>`. Sem isso, o commit sai com o nome e o e-mail da configuração global da máquina, que costumam ser os pessoais.

## 3. Os hooks são a rede

- O `pre-commit` roda o compilador, o lint, os testes dos arquivos tocados e as catracas. O `commit-msg` confere a mensagem.
- **Nunca** `--no-verify`, nunca desligar o hook, nunca citar na mensagem a opção que o salta.
- Hook recusou: leia a saída, corrija a causa e commite de novo. Se o hook estiver errado, corrija o hook num commit próprio.
- **O hook do git vale também para quem commita à mão; o hook do agente só trava o agente.** O que tem de valer sempre vai no hook do git, e no CI para quem o desligar.
- **Uma guarda no agente fecha as saídas** (modelo em [`modelos/claude/hooks/`](https://github.com/Carlobks/Morg-laws/tree/main/modelos/claude/hooks)). Ela recusa:
  - `--no-verify` (ou `-n` num commit);
  - mudar ou desligar o `core.hooksPath`;
  - `git add -A`, `-u`, `.`, `--all`, `--update` ou `:/` (no `git add` só passam caminhos e opções que não alargam o que se prepara), e `git commit -a`;
  - commit sem caminhos fora de um merge;
  - `-m` com várias linhas;
  - `git stash`.

  Duas destas brechas foram abertas pelo próprio agente, num commit dele.

## 4. Correção sem teste tem de dizer porquê

Um commit `fix(…)` traz o teste que pega o bug, visto a falhar antes da correção. Quando não há como testar, o corpo leva a linha:

```
Sem-teste: <motivo concreto>
```

Um hook `commit-msg` pode exigi-lo. Num projeto real, 86 de 199 commits de correção não tinham teste antes desta regra.

O mesmo hook pode exigir outras marcas, cada uma com o motivo concreto (modelo em [`modelos/git/`](https://github.com/Carlobks/Morg-laws/tree/main/modelos/git)):

| Marca | Quando |
|---|---|
| `Teste-mudado:` | O commit tira ou muda linhas de um teste que já existia. Acrescentar casos não pede nada. |
| `Sem-changelog:` | Um `feat` ou `fix` no que se instala sem fragmento do changelog. |
| `Changelog-corrigido:` | O commit muda uma versão já lançada do `CHANGELOG.md`. |

## 5. Changelog por fragmento

- Um `CHANGELOG.md` único colide quando várias sessões escrevem ao mesmo tempo.
- Cada mudança que alguém de fora nota leva um arquivo próprio: `changelog.d/AAAA-MM-DD-assunto.md`. O hash não entra no nome, porque ainda não existe antes do commit.
- A categoria vai na primeira linha do arquivo (`Categoria: Corrigido`), não no nome: um nome errado mudaria a categoria sem ninguém notar. As categorias são as do Keep a Changelog.
- Mudança interna (refatoração, teste, documentação de trabalho) não leva fragmento.
- **A versão sobe só no lançamento:** um script junta os fragmentos, calcula a versão SemVer pelas categorias (`Removido` ou uma linha `Incompatível:` sobe o MAIOR) e escreve o `VERSION` no mesmo commit. À mão, a versão diverge do changelog. Modelo em [`modelos/changelog/`](https://github.com/Carlobks/Morg-laws/tree/main/modelos/changelog).

## 6. Fechar um ciclo

Antes de dizer "feito":

1. **Separar o que é seu.** `git status --short -uall`, e para cada arquivo, `git log -1 -- <arquivo>` e a memória do que você mexeu. O que é de outra sessão não se toca.
2. **Rodar os portões** do projeto (tipos, lint, testes relacionados).
3. **Commitar por caminho**, em commits atômicos.
4. **Fragmento** do changelog, se a mudança se vê de fora.
5. **Registrar os bugs encontrados e não corrigidos**, no lugar que o projeto usa para isso, organizados por área. Sem um rastreador que o agente possa escrever, é **um arquivo por bug**, numa pasta por área (a pasta é a área): um arquivo único colide entre sessões, como o changelog (§5). O commit que o corrige leva uma marca que aponta para o arquivo e o fecha no mesmo commit. O índice dos abertos gera-se por script e não se commita. O bug é um item aberto, que muitas sessões criam e fecham; uma lição que fica depois da correção vai para as armadilhas (molde `modelos/documentos/armadilhas.md`).
6. **Dizer o que ficou por fazer e o que não se verificou.** Pedir o push só com os portões verdes.

## 7. Quando algo dá errado

- **`index.lock` existe:** veja a skill `orquestrando-sessoes`. Nunca apague o lock de outro processo. Um lock seu e velho prova-se e renomeia-se.
- **Arquivo preparado com a versão errada:** commitar por caminho grava o que está no disco e passa por cima do que ficou preparado.
- **Commit de outra sessão levou o seu arquivo:** não reescreva o histórico partilhado. Faça um commit novo com a versão certa e avise.
- **Histórico já publicado com um dado que não devia:** se não é segredo, não se reescreve (muda os hashes de todos). Registre a exceção numa decisão escrita e trave o dado com um teste para não voltar. Segredo publicado roda-se ou revoga-se, sempre.
- **Marca de executável no Windows:** com `core.filemode=false`, `git commit -- <caminhos>` lê o arquivo do disco e grava-o como `100644`, perdendo o `+x` preparado. Use `git add --chmod=+x` e `git commit -i -- <caminho>`.
- **`git checkout -- <arquivo>` (ou `git restore`) apaga as mudanças por commitar, sem volta.** Num script que repõe um arquivo depois de um teste, guarde uma cópia antes e reponha a cópia.

## Fontes

As regras vêm da prática dos projetos de origem. Os números (109 arquivos, 86 de 199) foram medidos lá. A parte do `index.lock` apoia-se no código do git (`lockfile.c`). O changelog e a versão apoiam-se no Keep a Changelog, no towncrier e no SemVer. Um arquivo por bug (§6, passo 5) apoia-se no towncrier e no texto do GitLab sobre o changelog que colidia; a marca no commit e o índice gerado vêm da prática dos projetos de origem. Todas estão em [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md).
