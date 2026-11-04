"""Alarmes silenciados só com motivo, e nunca mais do que hoje (Morg-laws: sem silenciar alarme; não piorar).

Conta os `noqa`, `pragma: no cover`, `node:coverage disable`, `biome-ignore`, `eslint-disable`, `@ts-expect-error`,
`@ts-ignore` e `SuppressMessage` no código (testes de fora: lá são exemplos), em `//` e em `/* */` (a forma do
JSX). Cada um tem o motivo na mesma linha, depois de " — ": um comentário na linha de cima não conta, porque pode
ser um TODO ou outro alarme. A contagem POR TIPO, no projeto inteiro, não sobe: a linha de base
`tests/linhas-de-base/alarmes.json` guarda-a em `{"*": {"<tipo>": n}}` (linha_de_base.py), por isso mudar um alarme
de arquivo não conta. Quem tira um desce a base no mesmo commit. Um alarme novo justificado sobe a base com a linha
`Alarme-novo: <motivo>` na mensagem do commit: o commit-msg (mensagem_commit.py) e o CI conferem-na. Um `noqa` só
pode citar regras que o ruff tem ligadas, e isso pergunta-se ao próprio ruff: uma auditoria real deu duas regras
como desligadas, e o ruff liga-as por padrão. É a mesma regra do molde TypeScript alarmes.test.ts, que julga os
mesmos arquivos.
Limites conhecidos: as extensões `.mts`, `.cts` e `.cjs` ficam de fora (acrescente-as no bloco abaixo, nas duas
línguas); só se vê a diretiva no início de um comentário de linha ou de bloco.
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import re
import shutil
import subprocess
import sys
import unittest

from carregar_por_caminho import RAIZ
from linha_de_base import TresVerificacoesDaCatraca, arquivos_do_indice, ler_do_git

# Ajuste ao projeto. Os mesmos do molde TypeScript alarmes.test.ts.
EXTENSOES_COM_ALARMES = (".py", ".js", ".mjs", ".jsx", ".ts", ".tsx", ".ps1", ".psm1", ".html")
FORA_DOS_ALARMES = ("tests/", "vendor/", "node_modules/")
TODO_O_PROJETO = "*"  # a chave da contagem por tipo na linha de base

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


def conta_alarmes(caminho):
    return (caminho.endswith(EXTENSOES_COM_ALARMES)
            and not any(caminho.startswith(fora) or f"/{fora}" in caminho for fora in FORA_DOS_ALARMES))


def alarmes():
    """[(tipo, caminho, número da linha, linha)] de todos os alarmes silenciados do índice."""
    resultado = []
    for caminho, texto in ler_do_git([caminho for caminho in arquivos_do_indice() if conta_alarmes(caminho)]).items():
        for numero, linha in enumerate(texto.splitlines(), 1):
            resultado += [(tipo, caminho, numero, linha) for tipo, padrao in ALARMES.items() if padrao.search(linha)]
    return resultado


def contagem_por_tipo(achados):
    """{"*": {tipo: quantos}} dos alarmes achados (vazio se não houver nenhum)."""
    contagem = {}
    for tipo, *_ in achados:
        contagem[tipo] = contagem.get(tipo, 0) + 1
    return {TODO_O_PROJETO: contagem} if contagem else {}


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

    def test_conta_por_tipo_em_todo_o_projeto(self):
        achados = [("noqa", "a.py", 1, ""), ("noqa", "b.py", 3, ""), ("eslint-disable", "c.ts", 2, "")]
        self.assertEqual(contagem_por_tipo(achados), {"*": {"noqa": 2, "eslint-disable": 1}})
        self.assertEqual(contagem_por_tipo([]), {})

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


class ContagemDosAlarmes(TresVerificacoesDaCatraca, unittest.TestCase):
    REGRA = "alarmes"
    CONSELHO = "corrija o apontado em vez de silenciar; um alarme justificado leva 'Alarme-novo: <motivo>' no commit"
    MARCA_PARA_SUBIR = "Alarme-novo:"

    def medir(self):
        type(self)._achados = alarmes()
        return contagem_por_tipo(self._achados)

    def julga(self, caminho, metrica):
        return caminho == TODO_O_PROJETO

    def detalhe(self, caminho, metrica):
        return " — em " + ", ".join(f"{arquivo}:{numero}" for tipo, arquivo, numero, _ in self._achados if tipo == metrica)


if __name__ == "__main__":
    unittest.main()
