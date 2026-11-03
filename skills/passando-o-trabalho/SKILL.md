---
name: passando-o-trabalho
description: Guarda o trabalho em curso num handoff por assunto (.context/HANDOFF-<assunto>.md) antes de compactar a conversa ou de parar, commita só esse arquivo, entrega o /compact pronto para o Claude Code ou para o Codex e conduz a retomada depois. O handoff leva o estado conferido no git, as decisões, o que já falhou e não se repete, e os próximos passos. Usar quando a conversa está longa e vai ser compactada, quando a dúvida é compactar ou abrir uma sessão nova porque a conversa cresceu, quando o trabalho para e continua em outra sessão ou em outro dia, ou ao retomar depois de compactar («lê o handoff»). Não usar para dividir trabalho entre sessões nem pedir uma auditoria independente (é a orquestrando-sessoes), nem para commits, mensagens ou push do dia a dia (é a git-e-commits), nem para resumir documentos ou escrever changelog.
---

# Passando o trabalho

O resumo de uma compactação é escrito pelo próprio modelo, com a janela cheia, e perde o que mais faz falta para
continuar: caminhos, nomes, erros literais e o que já se tentou sem sucesso. Sem essa lista, o agente volta a propor
o que já se descartou (livro *Competente o Suficiente*, pp. 30–32). Esta skill põe esse estado num arquivo
no git **antes** de compactar ou de parar, e o resumo só precisa de apontar para ele.

O essencial, se esta skill chegar cortada depois de uma compactação:

1. Conferir o estado no git, sem despejar diffs na conversa.
2. Gravar `.context/HANDOFF-<assunto>.md` com Objetivo, Estado verificado, Decisões, Descartado e Próximos passos.
3. Commitar **só** esse arquivo, pelo caminho, com os hooks do projeto. Pasta ignorada: ver a seção 3.
4. Entregar o comando de compactação e a mensagem de retomada.
5. Ao retomar: ler o handoff inteiro, comparar com o `git status -s`, reler o «Descartado», seguir o passo 1.

## 1. Conferir o estado, em silêncio

Na raiz do repositório:

```
git rev-parse --show-toplevel
git status -s
git diff --stat
git diff --cached --stat
```

- Use a saída só para preencher o handoff. Não a cole na conversa nem rode o `git diff` completo: o objetivo é
  poupar a janela.
- **Testes:** o resultado da última execução real que aparece na conversa, com a mensagem de erro literal. Nada
  rodado: «não executado nesta sessão». Não rode a suíte inteira só para o handoff.
- **Sem git:** grave o handoff em `.context/` da pasta atual (crie a pasta se ela não existir), escreva «sem git» no
  estado e marque cada arquivo citado como **não verificado**. Pule a seção 3 e diga na resposta que o handoff ficou
  só no disco.

## 2. Gravar o handoff

**Um arquivo por assunto:** `.context/HANDOFF-<assunto>.md`, com um assunto curto, em minúsculas e com hífens, que
se reconheça daqui a uma semana. Nunca um `HANDOFF.md` genérico: com outra sessão na mesma pasta, ele é
sobrescrito e apaga o estado da outra. Sem datas nem ids de sessão no nome, e nada fora de `.context/`.

- Antes de gravar, liste `.context/HANDOFF-*.md`. O do **mesmo assunto** se atualiza; nos **dos outros** não se toca.
- **Leia o anterior antes de reescrever.** Reescreva o arquivo inteiro, mas leve para a versão nova as decisões e o
  «Descartado» que continuam válidos. Perder essa lista é o que faz o agente repetir o que já falhou. Um anterior
  com títulos antigos passa aos novos (seção 5).

**O formato.** Os títulos são estes, nesta ordem (o teste `test_docs_indices.py` dos modelos os confere); o molde
está em `modelos/documentos/handoff.md`.

