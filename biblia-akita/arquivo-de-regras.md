# O arquivo de regras do agente

Resumo com palavras nossas de *Competente o Suficiente*, de Fabio Akita, sobre o arquivo que o agente lê em todo pedido (`AGENTS.md`, `CLAUDE.md` ou equivalente). A página é a impressa. A barreira diz como impor o item: **texto** (regra escrita) ou **máquina** (permissão, hook, teste, CI, configuração). «Onde aplicar» diz que skill do Morg-laws já o aplica, ou «ainda nenhuma». O que o livro diz em forma de proibição está no [nao-faca.md](nao-faca.md) e não se repete aqui.

## 1. Quando e com que forma

- Escreva o arquivo de regras no primeiro dia: a arquitetura, onde fica cada coisa e as convenções. Sem ele, o agente faz o que é mais comum no treino, e não o que o seu projeto pede. (pp. 64, 126) · **texto** · onde aplicar: `escrevendo-regras-de-agente`
- Ele é, na prática, o prompt de sistema que você mesmo escreve, e uma das três gavetas da memória do projeto. (pp. 126, 387) · **texto** · onde aplicar: `escrevendo-regras-de-agente`
- Escreva curto, direto e em ordens; nada de prosa filosófica. O arquivo é relido a cada pedido e cada linha ocupa espaço. (p. 126) · **máquina** (limite de linhas no CI) · onde aplicar: `escrevendo-regras-de-agente`
- Escreva em linguagem comum e clara, como para alguém no primeiro dia de estágio. (p. 42) · **texto** · onde aplicar: `escrevendo-regras-de-agente`
- Quem só usa um chat tem o mesmo papel no campo de instruções permanentes. (pp. 127, 387) · **texto** · onde aplicar: ainda nenhuma

## 2. O que vai dentro

- Um trecho típico tem cinco linhas: arquivos abaixo de 500 linhas, cada um com uma responsabilidade; nomes específicos e únicos; comentários mantidos ao refatorar; cada bug com um teste que o reproduz; os testes num só comando. (p. 127) · **máquina** (testes prontos) · onde aplicar: `codigo-legivel`, `testes-e-provas`
- Escreva as proteções que o agente não poria por si (tentar de novo, tempo-limite, degradar sem cair) e o que ele não sabe do sistema: que tabelas crescem, que tempos de resposta se esperam, o que tem de ser atômico, o que não pode rodar duas vezes e o que nunca pode vazar. (pp. 126, 275) · **texto** · onde aplicar: `escrevendo-regras-de-agente`
- As regras do negócio de cada empresa ficaram fora do treino: o modelo só conhece o que é público e nunca trabalhou em empresa nenhuma. (pp. 114–115, 315–316) · **texto** · onde aplicar: `escrevendo-regras-de-agente`
- Guarde a lista das armadilhas já encontradas, e cada problema novo entra nela. O arquivo de um projeto do autor chegou a cerca de setecentas linhas assim; é o que funcionou num projeto pequeno de uma pessoa, não uma meta de tamanho. (p. 86) · **texto** · onde aplicar: `escrevendo-regras-de-agente`
- Escreva o código para um leitor com pressa: arquivos e funções pequenos, nomes únicos (o agente procura com `grep`) e comentários que dizem o porquê. Uma verificação automática recusa as funções gigantes. (pp. 124–125, 243–244) · **máquina** (teste de tamanho de função) · onde aplicar: `codigo-legivel`
- Na tela, mostre a quem usa a informação de que precisa para agir, não o número interno do sistema. (pp. 218–219) · **texto** · onde aplicar: `desenhando-telas`

## 3. Como cresce

- Cada regra nasce de um erro vivido, não da opinião de alguém de fora. Acrescente uma linha quando corrigir o mesmo deslize três vezes. (pp. 127–129) · **texto** · onde aplicar: `escrevendo-regras-de-agente`
- Junte as regras repetidas num só lugar: com duas instruções diferentes sobre o mesmo assunto, o modelo segue uma ou outra conforme o dia. O mesmo vale para um valor de configuração. (pp. 94, 99) · **texto** · onde aplicar: `escrevendo-regras-de-agente`
- O tamanho importa porque cada palavra é relida e paga a cada mensagem, a precisão cai antes do limite e o meio do contexto é o que mais se perde. O agente também lê arquivos em fatias e corta em silêncio os resultados muito grandes. (pp. 31, 33, 124) · **máquina** (limite de linhas) · onde aplicar: `escrevendo-regras-de-agente`
- Um índice de memória sempre carregado fica abaixo de umas duzentas linhas, com uma linha curta por assunto a apontar para um arquivo de tópico. Escreva primeiro o tópico e só depois a linha do índice; fatos soltos não se guardam no índice. (p. 34) · **texto** · onde aplicar: `passando-o-trabalho`

## 4. Skills, camadas e ferramentas

- Poucas skills, todas em uso: cada uma disputa a atenção do modelo, e a que ficou encostada é dívida. Um exemplo vivo no próprio código tem uma vantagem: quando quebra, alguém o conserta, e por isso não envelhece. (pp. 128–129, 412–413) · **texto** · onde aplicar: `escrevendo-regras-de-agente`
- Não acrescente nenhuma ferramenta que fique entre você e o agente antes de sentir, no trabalho, a falta dela: trabalhe com o agente de sempre, sem intermediários. (pp. 210–211) · **texto** · onde aplicar: ainda nenhuma
- Separe a configuração pessoal do trabalho que precisa de um resultado limpo: um plugin esquecido mudou notas de uma avaliação em dezenas de pontos, para cima e para baixo. (p. 48) · **texto** · onde aplicar: ainda nenhuma
- Boa parte do que faz um agente parecer inteligente está no programa à volta do modelo, e quem já tinha processo, testes e regras escritas tirou mais proveito dele. (pp. 39, 320–322) · **texto** · onde aplicar: ainda nenhuma
- Quando o agente troca de padrão sem motivo, ou puxa o desenho para o formato que viu no treino, pare-o e pergunte porquê. (pp. 70, 416) · **texto** · onde aplicar: ainda nenhuma
- Escolha a linguagem pelo problema a resolver e pelo tamanho do ecossistema à volta: quem luta com o compilador agora é o modelo. Os erros repetidos viram regra, teste ou skill, não troca de linguagem; a linguagem não substitui a arquitetura. (pp. 143, 282, 430) · **texto** · onde aplicar: ainda nenhuma
