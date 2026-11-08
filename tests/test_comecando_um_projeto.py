"""O molde do documento do projeto (`modelos/documentos/projeto.md`) guarda o que a primeira conversa com um projeto
precisa, conferido sem rede e sobre o texto:

- tem as oito seções, na ordem: O que é, Para quem, O que faz, O que não faz, Restrições, Arquitetura, Palavras do
  dono e Perguntas em aberto;
- não leva palavras nem construções do português de Portugal.
E a skill `comecando-um-projeto`:
- tem as seções do plano, na ordem, e cita os sete destinos do que escreve no projeto;
- cada cópia de `assets/` é igual, byte a byte, ao seu molde; nenhum arquivo de `assets/` fica fora do mapa; nenhum
  arquivo de `skills/` se chama `AGENTS.md`, `CLAUDE.md` nem `CLAUDE.local.md` (a ferramenta o carregaria como regra);
- o `SKILL.md` e o `evals/` não levam palavras nem construções do português de Portugal (as cópias de `assets/` ficam
  de fora: são iguais aos moldes).
As funções recebem o texto ou a raiz, para os casos de erro serem provados sem tocar no repositório.
"""

import re
import shutil
import tempfile
import unittest
from pathlib import Path

from carregar_modelos import MODELOS, RAIZ
from leitura_do_repositorio import ler
from lingua_do_brasil import erros_de_lingua

MOLDE_DO_PROJETO = MODELOS / "documentos" / "projeto.md"
PASTA_DA_SKILL = "skills/comecando-um-projeto"
SECOES_DA_SKILL = ("Começando um projeto", "1. Quando usar e o que deixa", "2. Projeto novo ou projeto que já existe",
                   "3. As rondas", "4. O que se escreve", "5. Escolhas grandes viram ADR", "6. Mensagem inicial",
                   "7. O que entregar no fim", "Fontes")
DESTINOS_DA_SKILL = ("docs/projeto.md", "docs/README.md", "AGENTS.md", "CLAUDE.md", "docs/regras-e-barreiras.md",
                     "docs/planos/", "docs/decisoes/")
COPIAS_DOS_MOLDES = {f"assets/molde-{nome}.md": f"modelos/documentos/{nome}.md"
                     for nome in ("projeto", "AGENTS", "CLAUDE", "regras-e-barreiras", "plano", "adr")}
NOMES_QUE_AS_FERRAMENTAS_CARREGAM = ("AGENTS.md", "CLAUDE.md", "CLAUDE.local.md")
SECOES_DO_PROJETO = ("O que é", "Para quem", "O que faz", "O que não faz", "Restrições", "Arquitetura",
                     "Palavras do dono", "Perguntas em aberto")


def secoes_do_molde(texto):
    """Os títulos `## …` do texto, na ordem em que aparecem."""
    return re.findall(r"^## (.+?)\s*$", texto, re.MULTILINE)


def erros_do_molde(texto):
    achadas = secoes_do_molde(texto)
    erros = [f"falta a seção «{titulo}»" for titulo in SECOES_DO_PROJETO if titulo not in achadas]
    ordem = [titulo for titulo in achadas if titulo in SECOES_DO_PROJETO]
    if not erros and ordem != list(SECOES_DO_PROJETO):
        erros.append(f"as seções estão fora da ordem: {ordem}")
    return erros


def erros_da_skill(texto):
    """As seções fora da ordem ou em falta e os destinos que o corpo da skill não cita."""
    achadas = re.findall(r"^#{1,2} (.+?)\s*$", texto, re.MULTILINE)
    erros = [f"falta a seção «{titulo}»" for titulo in SECOES_DA_SKILL if titulo not in achadas]
    ordem = [titulo for titulo in achadas if titulo in SECOES_DA_SKILL]
    if not erros and ordem != list(SECOES_DA_SKILL):
        erros.append(f"as seções estão fora da ordem: {ordem}")
    return erros + [f"falta citar o destino `{destino}`" for destino in DESTINOS_DA_SKILL if destino not in texto]


def erros_das_copias(raiz):
    """Cópia em falta ou diferente do molde, arquivo de `assets/` fora do mapa e nome que a ferramenta carregaria."""
    pasta = raiz / PASTA_DA_SKILL
    erros = []
    for copia, molde in COPIAS_DOS_MOLDES.items():
        if not (pasta / copia).is_file():
            erros.append(f"falta a cópia {copia}")
        elif (pasta / copia).read_bytes() != (raiz / molde).read_bytes():
            erros.append(f"{copia} difere de {molde}")
    achados = {p.relative_to(pasta).as_posix() for p in (pasta / "assets").rglob("*") if p.is_file()}
    erros += [f"{extra} está em assets/ e fora do mapa" for extra in sorted(achados - set(COPIAS_DOS_MOLDES))]
    nomes = [p for p in (raiz / "skills").rglob("*") if p.name in NOMES_QUE_AS_FERRAMENTAS_CARREGAM]
    return erros + [f"{p.relative_to(raiz).as_posix()} seria carregado como regra da sessão" for p in nomes]


def erros_de_lingua_da_skill(raiz):
    pasta = raiz / PASTA_DA_SKILL
    return [erro for arquivo in ("SKILL.md", "evals/trigger-eval.json")
            for erro in erros_de_lingua(arquivo, ler(pasta / arquivo))]


