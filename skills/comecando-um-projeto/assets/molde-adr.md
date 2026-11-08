# <NNNN> — <a decisão, numa frase>

Vive em `docs/decisoes/NNNN-titulo.md`. Os números são seguidos e nunca se reutilizam; uma decisão revista ganha
uma ADR nova que diz qual substitui. Formato de Michael Nygard (contexto, decisão, consequências).

- **Estado:** <proposta | aceita (<AAAA-MM-DD>, aprovada pelo dono) | substituída pela <NNNN>>
- **Contexto:** <o problema e as forças em jogo; o que se mediu; a pesquisa em `docs/pesquisa/…`>.
- **Decisão:** <o que se decidiu, de forma que se possa conferir>.
- **Consequências:** <o que fica mais fácil, o que fica mais difícil, que barreira a obriga>.

---

## Exemplo: o histórico já publicado não se reescreve

- **Estado:** aceita.
- **Contexto:** uma verificação achou um caminho pessoal em commits antigos, já publicados. A árvore atual está
  limpa e um teste impede que o caminho volte. Reescrever o histórico muda os hashes de todos os clones e de todos
  os documentos que os citam.
- **Decisão:** não reescrever. Os commits ficam como estão, registados aqui como exceção. Um segredo publicado é
  outro caso: roda-se ou revoga-se, sempre.
- **Consequências:** o dado continua no histórico; a regra "sem dados reais" vale daqui para a frente, com o teste.
