"""O molde que se copia para um projeto (modelos/documentos/AGENTS.md) e o AGENTS.md do Morg-laws dizem o mesmo:

1. as seções «Núcleo» e «Nunca» são iguais nos dois, inteiras: cada linha, com ou sem título, e cada parágrafo. Só se
   ignora onde a linha quebra (os espaços e as quebras contam como um espaço). O título da seção pode levar um
   complemento entre parênteses (`## Núcleo (vale para qualquer projeto)`), nada mais;
2. o molde não leva as regras que só valem para o Morg-laws: nenhum título `## Regras d…`, nem o parágrafo
   «No repositório Morg-laws», nem nenhum item das «Regras deste repositório» do AGENTS.md, onde quer que esteja;
3. o molde CLAUDE.md começa por `@AGENTS.md` e não tem regras próprias: sem a linha, o Claude Code do projeto não lê
   regra nenhuma, e uma regra só no CLAUDE.md deixaria de ser igual nos agentes;
4. cada item do «Nunca» começa o corpo por «nunca», para se ler certo também fora da seção (quem procura a regra pelo
   título recebe só a linha dela);
5. a regra que cita o `git add -A` tem, no mapa das barreiras, a guarda que o recusa (`guarda_do_git.py`).
O padrão dos títulos é o do modelos/testes/test_regras.py, carregado de lá: uma só fonte.
As funções recebem o texto, para os casos de erro serem provados sem tocar nos arquivos do repositório.
"""

import re
import sys
import types
import unittest

from carregar_modelos import MODELOS, PASTA_TESTES_MODELO, RAIZ, carregar

# O modelo importa RAIZ de carregar_por_caminho; aqui a raiz é a deste repositório.
sys.modules["carregar_por_caminho"] = types.SimpleNamespace(RAIZ=RAIZ)
TITULO = carregar(PASTA_TESTES_MODELO / "test_regras.py", "test_regras_modelo_do_nucleo").TITULO
del sys.modules["carregar_por_caminho"]

SECOES_IGUAIS = ("Núcleo", "Nunca")
SECAO_DO_REPOSITORIO = "Regras deste repositório"
TITULO_DAS_REGRAS_DO_REPOSITORIO = re.compile(r"^## Regras d", re.MULTILINE | re.IGNORECASE)
PARAGRAFO_DO_REPOSITORIO = "No repositório Morg-laws"
IMPORTACAO = "@AGENTS.md"


def secao(texto, nome):
    """As linhas da seção `## <nome>` (ou `## <nome> (…)`) até à seção seguinte, ou None se não houver."""
    linhas, dentro, achada = [], False, False
    for linha in texto.splitlines():
        if linha.startswith("## "):
            dentro = linha[3:] == nome or linha[3:].startswith(nome + " (")
            achada = achada or dentro
        elif dentro:
            linhas.append(linha)
    return linhas if achada else None


def normalizada(linhas):
    return re.sub(r"\s+", " ", "\n".join(linhas)).strip()


def regras_da_secao(linhas):
    """{título: texto da regra com as continuações} das linhas de uma seção."""
    regras, atual = {}, None
    for linha in linhas:
        cabeca = TITULO.match(linha[2:]) if linha.startswith("- ") else None
        if cabeca:
            atual = cabeca.group(1)
            regras[atual] = linha
        elif atual and linha.startswith("  "):
            regras[atual] += " " + linha.strip()
        else:
            atual = None
    return regras


def diferenca_da_secao(nome, do_molde, do_repositorio):
    """A mensagem da seção que difere entre os dois, ou None."""
    molde, repositorio = secao(do_molde, nome), secao(do_repositorio, nome)
    if molde is None or repositorio is None:
        return f"«{nome}»: falta a seção `## {nome}` no {'molde' if molde is None else 'AGENTS.md'}"
    if normalizada(molde) == normalizada(repositorio):
        return None
    regras_m, regras_r = regras_da_secao(molde), regras_da_secao(repositorio)
    titulos = sorted(t for t in set(regras_m) | set(regras_r) if regras_m.get(t) != regras_r.get(t))
    onde = ", ".join(titulos) or "fora das regras com título"
    return f"«{nome}» ({onde}): o molde e o AGENTS.md divergem — mude os dois no mesmo commit"


def diferencas(do_molde, do_repositorio):
    """Mensagens para cada seção que não é igual nos dois."""
    return [erro for nome in SECOES_IGUAIS if (erro := diferenca_da_secao(nome, do_molde, do_repositorio))]


def ler_o_agents_md():
    return (RAIZ / "AGENTS.md").read_text(encoding="utf-8")


