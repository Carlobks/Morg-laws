# Datas e validação

## Compare datas como texto, não como `Date`

**O que aconteceu:** um filtro por mês excluía o dia 1.
**Por que:** `new Date('2026-08-01')` é lido como meia-noite em UTC. Num fuso a oeste de Greenwich, isso é 31/07.
**Como fazer:** para datas sem hora (`AAAA-MM-DD`), compare as strings (`data >= '2026-08-01'`). Converta para `Date` só quando precisar de hora.

## A data de hoje no servidor vem de uma função única

**Por que:** `new Date().toISOString()` espalhado pelo código dá resultados diferentes conforme o fuso do servidor.
**Como fazer:** uma função (`hojeISO()`) que fixa o fuso do negócio, usada em todo o lado.

## Locale fixo na formatação

Formate datas e números com o locale do projeto escrito no código (`toLocaleDateString('pt-BR')`), nunca com o padrão do navegador ou do servidor, que muda de máquina para máquina.

## `!valor` trata `0` e `''` como vazios

**O que aconteceu:** um campo com o valor `0` era recusado como "obrigatório".
**Como fazer:** use uma verificação estrita, por exemplo `valor === null || valor === undefined || valor === ''`, numa função `estaVazio()`.

## Edição parcial é PATCH, não PUT

**O que aconteceu:** salvar um formulário com só alguns campos apagou os outros.
**Por que:** os campos que faltavam chegaram como `undefined`, viraram `null` e sobrescreveram os valores guardados.
**Como fazer:** envie só os campos que mudaram e trate a escrita como PATCH.

## O valor por omissão escreve-se no código

**Regra de origem:** todo documento novo entra como oculto, com o valor escrito explicitamente pelo código.
**Como fazer:** a aplicação grava o valor seguro (por exemplo, `visivel: false`) em vez de contar com o padrão da coluna. Um padrão no banco muda com uma migração, sem ninguém rever o código que dependia dele.

## Toda chamada de rede longa leva timeout

Upload, download, chamadas a APIs externas: um `AbortController` com prazo explícito. Sem prazo, uma chamada pendurada prende a tela ou o servidor.
