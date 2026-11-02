"""Os workflows do GitHub Actions seguem as regras de segurança do Morg-laws. Lidos como texto (sem biblioteca YAML).

Cada regra tem o motivo ao lado:
- as actions ficam fixadas por SHA de commit, com a versão num comentário: uma tag pode ser mudada por quem a tem;
- o token só lê o repositório (`permissions: contents: read`) e o checkout não guarda a credencial; nenhum
  `write` ou `write-all`, nem dentro de um job, fora de ESCRITA_PERMITIDA (cada exceção com o motivo);
- nada de `pull_request_target`, que roda código de um fork com os segredos do repositório;
- nada é baixado direto para uma shell (`curl … | sh`, `sh -c "$(curl …)"`, `bash <(curl …)`, os mesmos casos do
  hook bloquear_segredos.py); um arquivo baixado (`-o`, `--output` ou `>`) tem o sha256 conferido.
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import re
import unittest

from carregar_por_caminho import RAIZ

# Ajuste ao projeto. "workflow.yml:linha da permissão" -> motivo (ex.: {"lancar.yml:contents: write": "cria a tag"}).
ESCRITA_PERMITIDA = {}

WORKFLOWS = sorted((RAIZ / ".github" / "workflows").glob("*.y*ml"))
SHA = re.compile(r"^\s*-?\s*uses: [\w.-]+/[\w./-]+@[0-9a-f]{40} # v\d+(?:\.\d+){0,2}$")
ESCRITA = re.compile(r"^\s*(permissions:\s*write-all|[\w-]+:\s*write)\s*(?:#.*)?$", re.MULTILINE)
_DOWNLOAD = r"\b(?:curl|wget)\b"
_SHELL = r"(?:ba|z)?sh"
PARA_SHELL = (
    re.compile(rf"{_DOWNLOAD}[^\n|]*\|\s*(?:sudo\s+)?{_SHELL}\b"),
    re.compile(rf"\b{_SHELL}\s+-c\s+[\"']?\$\(\s*{_DOWNLOAD}"),
    re.compile(rf"(?:\b{_SHELL}|\bsource)\s+<\(\s*{_DOWNLOAD}"),
)
BAIXADO = re.compile(rf"{_DOWNLOAD}[^\n]*?(?:\s-[oO]\s*|\s--output[\s=]|\s>\s*)([^\s\"']+)")


def texto(caminho):
    return caminho.read_bytes().decode("utf-8")


class Workflows(unittest.TestCase):

    def setUp(self):
        if not WORKFLOWS:
            self.skipTest("o projeto não tem workflows")

    def test_cada_action_fixada_por_sha_com_a_versao(self):
        for workflow in WORKFLOWS:
            for linha in texto(workflow).splitlines():
                if "uses:" in linha and "uses: ./" not in linha:
                    with self.subTest(workflow=workflow.name, linha=linha.strip()):
                        self.assertRegex(linha, SHA)

    def test_o_token_so_le_e_o_checkout_nao_guarda_a_credencial(self):
        for workflow in WORKFLOWS:
            conteudo = texto(workflow)
            with self.subTest(workflow=workflow.name):
                self.assertIn("\npermissions:\n  contents: read\n", conteudo)
                self.assertEqual(conteudo.count("actions/checkout@"), conteudo.count("persist-credentials: false"))
                self.assertNotIn("pull_request_target", conteudo)
            for permissao in ESCRITA.findall(conteudo):
                with self.subTest(workflow=workflow.name, permissao=permissao):
                    self.assertTrue(ESCRITA_PERMITIDA.get(f"{workflow.name}:{permissao}"),
                                    "o token só lê; uma escrita de verdade vai em ESCRITA_PERMITIDA com o motivo")

    def test_nada_baixado_direto_para_uma_shell(self):
        for workflow in WORKFLOWS:
            conteudo = texto(workflow)
            with self.subTest(workflow=workflow.name):
                for padrao in PARA_SHELL:
                    self.assertNotRegex(conteudo, padrao)
                for baixado in BAIXADO.findall(conteudo):
                    self.assertRegex(conteudo, rf"[0-9a-f]{{64}}\s+{re.escape(baixado)}[\"']?\s*\|\s*sha256sum -c",
                                     f"{baixado} baixado sem o sha256 conferido")


if __name__ == "__main__":
    unittest.main()
