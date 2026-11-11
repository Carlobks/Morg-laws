# Como este manual foi feito

## Um plano antes do texto

Este manual nasceu de um plano escrito antes de qualquer parte do texto. Uma sessão nova do agente, sem a conversa que o produziu, auditou esse plano a frio antes de o autor aprová-lo. O plano marcou as partes, o teto de palavras de cada uma e o formato de páginas duplas. O que está no PDF segue essa marcação, e o [README do manual](https://github.com/Carlobks/Morg-laws/blob/main/manual/README.md) mostra como o PDF é gerado.

## Uma fase de cada vez

O manual foi escrito por fases. Cada fase seguiu o mesmo ciclo, e cada passo dele rodou numa sessão nova do agente:

1. a implementação, que escreve a parte;
2. a auditoria a frio, feita por uma sessão sem a conversa que produziu o trabalho;
3. a conferência, que confere na fonte cada achado da auditoria;
4. as correções.

A sessão que orquestra só escreveu os pedidos e conferiu os resultados. É o método que a parte `05` ensina para o seu trabalho (P11, P14 e P15), aplicado aqui ao próprio manual. O [README do manual](https://github.com/Carlobks/Morg-laws/blob/main/manual/README.md) lista as partes que resultaram dele.

## As rondas ao autor

Toda decisão tomada no meio do caminho foi ao autor, com a opção recomendada marcada, e ficou escrita com o porquê. Algumas vezes ele escolheu outra opção que não a recomendada, e o texto segue a escolha dele, não a do agente. Isso vale para o que o manual chama de “as vozes da cabeça de Carlobks”, como a [parte `00`](https://github.com/Carlobks/Morg-laws/blob/main/manual/00-antes-de-comecar.md) explica. Quem lê o manual vê assim o que é fato de uma fonte e o que é preferência de uma pessoa.

## O verificador

O texto passa por um verificador automático. Ele confere os tetos de palavras de cada parte, as fontes em cada seção, a língua do texto e a paridade das páginas, isto é, que “Na prática” comece numa página par e “Por quê e fonte” na ímpar seguinte. O [verificador do manual](https://github.com/Carlobks/Morg-laws/blob/main/tests/verificador_do_manual.py) roda na suíte de testes, como qualquer outra regra do repositório, e a parte `08` conta como essas barreiras funcionam. Quando um detector acusa o texto, quem muda é o texto, e o detector fica como está.

## O que os leitores simulados apontaram

Antes de o texto ir para o autor, três personas o leram, cada uma numa sessão do agente:

- a Bia, que nunca usou um agente nem o git;
- o Davi, programador cético, que procura frase maior que a fonte;
- a Lena, que usa o [Codex](https://developers.openai.com/codex/skills).

Os números abaixo são o que elas apontaram:

- **Primeira ronda:** 84 achados, 35 da Bia, 26 do Davi e 23 da Lena.
- **Segunda ronda:** dos 83 achados relidos, 34 ficaram resolvidos, 17 em parte e 7 não resolvidos, e 25 ficaram fora pela triagem. Houve 32 achados novos: 24 da Bia, 5 do Davi e 3 da Lena.
- **A Bia, do zero:** ela listou 30 coisas de que precisaria antes do primeiro procedimento. O manual dizia 2 por inteiro, 13 em parte e 15 não dizia. Daí nasceu a parte `02`.
- **A Bia relendo a parte `02`:** dos 23 itens dela, 19 ficaram resolvidos e 4 em parte. Houve 13 achados novos.

A triagem seguiu uma regra simples. A falha de lógica, conferida na fonte, corrige-se sempre. A clareza entra se dois leitores a levantarem. O gosto de um só fica de fora. Os [modelos de issue](https://github.com/Carlobks/Morg-laws/tree/main/.github/ISSUE_TEMPLATE) do repositório seguem a mesma ideia: pedem a prova antes da opinião.

## O que estes números não são

Os números acima são o que agentes apontaram, lidos pelo próprio autor. Não são uma medição do manual. A prova do manual é o uso real: quem o seguir e tropeçar abre uma [issue no repositório](https://github.com/Carlobks/Morg-laws/issues), e é ali que se vai ver se ele serve.

## O limite da Lena

Um leitor simulado numa sessão do Claude não sabe o que o Codex faz: a Lena só aponta as frases que supõem o Claude Code. O que o manual diz do Codex confere-se na [documentação de skills do Codex](https://developers.openai.com/codex/skills), que é a fonte oficial.

## O que é do autor e o que é do agente

É do autor tudo o que é decisão: as escolhas marcadas como dele, o “Quem escreveu isto” da parte `00` e a leitura final de cada parte. É do agente a escrita do texto, as auditorias, as conferências e os leitores, sempre conferidos e aprovados pelo autor. A divisão está à vista de propósito, para que você saiba em quem confiar para quê, e qualquer erro que você achar nele se conta pelo mesmo caminho das [issues](https://github.com/Carlobks/Morg-laws/issues).
