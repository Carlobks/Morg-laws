"""Alarmes silenciados só com motivo, e nunca mais do que hoje (Morg-laws: sem silenciar alarme; não piorar).

Conta os `noqa`, `pragma: no cover`, `node:coverage disable`, `biome-ignore`, `eslint-disable`, `@ts-expect-error`,
`@ts-ignore` e `SuppressMessage` no código (testes de fora: lá são exemplos), em `//` e em `/* */` (a forma do
JSX). Cada um tem o motivo na mesma linha, depois de " — ": um comentário na linha de cima não conta, porque pode
ser um TODO ou outro alarme. A contagem por tipo não pode subir, e quem tira um baixa o número no mesmo commit
(catraca nos dois sentidos). Um `noqa` só pode citar regras que o ruff tem ligadas, e isso pergunta-se ao
próprio ruff: uma auditoria real deu duas regras como desligadas, e o ruff liga-as por padrão.
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import re
import shutil
import subprocess
import sys
import unittest

from carregar_por_caminho import RAIZ

# Ajuste ao projeto. Linha de base: a contagem de hoje por tipo. Só desce.
MAXIMO_POR_TIPO = {}
EXTENSOES_DE_CODIGO = (".py", ".js", ".mjs", ".jsx", ".ts", ".tsx", ".ps1", ".psm1", ".html")
FORA = ("tests/", "vendor/", "node_modules/")

# Só a diretiva verdadeira (um comentário que fala dela não conta).
ALARMES = {
    "noqa": re.compile(r"^\s*[^#\s].*#\s*noqa\b"),
    "pragma: no cover": re.compile(r"^\s*[^#\s].*#\s*pragma:\s*no cover"),
    "node:coverage disable": re.compile(r"^\s*/\*\s*node:coverage (?:disable|ignore)"),
    "biome-ignore": re.compile(r"^\s*//\s*biome-ignore"),
    "eslint-disable": re.compile(r"(?://|/\*)\s*eslint-disable"),
    "@ts-expect-error": re.compile(r"(?://|/\*)\s*@ts-expect-error"),
    "@ts-ignore": re.compile(r"(?://|/\*)\s*@ts-ignore"),
    "SuppressMessage": re.compile(r"\[\s*(?:System\.)?Diagnostics\.CodeAnalysis\.SuppressMessage"),
}


def arquivos_de_codigo():
    saida = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8",
                           check=True).stdout.splitlines()
    return [caminho for caminho in saida if caminho.endswith(EXTENSOES_DE_CODIGO)
            and not any(caminho.startswith(fora) or f"/{fora}" in caminho for fora in FORA)]


def alarmes():
    """[(tipo, caminho, número da linha, linha)] de todos os alarmes silenciados."""
    resultado = []
    for caminho in arquivos_de_codigo():
        linhas = (RAIZ / caminho).read_text(encoding="utf-8-sig").splitlines()
        for numero, linha in enumerate(linhas, 1):
            for tipo, padrao in ALARMES.items():
                if padrao.search(linha):
                    resultado.append((tipo, caminho, numero, linha))
    return resultado


def contagem_por_tipo():
    """{tipo: quantos} dos alarmes silenciados de hoje."""
    contagem = {}
    for tipo, *_ in alarmes():
        contagem[tipo] = contagem.get(tipo, 0) + 1
    return contagem


def regras_ligadas_no_ruff(arquivo):
    """Códigos das regras que o ruff roda neste repositório para `arquivo` (ruff check --show-settings)."""
    saida = subprocess.run([sys.executable, "-m", "ruff", "check", "--show-settings", arquivo], cwd=RAIZ,
                           capture_output=True, text=True, encoding="utf-8", check=True).stdout
    bloco = saida.split("linter.rules.enabled = [", 1)[1].split("]", 1)[0]
    return set(re.findall(r"\(([A-Z]+\d+)\)", bloco))


class AlarmesComMotivo(unittest.TestCase):

    def test_cada_alarme_tem_motivo(self):
        for tipo, caminho, numero, linha in alarmes():
            with self.subTest(alarme=f"{caminho}:{numero} {tipo}"):
                self.assertIn(" — ", linha, "falta o motivo na mesma linha, depois de —")

    def test_a_contagem_nao_sobe(self):
        for tipo, quantos in contagem_por_tipo().items():
            with self.subTest(tipo=tipo):
                self.assertLessEqual(quantos, MAXIMO_POR_TIPO.get(tipo, 0), "corrija o apontado em vez de silenciar")

    def test_a_linha_de_base_desce_com_a_contagem(self):
        contagem = contagem_por_tipo()
        for tipo, maximo in MAXIMO_POR_TIPO.items():
            with self.subTest(tipo=tipo):
                self.assertGreaterEqual(contagem.get(tipo, 0), maximo,
                                        f"saiu um alarme: baixe MAXIMO_POR_TIPO['{tipo}'] para {contagem.get(tipo, 0)}")

    def test_noqa_so_de_regras_ligadas(self):
        noqas = [(caminho, numero, linha) for tipo, caminho, numero, linha in alarmes() if tipo == "noqa"]
        if not noqas:
            self.skipTest("nenhum noqa no código")
        self.assertTrue(shutil.which("ruff") or subprocess.run([sys.executable, "-m", "ruff", "--version"],
                                                               capture_output=True, check=False).returncode == 0,
                        "há noqa e o ruff não está instalado: não dá para conferir")
        for caminho, numero, linha in noqas:
            ligadas = regras_ligadas_no_ruff(caminho)
            codigos = re.search(r"noqa:\s*([\w, ]+?)(?:\s+—|$)", linha)
            for codigo in (codigos.group(1).replace(" ", "").split(",") if codigos else []):
                with self.subTest(alarme=f"{caminho}:{numero} {codigo}"):
                    self.assertIn(codigo, ligadas, "regra que o ruff não roda: o noqa é ruído")


if __name__ == "__main__":
    unittest.main()
