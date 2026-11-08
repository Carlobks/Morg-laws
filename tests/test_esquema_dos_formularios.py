"""O esquema dos formulários de issue do Morg-laws, conferido pelo CI sem rede e contra o que o GitHub documenta
(sintaxe dos formulários, esquema dos campos e erros comuns de validação, lidas em 2026-11-08):

1. o YAML abre, o topo é um mapa e nenhuma chave é lida como booleana (`on`, `yes`) ou como não texto;
2. as chaves de topo são as permitidas, `name`, `description` e `body` existem, `name` vem primeiro, não é vazio, tem
   mais de 3 caracteres e é único;
3. o `body` não é vazio, tem um campo que não é `markdown`, cada campo só leva as chaves do tipo dele, os `id` e os
   `label` (também os das caixas) não se repetem e as opções são texto, sem `None`, vazias ou `n/a` com `default`.
Valem para os formulários de `.github/ISSUE_TEMPLATE/` e para o molde `modelos/github/ISSUE_TEMPLATE/erro.yml` (a
sintaxe é a mesma). As funções recebem o texto e devolvem a lista dos erros, para os casos serem provados numa pasta
ou num texto à parte. O esquema está em *public preview*: o teste confere o que a página diz hoje, e não prova que o
GitHub mostra o formulário. O conteúdo, a política e os endereços ficam em `test_modelos_do_github.py`.
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:  # primeiro de tudo: sem o PyYAML o teste falha com o texto da casa, e não se esconde num skip
    import yaml
except ImportError as erro:
    raise ImportError("Falta o PyYAML: pip install pyyaml (o CI fixa a 6.0.3 no seguranca.yml).") from erro

from carregar_modelos import RAIZ
from leitura_do_repositorio import ler

PASTA_DOS_FORMULARIOS = RAIZ / ".github" / "ISSUE_TEMPLATE"
MOLDE_DE_ERRO = RAIZ / "modelos" / "github" / "ISSUE_TEMPLATE" / "erro.yml"
CHAVES_DE_TOPO = {"name": str, "description": str, "body": list, "assignees": (list, str), "labels": (list, str),
                  "title": str, "type": str, "projects": (list, str)}
CHAVES_DO_BLOCO = {"type": str, "id": str, "attributes": dict, "validations": dict}
_TEXTO = {"label": str, "description": str}
ATRIBUTOS_DO_CAMPO = {
    "markdown": {"value": str},
    "textarea": {**_TEXTO, "placeholder": str, "value": str, "render": str},
    "input": {**_TEXTO, "placeholder": str, "value": str},
    "dropdown": {**_TEXTO, "multiple": bool, "options": list, "default": int},
    "checkboxes": {**_TEXTO, "options": list},
    "upload": _TEXTO,
}
VALIDACOES_DO_CAMPO = {
    "markdown": {}, "textarea": {"required": bool, "min_length": int}, "input": {"required": bool, "min_length": int},
    "dropdown": {"required": bool}, "checkboxes": {"required": bool}, "upload": {"required": bool, "accept": str},
}
ID_VALIDO = re.compile(r"[A-Za-z0-9_-]+")
NAO_ALFANUMERICO = re.compile(r"\W")


def tipo_certo(valor, esperado):
    if esperado is int:  # o booleano também é um int em Python, e aqui não vale
        return isinstance(valor, int) and not isinstance(valor, bool)
    return isinstance(valor, esperado)


def erros_de_chaves(onde, dado, permitidas, palavra):
    """Chaves fora das permitidas e valores do tipo errado, num mapa."""
    if not isinstance(dado, dict):
        return [f"{onde}: deve ser um mapa"]
    erros = []
    for chave, valor in dado.items():
        if chave not in permitidas:
            erros.append(f"{onde}: `{chave}` is not a permitted {palavra}")
        elif not tipo_certo(valor, permitidas[chave]):
            erros.append(f"{onde}: `{chave}` tem o tipo errado")
    return erros


def ler_yaml(texto):
    """(mapa do topo, erros): o YAML abre, o topo é um mapa e as chaves são texto (nada de `on` nem `yes`)."""
    try:
        dados = yaml.safe_load(texto)
    except yaml.YAMLError as erro:
        return None, [f"YAML inválido: {str(erro).splitlines()[0]}"]
    if not isinstance(dados, dict):
        return None, ["O topo do arquivo deve ser um mapa"]
    erros = ["Forbidden keys: " + repr(chave) for chave in dados if isinstance(chave, bool)]
    erros += [f"`{chave}` must be a string" for chave in dados if not isinstance(chave, (str, bool))]
    return dados, erros


def vazio(valor):
    return isinstance(valor, str) and not valor.strip()


def erros_de_topo(dados):
    erros = [f"Required top level key `{chave}` is missing" for chave in ("name", "description", "body")
             if chave not in dados]
    if dados and next(iter(dados)) != "name":
        erros.append("`name` deve ser a primeira chave")
    erros += [f"topo: `{chave}` está vazio" for chave in ("name", "description", "title") if vazio(dados.get(chave))]
    nome = dados.get("name")
    if isinstance(nome, str) and nome.strip() and len(nome.strip()) <= 3:
        erros.append("topo: o `name` deve ter mais de 3 caracteres, ou o GitHub não mostra o formulário")
    return erros + erros_de_chaves("topo", dados, CHAVES_DE_TOPO, "key")


def erros_das_caixas(onde, opcoes):
    erros = []
    for numero, opcao in enumerate(opcoes):
        local = f"{onde}.options[{numero}]"
        erros += erros_de_chaves(local, opcao, {"label": str, "required": bool}, "key")
        if isinstance(opcao, dict) and "label" not in opcao:
            erros.append(f"{local}: required attribute key `label` is missing")
        erros += [f"{local}: `label` está vazio"] if isinstance(opcao, dict) and vazio(opcao.get("label")) else []
    rotulos = [o["label"] for o in opcoes if isinstance(o, dict) and isinstance(o.get("label"), str)]
    if len(set(rotulos)) != len(rotulos):
        erros.append(f"{onde}: Checkboxes must have unique labels")
    return erros


def erros_da_lista(onde, atributos, opcoes):
    """O `dropdown`: opções de texto (antes da conta de repetidos), sem vazias, `default` dentro e sem `n/a`."""
    erros = []
    if any(isinstance(opcao, bool) for opcao in opcoes):
        erros.append(f"{onde}: `options` must not include booleans. "
                     "Please wrap values such as 'yes', and 'true' in quotes")
    textos = [opcao for opcao in opcoes if isinstance(opcao, str)]
    if len(textos) != len(opcoes) and not any(isinstance(opcao, bool) for opcao in opcoes):
        erros.append(f"{onde}: `options` must be strings")
    if any(str(opcao).strip().lower() == "none" for opcao in opcoes):
        erros.append(f"{onde}: `options` must not include the reserved word, none")
    if any(vazio(opcao) for opcao in textos):
        erros.append(f"{onde}: `options` não pode ter opção vazia")
    if len(textos) == len(opcoes) and len(set(textos)) != len(textos):
        erros.append(f"{onde}: `options` must be unique")
    return erros + erros_do_default(onde, atributos, opcoes)


def erros_do_default(onde, atributos, opcoes):
    """O `default` é um índice dentro das opções, e com ele a opção «n/a» não vale."""
    padrao = atributos.get("default")
    erros = [f"{onde}: `default` fora das opções"] if tipo_certo(padrao, int) and not 0 <= padrao < len(opcoes) else []
    if "default" in atributos and any(str(opcao).strip().lower() == "n/a" for opcao in opcoes):
        erros.append(f"{onde}: com `default` não pode haver a opção n/a")
    return erros


def erros_das_opcoes(onde, tipo, atributos):
    opcoes = atributos.get("options")
    if tipo not in ("dropdown", "checkboxes"):
        return []
    if not isinstance(opcoes, list) or not opcoes:
        return [f"{onde}: `options` must be a non-empty list"]
    return erros_das_caixas(onde, opcoes) if tipo == "checkboxes" else erros_da_lista(onde, atributos, opcoes)


def erros_do_conteudo(onde, tipo, bloco):
    atributos = bloco["attributes"] if isinstance(bloco.get("attributes"), dict) else {}
    obrigatorio = "value" if tipo == "markdown" else "label"
    erros = [f"{onde}: required attribute key `{obrigatorio}` is missing"] if obrigatorio not in atributos else []
    if "id" in bloco and (tipo == "markdown" or not ID_VALIDO.fullmatch(str(bloco["id"]))):
        erros.append(f"{onde}: `id` can only contain numbers, letters, -, _ (e não vale no markdown)")
    erros += [f"{onde}: `{chave}` está vazio" for chave, valor in atributos.items() if vazio(valor)]
    minimo = bloco["validations"].get("min_length") if isinstance(bloco.get("validations"), dict) else None
    if tipo_certo(minimo, int) and minimo < 0:
        erros.append(f"{onde}: `min_length` deve ser um inteiro não negativo")
    return erros + erros_das_opcoes(onde, tipo, atributos)


def erros_do_bloco(numero, bloco):
    onde = f"body[{numero}]"
    if not isinstance(bloco, dict):
        return [f"{onde}: deve ser um mapa"]
    tipo = bloco.get("type")
    if tipo is None:
        return [f"{onde}: required key type is missing"]
    if tipo not in ATRIBUTOS_DO_CAMPO:
        return [f"{onde}: `{tipo}` is not a valid input type"]
    erros = erros_de_chaves(onde, bloco, CHAVES_DO_BLOCO, "key")
    erros += erros_de_chaves(f"{onde}.attributes", bloco.get("attributes", {}), ATRIBUTOS_DO_CAMPO[tipo], "attribute")
    erros += erros_de_chaves(f"{onde}.validations", bloco.get("validations", {}), VALIDACOES_DO_CAMPO[tipo], "key")
    return erros + erros_do_conteudo(onde, tipo, bloco)


def erros_de_repetidos(blocos):
    """Os `id` e os `label` repetidos, e os parecidos demais (minúsculas e sem pontuação)."""
    ids = [str(bloco["id"]) for bloco in blocos if "id" in bloco]
    atributos = [bloco["attributes"] for bloco in blocos if isinstance(bloco.get("attributes"), dict)]
    rotulos = [a["label"] for a in atributos if isinstance(a.get("label"), str)]
    caixas = [o["label"] for a in atributos if isinstance(a.get("options"), list) for o in a["options"]
              if isinstance(o, dict) and isinstance(o.get("label"), str)]
    parecidos = {NAO_ALFANUMERICO.sub("", rotulo.lower()) for rotulo in rotulos}
    erros = ["Body must have unique ids"] if len(set(ids)) != len(ids) else []
    if len(set(rotulos + caixas)) != len(rotulos + caixas):
        erros.append("Body must have unique labels")
    elif len(parecidos) != len(rotulos):
        erros.append("Labels are too similar")
    return erros


def erros_do_corpo(corpo):
    if not corpo:
        return ["Body cannot be empty"]
    if not isinstance(corpo, list):
        return ["`body` deve ser uma lista"]
    blocos = [bloco for bloco in corpo if isinstance(bloco, dict)]
    erros = [erro for numero, bloco in enumerate(corpo) for erro in erros_do_bloco(numero, bloco)]
    if all(bloco.get("type") == "markdown" for bloco in blocos):
        erros.append("Body must contain at least one non-markdown field")
    return erros + erros_de_repetidos(blocos)


def erros_do_formulario(texto):
    """Todos os erros de esquema de um formulário (T1 a T3)."""
    dados, erros = ler_yaml(texto)
    if dados is None:
        return erros
    return erros + erros_de_topo(dados) + erros_do_corpo(dados.get("body"))


def erros_de_nomes(formularios):
    """{arquivo: texto} → o `name` repetido entre os formulários."""
    nomes = [yaml.safe_load(texto).get("name") for texto in formularios.values()]
    return ["Cada `name` deve ser único entre os formulários"] if len(set(nomes)) != len(nomes) else []


def formularios_da_pasta(pasta):
    """Todo `*.yml` e `*.yaml` da pasta menos o `config.yml`: o número na frente só ordena."""
    return sorted(c for c in pasta.iterdir() if c.suffix in (".yml", ".yaml") and c.name != "config.yml")


def formularios_do_repositorio():
    return formularios_da_pasta(PASTA_DOS_FORMULARIOS)


class EsquemaDosFormularios(unittest.TestCase):
    maxDiff = None  # a falha mostra todas as mensagens

    def test_o_molde_de_erro_passa_no_esquema(self):
        self.assertEqual(erros_do_formulario(ler(MOLDE_DE_ERRO)), [])

    def test_cada_formulario_do_repositorio_passa_no_esquema(self):
        for caminho in formularios_do_repositorio():
            with self.subTest(arquivo=caminho.name):
                self.assertEqual(erros_do_formulario(ler(caminho)), [])

    def test_o_name_e_unico_entre_os_formularios(self):
        self.assertEqual(erros_de_nomes({c.name: ler(c) for c in formularios_do_repositorio()}), [])

    def test_a_lista_traz_todo_yml_e_yaml_da_pasta_menos_o_config(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            for nome in ("1-a.yml", "outro.yml", "01-x.yml", "5-q.yaml", "config.yml", "sugestao.md"):
                (raiz / nome).write_text("name: X\nbody: []\n", encoding="utf-8")
            achados = [c.name for c in formularios_da_pasta(raiz)]
        self.assertEqual(achados, ["01-x.yml", "1-a.yml", "5-q.yaml", "outro.yml"])


BASE = """name: Form
description: D
title: "[F] "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: oi
  - type: input
    id: a
    attributes:
      label: Um
    validations:
      required: true
