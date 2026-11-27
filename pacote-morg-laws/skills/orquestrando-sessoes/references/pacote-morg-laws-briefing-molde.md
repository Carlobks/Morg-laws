# Molde do briefing da filha

Preenche-se com números medidos (`wc -c`, `grep -n '^#'`), não estimados. Soma de leitura + escrita ≤ ~60 mil tokens; se passar, parte-se a tarefa antes de abrir.

- **Objetivo:** uma frase, e o que é «feito».
- **Ler, por esta ordem:** `caminho` · secção «título» · linhas A–B · N KB (medido). Um ficheiro por linha. Ficheiro inteiro só se couber no orçamento.
- **Não ler:** as secções e os ficheiros que a filha não deve abrir (e porquê, se não for óbvio).
- **Do handoff (se houver):** só as linhas copiadas que tocam a fase, literais, incluindo as do «Descartado». Sem mandar ler o handoff, salvo continuação do mesmo assunto: então as secções pelo título.
- **Escrever:** os ficheiros e as secções tocadas, com `Edit`; o que fica fora.
- **Orçamento:** leitura X + escrita Y = Z mil tokens (teto ~60 mil).
- **Prova:** o comando e a saída esperada.
- **Modelo:** o escolhido pela tarefa (secção 4 da skill).
- **Fim:** título da sessão `OK | ÁREA · assunto`, hash do commit, o que não verificou.
- **Leitura:** `grep -n '^#'` e `Read` com `offset`/`limit`; nunca uma leitura acima do teto da ferramenta.
