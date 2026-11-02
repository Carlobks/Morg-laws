"""Hook perguntar_antes (modelos/claude/hooks/perguntar_antes.py): push, PR e instalações pedem sempre o "sim".

Num projeto real, com a regra "ask" de `Bash(git push *)` no settings.json, um `git push --dry-run` rodou sem
pergunta (modo automático). O hook devolve a decisão "ask" ao Claude Code, que pergunta seja qual for o modo.
"""

import json
import subprocess
import sys
import unittest

from carregar_modelos import PASTA_HOOKS, carregar_hook, correr_como_script

perguntar = carregar_hook("perguntar_antes")


class Decisao(unittest.TestCase):

    def test_pergunta_antes_de_publicar_ou_instalar(self):
        for comando in ['cd "C:/x y"; git push --dry-run C:/b.git HEAD:refs/heads/t', "git push origin main",
                        'git -C "C:/a b" push', "git -c x=y push --tags", "npm install", "npm i -D x", "npm ci",
                        "npx skills@1.7.4 add a/b", "pip install coverage", "py -m pip install ruff",
                        "winget install Gitleaks.Gitleaks", "Install-Module Pester -Force", "choco install x",
                        "scoop install x", "x && git.exe push",
                        "gh pr create --fill", "gh pr merge 3 --squash", "gh.exe pr create", "gh release create v1"]:
            with self.subTest(comando=comando):
                self.assertIsNotNone(perguntar.motivo_para_perguntar(comando))

    def test_pergunta_com_opcoes_globais_e_antes_de_escrever_no_github(self):
        # Comentar, aprovar ou editar uma PR também é público; e uma opção global do git não esconde o push.
        for comando in ["git --no-pager push", "git -P push origin", "git --git-dir=.git --work-tree=. push",
                        "git -c a=b --no-pager -C x push", "gh pr review 1 --approve", "gh pr comment 1 --body x",
                        "gh pr edit 1 --title x", "gh pr close 1", "gh pr ready 1", "gh pr reopen 1",
                        "gh issue create --title x", "gh issue comment 2 --body x", "gh issue close 2",
                        "gh release upload v1 a.zip", "gh release edit v1", "gh api -X POST repos/o/r/issues",
                        "gh api --method=PATCH repos/o/r", "gh api --method DELETE repos/o/r/x",
                        "gh api repos/o/r/issues -f title=x", "gh api graphql -F query=@q.graphql",
                        "gh api repos/o/r/x --input corpo.json", "x; gh.exe api -XPUT repos/o/r/y"]:
            with self.subTest(comando=comando):
                self.assertIsNotNone(perguntar.motivo_para_perguntar(comando))

    def test_nao_pergunta_nas_leituras_do_github(self):
        for comando in ["gh api repos/o/r/pulls", "gh api -X GET repos/o/r", "gh api --method get search -f q=x",
                        "gh issue view 2", "gh issue list", "gh pr diff 3", "git --no-pager log --grep push",
                        "git -C pasta status && echo push"]:
            with self.subTest(comando=comando):
                self.assertIsNone(perguntar.motivo_para_perguntar(comando))

    def test_nao_pergunta_o_resto(self):
        for comando in ["git status", "git log --grep push", "git commit -F m -- a.py", "npm audit --json",
                        "npm --version", "pip list", "winget show Gitleaks.Gitleaks", "Get-Module Pester",
                        "gh pr view 3", "gh pr list", "gh run view 1 --log-failed", "gh release view v1", ""]:
            with self.subTest(comando=comando):
                self.assertIsNone(perguntar.motivo_para_perguntar(comando))


class RegrasDoProprioAgente(unittest.TestCase):
    """O agente não muda as próprias regras de segurança sem o "sim" do dono."""

    def test_pergunta_ao_editar_as_regras(self):
        raiz = perguntar.RAIZ
        for caminho in [raiz / ".claude" / "settings.json", raiz / ".claude" / "settings.local.json",
                        raiz / ".claude" / "hooks" / "guarda_do_git.py", raiz / ".githooks" / "pre-commit",
                        str(raiz / ".claude" / "hooks" / "novo.py").replace("\\", "/")]:
            with self.subTest(caminho=str(caminho)):
                self.assertIsNotNone(perguntar.motivo_para_perguntar_arquivo(str(caminho)))

    def test_nao_pergunta_nos_outros_arquivos(self):
        for caminho in [perguntar.RAIZ / "scripts" / "testar.sh", perguntar.RAIZ / "docs" / "README.md",
                        perguntar.RAIZ.parent.parent / ".claude" / "settings.json", ""]:
            with self.subTest(caminho=str(caminho)):
                self.assertIsNone(perguntar.motivo_para_perguntar_arquivo(str(caminho)))


class ComoHook(unittest.TestCase):

    def correr(self, valor, ferramenta="Bash"):
        entrada = {"file_path": valor} if ferramenta in ("Write", "Edit") else {"command": valor}
        pedido = json.dumps({"tool_name": ferramenta, "tool_input": entrada}).encode("utf-8")
        return correr_como_script(PASTA_HOOKS / "perguntar_antes.py", pedido)

    def test_devolve_a_decisao_ask_com_o_motivo(self):
        codigo, saida, _ = self.correr("git push origin main")
        self.assertEqual(codigo, 0)
        decisao = json.loads(saida)["hookSpecificOutput"]
        self.assertEqual((decisao["hookEventName"], decisao["permissionDecision"]), ("PreToolUse", "ask"))
        self.assertIn("push", decisao["permissionDecisionReason"])

    def test_no_edit_das_regras_tambem_pergunta(self):
        _, saida, _ = self.correr(str(perguntar.RAIZ / ".claude" / "settings.json"), "Edit")
        self.assertIn(".claude/settings.json", json.loads(saida)["hookSpecificOutput"]["permissionDecisionReason"])

    def test_sem_motivo_nao_diz_nada(self):
        self.assertEqual(self.correr("git status"), (0, "", ""))
        self.assertEqual(self.correr(str(perguntar.RAIZ / "README.md"), "Write"), (0, "", ""))

    def test_no_python_isolado_de_verdade(self):
        resultado = subprocess.run([sys.executable, "-I", str(PASTA_HOOKS / "perguntar_antes.py")],
                                   input=json.dumps({"tool_name": "Bash", "tool_input": {"command": "git push"}}),
                                   capture_output=True, text=True, encoding="utf-8", check=False, timeout=30)
        self.assertEqual(json.loads(resultado.stdout)["hookSpecificOutput"]["permissionDecision"], "ask")


if __name__ == "__main__":
    unittest.main()
