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

Compacte cedo: por volta de 150 mil tokens, sem esperar pela compactação automática, que só dispara perto do limite do modelo.

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

Cada mensagem manda a conversa inteira de volta, e uma conversa longa fica cara, lenta e menos atenta. O resumo da compactação perde o detalhe, e o agente volta a propor o que você já descartou. Por isso o combinado fica em arquivo, e não só na conversa (livro *Competente o Suficiente*, de Fabio Akita, pp. 30–32, 124, 411). O livro não dá um limiar de tokens.

As vozes da cabeça de Carlobks (decisão de 2026-11-06): compactar cedo. Porquê: numa medição do trabalho antes das regras, reler o contexto foi a maior parte do custo, 64% ([medições do uso](https://github.com/Carlobks/Morg-laws/blob/main/pesquisas/2026-11-05-linha-de-base-do-uso.md)).

As vozes da cabeça de Carlobks (decisão de 2026-11-06): o número é por volta de 150 mil tokens. Porquê: nas palavras dele, arrumadas, testou o plano Pro e o Max 5x; no Pro a janela é menor e ele compactava mais vezes; foi sentindo que 150 mil a 200 mil tokens era o máximo que queria usar. Compacta antes sempre que a tarefa ou o tempo deixam, porque quanto menos distração na janela, mais atenção o modelo dá ao que ele quer. É a prática de uma pessoa, e não um limite da ferramenta.

Os comandos estão na [documentação do Claude Code](https://code.claude.com/docs/en/commands): `/compact`, que aceita instruções de foco, e `/context`, que mostra o que ocupa a janela.

Onde vive no Morg-laws: a skill `passando-o-trabalho`, com a pergunta “compactar ou sessão nova?” e o comando pronto.

## P11 · Abrir uma sessão filha

### Na prática

Uma sessão filha é uma sessão nova que recebe um pedido escrito e devolve um resultado. Você a abre pelo seu agente ou à mão, e a vê trabalhar: pode lê-la e corrigi-la a meio.

O pedido leva o objetivo, os arquivos, o que já se descartou, como se prova e o modelo (P12). Um pedido de implementação, assim:

```
Título: ATIVO | ÁREA · implementação do passo 3

Implementa o passo 3 do plano. Trabalhas na pasta tal, em commits locais, sem push.
Antes de começar, confere que a árvore está limpa e que o último commit é o combinado.

Lê primeiro, e só isto: o plano (as seções 3 e 5), as regras do projeto e os testes que não podem quebrar.
O que se faz é o que o plano manda, e mais nada. Se algo não bater, não improvises: registra um desvio.

Em cada commit: estagia só os caminhos dele, roda os portões, commita por caminho.
Está proibido: ler segredos, escrever no banco, lançar sub-agentes, fazer push.
O relatório vai para tal arquivo: commits, a prova de cada passo, desvios e o que não se verificou.
Quando acabares, troca o título para OK e avisa num parágrafo.
```

O que costuma dar errado:

- Deixar o que não se faz de fora. A filha faz a mais.
- Pedir uma auditoria dizendo a sua conclusão. Ela tende a confirmá-la.
- Esquecer o que já falhou: a filha repete.

### Por quê e fonte

A filha nasce com o contexto limpo: só o que o pedido diz. Por isso o pedido carrega tudo, e o relatório volta como dado, que você confere, e não como verdade. Quem escreveu um trabalho não o audita bem: para uma leitura independente, abra uma sessão sem a conversa que o produziu, com um pedido neutro, sem a sua conclusão.

Prefira sessões novas a sub-agentes quando você quer ver e corrigir cada passo: um sub-agente não pode ser visto nem corrigido, e o erro volta no mesmo tom confiante dos acertos. Sub-agentes servem para buscas amplas e tarefas independentes, com o resultado conferido depois. Um agente gasta cerca de 4 vezes os tokens de uma conversa, e um sistema com vários agentes cerca de 15 vezes; só compensa quando a tarefa vale esse custo, e o conselho é começar pelo mais simples (dois artigos da Anthropic sobre agentes, com a data de leitura, na [seção “Uso e custo de agentes” do `FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#uso-e-custo-de-agentes)).

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

Ponha o modelo no pedido, ao abrir a filha, e não no `settings.json`: um `model` fixo ali valeria para todas as sessões.

O que costuma dar errado:

- Deixar o modelo padrão e descobrir tarde que a auditoria saiu num modelo pequeno.
- Usar o maior em tudo. O trabalho de rotina sai mais barato no médio.
- Fixar o modelo no `settings.json` e esquecer que ele vale para todas.

### Por quê e fonte

Um modelo mais barato pode baixar a qualidade, e é a auditoria e o plano que mais pagam por isso. O guia de boas práticas do Claude Code diz que o Sonnet custa menos no trabalho de rotina e que o Haiku serve para tarefas simples ([boas práticas](https://code.claude.com/docs/en/best-practices)). O livro de Fabio Akita manda escolher o modelo pelo preço, pelo tempo e pela ferramenta, e testar a combinação (pp. 45, 155, 159–161, 311–312).

As vozes da cabeça de Carlobks (decisão de 2026-11-06): a auditoria a frio fica no maior modelo. Porquê: a skill diz que um modelo mais barato pode baixar a qualidade, e por isso o plano e a auditoria ficam no maior ([`orquestrando-sessoes`](https://github.com/Carlobks/Morg-laws/blob/main/skills/orquestrando-sessoes/SKILL.md)). Uma segunda auditoria, em outro modelo ou em outra ferramenta, continua a valer.

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
- `OK`: terminou, sem nada fora da branch principal.
- `OFF`: parada de propósito.

A área vai em maiúsculas e o assunto em poucas palavras. Cada sessão troca o próprio título quando muda de estado. Quatro exemplos, dois reais e dois inventados (os do meio) no mesmo molde:

```
ATIVO | MORG-LAWS · plano do manual de uso
ESPERA | MORG-LAWS · pergunta sobre o formato (exemplo)
OK | MORG-LAWS · implementação da M2 (começar: 00, 01, 02)
OFF | MORG-LAWS · ideia guardada para depois (exemplo)
```

Como renomear: no Claude Code, `/rename <título>`, que você digita; o agente não digita comando de barra e deve pedir a você, com o título pronto. No Codex, o `/rename <nome>` também ([comandos do Codex](https://developers.openai.com/codex/cli/slash-commands)).

O que costuma dar errado:

- Esquecer de trocar o título ao mudar de estado.
- Um assunto longo demais: o título passa a não caber na lista.
- Deixar o agente da filha sem o id da própria sessão: quem orquestra troca o título dela.

### Por quê e fonte

Com muitas sessões abertas você se perde. O título diz, de relance, quais esperam por você e quais terminaram.

As vozes da cabeça de Carlobks (decisão de 2026-11-08): o título `ESTADO | ÁREA · assunto`. Porquê: nas palavras dele, arrumadas, tinha 70 sessões abertas e se perdia naquela imensidão; o título foi um jeito de se organizar. Criou também pastas para as sessões. Assim sabe no que está trabalhando no momento.

O `/rename` está na [documentação de comandos do Claude Code](https://code.claude.com/docs/en/commands): muda o nome da sessão e o mostra na barra do prompt; sem nome, gera um a partir da conversa. O nome tem no máximo 200 caracteres.

Onde vive no Morg-laws: a seção “Várias sessões na mesma pasta” da skill `orquestrando-sessoes`, que traz os quatro estados e a forma de renomear em cada ferramenta.