class MoldeDoProjeto(unittest.TestCase):
    def setUp(self):
        self.texto = ler(MOLDE_DO_PROJETO)

    def assertErro(self, texto, trecho):
        erros = erros_do_molde(texto)
        self.assertTrue(any(trecho in erro for erro in erros), f"esperava «{trecho}» em {erros}")

    def test_o_molde_passa(self):
        self.assertEqual([], erros_do_molde(self.texto))

    def test_sem_o_que_nao_faz_reprova(self):
        self.assertErro(self.texto.replace("## O que não faz", "## Outra coisa"), "falta a seção «O que não faz»")

    def test_secoes_trocadas_de_ordem_reprovam(self):
        trocado = self.texto.replace("## O que faz\n", "## @@\n").replace("## O que não faz\n", "## O que faz\n")
        self.assertErro(trocado.replace("## @@\n", "## O que não faz\n"), "fora da ordem")

    def test_palavra_de_portugal_no_molde_reprova(self):
        erros = erros_de_lingua("projeto.md", self.texto + "\nO ficheiro do projeto.\n")
        self.assertIn("ficheiro", erros[0])

    def test_o_molde_esta_em_portugues_do_brasil(self):
        self.assertEqual([], erros_de_lingua("projeto.md", self.texto))


class SkillComecandoUmProjeto(unittest.TestCase):
    def setUp(self):
        self.texto = ler(RAIZ / PASTA_DA_SKILL / "SKILL.md")

    def copia_do_repositorio(self):
        """Uma pasta temporária só com a skill, os moldes e a pasta `skills/`, para as mutações."""
        raiz = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, raiz)
        shutil.copytree(RAIZ / "skills", raiz / "skills")
        shutil.copytree(MODELOS / "documentos", raiz / "modelos" / "documentos")
        return raiz

    def test_a_skill_passa(self):
        self.assertEqual([], erros_da_skill(self.texto))

    def test_sem_a_secao_das_escolhas_grandes_reprova(self):
        mutado = self.texto.replace("## 5. Escolhas grandes viram ADR", "## 5. Outra")
        self.assertIn("falta a seção «5. Escolhas grandes viram ADR»", erros_da_skill(mutado))

    def test_secoes_fora_de_ordem_reprovam(self):
        mutado = self.texto.replace("## 6. Mensagem inicial", "## @@").replace("## 7. O que entregar no fim",
                                                                                "## 6. Mensagem inicial")
        erros = erros_da_skill(mutado.replace("## @@", "## 7. O que entregar no fim"))
        self.assertTrue(any("fora da ordem" in erro for erro in erros), erros)

    def test_sem_um_destino_reprova(self):
        erros = erros_da_skill(self.texto.replace("docs/decisoes/", "docs/outra/"))
        self.assertIn("falta citar o destino `docs/decisoes/`", erros)

    def test_as_copias_sao_iguais_aos_moldes(self):
        self.assertEqual([], erros_das_copias(RAIZ))

    def test_uma_copia_mudada_reprova(self):
        raiz = self.copia_do_repositorio()
        copia = raiz / PASTA_DA_SKILL / "assets" / "molde-AGENTS.md"
        copia.write_text(copia.read_text(encoding="utf-8") + "\numa linha a mais\n", encoding="utf-8")
        self.assertEqual(["assets/molde-AGENTS.md difere de modelos/documentos/AGENTS.md"], erros_das_copias(raiz))

    def test_uma_copia_em_falta_reprova(self):
        raiz = self.copia_do_repositorio()
        (raiz / PASTA_DA_SKILL / "assets" / "molde-adr.md").unlink()
        self.assertEqual(["falta a cópia assets/molde-adr.md"], erros_das_copias(raiz))

    def test_um_arquivo_a_mais_em_assets_reprova(self):
        raiz = self.copia_do_repositorio()
        (raiz / PASTA_DA_SKILL / "assets" / "sobra.md").write_text("x", encoding="utf-8")
        self.assertEqual(["assets/sobra.md está em assets/ e fora do mapa"], erros_das_copias(raiz))

    def test_uma_copia_com_o_nome_que_a_ferramenta_carrega_reprova(self):
        for nome in NOMES_QUE_AS_FERRAMENTAS_CARREGAM:
            with self.subTest(nome=nome):
                raiz = self.copia_do_repositorio()
                (raiz / PASTA_DA_SKILL / nome).write_text("x", encoding="utf-8")
                self.assertEqual([f"{PASTA_DA_SKILL}/{nome} seria carregado como regra da sessão"],
                                 erros_das_copias(raiz))

    def test_a_skill_esta_em_portugues_do_brasil(self):
        self.assertEqual([], erros_de_lingua_da_skill(RAIZ))

    def test_palavra_de_portugal_na_skill_reprova(self):
        raiz = self.copia_do_repositorio()
        arquivo = raiz / PASTA_DA_SKILL / "SKILL.md"
        arquivo.write_text(arquivo.read_text(encoding="utf-8") + "\nO ficheiro do projeto.\n", encoding="utf-8")
        self.assertIn("ficheiro", erros_de_lingua_da_skill(raiz)[0])


if __name__ == "__main__":
    unittest.main()
