"""Fins de linha coerentes com o .gitattributes (Morg-laws).

O git guarda todos os arquivos de texto em LF; no disco ficam em CRLF só os que o Windows roda (EM_CRLF) e em LF
todos os outros. Sem isto, os fins de linha ficam como calhou: num projeto real, um script de substituição com
"\\n" parecia funcionar e não trocava nada nos arquivos em CRLF. No `.gitattributes`, por exemplo:
    * text=auto eol=lf
    *.ps1 text eol=crlf
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import subprocess
import unittest

from carregar_por_caminho import RAIZ

# Ajuste ao projeto.
EM_CRLF = (".ps1", ".psm1", ".cmd", ".bat")


def estado_dos_arquivos():
    """[(índice, disco, atributos, caminho)] dos arquivos de texto, de `git ls-files --eol`."""
    saida = subprocess.run(["git", "ls-files", "--eol"], cwd=RAIZ, capture_output=True, text=True,
                           encoding="utf-8", check=True).stdout
    resultado = []
    for linha in saida.splitlines():
        marcas, caminho = linha.split("\t", 1)
        indice, disco, atributos = marcas.split(None, 2)
        if indice != "i/-text":  # binário
            resultado.append((indice[2:], disco[2:], atributos.strip()[5:], caminho))
    return resultado


class FinsDeLinha(unittest.TestCase):

    def test_ha_arquivos(self):
        self.assertGreater(len(estado_dos_arquivos()), 0)

    def test_o_git_guarda_o_texto_em_lf(self):
        errados = [caminho for indice, _, _, caminho in estado_dos_arquivos() if indice not in ("lf", "none")]
        self.assertEqual(errados, [], "falta normalizar: git add --renormalize -- <arquivos>")

    def test_no_disco_crlf_so_no_que_o_windows_roda(self):
        errados = [f"{caminho} ({disco})" for _, disco, _, caminho in estado_dos_arquivos()
                   if disco not in ("none", "crlf" if caminho.endswith(EM_CRLF) else "lf")]
        self.assertEqual(errados, [])

    def test_atributos_do_gitattributes(self):
        for _, _, atributos, caminho in estado_dos_arquivos():
            with self.subTest(arquivo=caminho):
                self.assertIn("eol=crlf" if caminho.endswith(EM_CRLF) else "eol=lf", atributos)


if __name__ == "__main__":
    unittest.main()
