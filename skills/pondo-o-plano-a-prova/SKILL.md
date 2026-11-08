---
name: pondo-o-plano-a-prova
description: Conduz uma conversa de perguntas com o dono do projeto até um plano, uma decisão, um pedido grande ou uma mudança ficar claro o bastante para ser executado sem adivinhar — o que se quer, onde, como é antes e como fica depois, o que não se deve tocar, o que não tem volta, quem decide o quê, e o oráculo, as linhas que dizem se o resultado está certo, escritas antes de começar. Usar quando um pedido grande ou uma mudança numa tela ou funcionalidade chega sem limites ou sem forma de validar, quando o dono pede para "apertar", "pôr à prova" ou "fazer as perguntas", ou antes de começar trabalho que custa caro desfazer. Não usar para uma tarefa pequena e clara (faz-se e diz-se o que se fez) nem para medir fatos que se podem consultar (lê-se o código ou os dados).
---

# Pondo o plano à prova

Um pedido grande com lacunas faz o agente preencher as lacunas sozinho, e cada palpite errado custa uma volta de retrabalho. Algumas perguntas bem escolhidas antes de começar saem mais baratas. Esta skill diz quais perguntas, como fazê-las e quando parar.

## 1. Antes de perguntar, ler

Não pergunte o que se pode descobrir. O código, os documentos, o histórico do git e os dados respondem a muitas dúvidas. Pergunte só o que **depende da vontade do dono**: objetivos, prioridades, limites, gosto, risco aceitável.

## 2. As cinco lacunas

Um pedido está pronto para executar quando tem resposta para estas cinco. Procure-as por esta ordem:

| Lacuna | Pergunta-guia | Por que importa |
|---|---|---|
| **Objetivo** | O que muda para quem usa, quando isto estiver pronto? | Sem isto, otimiza-se a coisa errada |
| **Fora do escopo** | O que **não** se deve tocar ou fazer? | O agente tende a fazer a mais |
| **Prova** | Como vamos saber que deu certo? Que comando, tela ou número? | Sem prova, "pronto" é opinião |
| **Sem volta** | O que, se der errado, não se desfaz? (dados, produção, algo publicado, dinheiro) | É onde vale parar e pedir o "sim" |
| **Quem decide** | Que decisões o dono quer tomar e quais pode deixar ao agente? | Evita perguntar demais e de menos |

## 2b. Quando o pedido é uma mudança

Uma mudança não pede cinco perguntas a mais: pede que três das lacunas sejam respondidas **com mais precisão**. As perguntas da mudança entram como uma forma mais fina das lacunas que já existem:

| Pergunta da mudança | Refina a lacuna | O que se pede ao dono |
|---|---|---|
| **Onde** | Objetivo | O lugar exato: a tela (nome ou print), o comando, o relatório, o arquivo. |
| **Antes** | Objetivo | O que acontece hoje, como a pessoa vê (print, saída, os passos para chegar lá). |
| **Depois** | Objetivo, Prova | O que deve acontecer, em termos do que a pessoa vê ou do estado que fica. |
| **O que entra** | Objetivo | A lista do que esta mudança faz; o que não estiver na lista não se faz. |
| **O que não se mexe** | Fora do escopo | O que tem de continuar igual (vira linha do oráculo, seção 3). |

As rondas continuam com no máximo quatro perguntas, e as da mudança entram nas mesmas rondas. O «antes» muitas vezes lê-se no código ou abre-se na tela: então pergunta-se só para confirmar.

**Pede a mudança elaborada** (estas perguntas e o oráculo) quando ela: mexe numa tela ou no que a pessoa já faz; toca em mais de um lugar ou em mais de três arquivos; tem um ponto sem volta (dados, produção, algo publicado, dinheiro); ou chega sem dizer o resultado esperado.

**Dispensa** quando a tarefa é pequena e clara: um só lugar, reversível, e o próprio pedido já diz o resultado («troca o texto do botão para Salvar»). Faz-se e diz-se o que se fez, sem perguntas nem oráculo.

## 3. O oráculo

O oráculo é a verificação escrita **antes** de começar que diz se o resultado está certo, **sem dizer como se faz**. É a resposta a «como vou saber que acertou?» em linhas que alguém de fora consegue conferir.

**Como o dono o escreve:** em linhas curtas, nas palavras dele, cada uma com uma situação e o que se vê. Há dois tipos de linha:

