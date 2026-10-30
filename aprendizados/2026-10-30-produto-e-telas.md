# Produto e telas

## Toda lista de trabalho precisa de uma porta de saída

**O que aconteceu:** uma lista de pendências tinha dezenas de itens e nenhum saía. O critério de saída existia no papel, mas nunca abria na prática.
**Como fazer:** ao criar uma lista de trabalho, meça quantos itens já saíram. Um sinal de fora (o estado da pessoa) serve de critério; uma arrumação de tela (arquivar) não.

## Uma forma de apagar, não quatro

**O que aconteceu:** um levantamento achou quatro padrões de apagar em uso no mesmo sistema (apagar de vez, marcar como apagado, arquivar, mover para o lixo), escolhidos tela a tela, sem critério.
**Como fazer:** meça quais padrões existem, escolha um por tipo de dado e escreva o critério. Dado com histórico marca-se como apagado (ver a skill `sql-postgres`). Apagar de vez fica para a limpeza de retenção.

## Um botão que abre "em breve" ensina a ignorá-lo

Botão sem função faz as pessoas aprenderem que aquele lugar não serve. Ou funciona, ou não aparece.

## Esconder o botão não é barreira

Um acesso exclusivo confere-se no servidor e no banco. Registre num arquivo cada acesso que só uma pessoa tem, e faça um teste (catraca) que obrigue a registrar os novos. E atenção: quem gere os interruptores pode dar acesso a si mesmo.

## Desligar alguém revoga o acesso na mesma operação

Quando uma pessoa sai, o fim do vínculo e a revogação do acesso acontecem juntos, numa só operação. E nenhuma rotina automática muda um estado que pede confirmação de uma pessoa.

## A mesma marca não serve a tela e o papel

Um logotipo desenhado para um fundo escuro desaparece num PDF de fundo branco. Tenha as duas versões e escolha pelo destino.

## Posição de campo num PDF é calculável

Com bibliotecas como o jsPDF, a posição de cada campo calcula-se a partir das medidas do texto. Não se adivinha por tentativa e erro.

## PDF digitalizado não tem texto

**O que aconteceu:** um PDF que era uma imagem digitalizada foi processado como vazio, e gravou zeros.
**Como fazer:** se a extração de texto devolver `''`, recuse com um motivo próprio ("documento sem texto, precisa de OCR") antes de gravar qualquer coisa.

## Camada visual guarda só o estado visual

Num quadro ou mapa de elementos, a camada visual guarda posição e tamanho. Os dados de negócio vêm sempre frescos das tabelas. Um elemento cujo registro foi apagado aparece como "fantasma", não com dados velhos.

## Campo novo editável entra no formulário que já existe

Um segundo botão de editar para um campo novo confunde. Acrescente o campo ao formulário de edição que já existe.

## Texto para o dono reescreve-se, não se cola

O texto técnico (commit, changelog) serve quem lê código. O aviso para quem usa o sistema reescreve-se em linguagem simples. A gravidade mede-se pelo pior efeito para quem usa, não pelo esforço de corrigir.
