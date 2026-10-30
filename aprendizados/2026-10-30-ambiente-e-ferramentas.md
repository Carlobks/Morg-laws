# Ambiente e ferramentas

## Windows: heredoc corrompe arquivos

**O que aconteceu:** arquivos escritos com heredoc no PowerShell ou no Git Bash ficaram com caracteres trocados ou quebras de linha erradas.
**Como fazer:** escreva os arquivos com a ferramenta de escrita do agente, e as mensagens de commit num arquivo (`git commit -F msg.txt`).

## Git Bash: colar com Ctrl+V pode estragar o comando

**O que aconteceu:** um comando colado chegou como `^[[200~mv …~` e deu "command not found".
**Por que:** o terminal marca o texto colado ("bracketed paste") e o shell não reconheceu a marca.
**Como fazer:** cole com o botão direito → Paste ou com Shift+Insert, ou digite comandos curtos.

## Edição em massa pode corromper sem avisar

**O que aconteceu:** uma ferramenta que substitui vários trechos de uma vez misturou blocos, porque o mesmo texto aparecia duas vezes no arquivo.
**Como fazer:** cada trecho a substituir tem de ser único no arquivo. Depois de uma edição com aviso, releia as linhas tocadas antes de continuar.

## Turbopack e bibliotecas de ícones

**O que aconteceu:** alguns ícones de uma biblioteca grande derrubaram páginas em produção com o Turbopack, sem erro no `tsc` nem no lint.
**Como fazer:** prefira ícones que o projeto já usa. Ícone novo só depois de um build que o prove. A lista de ícones problemáticos depende da versão: anote a versão quando registrar um.
**Versão:** observado em 2026, com Next.js 15/16 e Turbopack. *A confirmar a cada atualização.*

## Uma regra de lint desligada esconde os erros novos

**O que aconteceu:** uma regra desligada no projeto inteiro (por exemplo, `react-hooks/exhaustive-deps`) para calar o passivo antigo deixou passar omissões novas, não deliberadas.
**Como fazer:** rode a regra sozinha no arquivo que tocou:
```bash
npx eslint <arquivo> --rule '{"react-hooks/exhaustive-deps":"error"}'
```

## Verificar skills e hooks pelos registros reais

Um teste sintético ("finjo que sou o agente") engana. Para saber se uma skill acionou ou se um hook correu, leia os registros reais das sessões. Atenção ao fuso: os horários costumam estar em UTC.
