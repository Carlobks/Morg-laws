#!/bin/sh
# Lê texto da entrada padrão e recusa se casar com a lista negra local.
# A lista fica fora do repositório (é a lista dos nomes que não podem vazar).
# Caminho: git config morg.listaNegra <arquivo>. Quem clonou sem a lista recebe só um aviso.

lista=$(git config --get morg.listaNegra)
if [ -z "$lista" ]; then
  echo "aviso: morg.listaNegra não configurada; verificação de nomes não correu." >&2
  exit 0
fi
if [ ! -f "$lista" ]; then
  echo "ERRO: morg.listaNegra aponta para '$lista', que não existe." >&2
  exit 1
fi

padroes=$(mktemp)
grep -v -e '^[[:space:]]*#' -e '^[[:space:]]*$' "$lista" > "$padroes"

achados=$(grep -n -i -E -f "$padroes")
rm -f "$padroes"

if [ -n "$achados" ]; then
  echo "ERRO: conteúdo sensível encontrado ($1):" >&2
  echo "$achados" | head -20 >&2
  echo "Tire o nome ou o dado e tente de novo. A lista está em $lista." >&2
  exit 1
fi
exit 0
