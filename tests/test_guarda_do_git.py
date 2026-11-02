"""Guarda do git (modelos/claude/hooks/guarda_do_git.py): o agente não salta nem desliga os portões do git."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from carregar_modelos import PASTA_HOOKS, carregar_hook, correr_como_script
from projeto_de_exemplo import apagar, git

guarda = carregar_hook("guarda_do_git")


def hooks_certos():
    return ".githooks"


class Recusa(unittest.TestCase):

    def assertRecusa(self, comandos, texto, hooks_path=hooks_certos):
        for comando in comandos:
            with self.subTest(comando=comando):
                motivo = guarda.motivo_para_bloquear(comando, hooks_path)
                self.assertIsNotNone(motivo)
                self.assertIn(texto, motivo)

    def test_saltar_os_hooks(self):
        self.assertRecusa(['git commit --no-verify -F m.txt', 'git commit -n -F m.txt', 'git commit -qn -F m',
                           'git -C "C:/a b" commit --no-verify -F m', 'git push --no-verify',
                           'git merge --no-verify main'], "--no-verify")

    def test_mudar_ou_desligar_o_hooks_path(self):
        self.assertRecusa(['git config core.hooksPath /dev/null', 'git config --unset core.hooksPath',
                           'git config --local core.hooksPath x', 'git -c core.hooksPath=x commit -F m',
                           'git config core.hookspath ""'], "core.hooksPath")

    def test_commit_com_o_hooks_path_errado(self):
        self.assertRecusa(['git commit -F m.txt -- a.py'], "não é .githooks", hooks_path=lambda: "")

    def test_preparar_tudo(self):
        self.assertRecusa(["git add -A", "git add .", "git add --all", "git add -Av", "git add :/",
                           "git commit -a -F m", "git commit -am x", "git commit --all -F m",
                           "git commit -F m -- .", "cd x && git add . && git commit -F m"], "caminho")

    def test_preparar_todos_os_seguidos(self):
        # -u prepara de uma vez todos os arquivos já seguidos, também os que outra sessão mudou na mesma pasta.
        # Só passam as opções conhecidas por não alargar o que se prepara: uma opção nova cai aqui.
        self.assertRecusa(["git add -u", "git add --update", "git add -uv", "git add -vu", "git add -u -- a.py",
                           "git -C pasta add --update", "git add --pathspec-from-file=lista.txt",
                           "git add -p", "git add --no-ignore-removal"], "caminho")

    def test_commit_sem_caminhos(self):
        # Um commit sem caminhos leva o que outra sessão deixou preparado.
        self.assertRecusa(["git commit -F m.txt", "git commit --amend -F m.txt", "git commit -q -F m && git log"],
                          "por caminho")

    def test_saltar_os_testes_com_a_marca(self):
        self.assertRecusa(["MORG_A_TESTAR=1 git commit -F m -- a.py", "$env:MORG_A_TESTAR='1'; git commit -F m -- a",
                           "set MORG_A_TESTAR=1&& git commit -F m -- a"], "MORG_A_TESTAR")

    def test_mensagem_com_varias_linhas(self):
        # Com caminhos: sem eles a recusa viria da regra "sem caminhos" e o teste passaria sem chegar aqui.
        self.assertRecusa(['git commit -m "título\n\ncorpo" -- a.txt', 'git commit --message="a\nb" -- a.txt',
                           "git commit -m \"$(cat <<'EOF'\nx\nEOF\n)\" -- a.txt", 'git commit -qm "a\nb" -- a.txt'],
                          "várias linhas")

    def test_stash(self):
        self.assertRecusa(["git stash", "git stash push -m x", "git stash -u", "git stash pop", "git stash drop",
                           "x && git stash apply"], "stash")


class DeixaPassar(unittest.TestCase):

    def test_comandos_normais(self):
        lido = mock.Mock(return_value=".githooks")
        for comando in ['git add -- a.py "b c.md"', 'git commit -F m.txt -- a.py', 'git commit -m "uma linha" a.py',
                        'git config --get core.hooksPath', 'git config core.hooksPath',
                        'git config core.hooksPath .githooks', 'git push -n origin main', 'git status --short -uall',
                        'git log --oneline -5', 'git commit --amend -F m.txt -- a.py', "echo 'sem aspas fechadas",
                        'git commit -F m --author "Ana <a@example.com>" -- a.py', 'git commit -C HEAD -- a.py',
                        'git commit -F m -- -arquivo-com-hifen.py', 'git -C pasta --no-pager log', 'ls -la',
                        'git stash list', 'git stash show -p stash@{0}', '', 'git add a.py', 'git add -v -- a.py',
                        'git add --chmod=+x -- .githooks/pre-commit', 'git add -N -- novo.py', 'git add -f -- x.log',
                        'git add --dry-run -- a.py']:
            with self.subTest(comando=comando):
                self.assertIsNone(guarda.motivo_para_bloquear(comando, lido))

    def test_commit_que_fecha_um_merge_vai_sem_caminhos(self):
        with mock.patch.object(guarda, "merge_em_curso", return_value=True):
            self.assertIsNone(guarda.motivo_para_bloquear("git commit -F m.txt", hooks_certos))

    def test_fora_de_um_repositorio_nao_ha_merge(self):
        pasta = Path(tempfile.mkdtemp(prefix="morg-sem-git-"))
        self.addCleanup(apagar, pasta)
        self.assertFalse(guarda.merge_em_curso(pasta))

    def test_merge_em_curso_num_worktree(self):
        # Num worktree o .git é um arquivo e o MERGE_HEAD fica na pasta do worktree dentro do repositório principal.
        principal = Path(tempfile.mkdtemp(prefix="morg-merge-"))
        self.addCleanup(apagar, principal)
        git(principal, "init", "-q", "-b", "main")
        arvore_vazia = git(principal, "write-tree").stdout.strip()
        commit = git(principal, "-c", "user.name=Ana", "-c", "user.email=a@example.com", "commit-tree", arvore_vazia,
                     "-m", "x").stdout.strip()
        git(principal, "update-ref", "refs/heads/main", commit)
        git(principal, "worktree", "add", "-q", "-b", "outro", str(principal / "arvore"))
        arvore = principal / "arvore"
        self.assertFalse(guarda.merge_em_curso(arvore))
        merge_head = Path(git(arvore, "rev-parse", "--path-format=absolute", "--git-path", "MERGE_HEAD").stdout.strip())
        merge_head.write_text(commit + "\n", encoding="utf-8")
        self.assertTrue(guarda.merge_em_curso(arvore))

    def test_so_le_o_hooks_path_quando_ha_commit(self):
        lido = mock.Mock(return_value="")
        guarda.motivo_para_bloquear("git status && git log", lido)
        lido.assert_not_called()

    def test_aspas_por_fechar_usam_a_divisao_simples(self):
        self.assertIsNotNone(guarda.motivo_para_bloquear("git add . ; echo 'x", hooks_certos))


class PontoDeEntrada(unittest.TestCase):

    def test_le_o_hooks_path_do_repositorio(self):
        correr = mock.Mock(return_value=SimpleNamespace(stdout=" .githooks \n"))
        self.assertEqual(guarda.ler_hooks_path(correr), ".githooks")
        self.assertEqual(correr.call_args.args[0][-3:], ["config", "--get", "core.hooksPath"])

    def correr(self, comando):
        return subprocess.run([sys.executable, "-I", str(PASTA_HOOKS / "guarda_do_git.py")],
                              input=json.dumps({"tool_name": "Bash", "tool_input": {"command": comando}}),
                              capture_output=True, text=True, encoding="utf-8", check=False, timeout=30)

    def test_como_hook_sai_com_2_e_explica(self):
        resultado = self.correr("git add -A")
        self.assertEqual(resultado.returncode, 2)
        self.assertIn("Morg-laws", resultado.stderr)

    def test_como_hook_deixa_passar(self):
        self.assertEqual(self.correr("git status").returncode, 0)

    def correr_no_processo(self, comando):
        # O subprocesso prova o -I real, mas não conta na cobertura; este passa pelo mesmo main() e conta.
        pedido = json.dumps({"tool_name": "Bash", "tool_input": {"command": comando}}).encode("utf-8")
        return correr_como_script(PASTA_HOOKS / "guarda_do_git.py", pedido)

    def test_no_processo_recusa_com_2_e_explica(self):
        codigo, _, erro = self.correr_no_processo("git commit --no-verify -F m -- a")
        self.assertEqual(codigo, 2)
        self.assertIn("portões do git", erro)

    def test_no_processo_deixa_passar_lendo_o_hooks_path_real(self):
        self.assertEqual(self.correr_no_processo("git commit -F m -- a.txt"), (0, "", ""))

    def test_este_repositorio_tem_os_portoes_ligados(self):
        self.assertEqual(guarda.ler_hooks_path(), ".githooks", "rode: git config core.hooksPath .githooks")


if __name__ == "__main__":
    unittest.main()
