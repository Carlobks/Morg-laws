"""As metas da narrativa (`scripts/metas-da-narrativa.py`, A1 a A4): só avisam. Cada meta tem um capítulo que a cumpre (sem aviso)
e um que a falha (com aviso), e o script sai sempre com 0."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from carregar_modelos import RAIZ

SCRIPT = RAIZ / "scripts" / "metas-da-narrativa.py"
especificacao = importlib.util.spec_from_file_location("metas_da_narrativa", SCRIPT)
metas = importlib.util.module_from_spec(especificacao)
especificacao.loader.exec_module(metas)

MARCA = "<!--raw-typst #marca-de-par() -->\n"
PROSA = "Eu decidi, em março de 2026, que a minha pasta seria só minha. " + "Eu vi a minha pasta no texto. " * 450
BOM = "# Um capítulo\n\n" + PROSA + "\n\n> Uma frase que fica.\n"


def avisos(**capitulos):
    return metas.avisos_dos_capitulos({f"{nome}.md": texto for nome, texto in capitulos.items()})


class AsMetas(unittest.TestCase):

    def test_um_capitulo_que_cumpre_tudo_nao_tem_aviso(self):
        self.assertEqual(avisos(a=BOM, b=BOM), [])

    def test_a1_primeira_pessoa_abaixo_de_5_por_mil_avisa(self):
        pouco = "# C\n\nEm 2026 a pasta nasceu. " + "A pasta é do texto. " * 900 + "\n\n> Síntese.\n"
        self.assertTrue(any(a.startswith("A1 a.md") for a in avisos(a=pouco)))
        self.assertFalse(any(a.startswith("A1") for a in avisos(a=BOM)))
        self.assertEqual(metas.avisos_dos_capitulos({"vazio.md": ""})[0][:2], "A1")

    def test_a2_a_primeira_frase_sem_mes_ano_nem_episodio_avisa(self):
        sem = BOM.replace("Eu decidi, em março de 2026, que a minha pasta seria só minha.", "A pasta é uma pasta.")
        self.assertTrue(any(a.startswith("A2 a.md") for a in avisos(a=sem)))
        com_ano = BOM.replace("Eu decidi, em março de 2026, que a minha pasta seria só minha.", "Em 2026 a pasta nasceu.")
        self.assertFalse(any(a.startswith("A2") for a in avisos(a=com_ano)))
        so_eu = BOM.replace("em março de 2026, ", "")
        self.assertFalse(any(a.startswith("A2") for a in avisos(a=so_eu)))
        self.assertEqual(metas.primeira_frase(["# Título", "> citação", ""]), "")

    def test_a3_sem_frase_sintese_em_destaque_avisa(self):
        self.assertTrue(any(a.startswith("A3 a.md") for a in avisos(a=BOM.replace("> Uma frase", "Uma frase"))))
        self.assertFalse(any(a.startswith("A3") for a in avisos(a=BOM)))

    def test_a4_menos_de_3_paginas_ou_mais_de_3_vezes_a_media_avisa(self):
        curto = "# C\n\nEm 2026 eu escrevi isto.\n\n> Síntese.\n"
        achados = avisos(a=BOM, b=curto)
        self.assertTrue(any(a.startswith("A4 b.md") and "mínimo" in a for a in achados))
        enorme = BOM + ("Mais palavras aqui. " * 12000)
        achados = avisos(a=BOM, b=BOM, c=BOM, d=BOM, e=BOM, f=enorme)
        self.assertTrue(any(a.startswith("A4 f.md") and "vezes a média" in a for a in achados))
        self.assertEqual([a for a in achados if a.startswith("A4") and "a.md" in a], [])

    def test_os_pares_contam_duas_paginas_cada_e_o_marcador_nao_conta_palavras(self):
        com_par = BOM + MARCA + "## Par\n\n### Na prática\n\nTexto.\n\n### Por quê\n\nTexto.\n"
        self.assertAlmostEqual(metas.paginas_estimadas(com_par.splitlines()) - metas.paginas_estimadas(BOM.splitlines()), 2, delta=0.1)
        self.assertEqual(metas.prosa(MARCA + "```\nx\n```\nfica\n"), ["fica"])

    def test_o_script_imprime_e_sai_sempre_com_0(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "manual").mkdir()
            (raiz / "manual" / "cap-01-x.md").write_text("# C\n\nSem nada.\n", encoding="utf-8")
            self.assertEqual(metas.principal(raiz), 0)
        feito = subprocess.run([sys.executable, "-I", str(SCRIPT)], check=False, capture_output=True, text=True,
                               encoding="utf-8")
        self.assertEqual(feito.returncode, 0)
        self.assertIn("metas da narrativa", feito.stdout)

    def test_um_erro_dentro_do_script_nao_muda_a_saida_0(self):
        copia = Path(tempfile.mkdtemp(prefix="morg-metas-")) / "scripts"
        copia.mkdir()
        (copia / "metas-da-narrativa.py").write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
        (copia.parent / "manual").mkdir()
        (copia.parent / "manual" / "cap-01-x.md").write_bytes(b"\xff\xfe\x00 invalido")
        feito = subprocess.run([sys.executable, "-I", str(copia / "metas-da-narrativa.py")], check=False, capture_output=True,
                               text=True, encoding="utf-8")
        self.assertEqual(feito.returncode, 0)
        self.assertIn("não correram", feito.stdout)


if __name__ == "__main__":
    unittest.main()
