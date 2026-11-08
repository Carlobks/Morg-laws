"""O conteúdo dos formulários de issue do Morg-laws, o `config.yml`, o modelo de pull request e a política de
segurança, conferidos pelo CI sem rede (o esquema dos formulários está em `test_esquema_dos_formularios.py`):

- a prova obrigatória, o aviso de público, a caixa de revisão e as etiquetas que existem (T4);
- o `config.yml` (T5), o modelo de PR (T6) e o `SECURITY.md` (T7);
- os links só do próprio repositório ou com fonte (T8), a língua do português do Brasil (T9) e os endereços (T10).
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
from leitura_do_repositorio import arquivos_do_git, ler
from lingua_do_brasil import erros_de_lingua
from test_caminhos_do_morg_laws import ENDERECO_PROPRIO, LINK_RELATIVO, erro_do_link
from test_esquema_dos_formularios import (
    PASTA_DOS_FORMULARIOS,
    erros_de_chaves,
    formularios_da_pasta,
    formularios_do_repositorio,
)
from test_fontes_e_pesquisas import links_sem_fonte

# as etiquetas, medidas em 2026-11-07
ETIQUETAS_QUE_EXISTEM = frozenset({"accessibility", "bug", "documentation", "duplicate", "enhancement",
                                   "good first issue", "help wanted", "invalid", "question", "wontfix"})
AVISO_DE_PUBLICO = ("Este repositório é público", "nomes de projetos, empresas ou pessoas")
LINK_DO_AVISO_PRIVADO = "https://github.com/Carlobks/Morg-laws/security/advisories/new"
CAMPO_DA_PROVA = {"1-problema-numa-regra.yml": "prova", "2-sugestao.yml": "prova",
                  "3-correcao-de-fonte.yml": "fonte_diz"}
FORMULARIO_DE_CONTATO = "4-pedir-contato-de-seguranca.yml"
CONFIG_DOS_FORMULARIOS = PASTA_DOS_FORMULARIOS / "config.yml"


def campo_por_id(dados, identificador):
    return next((bloco for bloco in dados["body"] if bloco.get("id") == identificador), None)


def obrigatorio(campo):
    return bool(campo) and campo.get("validations", {}).get("required") is True


def caixa_obrigatoria(campo):
    return bool(campo) and any(opcao.get("required") is True for opcao in campo["attributes"]["options"])


def etiquetas_de(dados):
    etiquetas = dados.get("labels", [])
    return [e.strip() for e in etiquetas.split(",")] if isinstance(etiquetas, str) else etiquetas


def erros_do_contato(nome, dados, avisos):
    erros = [f"{nome}: nenhum input ou textarea pode ser obrigatório" for bloco in dados["body"]
             if bloco["type"] in ("input", "textarea") and obrigatorio(bloco)]
    if "não escreva nenhum detalhe" not in avisos.lower():
        erros.append(f"{nome}: falta a frase «não escreva nenhum detalhe» no markdown")
    if not caixa_obrigatoria(campo_por_id(dados, "sem_detalhes")):
        erros.append(f"{nome}: a caixa `sem_detalhes` deve ter a opção com required: true")
    return erros


def erros_do_conteudo_do_repositorio(nome, dados):
    """T4: o aviso de público, a prova obrigatória, a caixa de revisão e as etiquetas que existem."""
    avisos = " ".join(bloco["attributes"]["value"] for bloco in dados["body"] if bloco["type"] == "markdown")
    erros = [f"{nome}: falta o aviso de público ({frase})" for frase in AVISO_DE_PUBLICO if frase not in avisos]
    erros += [f"{nome}: a etiqueta `{e}` não existe no repositório" for e in etiquetas_de(dados)
              if e not in ETIQUETAS_QUE_EXISTEM]
    if nome == FORMULARIO_DE_CONTATO:
        return erros + erros_do_contato(nome, dados, avisos)
    if nome not in CAMPO_DA_PROVA:
        return erros + [f"{nome}: formulário sem campo da prova em CAMPO_DA_PROVA"]
    if not obrigatorio(campo_por_id(dados, CAMPO_DA_PROVA[nome])):
        erros.append(f"{nome}: o campo `{CAMPO_DA_PROVA[nome]}` deve ter required: true")
    if not caixa_obrigatoria(campo_por_id(dados, "revisado")):
        erros.append(f"{nome}: a caixa `revisado` deve ter a opção com required: true")
    return erros


def erros_dos_links_de_contato(links):
    erros = []
    for numero, link in enumerate(links):
        onde = f"contact_links[{numero}]"
        erros += erros_de_chaves(onde, link, {"name": str, "url": str, "about": str}, "key")
        erros += [f"{onde}: falta `{c}`" for c in ("name", "url", "about") if isinstance(link, dict) and c not in link]
        if isinstance(link, dict) and not str(link.get("url", "")).startswith("https://"):
            erros.append(f"{onde}: o url deve começar por https://")
    return erros


def erros_do_config(texto):
    """T5: só `blank_issues_enabled: false` e `contact_links`, com o link do aviso privado."""
    dados = yaml.safe_load(texto)
    if not isinstance(dados, dict):
        return ["config.yml: o topo deve ser um mapa"]
    erros = erros_de_chaves("config", dados, {"blank_issues_enabled": bool, "contact_links": list}, "key")
    if dados.get("blank_issues_enabled") is not False:
        erros.append("config: `blank_issues_enabled` deve ser false")
    links = dados.get("contact_links") if isinstance(dados.get("contact_links"), list) else []
    if LINK_DO_AVISO_PRIVADO not in [link.get("url") for link in links if isinstance(link, dict)]:
        erros.append(f"config: falta o link {LINK_DO_AVISO_PRIVADO}")
    return erros + erros_dos_links_de_contato(links)


def sem_fonte_dos_yml(raiz, arquivos):
    """T8: cada link dos .yml é do próprio repositório ou abre uma entrada do FONTES.md."""
    return links_sem_fonte(raiz, arquivos)


def erros_da_pasta_dos_formularios(pasta):
    """Os formulários da pasta são os esperados, e nenhum modelo em Markdown (só o formulário obriga a prova)."""
    esperados = sorted([*CAMPO_DA_PROVA, FORMULARIO_DE_CONTATO])
    achados = [c.name for c in formularios_da_pasta(pasta)]
    erros = [f"formulários da pasta: {achados}, e o esperado é {esperados}"] if achados != esperados else []
    return erros + [f"{c.name}: um modelo em Markdown não obriga a prova; use um formulário"
                    for c in pasta.glob("*.md")]


def arquivos_novos_do_github():
    pasta = RAIZ / ".github"
    return sorted(c for c in pasta.rglob("*") if c.is_file() and "workflows" not in c.parts)


class ConteudoDosFormulariosDoRepositorio(unittest.TestCase):
    maxDiff = None

    def test_os_quatro_formularios_existem_e_cumprem_o_conteudo(self):
        self.assertEqual(erros_da_pasta_dos_formularios(PASTA_DOS_FORMULARIOS), [])
        for caminho in formularios_do_repositorio():
            with self.subTest(arquivo=caminho.name):
                self.assertEqual(erros_do_conteudo_do_repositorio(caminho.name, yaml.safe_load(ler(caminho))), [])

    def test_o_config_cumpre_o_que_o_plano_pede(self):
        self.assertEqual(erros_do_config(ler(CONFIG_DOS_FORMULARIOS)), [])

    def test_os_links_dos_yml_sao_do_repositorio_ou_tem_fonte(self):
        arquivos = [c.relative_to(RAIZ).as_posix() for c in PASTA_DOS_FORMULARIOS.glob("*.yml")]
        self.assertEqual(sem_fonte_dos_yml(RAIZ, arquivos), [])

    def test_os_arquivos_novos_do_github_estao_em_portugues_do_brasil(self):
        for caminho in arquivos_novos_do_github():
            with self.subTest(arquivo=caminho.name):
                self.assertEqual(erros_de_lingua(caminho.name, ler(caminho)), [])


def tirar_o_required_da_prova(dados):
    del campo_por_id(dados, "prova")["validations"]["required"]


def mais_um_textarea_obrigatorio(dados):
    dados["body"].append({"type": "textarea", "attributes": {"label": "x"}, "validations": {"required": True}})


def tirar_o_required_da_caixa(dados):
    del campo_por_id(dados, "sem_detalhes")["attributes"]["options"][0]["required"]


CASOS_DO_CONTEUDO = (
    ("1-problema-numa-regra.yml", tirar_o_required_da_prova, "o campo `prova` deve ter required: true"),
    ("2-sugestao.yml", lambda dados: dados.update(labels=["erro"]), "a etiqueta `erro` não existe"),
    ("3-correcao-de-fonte.yml", lambda dados: dados["body"].pop(0), "falta o aviso de público"),
    ("1-problema-numa-regra.yml", lambda dados: dados["body"].pop(), "a caixa `revisado` deve ter"),
    ("novo.yml", lambda dados: None, "sem campo da prova em CAMPO_DA_PROVA"),
    (FORMULARIO_DE_CONTATO, mais_um_textarea_obrigatorio, "nenhum input ou textarea pode ser obrigatório"),
    (FORMULARIO_DE_CONTATO, tirar_o_required_da_caixa, "a caixa `sem_detalhes` deve ter"),
    (FORMULARIO_DE_CONTATO, lambda dados: dados["body"].pop(0), "falta a frase «não escreva nenhum detalhe»"),
)
CASOS_DO_CONFIG = (
    ("blank_issues_enabled: false", "blank_issues_enabled: true", "`blank_issues_enabled` deve ser false"),
    ("url: " + LINK_DO_AVISO_PRIVADO, "url: https://github.com/Carlobks/Morg-laws/security/policy", "falta o link"),
    ("url: https://github.com/Carlobks/Morg-laws/security/policy", "url: http://exemplo.test",
     "deve começar por https://"),
    ("contact_links:", "contato:", "`contato` is not a permitted key"),
    ("    about: O que conta", "    sobre: O que conta", "falta `about`"),
)


class CasosDeErroDoConteudo(unittest.TestCase):
    maxDiff = None

    def test_cada_mutacao_do_conteudo_reprova_com_a_mensagem_dela(self):
        for nome, mudar, fragmento in CASOS_DO_CONTEUDO:
            with self.subTest(caso=fragmento):
                arquivo = nome if nome != "novo.yml" else FORMULARIO_DE_CONTATO
                dados = yaml.safe_load(ler(PASTA_DOS_FORMULARIOS / arquivo))
                mudar(dados)
                erros = erros_do_conteudo_do_repositorio(nome, dados)
                self.assertTrue(any(fragmento in erro for erro in erros), f"{fragmento!r} não está em {erros}")

    def test_cada_mutacao_do_config_reprova_com_a_mensagem_dela(self):
        texto = ler(CONFIG_DOS_FORMULARIOS)
        for antigo, novo, fragmento in CASOS_DO_CONFIG:
            with self.subTest(caso=fragmento):
                self.assertIn(antigo, texto)
                erros = erros_do_config(texto.replace(antigo, novo, 1))
                self.assertTrue(any(fragmento in erro for erro in erros), f"{fragmento!r} não está em {erros}")
        self.assertEqual(erros_do_config("- a\n"), ["config.yml: o topo deve ser um mapa"])

    def test_link_de_fora_sem_entrada_no_fontes_reprova_e_o_proprio_repositorio_passa(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "FONTES.md").write_text("## A\n", encoding="utf-8")
            (raiz / "a.yml").write_text("x: https://outro.test/x\ny: " + LINK_DO_AVISO_PRIVADO + "\n", encoding="utf-8")
            self.assertEqual(len(sem_fonte_dos_yml(raiz, ["a.yml"])), 1)

    def test_a_lingua_de_portugal_reprova_e_os_falsos_positivos_passam(self):
        for texto in ("dir-lhe-ei", "dar-me-á", "far-nos-ia", "dir-vos-ia", "dir-lhes-ão", "dir-te-ei"):
            with self.subTest(mesoclise=texto):
                self.assertEqual(len(erros_de_lingua("a.md", texto)), 1)
        self.assertEqual(erros_de_lingua("a.md", "bem-te-vi e bem-me-quer"), [])
        for texto in ("O registo", "Vamos partilhar", "continua a ver", "espalhá-lo-ia", "um artefacto", "o ficheiro",
                      "o contacto", "a equipa", "o facto", "se salta", "o utilizador", "no ecrã"):
            with self.subTest(texto=texto):
                self.assertEqual(len(erros_de_lingua("a.md", texto)), 1)
        for texto in ("equipamento", "para correr", "ressalta", "saltar", "tem a ver", "de fato", "o contato"):
            with self.subTest(texto=texto):
                self.assertEqual(erros_de_lingua("a.md", texto), [])


MODELO_DE_PR = RAIZ / ".github" / "pull_request_template.md"
POLITICA_DE_SEGURANCA = RAIZ / ".github" / "SECURITY.md"
OUTRAS_POLITICAS = (RAIZ / "SECURITY.md", RAIZ / "docs" / "SECURITY.md")
ENDERECO_DO_FORMULARIO = re.compile(
    r"https://github\.com/Carlobks/Morg-laws/issues/new\?(?:[^\s)>#]*&)?template=([\w.-]+)")
ITENS_DO_MODELO_DE_PR = ("scripts/testar.sh", "FONTES.md", "pesquisas/", "português do Brasil")
SECOES_DO_MODELO_DE_PR = ("## Prova", "## O que não se verificou")


def erros_do_modelo_de_pr(texto):
    """T6: o aviso, as seções, os itens da lista e nenhum link relativo (o texto vai parar ao corpo da PR)."""
    erros = [f"pull_request_template.md: falta o aviso de público ({frase})" for frase in AVISO_DE_PUBLICO
             if frase not in texto]
    erros += [f"pull_request_template.md: falta a seção «{secao}»" for secao in SECOES_DO_MODELO_DE_PR
              if secao not in texto]
    erros += [f"pull_request_template.md: a lista não cita {item}" for item in ITENS_DO_MODELO_DE_PR
              if item not in texto]
    erros += [f"pull_request_template.md: ({alvo}) é um link relativo; use o link completo do repositório"
              for alvo in sorted(set(LINK_RELATIVO.findall(texto)))]
    return erros


def erros_da_politica(texto, outras):
    """T7: o link do aviso privado, o aviso, o apontador para o 4.º formulário, o dado pessoal, e uma política só."""
    formularios = ENDERECO_DO_FORMULARIO.findall(texto)
    erros = [f"SECURITY.md: falta o aviso de público ({frase})" for frase in AVISO_DE_PUBLICO if frase not in texto]
    if LINK_DO_AVISO_PRIVADO not in texto:
        erros.append(f"SECURITY.md: falta o link {LINK_DO_AVISO_PRIVADO}")
    if FORMULARIO_DE_CONTATO not in formularios:
        erros.append(f"SECURITY.md: falta o link do formulário (template={FORMULARIO_DE_CONTATO})")
    if "dado pessoal" not in texto.lower():
        erros.append("SECURITY.md: falta a menção do dado pessoal publicado por engano")
    if "pela issue de contato" not in texto:
        erros.append("SECURITY.md: a resposta também vem pela issue de contato (o 4.º formulário não dá aviso)")
    return erros + [f"{outra}: há outra política de segurança; o GitHub escolhe uma só" for outra in outras]


def erros_dos_enderecos(raiz, arquivos, com_blob):
    """T10: cada `template=` aponta para um formulário do git; cada `…/blob/main/…` de `com_blob` chega a um arquivo."""
    erros, conhecidos = [], set(arquivos)
    for nome in sorted(a for a in arquivos if a.endswith((".md", ".yml"))):
        texto = ler(raiz / nome)
        erros += [f"{nome}: template={t} não é um formulário de .github/ISSUE_TEMPLATE"
                  for t in ENDERECO_DO_FORMULARIO.findall(texto) if f".github/ISSUE_TEMPLATE/{t}" not in conhecidos]
        destinos = sorted({m[1:] for m in ENDERECO_PROPRIO.findall(texto)}) if nome in com_blob else []
        for ref, caminho, ancora in destinos:
            erro = erro_do_link(raiz, conhecidos, ref, caminho, ancora)
            erros += [f"{nome}: …/{caminho} — {erro}"] if erro else []
    return erros


def arquivos_com_blob(raiz):
    """Os arquivos novos cujos `…/blob/main/…` se conferem: o modelo de PR, a política, os READMEs e os `.yml`."""
    pasta = raiz / ".github" / "ISSUE_TEMPLATE"
    yml = [*formularios_da_pasta(pasta), pasta / "config.yml"]
    return [".github/pull_request_template.md", ".github/SECURITY.md", "README.md", "biblia-akita/README.md",
            *(c.relative_to(raiz).as_posix() for c in yml)]


def erros_dos_enderecos_do_repositorio():
    return erros_dos_enderecos(RAIZ, arquivos_do_git(RAIZ), arquivos_com_blob(RAIZ))


class ModeloDePrEPoliticaDoRepositorio(unittest.TestCase):
    maxDiff = None

    def test_o_modelo_de_pr_cumpre_o_que_o_plano_pede(self):
        self.assertEqual(erros_do_modelo_de_pr(ler(MODELO_DE_PR)), [])

    def test_a_politica_cumpre_o_que_o_plano_pede(self):
        self.assertEqual(erros_da_politica(ler(POLITICA_DE_SEGURANCA), [c for c in OUTRAS_POLITICAS if c.exists()]), [])

    def test_os_enderecos_do_proprio_repositorio_chegam_ao_destino(self):
        self.assertEqual(erros_dos_enderecos_do_repositorio(), [])


class CasosDeErroDoModeloEDaPolitica(unittest.TestCase):
    maxDiff = None

    def reprova(self, erros, fragmento):
        self.assertTrue(any(fragmento in erro for erro in erros), f"{fragmento!r} não está em {erros}")

    def test_o_modelo_de_pr_reprova_sem_o_item_do_fontes_e_com_link_relativo(self):
        texto = ler(MODELO_DE_PR)
        self.reprova(erros_do_modelo_de_pr(texto.replace("`FONTES.md`", "o arquivo de fontes")), "não cita FONTES.md")
        self.reprova(erros_do_modelo_de_pr(texto + "[x](../README.md)\n"), "(../README.md) é um link relativo")
        self.reprova(erros_do_modelo_de_pr(texto.replace("## Prova", "## Teste")), "falta a seção «## Prova»")
        self.reprova(erros_do_modelo_de_pr(texto.replace("Este repositório é público", "Aviso")), "falta o aviso")

    def test_a_pasta_reprova_o_formulario_fora_da_lista_e_o_modelo_em_markdown(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            for nome in (*CAMPO_DA_PROVA, FORMULARIO_DE_CONTATO, "config.yml"):
                (raiz / nome).write_text("x: 1\n", encoding="utf-8")
            self.assertEqual(erros_da_pasta_dos_formularios(raiz), [])
            for extra in ("outro.yml", "01-x.yml", "5-quebrado.yaml", "sugestao.md"):
                with self.subTest(extra=extra):
                    (raiz / extra).write_text("x: 1\n", encoding="utf-8")
                    self.assertTrue(erros_da_pasta_dos_formularios(raiz), extra)
                    (raiz / extra).unlink()

    def test_o_link_blob_quebrado_num_yml_reprova_e_o_do_repositorio_passa(self):
        endereco = "https://github.com/Carlobks/Morg-laws/blob/main/NAO-EXISTE.md"
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)
            config = raiz / ".github" / "ISSUE_TEMPLATE" / "config.yml"
            config.write_text(f"url: {endereco}\n", encoding="utf-8")
            erros = erros_dos_enderecos(raiz, [".github/ISSUE_TEMPLATE/config.yml"], arquivos_com_blob(raiz))
        self.reprova(erros, "config.yml: …/NAO-EXISTE.md — o arquivo não existe no git")

    def test_a_politica_reprova_sem_o_link_com_o_apontador_trocado_e_com_outra_politica(self):
        texto = ler(POLITICA_DE_SEGURANCA)
        sem_o_link = texto.replace(LINK_DO_AVISO_PRIVADO, "https://x.test")
        self.reprova(erros_da_politica(sem_o_link, []), "falta o link https")
        trocado = texto.replace("template=" + FORMULARIO_DE_CONTATO, "template=1-problema-numa-regra.yml")
        self.reprova(erros_da_politica(trocado, []), "falta o link do formulário")
        self.reprova(erros_da_politica(texto.replace("dado pessoal", "dado"), []), "falta a menção do dado pessoal")
        sem_a_issue = texto.replace("pela issue de contato", "pelo aviso")
        self.reprova(erros_da_politica(sem_a_issue, []), "a resposta também vem pela issue de contato")
        self.reprova(erros_da_politica(texto.replace("Este repositório é público", "A"), []), "falta o aviso")
        self.reprova(erros_da_politica(texto, [Path("SECURITY.md")]), "há outra política de segurança")

    def test_os_enderecos_reprovam_o_formulario_que_nao_existe_e_o_arquivo_que_nao_existe(self):
        endereco = "https://github.com/Carlobks/Morg-laws"
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "a.md").write_text(
                f"{endereco}/issues/new?template=3-correcao-de-fonte.yml e {endereco}/blob/main/"
                ".github/SEGURANCA.md e [ok]({endereco}/issues/new?labels=x&template=b.yml)\n", encoding="utf-8")
            (raiz / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)
            (raiz / ".github" / "ISSUE_TEMPLATE" / "b.yml").write_text("x: 1\n", encoding="utf-8")
            erros = erros_dos_enderecos(raiz, ["a.md", ".github/ISSUE_TEMPLATE/b.yml"], ["a.md"])
        self.reprova(erros, "template=3-correcao-de-fonte.yml não é um formulário")
        self.reprova(erros, "SEGURANCA.md — o arquivo não existe no git")
        self.assertEqual(len(erros), 2)


class SemOPyYAMLNoConteudo(unittest.TestCase):
    def test_sem_o_pyyaml_o_import_falha_com_o_texto_da_casa(self):
        # -S tira os pacotes do venv do caminho: o import do yaml falha, e o teste não se esconde num skip.
        corrida = subprocess.run([sys.executable, "-I", "-S", str(Path(__file__).resolve())], cwd=RAIZ, check=False,
                                 capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(corrida.returncode, 0)
        self.assertIn("ImportError: Falta o PyYAML: pip install pyyaml", corrida.stderr)


if __name__ == "__main__":
    unittest.main()
