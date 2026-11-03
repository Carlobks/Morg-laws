"""O molde que se copia para um projeto (modelos/documentos/AGENTS.md) e o AGENTS.md do Morg-laws dizem o mesmo:

1. as seções «Núcleo» e «Nunca» têm, nos dois, as mesmas regras `- **TÍTULO:** …`, com o mesmo texto (as linhas de
   continuação contam, juntadas com um espaço); uma regra mudada num só dos dois é recusada, com o título;
2. o molde não leva as regras que só valem para o Morg-laws: nem a seção «Regras deste repositório» nem o parágrafo
   «No repositório Morg-laws».
As funções recebem o texto, para os casos de erro serem provados sem tocar nos arquivos do repositório.
"""

import re
import unittest

from carregar_modelos import MODELOS, RAIZ

SECOES_IGUAIS = ("Núcleo", "Nunca")
SO_DO_MORG_LAWS = ("## Regras deste repositório", "No repositório Morg-laws")
# O mesmo padrão de título do modelos/testes/test_regras.py.
TITULO = re.compile(r"\*\*([A-ZÀ-Ý0-9][A-ZÀ-Ý0-9 ,.º%/-]*[A-ZÀ-Ý0-9%]):\*\*")


def regras_da_secao(texto, secao):
    """{título: texto da regra com as continuações} da seção `## <secao>…`, até à seção seguinte."""
    regras, atual, dentro = {}, None, False
    for linha in texto.splitlines():
        if linha.startswith("## "):
            dentro, atual = linha[3:].startswith(secao), None
        elif dentro and linha.startswith("- ") and TITULO.match(linha[2:]):
            atual = TITULO.match(linha[2:]).group(1)
            regras[atual] = linha
        elif dentro and atual and linha.startswith("  "):
            regras[atual] += " " + linha.strip()
        else:
            atual = None
    return regras


def diferencas(do_molde, do_repositorio):
    """Mensagens para cada regra que falta num dos dois ou que tem texto diferente, seção a seção."""
    erros = []
    for secao in SECOES_IGUAIS:
        molde, repositorio = regras_da_secao(do_molde, secao), regras_da_secao(do_repositorio, secao)
        if not molde:
            erros.append(f"«{secao}»: o molde não tem nenhuma regra no formato - **TÍTULO:** …")
        for titulo in sorted(set(molde) | set(repositorio)):
            if molde.get(titulo) != repositorio.get(titulo):
                erros.append(f"«{secao}» / {titulo}: o molde e o AGENTS.md divergem — mude os dois no mesmo commit")
    return erros


def regras_so_do_morg_laws(do_molde):
    return [f"o molde leva «{trecho}», que só vale para o Morg-laws" for trecho in SO_DO_MORG_LAWS if trecho in do_molde]


class NucleoIgualNoMolde(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.molde = (MODELOS / "documentos" / "AGENTS.md").read_text(encoding="utf-8")
        self.repositorio = (RAIZ / "AGENTS.md").read_text(encoding="utf-8")

    def test_o_molde_e_o_agents_md_dizem_o_mesmo(self):
        self.assertEqual(diferencas(self.molde, self.repositorio), [])

    def test_o_molde_nao_leva_as_regras_do_morg_laws(self):
        self.assertEqual(regras_so_do_morg_laws(self.molde), [])


NUCLEO = ("## Núcleo\n\n- **PROVAR MEDINDO:** comando e saída.\n  Dizer o que não se verificou. · *Parecer certo.*\n"
          "\n## Nunca\n\n- **SEM SEGREDOS:** ler `.env`. · *Um segredo lido sai.*\n")


class ReprovaQuandoDeve(unittest.TestCase):
    """Os casos da prova do plano, só com texto."""

    def test_regra_diferente_no_molde(self):
        mudado = NUCLEO.replace("Dizer o que", "Dizer só o que")
        self.assertEqual(diferencas(mudado, NUCLEO),
                         ["«Núcleo» / PROVAR MEDINDO: o molde e o AGENTS.md divergem — mude os dois no mesmo commit"])

    def test_regra_a_mais_num_dos_dois_e_molde_vazio(self):
        a_mais = NUCLEO + "- **SEM DADOS REAIS:** nada. · *Não sai.*\n"
        self.assertEqual(diferencas(NUCLEO, a_mais),
                         ["«Nunca» / SEM DADOS REAIS: o molde e o AGENTS.md divergem — mude os dois no mesmo commit"])
        self.assertIn("«Núcleo»: o molde não tem nenhuma regra no formato - **TÍTULO:** …", diferencas("", NUCLEO))

    def test_iguais_passam_mesmo_com_o_titulo_da_secao_mais_longo(self):
        self.assertEqual(diferencas(NUCLEO, NUCLEO.replace("## Núcleo", "## Núcleo (vale para qualquer projeto)")), [])
        self.assertEqual(regras_da_secao(NUCLEO + "\n## Índice\n\n- **PROVAR MEDINDO:** outro.\n", "Núcleo"),
                         regras_da_secao(NUCLEO, "Núcleo"))

    def test_o_molde_com_as_regras_do_repositorio(self):
        self.assertEqual(regras_so_do_morg_laws(NUCLEO + "\n## Regras deste repositório\n\n- Público.\n"),
                         ["o molde leva «## Regras deste repositório», que só vale para o Morg-laws"])
        self.assertEqual(regras_so_do_morg_laws(NUCLEO), [])


if __name__ == "__main__":
    unittest.main()
