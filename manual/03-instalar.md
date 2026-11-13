# Instalar

Cinco passos põem o Morg-laws para funcionar num projeto: instalar as skills, pôr as regras, ligar as barreiras, guardar a lista negra e fazer a primeira mensagem. Faça na ordem, no seu projeto. Se o git, o Node, o Python, a pasta do projeto ou a cópia deste repositório ainda faltam, a parte `02` leva você até eles.

Cada passo é um par de páginas. Se você só quer fazer, leia a da esquerda de cada um e vá em frente.

## P1 · Instalar as skills

### Na prática

Na raiz do seu projeto, rode:

```
npx skills add Carlobks/Morg-laws -a claude-code -y
```

Esse comando foi testado na versão 1.7.4 do pacote. Ele copia as skills do repositório para a pasta do agente e cria um arquivo com a origem de cada uma:

```
.claude/skills/<nome-da-skill>/
skills-lock.json
```

Para o Codex, troque `claude-code` por `codex`: as skills vão para `.agents/skills/` ([documentação do Codex](https://developers.openai.com/codex/skills)).

O que costuma dar errado:

- Achar que acabou. O comando instala só as skills. O `AGENTS.md` não vem, e o passo seguinte existe por isso.
- Instalar sem ler. A ferramenta avisa no fim que as skills rodam com todas as permissões do agente. Leia a que lhe interessa antes de confiar nela.
- Rodar fora do projeto. Confira com `pwd` ou `cd` que a pasta é a raiz do repositório.

### Por quê e fonte

O `npx skills add` procura a pasta `skills/` do repositório, e só ela. O `AGENTS.md` e o `CLAUDE.md` da raiz não fazem parte de nenhuma skill e ficam de fora: foi o que um teste numa pasta vazia mostrou, comparando arquivo a arquivo com o repositório, sem nenhuma diferença nas skills. Esse teste é de 2026-10-30, na versão 1.7.4 do pacote.

A ferramenta, o [skills da Vercel](https://github.com/vercel-labs/skills), instala para o Claude Code em `.claude/skills/` e para o Codex em `.agents/skills/`, e o Codex procura as suas skills nessa pasta, segundo a [documentação de skills do Codex](https://developers.openai.com/codex/skills). Só a descrição de cada skill entra no começo da conversa; o corpo abre quando ela é usada, como diz a [documentação de skills do Claude Code](https://code.claude.com/docs/en/skills). Por isso instalar muitas skills é barato, e ainda assim cada uma que você não usa é leitura a mais.

O aviso de ler antes é conselho do livro: skill de terceiros só com leitura completa e uma dor concreta que ela resolva (pp. 128–129 do livro *Competente o Suficiente*, de Fabio Akita). Trate-a como código que você roda.

Onde vive no Morg-laws: o resultado do teste está em `aprendizados/2026-10-30-instalacao-das-skills.md`, e a linha do comando está no `README.md` da raiz.

## P2 · Pôr as regras

### Na prática

As regras vêm de um molde, não do `AGENTS.md` da raiz do Morg-laws, que leva também as regras de quem trabalha nele.

1. Copie `modelos/documentos/AGENTS.md` para a raiz do seu projeto, com o mesmo nome.
2. Copie `modelos/documentos/CLAUDE.md` para a raiz. Ele tem a linha `@AGENTS.md`, que manda o Claude Code ler o outro.
3. No `AGENTS.md`, preencha o que está entre `<…>`: o nome, uma linha do que o projeto é e a **Regra n.º 1**, o perigo mais caro do seu projeto.

Uma Regra n.º 1 preenchida, para uma loja de bolos inventada:

```
- **NUNCA APAGAR UM PEDIDO PAGO:** um pedido pago só se cancela, com o motivo, e fica no histórico. · *Uma tela de “limpar” apagou três pedidos pagos e ninguém soube de quem era o bolo.*
```

O que costuma dar errado:

- Deixar um `<…>` sem preencher.
- Pôr dez regras na Regra n.º 1. É uma só, a mais cara.
- Passar de 100 linhas, somando o `AGENTS.md` e o `CLAUDE.md`. Os dois são lidos inteiros em todo turno, e o `test_regras.py` do molde reprova acima disso.

### Por quê e fonte

O `AGENTS.md` é o arquivo que várias ferramentas leem, num [formato aberto](https://agents.md). O Claude Code, porém, lê o `CLAUDE.md`, e com os dois lado a lado lê só ele: daí a linha `@AGENTS.md`, que importa o outro, como diz a [documentação de memória do Claude Code](https://code.claude.com/docs/en/memory). Um import não economiza contexto, só evita escrever as regras duas vezes.

O arquivo é curto de propósito. Um estudo sobre arquivos de contexto achou que eles em geral não melhoram a taxa de tarefas resolvidas e que aumentam o custo em mais de 20% em média ([o estudo no arXiv](https://arxiv.org/abs/2602.11988)); outro, de cinco corridas num só repositório, viu um `AGENTS.md` de 12 linhas deixar o agente mais rápido e mais barato, e o autor mesmo o chama de um único ponto de dados ([AAIF](https://aaif.io/blog/measuring-agents-md-what-five-runs-show-that-one-doesn-t)). Nenhum dos dois diz qual o tamanho certo. O limite de 100 linhas é o do teste do molde; o `AGENTS.md` do próprio Morg-laws fica em 60, e um hook dele o confere.

A Regra n.º 1 ganha um lugar só dela porque o perigo mais caro merece uma linha à parte, e o motivo escrito ao lado mostra ao agente o que custou da última vez. Essa forma, com a regra e o motivo juntos, é a que o teste do repositório confere em todas as regras.

Onde vive no Morg-laws: o molde é `modelos/documentos/AGENTS.md`, e o teste `modelos/testes/test_regras.py` confere que cada regra tem o seu motivo.

## P3 · Ligar as barreiras

### Na prática

Texto é conselho. Para as regras serem cumpridas, copie as barreiras do Morg-laws:

1. Copie `modelos/claude/` para `.claude/` do seu projeto: são os hooks do agente e o `settings.json` do Claude Code.
2. Copie `modelos/git/hooks/` para `.githooks/` e `modelos/git/portoes/` para `scripts/portoes/`: os hooks do git chamam esses scripts, e sem eles todo commit é recusado. No Linux e no macOS, confira a marca de executável no disco com `ls -l .githooks`, e `chmod +x .githooks/*` se faltar o `x`.
3. Ligue os hooks do git: `git config core.hooksPath .githooks`.
4. Copie `modelos/testes/test_regras.py` e o `carregar_por_caminho.py` para `tests/`. O `COMANDO_DOS_TESTES`, no `pre-commit`, fica vazio até o ajuste da parte `08`.
5. Prove: peça ao agente um commit com `--no-verify` e veja a recusa.
6. Prove também o hook do git: faça você um commit de teste, como o da parte `02`. O `pre-commit` o recusa, pedindo o `COMANDO_DOS_TESTES`, e a recusa prova que ele rodou. Se a do 5 não recusar, confira o `.claude/settings.json`; se o 6 passar, o `core.hooksPath` e a marca de executável.

O que o hook do agente responde, de verdade, a esse pedido (o resto da frase diz o que a opção faz):

```
Bloqueado (portões do git, Morg-laws): --no-verify …
```

No Claude Code, o comando sai com código 2, e o agente não commita.

O que costuma dar errado:

- Copiar e nunca provar. Um hook que não inicia pode deixar tudo passar.
- Esquecer o `core.hooksPath`: sem ele os hooks do git não rodam.

### Por quê e fonte

Um `AGENTS.md` é orientação, não barreira: o agente pode esquecê-lo ou escolher outro caminho. Por isso o que tem de ser cumprido vira hook, teste ou CI. No Claude Code, um hook `PreToolUse` que sai com 2 bloqueia a chamada e mostra o motivo ao agente, e o campo `onFailure` com o valor `block` faz um hook que falha também bloquear, desde a versão 2.1.295 (o `claude --version` mostra a sua; [documentação de hooks](https://code.claude.com/docs/en/hooks)). Numa versão mais antiga o campo é ignorado, e um hook que não inicia deixa passar. O código 2 é o número com que o hook diz “recusei”.

Há duas camadas, e uma cobre a outra. Os hooks do agente (`modelos/claude/`) olham o que o agente tenta fazer, como o `--no-verify` acima. Os hooks do git (`.githooks/`) rodam em todo commit, do agente ou feito à mão; o `git add --chmod=+x .githooks/*` grava a marca de executável também no git, para quem clonar depois. As duas se somam às permissões do agente, que a [documentação de permissões](https://code.claude.com/docs/en/permissions) descreve.

Na dúvida de por onde começar, o mínimo recomendado é a guarda do git, o hook de segredos e o que pergunta antes do push, mais o `pre-commit` e o `test_regras.py`. O resto vem quando você sentir falta.

Onde vive no Morg-laws: a lista completa, com o que cada arquivo recusa, está em `modelos/README.md`; a sonda de cada barreira, na skill `auditoria-de-seguranca`.

## P4 · A lista negra e o e-mail noreply

### Na prática

Dois cuidados para o que você commita não expor ninguém.

1. Identidade só deste repositório, com o e-mail noreply que o GitHub dá à sua conta:
   `git config --local user.email "o seu e-mail noreply"`
2. Uma lista negra fora do repositório, um termo por linha, e o git sabendo onde ela está:
   `git config morg.listaNegra <caminho da lista>`

A lista guarda o que nunca pode aparecer num commit. Um exemplo com três termos inventados (maiúsculas não importam, o hook as ignora):

```
padaria exemplo
joana teste
12345678
```

O `pre-commit` recusa um commit se o autor, um nome de arquivo ou uma linha nova tiver um desses termos.

O que costuma dar errado:

- Pôr a lista dentro do repositório. Ela então publica o que devia esconder.
- Esquecer o e-mail: sem ele, o commit sai com o da configuração global, que em outra máquina costuma ser o pessoal.
- Sem a lista, o hook só avisa, não recusa.

### Por quê e fonte

O que entra num repositório público não sai mais: o histórico guarda tudo, também o que você apagou depois. Por isso um nome, um e-mail ou um número real nunca entram, e o filtro tem de rodar antes do commit, não depois. A lista fica fora do repositório porque, dentro dele, seria a lista dos nomes que você queria esconder.

O e-mail noreply é público por desenho, e por isso seguro de commitar. Sem a identidade local, o commit usa a global da máquina: o noreply, se você seguiu a parte `02`, e em outra máquina, em geral, a pessoal; o portão `identidade.py` recusa outro e-mail. Uma regra do próprio `AGENTS.md` diz o mesmo em curto: nunca dados reais em testes, exemplos ou commits.

O hook lê a lista sozinho, então o agente não precisa abri-la: a pasta que o modelo sugere para ela, `~/.config/morg-laws`, já vem negada ao agente no `settings.json` (o arquivo de permissões do Claude Code).

Onde vive no Morg-laws: `modelos/git/hooks/pre-commit` e `modelos/git/portoes/lista_negra.py`; a nota sobre a identidade está na [nota de aprendizado sobre o git](https://github.com/Carlobks/Morg-laws/blob/main/aprendizados/2026-11-01-git.md).

## P5 · A primeira mensagem

### Na prática

Com tudo no lugar, abra o agente na raiz do projeto e mande a mensagem que chama a skill de começo.

No Claude Code:

```
/comecando-um-projeto Quero começar (ou organizar) este projeto com você. Antes de escrever código, me faça as perguntas em rondas, confirme comigo cada resposta e deixe escritos o documento do projeto, o AGENTS.md, o primeiro plano e as decisões de arquitetura.
```

No Codex, o mesmo texto, com `$` no lugar da barra ([documentação do Codex](https://developers.openai.com/codex/skills)).

O agente vai perguntar. Responda por rondas, e leia o que ele escreveu antes de aceitar.

O que costuma dar errado:

- Pedir o código antes de as respostas existirem. A skill serve para o contrário.
- Aceitar o `AGENTS.md` sem ler. É o arquivo que o agente lerá em todo turno.

### Por quê e fonte

Escrever o documento do projeto, as regras e o primeiro plano antes de qualquer código dá ao agente o que está na sua cabeça e que ele não adivinha. A skill conduz isso em rondas de perguntas, e cada resposta fica confirmada antes de virar texto.

Chamar a skill pelo nome é mais firme do que esperar que o agente a escolha: no Claude Code, `/nome-da-skill` no começo da mensagem chama a skill, e o resto do texto chega como argumento ([documentação de skills do Claude Code](https://code.claude.com/docs/en/skills)); no Codex, digita-se `$` e o nome da skill, ou usa-se `/skills` ([documentação de skills do Codex](https://developers.openai.com/codex/skills)). Nos dois, o agente também pode abrir a skill sozinho pela descrição.

A mensagem acima é a que o `README.md` da raiz já traz. Se o seu projeto já existe e tem código, ela vale do mesmo jeito: a skill organiza em vez de começar do zero.

Onde vive no Morg-laws: a skill `comecando-um-projeto` e a seção “Primeira mensagem num projeto” do `README.md` da raiz.
