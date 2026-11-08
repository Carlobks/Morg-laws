"""Toda skill do Morg-laws tem o formato que as duas ferramentas pedem, conferido sem rede e sem tocar na skill:

- o `name` é igual ao nome da pasta, só tem `a-z`, algarismos e hífens, não começa nem acaba em hífen, não tem hífen
  duplo, tem até 64 caracteres e não leva as palavras reservadas `claude` e `anthropic` (a página das skills da
  plataforma e a especificação aberta, no `FONTES.md`);
- o cabeçalho é YAML válido (lido com o `yaml`; um «: » solto numa descrição sem aspas o parte);
- a `description` tem de 1 a 1024 caracteres e traz «Usar» e «Não usar»;
- cada skill citada numa descrição como «é a <nome>», com ou sem crases, existe em `skills/` (só apanha essa forma, com
  hífen no nome);
- o arquivo tem menos de 500 linhas;
- o `evals/trigger-eval.json` tem pelo menos 10 casos, com `should_trigger` verdadeiro e falso.
As funções recebem a raiz, para os casos de erro serem provados numa pasta temporária.
"""

import json
import re
import tempfile
import unittest
from pathlib import Path

try:  # primeiro de tudo: sem o PyYAML o teste falha com o texto da casa, e não se esconde num skip
    import yaml
except ImportError as erro:
    raise ImportError("Falta o PyYAML: pip install pyyaml (o CI fixa a 6.0.3 no seguranca.yml).") from erro

from carregar_modelos import RAIZ
from leitura_do_repositorio import ler

NOME_VALIDO = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
PALAVRAS_RESERVADAS = ("claude", "anthropic")
REFERENCIA_A_SKILL = re.compile(r"é a `?([a-z0-9]+(?:-[a-z0-9]+)+)`?")
LIMITE_DA_DESCRICAO = 1024
LIMITE_DE_LINHAS = 500
MINIMO_DE_CASOS = 10


def cabecalho(texto):
    """O cabeçalho entre os dois `---`, lido como YAML (levanta `yaml.YAMLError` se não for YAML válido); vazio se faltar."""
    if not texto.startswith("---"):
        return {}
    lido = yaml.safe_load(texto.split("---")[1])
    return lido if isinstance(lido, dict) else {}


def campo(texto, chave):
    """O valor do campo `chave` do cabeçalho, como texto; vazio se faltar."""
    return str(cabecalho(texto).get(chave) or "").strip()


def erros_do_nome(pasta, nome):
    if nome != pasta:
        return [f"{pasta}: o name «{nome}» não é igual ao nome da pasta"]
    erros = []
    if not NOME_VALIDO.fullmatch(nome) or len(nome) > 64:
        erros.append(f"{pasta}: o name «{nome}» foge de a-z, algarismos e hífens simples, até 64 caracteres")
    erros += [f"{pasta}: o name leva a palavra reservada «{p}»" for p in PALAVRAS_RESERVADAS if p in nome]
    return erros


def erros_da_descricao(pasta, descricao, nomes_das_skills):
    erros = []
    if not 1 <= len(descricao) <= LIMITE_DA_DESCRICAO:
        erros.append(f"{pasta}: a description tem {len(descricao)} caracteres; o limite é de 1 a {LIMITE_DA_DESCRICAO}")
    erros += [f"{pasta}: a description não traz «{frase}»" for frase in ("Usar", "Não usar") if frase not in descricao]
    erros += [f"{pasta}: a description cita «é a {citada}», que não existe em skills/"
              for citada in REFERENCIA_A_SKILL.findall(descricao) if citada not in nomes_das_skills]
    return erros


def erros_dos_casos(pasta, caminho):
    if not caminho.is_file():
        return [f"{pasta}: falta evals/trigger-eval.json"]
    casos = json.loads(ler(caminho))
    erros = []
    if len(casos) < MINIMO_DE_CASOS:
        erros.append(f"{pasta}: o trigger-eval tem {len(casos)} casos; o mínimo é {MINIMO_DE_CASOS}")
    for valor in (True, False):
        if not any(caso.get("should_trigger") is valor for caso in casos):
            erros.append(f"{pasta}: o trigger-eval não tem nenhum caso com should_trigger {str(valor).lower()}")
    return erros


def erros_do_formato(raiz):
    """Uma mensagem por problema, em todas as skills da raiz."""
    arquivos = sorted((raiz / "skills").glob("*/SKILL.md"))
    nomes_das_skills = {arquivo.parent.name for arquivo in arquivos}
    erros = []
    for arquivo in arquivos:
        pasta, texto = arquivo.parent.name, ler(arquivo)
        try:
            cabecalho(texto)
        except yaml.YAMLError as erro:
            erros.append(f"{pasta}: o cabeçalho não é YAML válido ({str(erro).splitlines()[0]})")
            continue
        erros += erros_do_nome(pasta, campo(texto, "name"))
        erros += erros_da_descricao(pasta, campo(texto, "description"), nomes_das_skills)
        if len(texto.splitlines()) >= LIMITE_DE_LINHAS:
            erros.append(f"{pasta}: o SKILL.md tem {len(texto.splitlines())} linhas; o limite é {LIMITE_DE_LINHAS - 1}")
        erros += erros_dos_casos(pasta, arquivo.parent / "evals" / "trigger-eval.json")
    return erros


DESCRICAO_BOA = "Faz uma coisa. Usar quando precisar dela. Não usar para outra coisa."
CASOS_BONS = [{"query": f"q{i}", "should_trigger": i % 2 == 0} for i in range(MINIMO_DE_CASOS)]