"""
CAMPO_B = "  - type: input\n    id: b\n    attributes:\n      label: {}\n"
CAIXAS = "  - type: checkboxes\n    attributes:\n      label: C\n      options:\n{}"
LISTA = "  - type: dropdown\n    attributes:\n      label: L\n      options: {}\n"
CASOS_DE_ERRO = (
    ("TAB no recuo", lambda t: t.replace("  - type: input", "\t- type: input"), "YAML inválido"),
    ("body sem hífen", lambda t: t.replace("body:\n  - type: markdown", "body:\n  type: markdown"), "YAML inválido"),
    ("chave on", lambda t: t.replace("title:", "on: x\ntitle:"), "Forbidden keys: True"),
    ("chave numérica", lambda t: t.replace("title:", "7: x\ntitle:"), "`7` must be a string"),
    ("chave de topo errada", lambda t: t.replace("labels:", "labeles:"), "`labeles` is not a permitted key"),
    ("sem description", lambda t: t.replace("description: D\n", ""), "Required top level key `description`"),
    ("labels antes do name", lambda t: "labels: [bug]\n" + t.replace('labels: ["bug"]\n', ""), "primeira chave"),
    ("body vazio", lambda t: t.split("body:")[0] + "body: []\n", "Body cannot be empty"),
    ("body só com markdown", lambda t: t.split("  - type: input")[0], "at least one non-markdown field"),
    ("lable no lugar de label", lambda t: t.replace("label: Um", "lable: Um"), "`lable` is not a permitted attribute"),
    ("label faltando", lambda t: t.replace("label: Um", "placeholder: Um"), "required attribute key `label`"),
    ("dois id iguais", lambda t: t + CAMPO_B.format("Dois").replace("id: b", "id: a"), "unique ids"),
    ("id com espaço", lambda t: t.replace("id: a", "id: a b"), "`id` can only contain"),
    ("render num input", lambda t: t.replace("label: Um\n", "label: Um\n      render: shell\n"),
     "`render` is not a permitted"),
    ("required como texto", lambda t: t.replace("required: true", 'required: "sim"'), "`required` tem o tipo errado"),
    ("labels iguais", lambda t: t + CAMPO_B.format("Um"), "unique labels"),
    ("labels parecidos", lambda t: t + CAMPO_B.format("um!"), "Labels are too similar"),
    ("caixas iguais", lambda t: t + CAIXAS.format("        - label: A\n        - label: A\n"), "unique labels"),
    ("label só com espaços", lambda t: t.replace("label: Um", 'label: "  "'), "`label` está vazio"),
    ("opção None", lambda t: t + LISTA.format("[Sim, None]"), "reserved word, none"),
    ("Yes e No sem aspas", lambda t: t + LISTA.format("[Yes, No]"), "must not include booleans"),
    ("opções repetidas", lambda t: t + LISTA.format("[A, A]"), "`options` must be unique"),
    ("tipo inválido", lambda t: t.replace("type: input", "type: select"), "`select` is not a valid input type"),
    ("min_length como texto", lambda t: t.replace("required: true", 'min_length: "3"'),
     "`min_length` tem o tipo errado"),
    ("name vazio", lambda t: t.replace("name: Form", 'name: ""'), "`name` está vazio"),
    ("name só com espaços", lambda t: t.replace("name: Form", 'name: "  "'), "`name` está vazio"),
    ("name de 3 letras", lambda t: t.replace("name: Form", "name: Abc"), "mais de 3 caracteres"),
    ("description em branco", lambda t: t.replace("description: D", 'description: " "'), "`description` está vazio"),
    ("title vazio", lambda t: t.replace('title: "[F] "', 'title: ""'), "`title` está vazio"),
    ("caixa sem label", lambda t: t + CAIXAS.format("        - required: true\n"), "required attribute key `label`"),
    ("caixa com label vazio", lambda t: t + CAIXAS.format('        - label: ""\n'), "`label` está vazio"),
    ("caixa com o label de um campo", lambda t: t + CAIXAS.format("        - label: Um\n"), "unique labels"),
    ("opção de lista que é número", lambda t: t + LISTA.format("[A, 2]"), "`options` must be strings"),
    ("opção de lista vazia", lambda t: t + LISTA.format('[A, ""]'), "`options` não pode ter opção vazia"),
    ("default fora das opções", lambda t: t + LISTA.format("[A, B]\n      default: 9"), "`default` fora das opções"),
    ("default negativo", lambda t: t + LISTA.format("[A, B]\n      default: -1"), "`default` fora das opções"),
    ("n/a com default", lambda t: t + LISTA.format("[A, n/a]\n      default: 0"), "não pode haver a opção n/a"),
    ("min_length < 0", lambda t: t.replace("required: true", "min_length: -1"), "`min_length` deve ser um inteiro"),
)


class CasosDeErroDoEsquema(unittest.TestCase):
    maxDiff = None

    def test_a_base_e_certa_e_cada_mutacao_reprova_com_a_mensagem_dela(self):
        self.assertEqual(erros_do_formulario(BASE), [])
        for rotulo, mudar, fragmento in CASOS_DE_ERRO:
            with self.subTest(caso=rotulo):
                erros = erros_do_formulario(mudar(BASE))
                self.assertTrue(any(fragmento in erro for erro in erros), f"{fragmento!r} não está em {erros}")

    def test_campos_validos_de_todos_os_tipos_passam(self):
        texto = BASE + LISTA.format('["Sim", "Não"]') + CAIXAS.format("        - label: A\n          required: true\n")
        texto += "  - type: upload\n    attributes:\n      label: U\n    validations:\n      accept: .png\n"
        texto += "  - type: textarea\n    attributes:\n      label: T\n    validations:\n      min_length: 3\n"
        self.assertEqual(erros_do_formulario(texto), [])

    def test_o_topo_que_nao_e_um_mapa_e_o_name_repetido_reprovam(self):
        self.assertEqual(erros_do_formulario("- a\n"), ["O topo do arquivo deve ser um mapa"])
        self.assertEqual(erros_de_nomes({"a": BASE, "b": BASE}), ["Cada `name` deve ser único entre os formulários"])
        self.assertEqual(erros_de_nomes({"a": BASE, "b": BASE.replace("name: Form", "name: Outra")}), [])

    def test_o_corpo_e_o_bloco_com_a_forma_errada_reprovam(self):
        self.assertEqual(erros_do_corpo("texto"), ["`body` deve ser uma lista"])
        self.assertIn("body[0]: required key type is missing", erros_do_corpo([{"id": "a"}]))
        self.assertIn("body[0]: deve ser um mapa", erros_do_corpo(["a"]))
        self.assertIn("body[0].attributes: deve ser um mapa", erros_do_bloco(0, {"type": "input", "attributes": "x"}))


class SemOPyYAMLNoEsquema(unittest.TestCase):
    def test_sem_o_pyyaml_o_import_falha_com_o_texto_da_casa(self):
        # -S tira os pacotes do venv do caminho: o import do yaml falha, e o teste não se esconde num skip.
        corrida = subprocess.run([sys.executable, "-I", "-S", str(Path(__file__).resolve())], cwd=RAIZ, check=False,
                                 capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(corrida.returncode, 0)
        self.assertIn("ImportError: Falta o PyYAML: pip install pyyaml", corrida.stderr)


if __name__ == "__main__":
    unittest.main()
