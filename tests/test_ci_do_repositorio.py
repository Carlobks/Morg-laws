"""O CI do próprio Morg-laws segue as regras que ensina: roda o modelo modelos/testes/test_ci.py contra os workflows
deste repositório, e confere o que só este CI precisa (o comando único e o AGENTS.md curto)."""

import sys
import types
import unittest

from carregar_modelos import PASTA_TESTES_MODELO, RAIZ, carregar

# O modelo importa RAIZ de carregar_por_caminho; aqui a raiz é a deste repositório.
sys.modules["carregar_por_caminho"] = types.SimpleNamespace(RAIZ=RAIZ)
modelo = carregar(PASTA_TESTES_MODELO / "test_ci.py", "test_ci_modelo")
del sys.modules["carregar_por_caminho"]

# O modelo ordena os workflows por nome: com mais de um, o primeiro deixa de ser o da segurança.
WORKFLOW_DE_SEGURANCA = RAIZ / ".github" / "workflows" / "seguranca.yml"


class WorkflowsDoMorgLaws(modelo.Workflows):
    """As regras do modelo (SHA, token só de leitura, nada baixado sem sha256), aplicadas aqui."""

    def test_ha_workflows(self):
        self.assertEqual([workflow.name for workflow in modelo.WORKFLOWS], ["seguranca.yml"])

    def test_roda_o_comando_unico_e_confere_o_agents_md(self):
        texto = modelo.texto_do_workflow(WORKFLOW_DE_SEGURANCA)
        self.assertIn("run: sh scripts/testar.sh", texto)
        self.assertIn("git config core.hooksPath .githooks", texto)
        self.assertIn('test "$linhas" -le 60', texto)
        self.assertNotIn("gitleaks/gitleaks-action", texto, "o gitleaks é o binário conferido, sem action de terceiros")

    def test_o_so_encolhe_compara_com_o_ramo_de_destino_e_o_lockfile_e_auditado(self):
        for nome, texto in (("seguranca.yml", modelo.texto_do_workflow(WORKFLOW_DE_SEGURANCA)),
                            ("molde ci.yml", (RAIZ / "modelos" / "github" / "workflows" / "ci.yml").read_text("utf-8"))):
            with self.subTest(workflow=nome):
                self.assertEqual(erros_do_so_encolhe(texto), [])
        self.assertIn("npm audit --audit-level=high", modelo.texto_do_workflow(WORKFLOW_DE_SEGURANCA))


class MoldeDeCiServeTypeScript(unittest.TestCase):
    """Um projeto TypeScript que copia o molde de CI tem o Node fixado, o npm ci do lockfile e o npm audit."""

    def test_o_molde_tem_o_bloco_typescript(self):
        texto = (RAIZ / "modelos" / "github" / "workflows" / "ci.yml").read_text("utf-8")
        self.assertEqual(erros_do_bloco_typescript(texto), [])


def erros_do_bloco_typescript(texto):
    """O que falta ao molde de CI para servir um projeto com package-lock.json."""
    pedidos = ("actions/setup-node@", "node-version-file: .nvmrc", "npm ci", "npm audit --audit-level=high",
               "hashFiles('package-lock.json')")
    return [pedido for pedido in pedidos if pedido not in texto]


def erros_do_so_encolhe(texto):
    """O que falta a um workflow para o «só encolhe» das linhas de base funcionar no CI e numa PR."""
    pedidos = ("fetch-depth: 0", "MORG_BASE_DE_COMPARACAO: ${{ github.event.pull_request.base.sha || github.event.before }}")
    return [pedido for pedido in pedidos if pedido not in texto]


del modelo.Workflows  # senão o unittest roda a classe do modelo uma segunda vez, sem os testes daqui

if __name__ == "__main__":
    unittest.main()