| Título | O que leva |
|---|---|
| `## Objetivo` | O objetivo principal numa linha, o passo exato em curso e onde está o plano. |
| `## Estado verificado (<data>, ramo <ramo>)` | Os commits com o hash curto entre crases (o teste confere que existem). Uma tabela por arquivo: caminho, status do `git status -s` e o que mudou (funções, linhas). Os testes: o comando e o resultado, com o erro literal num bloco de código. |
| `## Decisões e porquê` | As do dono (perguntadas, com a recomendação) e as técnicas (com o motivo medido). |
| `## Descartado` | O «não repetir»: o que se tentou → o que aconteceu, com o erro → porque se largou. |
| `## Próximos passos` | De 1 a 3 passos, cada um executável sem perguntar: arquivo, função, comando. |

Regras do conteúdo:

- **O literal vence a paráfrase:** caminhos, nomes, números de linha e erros exatamente como são.
- **O verificado fica separado do suposto:** o que veio do git ou de uma execução real é verificado; o que veio só da
  conversa leva «(não verificado)».
- **Nada de segredos nem dados pessoais:** chaves, tokens, senhas e strings de conexão viram `<REDIGIDO>`.
- **Curto:** menos de 150 linhas. Seção vazia leva «nenhum» e não some.
- Um hash entre crases tem de ser de um commit que existe. O commit do próprio handoff não é citado nele.

## 3. Commitar o handoff, sozinho

O handoff vai para o git **a cada compactação**, antes do `/compact`, **e no fecho de cada fase**. Assim, quem
retoma em outra máquina ou em outra sessão o encontra, e o histórico mostra como o estado mudou.

```
git check-ignore -q .context/HANDOFF-<assunto>.md   # sai com 0 se o arquivo estiver ignorado
git add -- .context/HANDOFF-<assunto>.md
git commit -F <arquivo-da-mensagem> -- .context/HANDOFF-<assunto>.md
```

- Pelo caminho, sempre: um `git commit` sem caminho leva o que outra sessão deixou preparado. O `git add` é preciso
  porque o git recusa um commit por caminho de um arquivo que ainda não conhece.
- Os hooks do projeto rodam. Hook recusou: a causa é corrigida, e o hook nunca é pulado.
- **`.context/` ignorado:** o handoff é gravado mesmo assim. Nunca mexa no `.gitignore` nem force o `git add`. O
  resto depende de haver um motivo escrito:
  - **Com motivo:** um comentário no `.gitignore` ou um arquivo de decisão do projeto explica por que a pasta está
    ignorada. Um projeto pode ignorá-la, por exemplo, porque uma ferramenta lê tudo o que o git não ignora e um
    handoff a quebra. Não pergunte nada: o handoff fica só no disco, e a resposta diz isso numa linha.
  - **Sem motivo:** procure a resposta nas «Decisões e porquê» dos `HANDOFF-*.md` da pasta e, se ela estiver lá,
    siga-a. Se não estiver, pergunte ao dono se tira a pasta do `.gitignore`, uma única vez por projeto, e registe a
    resposta nas Decisões deste handoff. Com um «não», o handoff fica só no disco, e a resposta diz isso.

## 4. Compactar

**Compactar ou abrir uma sessão nova?** Quando a conversa cresceu, a pergunta é desta skill. Para continuar o mesmo
trabalho, compacte com o handoff. Para um trabalho sem relação com este, grave o handoff e abra uma sessão nova: ela
não precisa do histórico desta. Dividir o trabalho em várias sessões é da skill `orquestrando-sessoes`.

**Quando:** a prática do autor do Morg-laws é compactar à mão por volta de **50% da janela**, com instruções, em vez
de esperar pela automática no limite. **O número é dele**, escolhido para uso próprio: nem o livro abaixo nem a
documentação oficial recomendam uma percentagem. O porquê de compactar cedo vem do livro *Competente o Suficiente*: a janela
cheia custa dinheiro, porque é relida a cada mensagem, custa tempo e torna mais difícil achar o que importa (p. 31); a
atenção cai à medida que ela enche (p. 124); e uma sessão longa fica cheia de tentativas antigas (p. 411). No Claude
Code, o `/context` mostra o que ocupa a janela.

