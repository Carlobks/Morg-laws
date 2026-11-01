"""O settings.json modelo liga cada hook do agente, e cada um bloqueia também se ele próprio falhar."""

import json
import re
import unittest

from carregar_modelos import MODELOS, PASTA_HOOKS

SETTINGS = json.loads((MODELOS / "claude" / "settings.json").read_text(encoding="utf-8"))


def hooks_ligados():
    return [hook for grupo in SETTINGS["hooks"]["PreToolUse"] for hook in grupo["hooks"]]


class LigacaoNoSettings(unittest.TestCase):

    def test_cada_hook_existe_e_bloqueia_se_falhar(self):
        for hook in hooks_ligados():
            nome = re.search(r"\.claude/hooks/(\w+\.py)", hook["command"]).group(1)
            with self.subTest(hook=nome):
                self.assertTrue((PASTA_HOOKS / nome).is_file())
                self.assertEqual(hook.get("onFailure"), "block", "sem onFailure: block, um hook partido deixa passar")
                self.assertIn('-I "$r/.claude/hooks/', hook["command"], "Python sempre isolado")

    def test_todos_os_hooks_da_pasta_estao_ligados(self):
        ligados = {re.search(r"(\w+\.py)", hook["command"]).group(1) for hook in hooks_ligados()}
        self.assertEqual(ligados, {caminho.name for caminho in PASTA_HOOKS.glob("*.py")})

    def test_o_modo_que_salta_as_permissoes_esta_desligado(self):
        # O test_permissoes.py modelo confere o resto deste settings.json no projeto de exemplo
        # (test_exemplo_com_os_modelos.py).
        self.assertEqual(SETTINGS["permissions"]["disableBypassPermissionsMode"], "disable")


if __name__ == "__main__":
    unittest.main()
