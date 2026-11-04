#!/bin/sh
# Comando único de testes do Morg-laws: unittest com cobertura de linhas e ramos a 100 % dos modelos em Python
# (hooks do agente, portões do git e changelog), os testes-modelo nos projetos de exemplo Python e TypeScript, as
# duas línguas com o mesmo veredito e o ruff.
# Python: MORG_PY, ou py (Windows), ou python3. Sem -I aqui: o coverage e o ruff vivem nos pacotes do usuário;
# os testes rodam cada modelo com -I.
# Precisa de: coverage e ruff (pip install coverage ruff), e do Node (a versão de tests/exemplo-ts/.nvmrc) com o npm.
# Rodar da raiz: sh scripts/testar.sh
raiz=$(cd "$(dirname "$0")/.." && pwd) || exit 1
cd "$raiz" || exit 1
py=${MORG_PY:-$(command -v py || command -v python3)}

echo "== TypeScript (npm ci no projeto de exemplo, só se o package-lock.json mudou)"
exemplo=tests/exemplo-ts
node_fixado=v$(tr -d '[:space:]' < "$exemplo/.nvmrc")
node_daqui=$(node --version 2>/dev/null)
if [ "$node_daqui" != "$node_fixado" ]; then
  echo "AVISO: o Node daqui é ${node_daqui:-nenhum} e o fixado em $exemplo/.nvmrc é $node_fixado; o CI usa o fixado." >&2
fi
if [ ! -f "$exemplo/node_modules/.package-lock.json" ] || [ "$exemplo/package-lock.json" -nt "$exemplo/node_modules/.package-lock.json" ]; then
  (cd "$exemplo" && npm ci --ignore-scripts --no-audit --no-fund) || { echo "FALHOU: npm ci do exemplo." >&2; exit 1; }
fi

echo "== Python (unittest + coverage)"
"$py" -m coverage run --branch --source=modelos/claude/hooks,modelos/git/portoes,modelos/changelog -m unittest discover -s tests || {
  echo "FALHOU: testes." >&2; exit 1; }
"$py" -m coverage report --show-missing --fail-under=100 || { echo "FALHOU: cobertura abaixo de 100 %." >&2; exit 1; }

echo "== Lint (ruff)"
"$py" -m ruff check modelos tests || { echo "FALHOU: ruff." >&2; exit 1; }

echo "OK: todos os testes passaram."