class FormatoDasSkills(unittest.TestCase):
    def test_todas_as_skills_do_repositorio_passam(self):
        self.assertEqual([], erros_do_formato(RAIZ))

    def montar(self, nome="exemplo", pasta="exemplo", descricao=DESCRICAO_BOA, casos=None, linhas=10):
        diretorio = tempfile.TemporaryDirectory()
        self.addCleanup(diretorio.cleanup)
        skill = Path(diretorio.name) / "skills" / pasta
        (skill / "evals").mkdir(parents=True)
        corpo = "\n".join(["linha"] * linhas)
        (skill / "SKILL.md").write_text(f"---\nname: {nome}\ndescription: {descricao}\n---\n{corpo}\n", encoding="utf-8")
        (skill / "evals" / "trigger-eval.json").write_text(json.dumps(CASOS_BONS if casos is None else casos),
                                                           encoding="utf-8")
        return Path(diretorio.name)

    def assertErro(self, raiz, trecho):
        erros = erros_do_formato(raiz)
        self.assertTrue(any(trecho in erro for erro in erros), f"esperava «{trecho}» em {erros}")

    def test_uma_skill_certa_passa(self):
        self.assertEqual([], erros_do_formato(self.montar()))

    def test_o_name_diferente_da_pasta_reprova(self):
        self.assertErro(self.montar(nome="outro"), "não é igual ao nome da pasta")

    def test_hifen_duplo_reprova(self):
        self.assertErro(self.montar(nome="pondo--o", pasta="pondo--o"), "foge de a-z")

    def test_palavra_reservada_reprova(self):
        self.assertErro(self.montar(nome="claude-ajuda", pasta="claude-ajuda"), "palavra reservada «claude»")

    def test_descricao_de_1025_caracteres_reprova(self):
        descricao = DESCRICAO_BOA + "x" * (LIMITE_DA_DESCRICAO + 1 - len(DESCRICAO_BOA))
        self.assertErro(self.montar(descricao=descricao), "tem 1025 caracteres")

    def test_descricao_sem_nao_usar_reprova(self):
        self.assertErro(self.montar(descricao="Faz uma coisa. Usar quando precisar dela."), "não traz «Não usar»")

    def test_skill_citada_que_nao_existe_reprova(self):
        self.assertErro(self.montar(descricao=DESCRICAO_BOA + " (é a skill-que-nao-existe)"),
                        "«é a skill-que-nao-existe», que não existe")

    def test_skill_citada_que_existe_passa(self):
        raiz = self.montar(descricao=DESCRICAO_BOA + " (é a exemplo-outro)")
        (raiz / "skills" / "exemplo-outro").mkdir()
        (raiz / "skills" / "exemplo-outro" / "SKILL.md").write_text(
            f"---\nname: exemplo-outro\ndescription: {DESCRICAO_BOA}\n---\n", encoding="utf-8")
        (raiz / "skills" / "exemplo-outro" / "evals").mkdir()
        (raiz / "skills" / "exemplo-outro" / "evals" / "trigger-eval.json").write_text(
            json.dumps(CASOS_BONS), encoding="utf-8")
        self.assertEqual([], erros_do_formato(raiz))

    def test_casos_so_verdadeiros_reprovam(self):
        casos = [{"query": f"q{i}", "should_trigger": True} for i in range(MINIMO_DE_CASOS)]
        self.assertErro(self.montar(casos=casos), "nenhum caso com should_trigger false")

    def test_menos_de_dez_casos_reprovam(self):
        self.assertErro(self.montar(casos=CASOS_BONS[:4]), "o mínimo é 10")

    def test_skill_citada_com_crases_que_nao_existe_reprova(self):
        self.assertErro(self.montar(descricao=DESCRICAO_BOA + " (é a `skill-que-nao-existe`)"),
                        "«é a skill-que-nao-existe», que não existe")

    def test_descricao_de_1024_caracteres_passa(self):
        descricao = DESCRICAO_BOA + "x" * (LIMITE_DA_DESCRICAO - len(DESCRICAO_BOA))
        self.assertEqual([], erros_do_formato(self.montar(descricao=descricao)))

    def test_arquivo_de_499_linhas_passa(self):
        # `linhas` são só as do corpo; o cabeçalho põe mais 4 (`---`, name, description, `---`)
        self.assertEqual([], erros_do_formato(self.montar(linhas=LIMITE_DE_LINHAS - 1 - 4)))

    def test_arquivo_de_500_linhas_reprova(self):
        self.assertErro(self.montar(linhas=LIMITE_DE_LINHAS - 4), "linhas; o limite é 499")

    def test_cabecalho_que_nao_e_yaml_reprova(self):
        self.assertErro(self.montar(descricao="Faz uma coisa: a outra. Usar quando precisar. Não usar para nada."),
                        "o cabeçalho não é YAML válido")

    def test_descricao_entre_aspas_com_dois_pontos_passa(self):
        descricao = '"Faz uma coisa: a outra. Usar quando precisar. Não usar para nada."'
        self.assertEqual([], erros_do_formato(self.montar(descricao=descricao)))

    def test_descricao_em_bloco_do_yaml_passa(self):
        self.assertEqual([], erros_do_formato(self.montar(descricao=">\n  " + DESCRICAO_BOA)))

    def test_cabecalho_que_nao_e_um_mapa_vem_vazio(self):
        self.assertEqual({}, cabecalho("---\n- a\n- b\n---\n"))

    def test_o_campo_vazio_vem_vazio(self):
        self.assertEqual("", campo("sem cabeçalho", "name"))


if __name__ == "__main__":
    unittest.main()
