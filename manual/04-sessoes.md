# Sessões

Uma sessão é uma conversa com o agente, com a memória do que ficou dito nela. Esta parte diz quando continuar uma conversa, quando compactá-la e quando abrir uma sessão nova; como pedir o trabalho a uma sessão filha; qual modelo pôr em cada uma; e como dar nome às sessões para você não se perder.

## P10 · Continuar, compactar ou abrir uma sessão nova

### Na prática

Quando a conversa cresceu, escolha por esta tabela:

| Situação | O que fazer |
|---|---|
| Mesmo trabalho, conversa já longa | Compacte, com o handoff gravado antes |
| Trabalho sem relação com o anterior | Grave o handoff e abra uma sessão nova |
| Pausa de mais de uma hora, ou fim do dia | Grave o handoff e, ao voltar, abra uma sessão nova que o lê |

O handoff é um arquivo com o estado do trabalho, as decisões e o que já falhou (P16). Compactar é pedir ao agente que troque a conversa antiga por um resumo; no Claude Code, o `/compact` aceita instruções do que guardar.

Compacte cedo: por volta de 150 mil tokens, sem esperar pela compactação automática, que só dispara perto do limite do modelo. No Claude Code, o `/context` mostra quanto da janela está ocupado.

Um exemplo. Uma orquestradora (a sessão que só escreve pedidos e decide, P14) conduz um trabalho em fases. Ela não continua a mesma conversa:

```
Cada passo (plano, implementação, auditoria, correção) vai para uma sessão nova, com um pedido escrito.
Em cada troca de fase: handoff gravado, depois compactar.
No fim do dia, ou numa pausa longa: handoff gravado e sessão nova no dia seguinte.
```

O que costuma dar errado:

- Esperar pela compactação automática e perder o combinado do começo da conversa.
- Compactar sem gravar o handoff: o resumo é escrito pelo próprio agente, com a janela cheia.
- Deixar uma sessão aberta durante dias: ela junta assuntos, e cada pedido relê todos.

### Por quê e fonte

Cada mensagem manda a conversa inteira de volta, e uma conversa longa fica cara, lenta e menos atenta. O resumo da compactação perde o detalhe, e o agente volta a propor o que você já descartou. Por isso o combinado fica em arquivo, e não só na conversa (livro *Competente o Suficiente*, de Fabio Akita, pp. 30–32, 39, 411). O livro não dá um limiar de tokens.

As vozes da cabeça de Carlobks (decisão de 2026-11-06): compactar cedo. Porquê: numa medição do trabalho antes das regras, reler o contexto foi a maior parte do custo, 64% ([medições do uso](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-05-linha-de-base-do-uso.md)). O número diz que reler pesa, não em que ponto compactar.

Outra decisão de Carlobks (2026-11-06): o número é por volta de 150 mil tokens. Porquê: nas palavras dele, arrumadas, testou o plano Pro e o Max 5x; no Pro a janela é menor e ele compactava mais vezes; foi sentindo que 150 mil a 200 mil tokens era o máximo que queria usar. Muitas vezes compacta antes, quando a tarefa ou o tempo deixam, porque quanto menos distração na janela, mais atenção o modelo dá ao que ele quer. É a prática de uma pessoa, e não um limite da ferramenta.

