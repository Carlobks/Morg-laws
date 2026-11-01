"""As regras do agente ficam curtas, com motivo, com barreira e sem apontar para o que não existe (Morg-laws).

- O arquivo de regras é lido em todo turno: no máximo MAXIMO_DE_LINHAS linhas de MAXIMO_POR_LINHA caracteres.
- Cada regra é `- **TÍTULO:** regra. · *motivo*`: título único em maiúsculas e o motivo depois de "· *".
- Cada regra tem uma linha no mapa das barreiras (modelo em modelos/documentos/regras-e-barreiras.md do Morg-laws):
  "texto é conselho; o que tem de ser cumprido vira hook, teste ou CI".
- Uma barreira "por fazer (<fase>)" só vale enquanto a fase não está marcada como feita no plano.
- Um caminho citado que já não existe ensina o agente a saltar a regra inteira: todos têm de existir.
- As skills do índice estão instaladas, e as instaladas estão no índice (e no skills-lock.json, se houver).
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import json
import re
import unittest

from carregar_por_caminho import RAIZ

# Ajuste ao projeto.
ARQUIVO_DE_REGRAS = RAIZ / "CLAUDE.md"
MAPA = RAIZ / "docs" / "regras-e-barreiras.md"
PLANO = RAIZ / "docs" / "plano.md"  # onde as fases "por fazer" se marcam como feitas (- [x] **<fase> …)
PASTA_SKILLS = RAIZ / ".claude" / "skills"
SECAO_DAS_SKILLS = "## Quando ler que skill"
MAXIMO_DE_LINHAS, MAXIMO_POR_LINHA = 100, 160
CAMINHOS_DE_EXEMPLO = set()  # caminhos citados de propósito que não existem (ex.: um nome com AAAA-MM-DD)

TITULO = re.compile(r"\*\*([A-ZÀ-Ý0-9][A-ZÀ-Ý0-9 ,.º%/-]*[A-ZÀ-Ý0-9%]):\*\*")
BARREIRAS = ("hook", "git", "teste", "permissão", "CI", "texto", "por fazer")
CAMINHO = re.compile(r"`((?![\w+.-]*://)[\w.-]+/[^`<>{}*\s]*|[\w.-]+\.(?:md|py|ps1|sh|json|txt|ya?ml|toml))`")


def texto(caminho):
    return caminho.read_text(encoding="utf-8")


def linhas_do_mapa():
    """{título: (barreira, onde)} da tabela do mapa."""
    resultado = {}
    for linha in texto(MAPA).splitlines():
        colunas = [coluna.strip() for coluna in linha.strip().strip("|").split("|")]
        if len(colunas) == 3 and TITULO.fullmatch(f"**{colunas[0]}:**"):
            resultado[colunas[0]] = (colunas[1], colunas[2])
    return resultado


def regras():
    """{título: texto da regra com as linhas de continuação} do arquivo de regras."""
    blocos, atual = {}, None
    for linha in texto(ARQUIVO_DE_REGRAS).splitlines():
        cabeca = TITULO.match(linha[2:]) if linha.startswith("- ") else None
        if cabeca:
            atual = cabeca.group(1)
            blocos[atual] = linha
        elif atual and linha.startswith("  "):
            blocos[atual] += " " + linha.strip()
        else:
            atual = None
    return blocos


class RegrasCurtas(unittest.TestCase):

    def test_tamanho(self):
        linhas = texto(ARQUIVO_DE_REGRAS).splitlines()
        self.assertLessEqual(len(linhas), MAXIMO_DE_LINHAS)
        longas = [numero for numero, linha in enumerate(linhas, 1) if len(linha) > MAXIMO_POR_LINHA]
        self.assertEqual(longas, [], f"linhas com mais de {MAXIMO_POR_LINHA} caracteres")

    def test_regras_com_titulo_unico(self):
        titulos = TITULO.findall(texto(ARQUIVO_DE_REGRAS))
        self.assertGreater(len(titulos), 0, "nenhuma regra no formato - **TÍTULO:** …")
        self.assertEqual(len(titulos), len(set(titulos)), "dois títulos iguais acabam por se contradizer")

    def test_cada_regra_tem_o_motivo(self):
        # O motivo é o que torna a regra aplicável a casos novos (skill escrevendo-regras-de-agente).
        todas = regras()
        self.assertEqual(set(todas), set(TITULO.findall(texto(ARQUIVO_DE_REGRAS))), "título fora de um item - ")
        self.assertEqual([titulo for titulo, corpo in todas.items() if "· *" not in corpo], [])


class CadaRegraTemBarreira(unittest.TestCase):

    def test_cada_regra_esta_no_mapa_e_o_mapa_nao_tem_regras_a_mais(self):
        self.assertEqual(set(TITULO.findall(texto(ARQUIVO_DE_REGRAS))), set(linhas_do_mapa()))

    def test_a_barreira_e_de_um_tipo_conhecido(self):
        for titulo, (barreira, _) in linhas_do_mapa().items():
            with self.subTest(regra=titulo):
                self.assertTrue(barreira.startswith(BARREIRAS), f"barreira '{barreira}' fora de {BARREIRAS}")

    def test_por_fazer_so_de_fases_por_fazer(self):
        # Num projeto real, uma regra dizia "por fazer" um dia depois de a barreira existir.
        plano = texto(PLANO) if PLANO.is_file() else ""
        for titulo, (barreira, _) in linhas_do_mapa().items():
            fase = re.match(r"por fazer \(([\w.-]+)\)", barreira)
            if fase:
                with self.subTest(regra=titulo, fase=fase.group(1)):
                    self.assertNotIn(f"- [x] **{fase.group(1)} ", plano, "a fase já está feita: atualize o mapa")


class NadaApontaParaOQueNaoExiste(unittest.TestCase):

    def test_caminhos_citados_existem(self):
        # Um caminho com pasta conta a partir da raiz; um nome solto pode estar em qualquer pasta.
        nomes = {caminho.name for caminho in RAIZ.rglob("*") if not {"node_modules", ".git"} & set(caminho.parts)}
        for arquivo in (ARQUIVO_DE_REGRAS, MAPA):
            for caminho in set(CAMINHO.findall(texto(arquivo))) - CAMINHOS_DE_EXEMPLO:
                with self.subTest(arquivo=arquivo.name, caminho=caminho):
                    existe = (RAIZ / caminho.rstrip("/")).exists() if "/" in caminho else caminho in nomes
                    self.assertTrue(existe, "caminho citado que já não existe")

    def test_skills_do_indice_instaladas(self):
        partes = texto(ARQUIVO_DE_REGRAS).split(SECAO_DAS_SKILLS)
        if len(partes) == 1 and not PASTA_SKILLS.is_dir():
            self.skipTest("o projeto não usa skills")
        citadas = set(re.findall(r"`([a-z0-9-]+)`", partes[1].split("\n## ")[0])) if len(partes) > 1 else set()
        instaladas = {pasta.name for pasta in PASTA_SKILLS.iterdir() if (pasta / "SKILL.md").is_file()}
        self.assertEqual(citadas, instaladas, "o índice e a pasta das skills divergem")
        trava = RAIZ / "skills-lock.json"
        if trava.is_file():
            self.assertEqual(set(json.loads(texto(trava))["skills"]), instaladas)


if __name__ == "__main__":
    unittest.main()
