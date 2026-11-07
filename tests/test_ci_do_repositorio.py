"""O CI do próprio Morg-laws segue as regras que ensina: roda o modelo modelos/testes/test_ci.py contra os workflows
deste repositório, e confere o que só este CI precisa (o comando único e o AGENTS.md curto)."""

import re
import sys
import tomllib
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
        self.assertEqual([workflow.name for workflow in modelo.WORKFLOWS], ["links.yml", "seguranca.yml"])

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


class LinksVivos(unittest.TestCase):
    """O workflow dos links externos (links.yml) e o lychee.toml dele: o que não pode mudar sem o teste avisar."""

    LINKS = RAIZ / ".github" / "workflows" / "links.yml"
    CHAVE = "key: lychee-${{ github.run_id }}-${{ github.run_attempt }}"

    def setUp(self):
        self.texto = modelo.texto_do_workflow(self.LINKS)
        self.config = tomllib.loads((RAIZ / "lychee.toml").read_text("utf-8"))

    def test_corre_no_push_na_pull_request_e_no_agendamento(self):
        gatilhos = self.texto.split("\non:\n")[1].split("\npermissions:")[0]
        for gatilho in ("  push:", "  pull_request:", "  schedule:"):
            self.assertIn(gatilho, gatilhos)
        # Só os .md, o lychee.toml e o próprio workflow disparam o push e a pull request.
        self.assertEqual(gatilhos.count('paths: ["**.md", "lychee.toml", ".github/workflows/links.yml"]'), 2)
        self.assertRegex(gatilhos, r'(?m)^\s*- cron: "')

    def test_o_push_so_de_branch_e_nao_corre_com_a_tag(self):
        push = self.texto.split("\n  push:\n")[1].split("\n  pull_request:")[0]
        self.assertIn('branches: ["main"]', push)

    def test_o_lychee_vem_com_o_sha256_conferido_e_sem_a_action_de_terceiros(self):
        # A linha acaba em `| sha256sum -c -`: com um `|| true` depois, o passo seguiria com o binário sem conferir.
        self.assertRegex(self.texto, re.compile(
            r"[0-9a-f]{64}\s+lychee\.tar\.gz[\"]?\s*\|\s*sha256sum -c -[ \t]*$", re.MULTILINE))
        self.assertNotIn("lycheeverse/lychee-action", self.texto, "a action baixa o binário sem conferir o sha256")
        for desliga in modelo.DESLIGA_A_CONFERENCIA:
            self.assertNotRegex(self.texto, desliga)

    def test_o_lychee_corre_com_o_config_dele(self):
        # O lychee 0.24.2 acharia o lychee.toml sozinho na pasta de trabalho; o --config fecha a porta a outro
        # arquivo e a uma mudança de pasta, e o `exclude` isento é parte do que o teste local confere.
        self.assertRegex(self.texto, r"(?m)lychee-x86_64-unknown-linux-gnu/lychee --config lychee\.toml\s*$")

    def test_a_chave_da_cache_muda_a_cada_corrida_nos_dois_passos_e_o_restore_procura_pelo_prefixo(self):
        self.assertEqual(self.texto.count(self.CHAVE), 2)
        self.assertEqual(self.texto.count("restore-keys: lychee-\n"), 1)

    def test_a_cache_grava_tambem_quando_o_job_falha(self):
        gravacao = self.texto.split("actions/cache/save@")[1]
        self.assertIn("if: always()", gravacao.split("with:")[0])

    def test_o_lychee_toml_pede_pouco_a_cada_site_e_so_links_externos(self):
        self.assertEqual(self.config["host_concurrency"], 1)
        self.assertGreater(self.config["max_retries"], 0)
        self.assertIs(self.config["cache"], True)
        self.assertNotIn("file", self.config["scheme"])
        self.assertEqual(self.config["host_request_interval"], "1s")
        self.assertEqual(self.config["max_concurrency"], 8)
        self.assertEqual(self.config["timeout"], 20)
        self.assertEqual(self.config["max_cache_age"], "1d")

    def test_o_403_e_o_429_contam_como_o_site_existe(self):
        self.assertEqual(self.config["accept"], ["100..=103", "200..=299", "403", "429"])


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