def regras_so_do_morg_laws(do_molde, do_repositorio=None):
    """Mensagens para o que o molde leva das regras que só valem para o Morg-laws, em qualquer forma."""
    do_repositorio = ler_o_agents_md() if do_repositorio is None else do_repositorio
    erros = [f"o molde leva «{t.group()}…», um título das regras deste repositório"
             for t in TITULO_DAS_REGRAS_DO_REPOSITORIO.finditer(do_molde)]
    if PARAGRAFO_DO_REPOSITORIO in do_molde:
        erros.append(f"o molde leva «{PARAGRAFO_DO_REPOSITORIO}», que só vale para o Morg-laws")
    molde = normalizada([do_molde])
    for linha in secao(do_repositorio, SECAO_DO_REPOSITORIO) or []:
        item = normalizada([linha.removeprefix("- ")]) if linha.startswith("- ") else ""
        if item and item in molde:
            erros.append(f"o molde leva a regra deste repositório «{item[:60]}»")
    return erros


def erros_do_claude_md(texto):
    """O molde CLAUDE.md começa por @AGENTS.md e não tem regras `- **TÍTULO:**` próprias."""
    erros = [] if texto.splitlines()[:1] == [IMPORTACAO] else [f"a primeira linha não é `{IMPORTACAO}`"]
    erros += [f"regra própria {titulo}: as regras ficam no AGENTS.md" for titulo in TITULO.findall(texto)]
    return erros


def nunca_sem_nunca(texto):
    """Os títulos do «Nunca» cujo corpo não começa por «nunca»."""
    return [titulo for titulo, regra in regras_da_secao(secao(texto, "Nunca") or []).items()
            if not regra.split(":**", 1)[1].strip().lower().startswith("nunca")]


def guarda_do_add_fora_do_lugar(do_molde, mapa):
    """Os títulos das regras que citam o `git add -A` e cuja linha do mapa não cita a guarda que o recusa."""
    regras = {**regras_da_secao(secao(do_molde, "Núcleo") or []), **regras_da_secao(secao(do_molde, "Nunca") or [])}
    linhas = {coluna[0]: coluna for coluna in ([c.strip() for c in linha.strip().strip("|").split("|")]
                                              for linha in mapa.splitlines()) if len(coluna) == 3}
    return [titulo for titulo, regra in regras.items()
            if "`git add -A`" in regra and "guarda_do_git.py" not in "".join(linhas.get(titulo, []))]