Os comandos estão na [documentação do Claude Code](https://code.claude.com/docs/en/commands): `/compact`, que aceita instruções de foco, e `/context`, que mostra o que ocupa a janela.

Onde vive no Morg-laws: a skill `passando-o-trabalho`, com a pergunta “compactar ou sessão nova?” e o comando pronto.

## P11 · Abrir uma sessão filha

### Na prática

Uma sessão filha é uma sessão nova que recebe um pedido escrito e devolve um resultado. Você a abre à mão, como qualquer sessão nova, e cola o pedido. E a vê trabalhar: pode lê-la e corrigi-la no meio do trabalho.

O pedido leva o objetivo, os arquivos, o que já se descartou, como se prova e o modelo (P12). Um pedido de implementação, assim:

```
Título: ATIVO | ÁREA · implementação do passo 3
Modelo: o médio (Sonnet)

Implemente o passo 3 do plano. Você trabalha na pasta tal, em commits locais, sem push.
Antes de começar, confira que a árvore está limpa e que o último commit é o combinado.

Leia primeiro, e só isto: o plano (as seções 3 e 5), as regras do projeto e os testes que não podem quebrar.
O que se faz é o que o plano manda, e mais nada. Se algo não bater, não improvise: registre um desvio.

Em cada commit: adicione só os caminhos dele, rode os portões, commite por caminho.
Está proibido: ler segredos, escrever no banco, lançar sub-agentes, fazer push.
O relatório vai para tal arquivo: commits, a prova de cada passo, desvios e o que não se verificou.
Quando acabar, troque o título para OK, ou me peça, com o título pronto (P13), e avise num parágrafo.
```

O que costuma dar errado:

- Deixar o que não se faz de fora. A filha faz a mais.
- Pedir uma auditoria dizendo a sua conclusão. Ela tende a confirmá-la (a fonte está no P15).
- Esquecer o que já falhou: a filha repete.

### Por quê e fonte

A filha nasce com o contexto limpo: só o que o pedido diz. Por isso o pedido carrega tudo, e o relatório volta como dado, que você confere, e não como verdade. Quem escreveu um trabalho não o audita bem: para uma leitura independente, abra uma sessão sem a conversa que o produziu, com um pedido neutro, sem a sua conclusão.

Prefira sessões novas a sub-agentes quando você quer ver e corrigir cada passo: um sub-agente não pode ser visto nem corrigido, e o erro volta no mesmo tom confiante dos acertos. Sub-agentes servem para buscas amplas e tarefas independentes, com o resultado conferido depois. Um agente gasta cerca de 4 vezes os tokens de uma conversa, e um sistema com vários agentes cerca de 15 vezes; só compensa quando a tarefa vale esse custo, e o conselho é começar pelo mais simples. O custo vale também para as sessões filhas, que com a orquestradora são um sistema de vários agentes: o que as separa dos sub-agentes é poder vê-las e corrigi-las, não o preço (dois artigos da Anthropic sobre agentes, com a data de leitura, na [seção “Uso e custo de agentes” do `FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#uso-e-custo-de-agentes)).

O livro de Fabio Akita recomenda a orquestra de agentes só para lotes independentes (pp. 49, 153–155, 210).

Onde vive no Morg-laws: a skill `orquestrando-sessoes`, seções “Sub-agentes ou sessões novas” e “Leitura independente”. O exemplo acima é o esqueleto de um pedido de implementação real, reescrito sem nomes, caminhos nem números.

## P12 · O modelo da filha

### Na prática

Escolha o modelo ao abrir a filha, pelo tamanho da tarefa:

| Tarefa da filha | Modelo |
|---|---|
| Buscas, contagens, leituras mecânicas, revisão de texto | O pequeno (Haiku) |
| Implementar um plano aprovado, escrever testes, aplicar as correções de uma auditoria | O médio (Sonnet) |
| Escrever um plano, auditar a frio, segurança, bug difícil | O maior (Opus) |

Os nomes entre parênteses são os do Claude Code. Em outra ferramenta, use o modelo do mesmo tamanho.

Ponha o modelo no pedido, ao abrir a filha, e não no `settings.json` do Claude Code: um `model` fixo ali valeria para todas as sessões.

O que costuma dar errado:

- Deixar o modelo padrão e descobrir tarde que a auditoria saiu num modelo pequeno.
- Usar o maior em tudo. O trabalho de rotina sai mais barato no médio.
- Fixar o modelo no `settings.json` e esquecer que ele vale para todas.

### Por quê e fonte

Um modelo mais barato pode baixar a qualidade, e é a auditoria e o plano que mais pagam por isso. O guia de boas práticas do Claude Code diz que o Sonnet custa menos no trabalho de rotina e que o Haiku serve para sub-agentes de tarefas simples ([boas práticas](https://code.claude.com/docs/en/best-practices)). O livro de Fabio Akita manda escolher o modelo pelo preço, pelo tempo e pela ferramenta, e testar a combinação (pp. 45, 155, 159–161, 311–312).

Mais uma decisão de Carlobks (2026-11-06): a auditoria a frio fica no maior modelo. Porquê: a skill diz que um modelo mais barato pode baixar a qualidade, e por isso o plano e a auditoria ficam no maior ([`orquestrando-sessoes`](https://github.com/Carlobks/Morg-laws/blob/main/skills/orquestrando-sessoes/SKILL.md)). Uma segunda auditoria, em outro modelo ou em outra ferramenta, continua a valer.

Onde vive no Morg-laws: a seção “A orquestradora magra e diária” da skill `orquestrando-sessoes`, que traz esta tabela.

## P13 · O nome da sessão

### Na prática

Dê a cada sessão um título que diga o estado dela:

```
ESTADO | ÁREA · assunto
```

Os quatro estados:

- `ATIVO`: trabalhando.
- `ESPERA`: esperando você ou outra sessão.
- `OK`: terminou, e tudo está commitado na branch principal.
- `OFF`: parada de propósito.

A área vai em maiúsculas e o assunto em poucas palavras. Cada sessão troca o próprio título quando muda de estado. Quatro exemplos, dois reais e dois inventados (o segundo e o quarto), no mesmo molde:

```
ATIVO | MORG-LAWS · plano do manual de uso
ESPERA | MORG-LAWS · pergunta sobre o formato (exemplo)
OK | MORG-LAWS · revisão da parte 02 do manual
OFF | MORG-LAWS · ideia guardada para depois (exemplo)
```

Como renomear:

- Na app de desktop do Claude Code: clique no título da sessão, ou peça ao agente, que tem essa ação lá.
- No terminal, no Claude Code e no Codex ([comandos do Codex](https://developers.openai.com/codex/cli/slash-commands)): `/rename <título>`, que você digita. O agente pede a você, com o título pronto.
- Na extensão e na app do Codex, a documentação não diz como: o agente escreve o título no topo da primeira resposta.

O que costuma dar errado:

- Esquecer de trocar o título ao mudar de estado.
- Um assunto longo demais: o título passa a não caber na lista.

### Por quê e fonte

Com muitas sessões abertas você se perde. O título diz, de relance, quais esperam por você e quais terminaram.

Uma decisão de Carlobks (2026-11-08): o título `ESTADO | ÁREA · assunto`. Porquê: nas palavras dele, arrumadas, tinha 70 sessões abertas e se perdia naquela imensidão; o título foi um jeito de se organizar. Criou também pastas para as sessões. Assim sabe no que está trabalhando no momento.

O `/rename` está na [documentação de comandos do Claude Code](https://code.claude.com/docs/en/commands): muda o nome da sessão e o mostra na barra do prompt; sem nome, gera um a partir da conversa. O nome tem no máximo 200 caracteres, e um comando só é reconhecido no começo da sua mensagem: quem o digita é você. Na app de desktop, clicar no título ou pedir ao agente vem da [documentação da app de desktop](https://code.claude.com/docs/en/desktop); o `/rename` do Codex, dos [comandos do Codex](https://developers.openai.com/codex/cli/slash-commands), que não dizem como se faz na extensão nem na app.

Onde vive no Morg-laws: a seção “Várias sessões na mesma pasta” da skill `orquestrando-sessoes`, que traz os quatro estados e a forma de renomear em cada ferramenta.

## P14 · A orquestradora magra e diária

### Na prática

Num trabalho com várias fases, uma sessão só orquestra. Ela escreve o pedido de cada filha (P11), recebe o resultado e decide o passo seguinte. Não lê código, não implementa e não audita: isso fica nas filhas.

Como ela se mantém magra:

- Lê só o veredito: o topo do relatório, a lista do que ficou por verificar e o resultado da conferência. Não lê o relatório inteiro nem os diffs.
- Pede que a filha avise no fim da fase, numa mensagem curta: o veredito, o commit e o que ficou por fazer. Um aviso no meio acorda a orquestradora sem decisão para tomar (na app de desktop do Claude Code).
- Ela se renova todo dia: no fim do dia grava o handoff (P16) e fecha; no dia seguinte, uma orquestradora nova o lê.

Um exemplo, o papel de uma orquestradora real, reescrito:

```
Papel: escrever os pedidos das filhas, receber os resultados, conferir no git os hashes, os testes
e o veredito de cada um (sem ler os diffs), levar as decisões ao dono e registrá-las.
Mais ninguém as registra.
Não faz: implementar, auditar, lançar sub-agentes.
Cada fase vai para uma sessão nova, com o modelo escolhido na hora: o maior para plano, auditoria
e conferência; o médio para implementar e corrigir.
Quando uma filha acaba, chega um aviso curto. Em cada troca de fase: handoff gravado, depois compactar.
```

O que costuma dar errado:

- A orquestradora começa a implementar “só uma correção pequena” e a conversa dela enche.
- Ela lê todos os relatórios inteiros e perde o fio das decisões.
- Fica viva por vários dias, e cada aviso sai mais caro que o anterior.

### Por quê e fonte

Na app de desktop do Claude Code, cada aviso de uma filha acorda a orquestradora, e cada vez que ela acorda relê o contexto inteiro. Quanto mais viva, mais cada aviso custa. Por isso ela encaminha e decide, e o trabalho pesado fica em sessões que nascem limpas e morrem no fim da fase. O livro de Fabio Akita recomenda a orquestra de agentes só para lotes independentes, porque ela custa mais tokens e mais coordenação (pp. 49, 153–155, 210).

Onde vive no Morg-laws: a seção “A orquestradora magra e diária” da skill `orquestrando-sessoes` ([`SKILL.md`](https://github.com/Carlobks/Morg-laws/blob/main/skills/orquestrando-sessoes/SKILL.md)), que traz a tabela do modelo da filha (P12). O custo de cada aviso vem das [boas práticas do Claude Code](https://code.claude.com/docs/en/best-practices): cada pedido manda a conversa inteira de volta.

## P15 · Auditoria a frio e conferência

### Na prática

Quem escreveu um trabalho não o audita bem: lê o que quis dizer, e não o que escreveu. Por isso a auditoria é uma sessão nova, sem a conversa que o produziu, e a conferência é outra sessão.

1. Abra uma sessão nova, no maior modelo (P12), com um pedido neutro: o objetivo, os arquivos, as fontes contra as quais conferir e o formato do relatório. Não diga a sua conclusão.
2. Peça um veredito no topo (“aprovado”, “aprovado com correções”, “refazer”), cada achado com o arquivo e a linha da fonte, e a lista do que não se verificou.
3. Antes de o achado chegar a você, abra outra sessão, só de conferência: ela confere cada afirmação na fonte, com um `grep` por termo.
4. Aplique a correção que a conferência afina, e não a que a auditoria propôs, quando elas divergirem.

Um exemplo, reescrito. O achado: a verificação que procura frases de prova acusava demais e de menos, porque o `grep` casava “à medida que” e deixava passar outros verbos de prova. A correção da auditoria reprovava toda frase com a palavra “regra” e um desses verbos. A conferência viu o defeito:

```
Essa correção reprova a própria ressalva que o texto precisa escrever:
“nenhum texto diz que as regras foram medidas”.
Correção afinada: a frase passa se tiver “não”, “nunca” ou “nenhum” antes do verbo.
Dois casos de teste: a ressalva passa; a afirmação seca reprova.
```

O que costuma dar errado:

- Passar ao auditor a sua hipótese: ele tende a confirmá-la.
- Levar o relatório a você sem a conferência, e descobrir o erro depois.
- Tratar o relatório como verdade, e não como dado.

### Por quê e fonte

O relatório de uma auditoria volta no mesmo tom confiante, acerte ou erre. Só uma leitura que parte da fonte separa um do outro, e o exemplo mostra o caso em que a correção proposta tinha um defeito que só a conferência viu. O livro de Fabio Akita mostra que, sem a fonte, o agente pode inventar um motivo plausível para uma decisão antiga (p. 32) e lembra que a explicação dele sobre como verificou não é prova (p. 357). Mais de um revisor, com modelos diferentes, também vem do livro (pp. 49, 156). Que o modelo tende a concordar com quem pede vem de uma [pesquisa sobre bajulação](https://arxiv.org/abs/2310.13548) em assistentes de IA: as respostas acompanham a crença de quem pergunta, mesmo quando ela não é a verdadeira.

Mais uma decisão de Carlobks (2026-11-06): a conferência vem antes de o achado chegar a ele. Porquê: nas palavras dele, arrumadas, foi experimentando: começou a pedir a conferência antes de o trabalho chegar a ele e sempre achava algum erro; então passou a pedir sempre, porque prefere receber o trabalho bem feito, com uma confirmação. Foi aprendendo a não confiar cegamente.

Onde vive no Morg-laws: as seções “Leitura independente” e “A orquestradora magra e diária” da skill `orquestrando-sessoes`.

## P16 · Passar o trabalho (handoff)

### Na prática

O handoff é o arquivo que a próxima sessão lê para continuar o trabalho. Grave-o antes de compactar e antes de parar, em `.context/HANDOFF-<assunto>.md`, um por assunto, e commite só esse arquivo, pelo caminho (P19, na parte 05). Na retomada, o agente o lê inteiro, roda `git status -s` e confere com o que o arquivo diz.

O molde `modelos/documentos/handoff.md` tem seis seções: objetivo, estado verificado, decisões e porquê, descartado, próximos passos e cuidados. Preenchido com um passo deste manual (a máquina em Python, a primeira subfase), ele fica assim:

```
# Handoff: manual-de-uso

## Objetivo
- Principal: escrever o manual de uso em Markdown e gerar o PDF.
- Passo em curso: a máquina em Python acabou; falta o molde do Typst.

## Estado verificado (2026-11-09, ramo `main`)
| Fase | Commits | O que ficou |
| Pesquisa | 1 | páginas duplas e as fontes |
| Verificador | 1 | as verificações do manual e os testes |
| Detector | 1 | detector de dados e `pre-commit` |
Testes: `sh scripts/testar.sh` passa, 501 testes, cobertura de 100%.

## Decisões e porquê
- O teto em palavras, e não em linhas: a linha muda com a largura.

## Descartado
- Contar o “medido” só por `grep` → casa “à medida que” → virou um detector com a ressalva.

## Próximos passos
1. Escrever o molde do Typst e provar com um par.

Cuidados: nenhum.
```

O que costuma dar errado:

- Confiar no arquivo sem conferir o git: o estado pode ter mudado.
- Esquecer o “Descartado”: a sessão nova propõe de novo o que já falhou.
- Deixar o handoff só no disco, sem commit.

### Por quê e fonte

Compactar troca a conversa por um resumo, e o resumo perde o motivo das decisões antigas. O que importa precisa estar em arquivo, no git, para a sessão seguinte começar do estado real. O livro de Fabio Akita diz que a decisão importante não fica só na conversa (pp. 32–33, 36), que o agente não aprende com a sessão e o que não se guarda evapora (pp. 319, 323), e que cada sessão precisa da própria passagem de turno (p. 387).

O formato do handoff, o commit a cada compactação e a sessão por assunto são prática do autor, e os problemas que os motivaram estão registrados na [linha de base do uso](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-05-linha-de-base-do-uso.md).

Onde vive no Morg-laws: a skill `passando-o-trabalho`, com o comando de compactação e a mensagem de retomada prontos, e o molde `modelos/documentos/handoff.md`.

## P17 · Várias sessões na mesma pasta

### Na prática

Quando duas sessões (ou duas pessoas) trabalham na mesma pasta, o índice do git e a branch são de todas. Cada uma cuida do que é seu:

- Commite sempre por caminho: `git commit -F msg -- <arquivos>`. Um `git commit` sem caminhos leva tudo o que outra sessão deixou preparado.
- Nunca use `git stash`: ele tira do disco também o que as outras sessões mudaram nos arquivos que o git já acompanha.
- Não commite trabalho alheio. O aviso de arquivos por commitar conta arquivos, e não donos: use `git log -1 -- <arquivo>` e a memória do que você mexeu.
- Confirme o `HEAD` antes de pedir um reteste: outra sessão pode ter mudado a branch.
- Um script que troca arquivos por um tempo roda num `git worktree` à parte.
- Se existir um `.git/index.lock`, não o apague: o de outra sessão sai sozinho; o seu, deixado por um comando interrompido, você renomeia depois de provar que é velho.

Um caso real: um commit de outra sessão levou o seu arquivo.

```
Não reescreva o histórico compartilhado.
Faça um commit novo com a versão certa e avise.
```

O que costuma dar errado:

- Rodar `git add .` e commitar o que era de outra sessão.
- Comparar com o código antigo usando `git stash`.
- Um teste de mutação rodando na pasta compartilhada: outra sessão vê falhas sem bug.

### Por quê e fonte

O índice do git é um só, e o `git commit` sem caminhos grava tudo o que está preparado, de quem for. O `git stash` esconde também o trabalho de quem não o pediu. Reescrever um histórico que outros já têm muda os hashes de todos e tira o chão de quem já o tinha. Por isso a saída de um engano é sempre um commit novo e um aviso, nunca refazer o passado.

Onde vive no Morg-laws: a seção “Várias sessões na mesma pasta” da skill `orquestrando-sessoes` e a seção “Quando algo dá errado” da skill `git-e-commits`. O `index.lock` se apoia no código do git (`lockfile.c`), na seção [“Git e contas” do `FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#git-e-contas). A regra de nunca commitar o trabalho de outra sessão está no `AGENTS.md`, como “só o próprio trabalho”.
