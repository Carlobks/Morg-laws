"""Hook lembrar_o_handoff (modelos/claude/hooks/lembrar_o_handoff.py): o /compact manual sem handoff gravado para."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from carregar_modelos import PASTA_HOOKS, carregar_hook, correr_como_script

lembrete = carregar_hook("lembrar_o_handoff")
HOOK_DO_LEMBRETE = PASTA_HOOKS / "lembrar_o_handoff.py"
AUTORIA_FALSA = {"GIT_AUTHOR_NAME": "Teste", "GIT_AUTHOR_EMAIL": "teste@example.com",
                 "GIT_COMMITTER_NAME": "Teste", "GIT_COMMITTER_EMAIL": "teste@example.com"}
HANDOFF = ".context/HANDOFF-exemplo.md"


def git_no_temporario(pasta, *argumentos, check=True):
    return subprocess.run(["git", *argumentos], cwd=pasta, capture_output=True, text=True, encoding="utf-8",
                          check=check, env={**os.environ, **AUTORIA_FALSA})


def commitar_sem_hooks(pasta):
    """Commita tudo o que está no disco pela canalização do git, que não roda os hooks de quem testa."""
    git_no_temporario(pasta, "add", "--", ".")
    arvore = git_no_temporario(pasta, "write-tree").stdout.strip()
    pai = git_no_temporario(pasta, "rev-parse", "--verify", "-q", "HEAD", check=False).stdout.strip()
    extra = ["-p", pai] if pai else []
    novo = git_no_temporario(pasta, "commit-tree", arvore, *extra, "-m", "teste").stdout.strip()
    git_no_temporario(pasta, "update-ref", "HEAD", novo)


def repositorio_temporario(caso):
    """Um repositório git novo, apagado no fim do teste."""
    pasta = Path(caso.enterContext(tempfile.TemporaryDirectory()))
    git_no_temporario(pasta, "init", "-q")
    return pasta


def gravar_texto(caminho, texto="# Handoff\n"):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding="utf-8")


def compactar(cwd, texto, trigger="manual"):
    pedido = {"hook_event_name": "PreCompact", "trigger": trigger, "custom_instructions": texto, "cwd": str(cwd)}
    return correr_como_script(HOOK_DO_LEMBRETE, json.dumps(pedido).encode("utf-8"))


class NoRepositorio(unittest.TestCase):

    def setUp(self):
        self.pasta = repositorio_temporario(self)
        gravar_texto(self.pasta / HANDOFF)
        gravar_texto(self.pasta / "src" / "a.py", "x = 1\n")
        commitar_sem_hooks(self.pasta)

    def test_com_o_handoff_commitado_passa(self):
        self.assertEqual(compactar(self.pasta, f"Leia o {HANDOFF} e continue"), (0, "", ""))

    def test_o_cwd_numa_subpasta_resolve_contra_a_raiz(self):
        self.assertEqual(compactar(self.pasta / "src", f"Leia o {HANDOFF}"), (0, "", ""))

    def test_o_caminho_absoluto_tambem_vale(self):
        self.assertEqual(compactar(self.pasta, f"Leia `{self.pasta / HANDOFF}`."), (0, "", ""))

    def test_para_sem_um_handoff_gravado(self):
        gravar_texto(self.pasta / ".context" / "HANDOFF-novo.md")
        casos = {
            "sem texto": "",
            "sem citar handoff": "resuma a conversa",
            "o colchete por preencher": "Leia o .context/HANDOFF-<assunto>.md",
            "um que não existe": "Leia o .context/HANDOFF-outro.md",
            "um nunca commitado": "Leia o .context/HANDOFF-novo.md",
        }
        for caso, texto in casos.items():
            with self.subTest(caso=caso):
                codigo, saida, erro = compactar(self.pasta, texto)
                self.assertEqual((codigo, saida), (2, ""))
                self.assertIn("não compacte", erro)

    def test_a_citacao_entre_colchetes_vale(self):
        # O modelo da skill põe os caminhos numa lista entre colchetes: o primeiro não pode sair com o «[» colado.
        segundo = ".context/HANDOFF-outro.md"
        for texto in (f"arquivos ativos: [{HANDOFF}, {segundo}]", f"[{HANDOFF}].", f"([{HANDOFF}])"):
            with self.subTest(texto=texto):
                self.assertEqual(compactar(self.pasta, texto), (0, "", ""))

    def test_a_marca_de_saida_nao_depende_de_maiusculas(self):
        for texto in ("Sem Handoff, só resumir", "SEM HANDOFF"):
            with self.subTest(texto=texto):
                self.assertEqual(compactar(self.pasta, texto), (0, "", ""))

    def test_para_com_mudancas_por_commitar(self):
        gravar_texto(self.pasta / HANDOFF, "# Handoff\n\nMudou.\n")
        self.assertEqual(compactar(self.pasta, f"Leia o {HANDOFF}")[0], 2)

    def test_a_marca_de_saida_e_a_automatica_passam(self):
        self.assertEqual(compactar(self.pasta, "Conversa curta, sem handoff."), (0, "", ""))
        self.assertEqual(compactar(self.pasta, "", trigger="auto"), (0, "", ""))


class PastaIgnorada(unittest.TestCase):

    def setUp(self):
        self.pasta = repositorio_temporario(self)
        gravar_texto(self.pasta / ".gitignore", ".context/\n")

    def test_o_arquivo_so_no_disco_basta(self):
        gravar_texto(self.pasta / HANDOFF)
        commitar_sem_hooks(self.pasta)
        self.assertEqual(compactar(self.pasta, f"Leia o {HANDOFF}"), (0, "", ""))

    def test_um_handoff_ja_rastreado_exige_o_commit(self):
        gravar_texto(self.pasta / HANDOFF)
        git_no_temporario(self.pasta, "add", "-f", "--", HANDOFF)
        commitar_sem_hooks(self.pasta)
        self.assertEqual(compactar(self.pasta, f"Leia o {HANDOFF}"), (0, "", ""))
        gravar_texto(self.pasta / HANDOFF, "# Handoff\n\nMudou.\n")
        self.assertEqual(compactar(self.pasta, f"Leia o {HANDOFF}")[0], 2)


class SemGit(unittest.TestCase):

    def test_basta_o_arquivo_existir(self):
        pasta = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.assertEqual(compactar(pasta, f"Leia o {HANDOFF}")[0], 2)
        gravar_texto(pasta / HANDOFF)
        self.assertEqual(compactar(pasta, f"Leia o {HANDOFF}"), (0, "", ""))

    def test_sem_o_programa_git_e_como_fora_de_um_repositorio(self):
        with mock.patch.object(lembrete.subprocess, "run", side_effect=FileNotFoundError):
            self.assertIsNone(lembrete.raiz_do_git(Path(".")))

    def test_sem_cwd_usa_a_pasta_atual(self):
        self.assertTrue(lembrete.deve_parar({"trigger": "manual", "custom_instructions": None}))


class HookQuebrado(unittest.TestCase):

    def correr_isolado(self, entrada):
        return subprocess.run([sys.executable, "-I", str(HOOK_DO_LEMBRETE)], input=entrada, capture_output=True,
                              text=True, encoding="utf-8", check=False, timeout=30)

    def test_no_python_isolado_de_verdade_para_com_2(self):
        resultado = self.correr_isolado(json.dumps({"trigger": "manual", "custom_instructions": "", "cwd": "."}))
        self.assertEqual(resultado.returncode, 2)
        self.assertIn("Compactação parada (Morg-laws)", resultado.stderr)

    def test_a_excecao_sai_com_outro_codigo_que_o_continue_deixa_passar(self):
        resultado = self.correr_isolado("isto não é JSON")
        self.assertNotIn(resultado.returncode, (0, 2))
        self.assertIn("Traceback", resultado.stderr)


if __name__ == "__main__":
    unittest.main()