class NucleoIgualNoMolde(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.molde = (MODELOS / "documentos" / "AGENTS.md").read_text(encoding="utf-8")
        self.repositorio = ler_o_agents_md()

    def test_o_molde_e_o_agents_md_dizem_o_mesmo(self):
        self.assertEqual(diferencas(self.molde, self.repositorio), [])

    def test_o_molde_nao_leva_as_regras_do_morg_laws(self):
        self.assertEqual(regras_so_do_morg_laws(self.molde, self.repositorio), [])

    def test_o_molde_claude_md_importa_o_agents_md_e_nao_tem_regras(self):
        self.assertEqual(erros_do_claude_md((MODELOS / "documentos" / "CLAUDE.md").read_text(encoding="utf-8")), [])

    def test_cada_item_do_nunca_comeca_por_nunca(self):
        self.assertEqual(nunca_sem_nunca(self.molde) + nunca_sem_nunca(self.repositorio), [])

    def test_o_git_add_tem_a_guarda_no_mapa(self):
        mapa = (MODELOS / "documentos" / "regras-e-barreiras.md").read_text(encoding="utf-8")
        self.assertEqual(guarda_do_add_fora_do_lugar(self.molde, mapa), [])


NUCLEO = ("## Núcleo\n\n- **PROVAR MEDINDO:** comando e saída.\n  Dizer o que não se verificou. · *Parecer certo.*\n"
          "\n## Nunca\n\n- **SEM SEGREDOS:** nunca ler `.env`. · *Um segredo lido sai.*\n")
REPOSITORIO = NUCLEO + "\n## Regras deste repositório\n\n- Escrita em português do Brasil.\n"


class ReprovaQuandoDeve(unittest.TestCase):
    """Os casos da prova do plano e da auditoria, só com texto."""

    def test_regra_diferente_no_molde(self):
        mudado = NUCLEO.replace("Dizer o que", "Dizer só o que")
        self.assertEqual(diferencas(mudado, NUCLEO),
                         ["«Núcleo» (PROVAR MEDINDO): o molde e o AGENTS.md divergem — mude os dois no mesmo commit"])

    def test_regra_a_mais_num_dos_dois_e_secao_em_falta(self):
        a_mais = NUCLEO + "- **SEM DADOS REAIS:** nunca dados. · *Não sai.*\n"
        self.assertEqual(diferencas(NUCLEO, a_mais),
                         ["«Nunca» (SEM DADOS REAIS): o molde e o AGENTS.md divergem — mude os dois no mesmo commit"])
        self.assertIn("«Núcleo»: falta a seção `## Núcleo` no molde", diferencas("", NUCLEO))

    def test_linha_sem_titulo_e_paragrafo_a_mais_no_molde(self):
        for extra in ("- Pode saltar os hooks quando tiver pressa.\n", "Exceção: neste projeto o push não pede o sim.\n"):
            with self.subTest(extra=extra):
                molde = NUCLEO.replace("- **PROVAR MEDINDO:**", extra + "- **PROVAR MEDINDO:**")
                self.assertEqual(diferencas(molde, NUCLEO), [("«Núcleo» (fora das regras com título): o molde e o "
                                                              "AGENTS.md divergem — mude os dois no mesmo commit")])

    def test_titulo_da_secao_mudado_so_no_molde(self):
        self.assertEqual(diferencas(NUCLEO.replace("## Núcleo", "## Núcleo antigo"), NUCLEO),
                         ["«Núcleo»: falta a seção `## Núcleo` no molde"])

    def test_iguais_passam_com_o_complemento_e_com_outra_quebra_de_linha(self):
        repositorio = NUCLEO.replace("## Núcleo", "## Núcleo (vale para qualquer projeto)")
        self.assertEqual(diferencas(NUCLEO.replace("saída.\n  Dizer", "saída. Dizer"), repositorio), [])
        self.assertEqual(regras_da_secao(secao(NUCLEO + "\n## Índice\n\n- **PROVAR MEDINDO:** outro.\n", "Núcleo")),
                         regras_da_secao(secao(NUCLEO, "Núcleo")))

    def test_o_molde_com_as_regras_do_repositorio_em_qualquer_forma(self):
        self.assertEqual(regras_so_do_morg_laws(NUCLEO + "\n## Regras do repositório\n\n- Público.\n", REPOSITORIO),
                         ["o molde leva «## Regras d…», um título das regras deste repositório"])
        solta = NUCLEO.replace("## Nunca\n", "## Nunca\n\n- Escrita em português\n  do Brasil.\n")
        self.assertEqual(regras_so_do_morg_laws(solta, REPOSITORIO),
                         ["o molde leva a regra deste repositório «Escrita em português do Brasil.»"])
        self.assertEqual(regras_so_do_morg_laws(NUCLEO + "No repositório Morg-laws: x.\n", REPOSITORIO),
                         ["o molde leva «No repositório Morg-laws», que só vale para o Morg-laws"])
        self.assertEqual(regras_so_do_morg_laws(NUCLEO, REPOSITORIO), [])

    def test_o_claude_md_sem_a_importacao_ou_com_regras(self):
        self.assertEqual(erros_do_claude_md("# CLAUDE.md\n\n@AGENTS.md\n"), ["a primeira linha não é `@AGENTS.md`"])
        self.assertEqual(erros_do_claude_md("@AGENTS.md\n\n- **SÓ AQUI:** x. · *y.*\n"),
                         ["regra própria SÓ AQUI: as regras ficam no AGENTS.md"])
        self.assertEqual(erros_do_claude_md("@AGENTS.md\n\n## Só no Claude Code\n\n<o que vale só lá>\n"), [])

    def test_item_do_nunca_sem_nunca(self):
        self.assertEqual(nunca_sem_nunca(NUCLEO.replace("nunca ler", "ler")), ["SEM SEGREDOS"])
        self.assertEqual(nunca_sem_nunca(NUCLEO.replace("nunca ler", "Nunca ler")), [])

    def test_git_add_sem_a_guarda_no_mapa(self):
        molde = NUCLEO.replace("comando e saída.", "nunca `git add -A`.")
        sem = "| PROVAR MEDINDO | hook | `.claude/hooks/perguntar_antes.py` |\n"
        com = "| PROVAR MEDINDO | hook | `perguntar_antes.py`; `.claude/hooks/guarda_do_git.py` recusa `add -A` |\n"
        self.assertEqual(guarda_do_add_fora_do_lugar(molde, sem), ["PROVAR MEDINDO"])
        self.assertEqual(guarda_do_add_fora_do_lugar(molde, com), [])


if __name__ == "__main__":
    unittest.main()
