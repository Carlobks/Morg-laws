#!/bin/sh
# Comando único de testes do Morg-laws: unittest com cobertura de linhas e ramos a 100 % dos modelos em Python
# (hooks do agente, portões do git e changelog), os testes-modelo num projeto de exemplo e o ruff.
# Python: MORG_PY, ou py (Windows), ou python3. Sem -I aqui: o coverage e o ruff vivem nos pacotes do usuário;
# os testes rodam cada modelo com -I.
# Precisa de: coverage e ruff (pip install coverage ruff). Rodar da raiz: sh scripts/testar.sh
raiz=$(cd "$(dirname "$0")/.." && pwd) || exit 1
cd "$raiz" || exit 1
py=${MORG_PY:-$(command -v py || command -v python3)}

echo "== Python (unittest + coverage)"
"$py" -m coverage run --branch --source=modelos/claude/hooks,modelos/git/portoes,modelos/changelog -m unittest discover -s tests || {
  echo "FALHOU: testes." >&2; exit 1; }
"$py" -m coverage report --show-missing --fail-under=100 || { echo "FALHOU: cobertura abaixo de 100 %." >&2; exit 1; }

echo "== Lint (ruff)"
"$py" -m ruff check modelos tests || { echo "FALHOU: ruff." >&2; exit 1; }

echo "OK: todos os testes passaram."
