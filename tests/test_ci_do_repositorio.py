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


class WorkflowsDoMorgLaws(modelo.Workflows):
    """As regras do modelo (SHA, token só de leitura, nada baixado sem sha256), aplicadas aqui."""

    def test_ha_workflows(self):
        self.assertEqual([workflow.name for workflow in modelo.WORKFLOWS], ["seguranca.yml"])

    def test_roda_o_comando_unico_e_confere_o_agents_md(self):
        texto = modelo.texto(modelo.WORKFLOWS[0])
        self.assertIn("run: sh scripts/testar.sh", texto)
        self.assertIn("git config core.hooksPath .githooks", texto)
        self.assertIn('test "$linhas" -le 60', texto)
        self.assertNotIn("gitleaks/gitleaks-action", texto, "o gitleaks é o binário conferido, sem action de terceiros")


del modelo.Workflows  # senão o unittest roda a classe do modelo uma segunda vez, sem os testes daqui

if __name__ == "__main__":
    unittest.main()