```
Oráculo
- Dado <a situação>, quando <a pessoa faz X>, então <o que ela vê ou o estado que fica>.
- Continua igual: <o que não se mexe>, conferido por <tela, comando, número>.
```

- **Linha do «depois»** (`Dado … quando … então …`): o que a mudança tem de trazer.
- **Linha «Continua igual»**: o que a mudança não pode estragar. Pelo menos uma por oráculo.

O agente pode propor um rascunho a partir das respostas; o oráculo só vale depois de o dono confirmá-lo, e fica no resumo final e junto ao plano.

**Julga o resultado, não o mecanismo.** Uma linha que nomeia uma função, uma tabela, um código de erro ou uma biblioteca reescreve-se em termos do que a pessoa vê ou do estado que fica. No banco de provas do [Morg-laws](https://github.com/Carlobks/Morg-laws/blob/main/prova/README.md), um oráculo que exigia um código de erro específico reprovou três soluções corretas, e oráculos que não conferiam tudo o que o pedido dizia aprovaram soluções erradas (uma tabela sem as colunas pedidas; uma que apagava os pedidos de outra pessoa). Por isso se julga o resultado e se cobre também o que não se mexe.

**Como o agente o usa:**

1. Antes de mexer, transforma cada linha numa conferência: um teste automático quando dá, senão um comando com a saída esperada, senão um passo para uma pessoa ver na tela.
2. Corre-as **antes**, no estado atual, e anota o resultado de cada uma. As duas espécies têm regras opostas:
   - a linha do «depois» **tem de falhar antes** («hoje: falha, aparece X»); se já passa, não prova nada sobre a mudança, e a dúvida vai ao dono;
   - a linha «Continua igual» **tem de passar antes e depois**; se já falha antes, o ponto de partida não é o que o dono descreveu, e a dúvida vai ao dono.
3. Depois da mudança, corre todas e relata **linha a linha**: passou, falhou, ou não se pôde conferir (e por quê). Nunca «pronto» sem esta lista.
4. Se o resultado não cabe no oráculo (o dono queria outra coisa), não se reescreve o oráculo para passar: volta-se ao dono.

## 4. Como perguntar

- **Em rondas curtas**, de no máximo quatro perguntas. Uma ronda só pergunta o que já se pode responder com o que se sabe. A resposta de uma pergunta pode mudar as seguintes.
- **Cada pergunta traz opções concretas** e uma delas marcada como recomendada, com o porquê numa frase. O dono pode aceitar a recomendação com uma palavra.
- **Explique o termo técnico** dentro da pergunta. Quem decide não precisa de saber o jargão para escolher bem.
- **Se a resposta for "explica melhor" ou "pesquisa antes",** pesquise ou explique e volte com a pergunta refeita. Não decida no lugar do dono.
- Use a ferramenta de perguntas do agente, quando houver, em vez de um formulário improvisado.

## 5. Quando parar

Pare quando as cinco lacunas tiverem resposta e, numa mudança, o dono tiver confirmado o oráculo; ou quando o dono disser que chega (numa mudança sem oráculo, o resumo diz isso). Não continue a perguntar por perguntar: cada ronda custa a atenção do dono.

## 6. O que entregar no fim

Um resumo curto, que o dono confirma antes de começar:

```
Objetivo: …
Fora do escopo: …
Prova de pronto: …
Pontos sem volta (pedem o "sim" na hora): …
Decisões do dono: …   Decisões deixadas ao agente: …
Mudança (se for uma): onde … / antes … / depois … / entra … / não se mexe …
Oráculo (obrigatório numa mudança): …
```

Guarde o resumo junto ao plano. Se a resposta do dono for um texto dele, guarde-o como ele escreveu.

## Fontes

Ver [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#inspirações-nada-copiado). Esta skill foi escrita do zero. A ideia de interrogar o dono antes de executar foi inspirada na skill "grill-me", de Matt Pocock, e no método de pedir com "o que não fazer" e "como validar", de Fabio Akita. O corte entre a mudança elaborada e a tarefa pequena, o esforço proporcional ao que está em jogo e o oráculo escrito antes vêm do livro *Competente o Suficiente* (pp. 118, 120–121 e 322–323), em [`FONTES.md`](https://github.com/Carlobks/Morg-laws/blob/main/FONTES.md#livros-e-autores); a regra de julgar o estado, e não o mecanismo, vem do [banco de provas](https://github.com/Carlobks/Morg-laws/blob/main/prova/README.md) deste repositório.
