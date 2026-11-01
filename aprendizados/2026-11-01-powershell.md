# PowerShell 5.1 (Windows)

## `Set-Content` e `Out-File` gravam com BOM ou em ANSI

**O que aconteceu:** um JSON gravado pelo instalador foi recusado pelo programa que o lia, e acentos de um `.ps1` saíram trocados.
**Por que:** no 5.1, `Set-Content` grava na página de código local (ANSI) e `Out-File` em UTF-8 **com** BOM; muitos leitores de JSON recusam o BOM. Ao contrário, um `.ps1` sem BOM é lido como ANSI.
**Como fazer:** grave com `[IO.File]::WriteAllText($caminho, $texto, (New-Object Text.UTF8Encoding $false))`. Os `.ps1` com acentos levam BOM; JSON, YAML e HTML não. Um teste pode conferir as duas coisas.
**Versão:** Windows PowerShell 5.1 (o PowerShell 7 grava UTF-8 sem BOM por omissão).

## Um programa que escreve no stderr vira exceção

**O que aconteceu:** com `$ErrorActionPreference = 'Stop'`, um programa que só avisava no stderr derrubou o script.
**Por que:** no 5.1, cada linha do stderr de um programa nativo vira um `ErrorRecord`.
**Como fazer:** `try { & programa … 2>$null } catch {}` e decida pelo `$LASTEXITCODE`.

## Num array, a vírgula liga antes do `+`

**O que aconteceu:** um script de substituições em massa desalinhou os pares "procura/troca" e trocou cada quebra de linha de um HTML por uma frase. O arquivo foi publicado numa linha só, com 65 000 caracteres.
**Por que:** em `@('a', 'b' + "`n" + 'c')`, a vírgula é avaliada antes do `+`, e os elementos não são os que parecem.
**Como fazer:** ponha cada valor composto entre parênteses, ou faça as trocas em Python com `assert` do número exato de ocorrências. Um teste que falha com linhas gigantes ou sem quebras apanha o resto.

## A crase é caractere de escape nas aspas duplas

**O que aconteceu:** três documentos em Markdown escritos por um here-string `@"…"@` perderam todas as crases.
**Por que:** dentro de `"…"`, `` `n`` vira quebra de linha, `` `a``, `` `v`` e `` `0`` viram caracteres invisíveis, e as outras crases somem.
**Como fazer:** escreva arquivos com a ferramenta de escrita do agente ou com aspas simples (`@'…'@`). Um teste pode recusar caracteres de controle nos arquivos de texto.

## As variáveis não distinguem maiúsculas

**O que aconteceu:** num teste, a variável `$bat` era o parâmetro `$Bat` do script testado, que via um valor que ninguém passou.
**Como fazer:** nos testes, use nomes que não colidam com os parâmetros e variáveis do script (`$arquivoBat`).

## `& $programa` que não existe não muda o `$LASTEXITCODE`

**O que aconteceu:** com o caminho do Python errado, cada passo dava `CommandNotFoundException`, o `$LASTEXITCODE` ficava com o valor anterior e o script de testes terminava com "OK: todos os testes passaram".
**Como fazer:** antes de contar com o `$LASTEXITCODE`, confirme o programa (`Get-Command $programa -ErrorAction SilentlyContinue`) e saia com 1 se não existir. Um teste roda o script com o caminho errado e exige a falha.

## `$USERPROFILE` (sintaxe do Bash) vem vazio

**O que aconteceu:** um comando dado ao dono com `$USERPROFILE` virou o caminho `/.glzr/...` no PowerShell, e o `pyw.exe` (sem console) saiu sem mostrar nada: parecia que a funcionalidade não funcionava.
**Como fazer:** comandos para o dono vão na sintaxe do terminal dele (`$env:USERPROFILE`, `& <exe>`). Para diagnosticar, rode com `py.exe`, que mostra os erros, em vez do `pyw.exe`.
