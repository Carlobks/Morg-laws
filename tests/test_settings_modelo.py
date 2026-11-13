"""O settings.json modelo liga cada hook do agente: os que vigiam o agente travam se falharem, os outros não param nada."""

import json
import re
import unittest

from carregar_modelos import MODELOS, PASTA_HOOKS

SETTINGS = json.loads((MODELOS / "claude" / "settings.json").read_text(encoding="utf-8"))
# Os hooks fora do PreToolUse: o evento e o matcher de cada um. Um hook quebrado aqui não pode parar a compactação.
FORA_DO_PRE_TOOL_USE = {"lembrar_o_handoff.py": ("PreCompact", "manual")}


def hooks_ligados():
    """(evento, matcher, hook) de cada hook ligado, em todos os eventos."""
    return [(evento, grupo.get("matcher"), hook) for evento, grupos in SETTINGS["hooks"].items()
            for grupo in grupos for hook in grupo["hooks"]]


def nome_do_hook(hook):
    return re.search(r"\.claude/hooks/(\w+\.py)", hook["command"]).group(1)


class LigacaoNoSettings(unittest.TestCase):

    def test_cada_hook_existe_e_roda_isolado(self):
        for _, _, hook in hooks_ligados():
            with self.subTest(hook=nome_do_hook(hook)):
                self.assertTrue((PASTA_HOOKS / nome_do_hook(hook)).is_file())
                self.assertIn('-I "$r/.claude/hooks/', hook["command"], "Python sempre isolado")

    def test_os_que_vigiam_o_agente_travam_se_falharem(self):
        for evento, _, hook in hooks_ligados():
            esperado = "block" if evento == "PreToolUse" else "continue"
            with self.subTest(hook=nome_do_hook(hook), evento=evento):
                self.assertEqual(hook.get("onFailure"), esperado,
                                 "no PreToolUse, um hook partido deixa passar; nos outros, pararia o trabalho")

    def test_os_de_fora_do_pre_tool_use_no_evento_certo(self):
        ligados = {nome_do_hook(hook): (evento, matcher) for evento, matcher, hook in hooks_ligados()
                   if evento != "PreToolUse"}
        self.assertEqual(ligados, FORA_DO_PRE_TOOL_USE)

    def test_todos_os_hooks_da_pasta_estao_ligados(self):
        ligados = {nome_do_hook(hook) for _, _, hook in hooks_ligados()}
        self.assertEqual(ligados, {caminho.name for caminho in PASTA_HOOKS.glob("*.py")})

    def test_o_modo_que_salta_as_permissoes_esta_desligado(self):
        # O test_permissoes.py modelo confere o resto deste settings.json no projeto de exemplo
        # (test_exemplo_com_os_modelos.py).
        self.assertEqual(SETTINGS["permissions"]["disableBypassPermissionsMode"], "disable")

    def test_o_molde_vem_sem_o_deny_dos_sub_agentes(self):
        # Mensagem rápida do que o projeto de exemplo já prova (test_exemplo_com_os_modelos.py): com SO_SESSOES = False,
        # o test_permissoes.py copiado falharia se o molde trouxesse "Agent" no deny.
        self.assertNotIn("Agent", SETTINGS["permissions"]["deny"])


if __name__ == "__main__":
    unittest.main()
