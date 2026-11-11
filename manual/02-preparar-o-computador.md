# Preparar o computador

Esta parte serve a quem nunca programou. Leva você do computador como ele está até o primeiro comando da parte seguinte funcionar: o Claude Code instalado, o git, o Node e o Python conferidos, uma pasta de projeto que já é um repositório e uma cópia do Morg-laws ao lado dela. Se você já tem tudo isso, pule para a `03`.

Um aviso de honestidade: o autor só usou estes passos no Linux. Os de Windows e de macOS vêm da documentação oficial de cada programa, lida para este manual, com o link em cada seção. Se um passo não bater com a sua tela, vale a página oficial.

## Que sistema você tem

Três sistemas aparecem aqui: Windows, macOS e Linux. Em cada passo em que o comando muda, há um bloco curto para cada um, e você segue só o seu. Se não sabe qual é o seu, é quase sempre o primeiro que você vê ao ligar a máquina: a tela com o menu Iniciar embaixo é o Windows, a barra com a maçã no canto de cima é o macOS, e o resto é Linux.

Os requisitos mínimos estão na [página de instalação do Claude Code](https://code.claude.com/docs/en/setup#system-requirements): macOS 13 ou mais novo, Windows 10 (versão 1809) ou mais novo, ou uma destas distribuições Linux: Ubuntu 20.04, Debian 10 ou Alpine 3.19, ou mais novas.

## O terminal: abrir e andar entre pastas

O terminal é a janela onde você digita os comandos. O [guia oficial do Claude Code](https://code.claude.com/docs/en/terminal-guide) diz como abri-lo:

- **Windows:** aperte `Win + X` e escolha o PowerShell (ou o Terminal). Use o PowerShell, não o prompt de comando (CMD): os dois se parecem, mas os comandos são outros. Você sabe qual é pelo começo da linha: no PowerShell ela começa por `PS`, e no CMD não.
- **macOS:** aperte `Cmd + Espaço`, digite `Terminal` e aperte Enter.
- **Linux:** aperte `Ctrl + Alt + T` ou procure “Terminal” no menu de aplicativos.

Para colar um comando, use `Cmd + V` no macOS, `Ctrl + Shift + V` no Linux e `Ctrl + V` (ou o botão direito) no PowerShell.

O terminal está sempre dentro de uma pasta, e os comandos agem sobre ela. Quatro comandos bastam para andar, e valem nos três sistemas (no PowerShell eles existem com esses mesmos nomes):

- `pwd` mostra em que pasta você está.
- `ls` lista o que há nela.
- `cd nome-da-pasta` entra numa pasta que está dentro desta; `cd ..` sobe uma pasta.
- `mkdir nome-da-pasta` cria uma pasta nova.

No macOS e no Linux, `cd ~` volta para a sua pasta pessoal; o PowerShell já abre nela.

## O Claude Code: conta, instalar e entrar

O Claude Code só funciona com uma conta paga: a [página oficial](https://code.claude.com/docs/en/setup#authenticate) lista as contas Pro, Max, Ultra, Team, Enterprise e Console, e diz que o plano gratuito do claude.ai não inclui o Claude Code. Os planos e os preços ficam no site do Claude. Crie a conta lá antes de seguir.

A instalação é um comando colado no terminal. Cada sistema tem o seu:

macOS ou Linux: na [página de instalação](https://code.claude.com/docs/en/setup#install-claude-code), aba “macOS, Linux, WSL”, está a linha do instalador. Ela começa por `curl -fsSL`, termina em `| bash` e leva no meio o endereço do instalador; copie-a inteira dali e cole no terminal. O manual não a repete porque o endereço é do site do Claude e pode mudar.

Windows, no PowerShell:

```
irm https://claude.ai/install.ps1 | iex
```

O comando não mostra progresso enquanto baixa: deixe a janela aberta e espere a mensagem de que o Claude Code foi instalado. Você não precisa de administrador no Windows. Quando acabar, feche o terminal, abra outro e confira:

```
claude --version
```

Aparece um número de versão. Para entrar, digite `claude` e aperte Enter: o programa abre o navegador para você entrar com a sua conta, e o terminal mostra “Login successful” quando termina. Se o navegador não abrir, a tecla `c` copia o endereço de login para você colar.
Fontes: [instalação](https://code.claude.com/docs/en/setup), [guia do terminal para iniciantes](https://code.claude.com/docs/en/terminal-guide) e [login](https://code.claude.com/docs/en/authentication).

## Instalar o git, o Node e o Python

O git guarda o histórico do projeto. O Node traz o `npx`, que o P1 usa. O Python roda os hooks e os testes. Instale os três e confira cada um com `--version`: um número de versão na tela é a prova de que o programa está instalado.

**Git.** A [página de instalação do git](https://git-scm.com/install/) manda para uma página por sistema.

- Windows: baixe o instalador em [git-scm.com/install/windows](https://git-scm.com/install/windows) e aceite as opções padrão, ou rode no PowerShell `winget install --id Git.Git -e --source winget`. A própria página avisa que o pacote do winget não é mantido pelo projeto Git for Windows e pode estar atrás da última versão.
- macOS: `xcode-select --install` instala o git junto com as ferramentas de linha de comando da Apple, ou `brew install git` se você já usa o Homebrew, segundo a [página do macOS](https://git-scm.com/install/mac).
- Linux: `sudo apt-get install git` no Debian e no Ubuntu, `sudo dnf install git` no Fedora, `sudo pacman -S git` no Arch, conforme a [página do Linux](https://git-scm.com/install/linux).

Confira:

```
git --version
```

**Node.** Na [página de download do Node](https://nodejs.org/en/download) escolha a versão marcada como LTS, a recomendada, e o instalador do seu sistema. Confira:

```
node --version
npm --version
```

No Windows, se o PowerShell recusar o `npm` com “running scripts is disabled on this system”, rode uma vez `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`: libera os scripts só para o seu usuário, sem administrador, segundo a [documentação da Microsoft](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-5.1).

**Python 3.** Sirva-se da [página de downloads do Python](https://www.python.org/downloads/).

- Windows: a página de downloads oferece o gerenciador de instalação do Python (também na loja de aplicativos da Microsoft), o caminho que a [documentação do Windows](https://docs.python.org/3/using/windows.html) recomenda. Depois dele existem os comandos `python`, `py` e `pymanager`, e este manual usa o `py`. Confira com `py --version`.
- macOS: baixe o instalador do Python 3 na mesma página e confira com `python3 --version`.
- Linux: a página de downloads do Python não dá pacote pronto para Linux e manda compilar o código-fonte. O autor usa o gerenciador de pacotes da própria distribuição, que é o jeito comum no Linux. Confira com `python3 --version`.

Procure sempre um número que comece por 3. Se aparecer um 2, o programa é velho demais.

## Quando o terminal “não acha” o programa

Depois de instalar, o terminal às vezes responde “comando não encontrado” (no Linux e no macOS, `command not found`) ou “não é reconhecido” (no Windows, `is not recognized`). Quase sempre a causa é uma de duas.

A primeira é que o terminal já estava aberto antes da instalação: ele só enxerga os programas novos depois de fechado e aberto de novo. Feche a janela, abra outra e repita o `--version`.

A segunda é que a pasta onde o programa foi parar não está na lista de lugares que o terminal procura, chamada PATH. Para o Claude Code, o [guia oficial](https://code.claude.com/docs/en/terminal-guide#troubleshooting) dá o conserto:

- macOS (shell Zsh, o padrão): `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc` e depois `source ~/.zshrc`.
- Linux (shell Bash): os mesmos dois comandos, com `~/.bashrc` no lugar de `~/.zshrc`.
- Windows, no PowerShell:

```
$currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
```

Feche o PowerShell e abra outro. No Windows, com o Python há mais um caso, descrito na [documentação do Python](https://docs.python.org/3/using/windows.html): se o `python` abre a loja de aplicativos em vez do Python, ative os apelidos “Python (default)” em “Gerenciar apelidos de execução de aplicativos”; e se o `py` reclama que não abre um arquivo, desinstale o “Python launcher” antigo em Aplicativos instalados.

## A conta no GitHub

O GitHub é o site onde o código fica guardado e onde o Morg-laws mora. Para este manual você só precisa da conta, que serve para a próxima seção e para o P4. Crie-a pela página de cadastro que a documentação indica: a [página oficial](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github) pede um e-mail e a verificação dele, que o GitHub faz por uma mensagem que você recebe.

Depois de criar a conta, a [página do e-mail de commit](https://docs.github.com/en/account-and-profile/how-tos/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address) mostra onde ligar a opção “Keep my email addresses private”: no site, na sua foto, Settings e Emails. Com ela ligada, os commits passam a usar um endereço noreply. Anote esse endereço: é o e-mail da próxima seção e o que o P4 pede.

## Seu nome e e-mail no git

O git escreve o nome e o e-mail de quem fez cada commit. Sem eles, o primeiro commit é recusado. Diga-os uma vez, para todos os projetos desta máquina. Troque o texto entre aspas pelo seu nome e pelo endereço noreply da sua conta no GitHub, mantendo as aspas:

```
git config --global user.name "seu nome"
git config --global user.email "seu endereço noreply"
```

Para conferir, `git config user.name` e `git config user.email` mostram o que ficou. Isso vem do [primeiro uso do git](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup), que explica que o `--global` vale para todos os projetos do seu usuário.

O noreply esconde o seu e-mail pessoal dos commits públicos. No P4, o manual confere esse mesmo endereço e o grava só no repositório do projeto.

## A pasta do projeto, o `git init` e o primeiro commit

O seu projeto é uma pasta como outra qualquer; vira um repositório quando você roda o `git init` dentro dela. Esse comando cria dentro da pasta uma subpasta escondida chamada `.git`, que guarda o histórico, e a [documentação do git](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository) diz que, nesse ponto, nada do projeto está registrado ainda.

Escolha onde a pasta fica, por exemplo na sua pasta pessoal, e crie e entre nela:

```
mkdir meu-projeto
cd meu-projeto
git init
```

Agora o primeiro commit. Um commit é uma fotografia do que você escolheu guardar, com uma mensagem. Faça com um arquivo de teste, na forma que o P19 vai usar: a mensagem num arquivo e o commit por caminho.

No macOS e no Linux:

```
echo "arquivo de teste" > teste.txt
echo "primeiro commit" > msg
git add -- teste.txt
git commit -F msg -- teste.txt
```

No PowerShell:

```
Set-Content teste.txt "arquivo de teste"
Set-Content msg "primeiro commit"
git add -- teste.txt
git commit -F msg -- teste.txt
```

O `-F msg` lê a mensagem do arquivo `msg`, e o `-- teste.txt` diz que o commit leva só aquele arquivo. Confira com:

```
git log --oneline
```

Aparece uma linha com o código curto do commit e a mensagem “primeiro commit”. Se o git responder que não sabe quem você é, volte à seção do nome e do e-mail. O arquivo `msg` fica de fora do commit, de propósito, e pode ser apagado quando quiser. No passo 6 do P3, repita-o com outro arquivo, já com os hooks ligados.

## A cópia do Morg-laws

O P2 e o P3 copiam arquivos do Morg-laws para o seu projeto, então você precisa de uma cópia dele na sua máquina. Em linguagem de git, isso é clonar: o `git clone` baixa o repositório inteiro, com o histórico, numa pasta nova com o nome dele, como diz a [documentação do git](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository).

A cópia fica fora da pasta do projeto, ao lado dela. Para isso, saia do projeto e clone:

```
cd ..
git clone https://github.com/Carlobks/Morg-laws
```

Os comandos são os mesmos nos três sistemas. Agora você tem duas pastas irmãs: `meu-projeto` e `Morg-laws`. Nunca clone dentro do projeto: a cópia viraria uma parte dele, e o git trataria um repositório dentro do outro.

## Abrir o Claude Code na pasta do projeto

O Claude Code trabalha na pasta onde você o abriu: os arquivos que ele cria vão para lá. Por isso abra-o sempre depois de entrar na pasta do projeto:

```
cd meu-projeto
claude
```

Essa pasta é a raiz do projeto, a pasta de nível mais alto, a que tem dentro a `.git` do `git init` e onde ficarão o `AGENTS.md` e o `CLAUDE.md`. Quando o manual diz “na raiz do seu projeto”, é nela que o terminal tem de estar, e o `pwd` confirma. Para sair do Claude Code, digite `exit`, ou aperte `Ctrl + D` duas vezes com a linha vazia. Esses passos estão também no [guia oficial](https://code.claude.com/docs/en/terminal-guide).

## Ver arquivos ocultos

Os nomes que começam por ponto, como `.git`, `.claude` e `.githooks`, são ocultos: os programas não os mostram a menos que você peça. O P1 cria a `.claude/skills/`, e quem não vê arquivos ocultos acha que o comando falhou.

- Windows: no explorador de arquivos, em Windows 11 clique em Exibir, depois em Mostrar, e marque Itens ocultos; em Windows 10, clique em Exibir, Opções, a aba Exibir, e marque “Mostrar arquivos, pastas e unidades ocultos”, segundo a [página da Microsoft](https://support.microsoft.com/en-us/windows/view-hidden-files-and-folders-in-windows-97fbc472-c603-9d90-91d0-1166d1d9f4b5).
- macOS e Linux: no terminal, `ls -a` lista tudo, ocultos incluídos. O autor usa assim no Linux.
- No PowerShell, a mesma lista sai com `ls -Force`.

## Copiar arquivos e editar um arquivo de texto

Copiar é o que o P2 e o P3 pedem o tempo todo. Se estiver no terminal, são comandos:

- macOS e Linux: `cp origem destino` copia um arquivo, e `cp -r origem/. destino` copia o que há dentro de uma pasta.
- PowerShell: `Copy-Item origem -Destination destino` copia um arquivo, e `Copy-Item origem\* -Destination destino -Recurse` copia o que há dentro de uma pasta, como na [documentação do PowerShell](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/copy-item).

Sem o `/.` ou o `\*`, a pasta iria parar dentro do destino que já existe. Um destino novo se cria antes: `mkdir -p destino` (no PowerShell, `mkdir destino`).

Com a pasta do Morg-laws ao lado do projeto, um exemplo, a partir da raiz do projeto, no macOS e no Linux:

```
cp ../Morg-laws/modelos/documentos/AGENTS.md .
```

No PowerShell, o mesmo é `Copy-Item ..\Morg-laws\modelos\documentos\AGENTS.md .`. O `..` é a pasta de cima e o `.` é a pasta onde você está. Se preferir arrastar os arquivos no explorador de arquivos, também serve.

Para editar um arquivo de texto, use um editor de texto simples. No Windows, `notepad .githooks\pre-commit` abre o arquivo no bloco de notas do Windows; no macOS e no Linux, `nano .githooks/pre-commit` abre um editor dentro do próprio terminal, e `Ctrl + O` com Enter salva e `Ctrl + X` sai. Um arquivo que o P3 manda editar, como o `pre-commit`, não tem extensão: abra-o assim, pelo nome. O autor usa o `nano` no Linux e não usou os outros dois nos outros sistemas.

## Quando um comando dá erro

Um erro no terminal é uma mensagem, não uma avaria. Faça nesta ordem:

1. Leia a primeira linha da mensagem inteira. Quase sempre ela diz o que faltou: “comando não encontrado” remete à seção do PATH, e “não é um repositório” (`not a git repository`) quer dizer que você está fora de uma pasta com `.git`, e o `pwd` mostra onde você está.
2. Confira o comando letra por letra, com os espaços. Um traço ou uma aspa fora do lugar é a causa mais comum.
3. Feche o terminal, abra outro e repita o comando uma vez.
4. Não use `sudo` nem “Executar como administrador” só para fazer um erro sumir (os comandos de instalação acima que trazem o `sudo` são a exceção): a página de instalação do Claude Code diz que no Windows não precisa de administrador, e a de instalação por npm manda não usar `sudo`, porque cria problemas de permissão.
5. Se ainda falhar, copie a mensagem inteira, sem cortar, e mostre-a ao Claude Code, dizendo o comando que você rodou e em que pasta estava. A parte `09` trata do que fazer quando o próprio agente erra. Os erros de instalação mais comuns têm conserto no [guia oficial](https://code.claude.com/docs/en/terminal-guide#troubleshooting).
