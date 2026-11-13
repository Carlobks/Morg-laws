"""Hook retomar_pelo_handoff (modelos/claude/hooks/retomar_pelo_handoff.py): depois de compactar, leia o handoff."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from carregar_modelos import PASTA_HOOKS, carregar_hook, correr_como_script
from test_lembrar_o_handoff import commitar_sem_hooks, gravar_texto, repositorio_temporario

retomada = carregar_hook("retomar_pelo_handoff")
HOOK_DA_RETOMADA = PASTA_HOOKS / "retomar_pelo_handoff.py"


def comecar_sessao(cwd, source="compact"):
    pedido = {"hook_event_name": "SessionStart", "source": source, "cwd": str(cwd)}
    return correr_como_script(HOOK_DA_RETOMADA, json.dumps(pedido).encode("utf-8"))


def contexto_do_agente(saida):
    """O additionalContext do JSON de saída, no lugar que o SessionStart lê."""
    especifico = json.loads(saida)["hookSpecificOutput"]
    assert especifico["hookEventName"] == "SessionStart"
    return especifico["additionalContext"]


class Retomada(unittest.TestCase):

    def setUp(self):
        self.pasta = repositorio_temporario(self)

    def test_sem_handoff_nao_diz_nada(self):
        self.assertEqual(comecar_sessao(self.pasta), (0, "", ""))
        (self.pasta / ".context").mkdir()
        self.assertEqual(comecar_sessao(self.pasta), (0, "", ""))

    def test_com_dois_lista_os_dois_e_manda_perguntar(self):
        gravar_texto(self.pasta / ".context" / "HANDOFF-caixa.md")
        gravar_texto(self.pasta / ".context" / "HANDOFF-folha.md")
        gravar_texto(self.pasta / "src" / "a.py", "x = 1\n")
        commitar_sem_hooks(self.pasta)
        codigo, saida, erro = comecar_sessao(self.pasta / "src")
        texto = contexto_do_agente(saida)
        self.assertEqual((codigo, erro), (0, ""))
        self.assertIn(".context/HANDOFF-caixa.md (último commit ", texto)
        self.assertIn(".context/HANDOFF-folha.md (último commit ", texto)
        self.assertIn("pergunte", texto)
        self.assertNotIn("continue", texto.lower())

    def test_a_data_do_commit_vem_no_fuso_da_maquina(self):
        # Um commit de quem está em -03:00 (10:00 lá) aparece às 13:00 numa máquina em UTC, como a hora do arquivo.
        gravar_texto(self.pasta / ".context" / "HANDOFF-caixa.md")
        with mock.patch.dict(os.environ, {"GIT_COMMITTER_DATE": "2026-11-13T10:00:00-03:00", "TZ": "UTC"}):
            commitar_sem_hooks(self.pasta)
            texto = contexto_do_agente(comecar_sessao(self.pasta)[1])
        self.assertIn(".context/HANDOFF-caixa.md (último commit 2026-11-13 13:00)", texto)

    def test_na_pasta_ignorada_sem_commit_traz_a_hora_do_arquivo(self):
        gravar_texto(self.pasta / ".gitignore", ".context/\n")
        gravar_texto(self.pasta / ".context" / "HANDOFF-caixa.md")
        commitar_sem_hooks(self.pasta)
        os.utime(self.pasta / ".context" / "HANDOFF-caixa.md", (1767268800, 1767268800))  # 2026-01-01 12:00 UTC
        texto = contexto_do_agente(comecar_sessao(self.pasta)[1])
        self.assertIn(".context/HANDOFF-caixa.md (sem commit; arquivo de 2026-01-0", texto)
        self.assertNotIn("último commit", texto)

    def test_outra_origem_nao_diz_nada(self):
        gravar_texto(self.pasta / ".context" / "HANDOFF-caixa.md")
        for origem in ("startup", "resume", "clear"):
            with self.subTest(origem=origem):
                self.assertEqual(comecar_sessao(self.pasta, origem), (0, "", ""))


class SemGitNaRetomada(unittest.TestCase):

    def test_fora_de_um_repositorio_usa_o_cwd(self):
        pasta = Path(self.enterContext(tempfile.TemporaryDirectory()))
        gravar_texto(pasta / ".context" / "HANDOFF-caixa.md")
        self.assertIn("HANDOFF-caixa.md (sem commit; arquivo de ", contexto_do_agente(comecar_sessao(pasta)[1]))

    def test_sem_o_programa_git(self):
        with mock.patch.object(retomada.subprocess, "run", side_effect=FileNotFoundError):
            self.assertEqual(retomada.git_da_retomada(Path("."), "status"), "")

    def test_no_python_isolado_de_verdade(self):
        pasta = Path(self.enterContext(tempfile.TemporaryDirectory()))
        gravar_texto(pasta / ".context" / "HANDOFF-caixa.md")
        resultado = subprocess.run([sys.executable, "-I", str(HOOK_DA_RETOMADA)], capture_output=True, text=True,
                                   input=json.dumps({"source": "compact", "cwd": str(pasta)}), encoding="utf-8",
                                   check=False, timeout=30)
        self.assertEqual(resultado.returncode, 0)
        self.assertIn("A conversa foi compactada.", contexto_do_agente(resultado.stdout))

    def test_sem_cwd_usa_a_pasta_atual(self):
        self.assertEqual(comecar_sessao("", source="compact")[0], 0)


if __name__ == "__main__":
    unittest.main()
