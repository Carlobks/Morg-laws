"""Permissões do agente em três colunas (Morg-laws; skill auditoria-de-seguranca, seção 8).

- **deny** (nunca): ler segredos (`.env`, chaves, credenciais, a lista negra fora do repositório);
- **ask** (pergunta antes): push, PR, instalar pacotes ou programas, mexer nas próprias regras de segurança;
- **allow** (sem perguntar): só leitura e o comando de testes.
As regras vivem em `.claude/settings.json` (vai no repositório, vale para quem o clonar). As de cada máquina ficam
em `.claude/settings.local.json`, que só pode apertar. O `ask` sozinho não pergunta no modo automático: o hook
`perguntar_antes.py` é que obriga (modelo em modelos/claude/ do Morg-laws).
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import json
import re
import unittest

from carregar_por_caminho import RAIZ

# Ajuste ao projeto.
NUNCA = {"Read(**/.env)", "Read(**/.env.*)", "Read(**/*.pem)", "Read(**/*.key)", "Read(~/.ssh/**)",
         "Read(~/.claude/.credentials.json)", "Read(~/.config/morg-laws/**)"}
PERGUNTA = {"Bash(git push)", "Bash(git push *)", "Bash(gh pr create*)", "Bash(gh pr merge*)",
            "Bash(npm install *)", "Bash(npx *)", "Bash(pip install *)",
            "Edit(.claude/settings.json)", "Edit(.claude/hooks/**)", "Edit(.githooks/**)"}
HOOKS_OBRIGATORIOS = ("guarda_do_git.py", "bloquear_segredos.py", "perguntar_antes.py")

# O que nunca pode estar em "allow": publica (push, PR), instala, apaga, salta os portões ou abre tudo.
PERIGOSO = re.compile(r"push|install|\bnpx\b|\brm\b|Remove-Item|--no-verify|reset --hard|^\w+\(\*\)$"
                      r"|\bpy(?:thon\d?)?(?:\.exe)? (?:-\w+ )*-\)"  # Python lido do stdin: roda qualquer código
                      r"|\bgh pr (?:\*|create|merge|close|edit|comment|review|ready)", re.IGNORECASE)


def configuracao(nome):
    caminho = RAIZ / ".claude" / nome
    return json.loads(caminho.read_text(encoding="utf-8")) if caminho.is_file() else {}


def permissoes(nome):
    return configuracao(nome).get("permissions", {})


class TresColunas(unittest.TestCase):

    def test_nunca_le_segredos(self):
        self.assertEqual(NUNCA - set(permissoes("settings.json").get("deny", [])), set())

    def test_pergunta_antes_do_que_nao_tem_volta(self):
        self.assertEqual(PERGUNTA - set(permissoes("settings.json").get("ask", [])), set())

    def test_allow_so_tem_leituras_e_testes(self):
        for nome in ("settings.json", "settings.local.json"):
            for regra in permissoes(nome).get("allow", []):
                with self.subTest(arquivo=nome, regra=regra):
                    self.assertIsNone(PERIGOSO.search(regra), "isto pertence à coluna ask ou deny")

    def test_o_local_nao_desfaz_o_deny_nem_o_ask(self):
        projeto = permissoes("settings.json")
        local_allow = set(permissoes("settings.local.json").get("allow", []))
        self.assertEqual(local_allow & (set(projeto.get("deny", [])) | set(projeto.get("ask", []))), set())

    def test_o_modo_que_salta_as_permissoes_esta_desligado(self):
        # Sem isto, o modo "bypass" ignora o deny, o ask e os hooks de uma vez.
        self.assertEqual(permissoes("settings.json").get("disableBypassPermissionsMode"), "disable")

    def test_os_hooks_estao_ligados_e_travam_se_falharem(self):
        comandos = json.dumps(configuracao("settings.json").get("hooks", {}))
        for hook in HOOKS_OBRIGATORIOS:
            with self.subTest(hook=hook):
                self.assertIn(hook, comandos)
        # Um hook que quebra e deixa passar é uma barreira que some sem ninguém ver.
        self.assertEqual(comandos.count('"type": "command"'), comandos.count('"onFailure": "block"'))

    def test_segredos_tambem_fora_do_git(self):
        ignorados = (RAIZ / ".gitignore").read_text(encoding="utf-8").splitlines()
        for padrao in (".env", ".env.*", "*.pem", "*.key"):
            with self.subTest(padrao=padrao):
                self.assertIn(padrao, ignorados)


if __name__ == "__main__":
    unittest.main()
