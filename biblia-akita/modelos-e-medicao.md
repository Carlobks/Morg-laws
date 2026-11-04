# Escolher e medir modelos

Resumo com palavras nossas de *Competente o Suficiente*, de Fabio Akita, sobre como escolher modelos e ler rankings e anúncios. A página é a impressa. A barreira diz como impor o item: **texto** (regra escrita) ou **máquina** (permissão, hook, teste, CI, configuração). «Onde aplicar» diz que skill do Morg-laws já o aplica, ou «ainda nenhuma». O que o livro diz em forma de proibição está no [nao-faca.md](nao-faca.md) e não se repete aqui.

## 1. Ler promessas, tabelas e anúncios

- Diante de uma promessa, pergunte também quem ganha se você acreditar nela, seja no milagre, seja no medo. (pp. 204, 209, 327–328) · **texto** · onde aplicar: ainda nenhuma
- Uma capacidade que ninguém de fora testou é só uma alegação. (pp. 173, 201, 400) · **texto** · onde aplicar: ainda nenhuma
- Diante de uma tabela de resultados, pergunte: que tarefa, que ferramenta e que critério; quantas vezes foi rodada; se a diferença é maior que o acaso; se houve correções publicadas; como se contou o custo; se a prova já está gasta ou se o modelo a viu no treino; quem escreveu a verificação; se o gabarito estava ao alcance; e se já rodou no seu caso. (pp. 151–152, 157–158, 398–399) · **texto** · onde aplicar: ainda nenhuma
- Diante de um anúncio, pergunte: quem lucra; se dá para testar de fora; o que quer dizer a palavra grande; contra quem e com que régua; o que sobra sem o nome da marca; se aconteceu ou só «poderia»; quanto custou; se as vozes são independentes; se as credenciais batem com as datas; e se precisa daquilo hoje. (pp. 213–214, 400–401) · **texto** · onde aplicar: ainda nenhuma
- Desconfie da demonstração de cinco segundos, do «perigoso demais para lançar», do anúncio da inteligência geral e das «capacidades que surgiram sozinhas». (pp. 25, 180, 202–203, 356) · **texto** · onde aplicar: ainda nenhuma
- Diante de uma percentagem, pergunte com que frequência o caso procurado aparece e qual é o preço de cada engano. Um exame que acerta 99% numa doença de um caso em mil dá razão em cerca de 9% dos positivos. Uma segunda opinião só vale se for independente. (p. 352) · **texto** · onde aplicar: ainda nenhuma

## 2. Escolher

- No topo, os modelos andam juntos: para programar no dia a dia, escolha pelo preço, pelo tempo de resposta e pela ferramenta que já usa. O resultado é a soma do modelo, do pedido, do programa à volta, do contexto, das ferramentas, da versão, da execução e da revisão; teste a combinação de modelo e ferramenta. (pp. 45, 155, 159–161, 311–312) · **texto** · onde aplicar: ainda nenhuma
- Faça o seu próprio teste: uma tarefa real que você sabe resolver, repetida mais de uma vez, às cegas, medindo o trabalho humano que ainda faltou. (pp. 91–92, 152, 331) · **texto** · onde aplicar: ainda nenhuma
- Ajuste o nível de esforço do modelo à tarefa: baixo para traduzir e resumir, alto para procurar falhas de segurança, bugs difíceis e otimizações. (p. 312) · **máquina** (configuração do agente) · onde aplicar: ainda nenhuma
- Modelos abertos, destilados, misturados ou «treinados em casa»: confira a origem e a licença. A destilação passa o estilo, e o conhecimento nem sempre, e «aberto», «local» e «de graça» são três coisas diferentes. (pp. 167–170, 177, 179, 195) · **texto** · onde aplicar: ainda nenhuma
- Para decisões fechadas (classificar, escolher entre opções), prefira modelos pequenos e especializados, testados contra um gabarito que não muda. Um modelo de chat não é a ferramenta para pôr rótulos. (pp. 181–182, 212, 321) · **texto** · onde aplicar: ainda nenhuma
- A nota que um modelo dá ao código não mede a qualidade do código. (p. 244) · **texto** · onde aplicar: `codigo-legivel`

## 3. O que há dentro da caixa

- O modelo só devolve o que viu no treino: rende mais em tecnologias populares, vê mal o que é fechado e devolve os erros dos fóruns arrumados e confiantes. A inteligência de base nivelou; o ganho vem das ferramentas à volta. (pp. 108, 135–136, 312–315, 348–349) · **texto** · onde aplicar: ainda nenhuma
- Por dentro, há um gerador do texto mais provável, com sorteio, sem nenhum passo que confira a verdade. Ser educado e ser bajulador saem, nele, do mesmo treino. (pp. 16–18, 352–358) · **texto** · onde aplicar: ainda nenhuma
- Repetir a pergunta pode trazer outra resposta: o modelo calcula as chances do pedaço seguinte e sorteia entre os mais prováveis. (p. 16) · **texto** · onde aplicar: ainda nenhuma
