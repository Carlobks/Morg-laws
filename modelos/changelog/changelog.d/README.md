# Fragmentos do changelog

Cada mudança que quem usa o projeto nota leva um arquivo aqui: `AAAA-MM-DD-assunto.md`, com o assunto em
minúsculas e hífens. Mudanças internas (refatoração, testes, documentação de trabalho) não levam. Um arquivo por
mudança não colide quando várias sessões trabalham ao mesmo tempo, como colidiria um `CHANGELOG.md` único.

```
Categoria: Corrigido
Incompatível: o que quem usa tem de mudar (linha opcional)

- O que mudou, escrito para quem usa o projeto.
  Uma linha de continuação começa com dois espaços.
```

Categorias, nesta ordem (Keep a Changelog): Adicionado, Alterado, Obsoleto, Removido, Corrigido, Segurança.

- O portão `commit-msg` recusa um `feat` ou `fix` que mexa no que se publica (`PUBLICADO` no
  `scripts/portoes/mensagem_commit.py`) sem um fragmento no mesmo commit, ou sem a linha `Sem-changelog: <motivo>`.
- A linha `Incompatível:` só entra quando quem usa tem de mudar algo; sobe o MAIOR da versão (no 0.x, o MENOR).
- `python -I scripts/changelog/juntar_changelog.py` junta-os no `CHANGELOG.md`, calcula a versão seguinte pelas
  categorias (SemVer), escreve-a no `VERSION` e apaga os fragmentos. Com `--rascunho`, só mostra.
- Depois do lançamento: uma tag anotada `vX.Y.Z` no commit da versão.