**A língua:** o comando de compactação e a mensagem de retomada escrevem-se na língua do usuário, a mesma em que ele
escreve na conversa. Os blocos abaixo estão em português do Brasil só como modelo do conteúdo.

**Claude Code:** o `/compact` aceita instruções de foco. Entregue-o numa linha só, com os colchetes preenchidos:

```text
/compact Guarde: 1) objetivo: [uma linha]; 2) arquivos ativos: [lista]; 3) não repetir: [o essencial do Descartado]; 4) erro atual: [literal, ou "nenhum"]. Deixe de fora saídas brutas de ferramentas e leituras antigas. No próximo turno, leia primeiro .context/HANDOFF-<assunto>.md.
```

E, depois dele, a mensagem para mandar quando a compactação terminar (o primeiro pedido da conversa nova):

```text
A conversa acabou de ser compactada. O estado está em .context/HANDOFF-<assunto>.md; os outros HANDOFF-*.md dessa pasta são de outros assuntos e não se tocam. Leia esse arquivo inteiro, rode git status -s e diga o que mudou em relação à tabela, releia o «Descartado» e não proponha nada dele. Diga numa frase onde estávamos e siga o passo 1 dos próximos passos ([resumo do passo]). Se ele pedir uma decisão minha, pergunte antes.
```

**Codex:** a documentação mostra o `/compact` sem argumentos, com uma confirmação antes de resumir. Como não há onde
pôr as instruções, elas vão na mensagem de retomada. Diga para rodar o `/compact` primeiro e entregue, num bloco só,
para colar logo depois:

```text
A conversa acabou de ser compactada. Objetivo: [uma linha]. Arquivos ativos: [lista]. Não repetir: [o essencial do Descartado]. Erro atual: [literal, ou "nenhum"]. O estado completo está em .context/HANDOFF-<assunto>.md; os outros HANDOFF-*.md dessa pasta são de outros assuntos e não se tocam. Leia esse arquivo inteiro, rode git status -s e diga o que mudou em relação à tabela, releia o «Descartado» e não proponha nada dele. Diga numa frase onde estávamos e siga o passo 1 dos próximos passos ([resumo do passo]). Se ele pedir uma decisão minha, pergunte antes.
```

Nos dois, o comando sai no fim da resposta, depois de uma linha com o caminho do handoff e o hash do commit (ou «só no
disco», se a pasta estiver ignorada).

## 5. Retomar

Quando o pedido ou o resumo mandar ler o handoff:

1. Leia-o inteiro. Sem caminho no pedido, liste `.context/HANDOFF-*.md`: um só, leia esse; vários, leia o do assunto
   da conversa, e se não estiver claro, pergunte qual.
2. Rode `git status -s` e `git log --oneline -5` e compare com o «Estado verificado». Se divergir, diga o quê antes
   de agir: outra sessão pode ter mexido.
3. Releia o «Descartado». Só se volta a uma dessas abordagens com um fato novo, e dizendo qual.
4. Siga o passo 1 dos «Próximos passos».

**Títulos antigos.** Um handoff gravado com outro molde pode trazer `## Estado do código (…)` e
`## Abordagens descartadas (…)`: valem como «Estado verificado» e «Descartado». A gravação seguinte usa os títulos
novos e leva o conteúdo. Até lá, o `test_docs_indices.py`, se o projeto o tiver, acusa a falta dessas duas seções.

No Claude Code, o handoff pode voltar sozinho depois de compactar (voltam até cinco arquivos lidos ou editados, e só
os pequenos inteiros), mas não conte com isso: leia-o.

## Fontes

Ver `FONTES.md`, seção «Compactação da conversa», e `pesquisas/2026-11-02-compactacao-claude-code-e-codex.md`: a
documentação do Claude Code (o `/compact`, a compactação automática e por inatividade, o que volta depois) e a do
Codex (o `/compact` e as skills); a especificação Agent Skills; o livro *Competente o Suficiente*, de Fabio Akita
(pp. 30–32, 124 e 411). O formato do handoff, o commit a cada compactação e os 50% são prática do autor do
Morg-laws.
