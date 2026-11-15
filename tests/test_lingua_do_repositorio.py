"""A língua do Brasil em todo o texto público do repositório: `.md`, `.json`, `.txt` e `.yml` do git, fora de `tests/` e
de `prova/`. Confere a lista de `lingua_do_brasil.py` (as seis formas com fronteira própria) e o texto de cada arquivo.

O código fora de `tests/` e de `prova/` (`.py`, `.ts`, `.mjs`, `.sh` e os scripts sem extensão que começam por `#!`: os
moldes, os portões e os scripts) também é lido,
com os escapes `\\n`, `\\t` e `\\r` trocados por um espaço: sem isso, `"Uma.\\nOutra"` viraria «nOutra». Uma citação fiel
de uma fonte de Portugal entra em `EXCECOES_DE_LINGUA`, à vista."""

import re
import subprocess
import unittest

from carregar_modelos import RAIZ
from lingua_do_brasil import erros_de_lingua

EXTENSOES = (".md", ".json", ".txt", ".yml")
EXTENSOES_DE_CODIGO = (".py", ".ts", ".mjs", ".sh")
ESCAPES_DO_CODIGO = re.compile(r"\\[ntr]")
FORA = ("tests/", "prova/")
# (arquivo, trecho): o trecho exato que o teste não confere. A citação é a mensagem real do projeto de origem.
EXCECOES_DE_LINGUA = frozenset({("projetos/erp-de-servicos/o-que-se-mediu.md", "109 ficheiros por commitar")})


def arquivos_publicos(extensoes):
    saida = subprocess.run(["git", "ls-files", "-z"], cwd=RAIZ, capture_output=True, check=True).stdout.decode("utf-8")
    nomes = [nome for nome in saida.split("\0") if nome.endswith(extensoes) and not nome.startswith(FORA)]
    return sorted(nome for nome in nomes if (RAIZ / nome).is_file())


def arquivos_de_texto_publico():
    return arquivos_publicos(EXTENSOES)


def arquivos_de_codigo():
    """O código com extensão e os scripts sem extensão (os hooks do git), que começam por `#!`."""
    saida = subprocess.run(["git", "ls-files", "-z"], cwd=RAIZ, capture_output=True, check=True).stdout.decode("utf-8")
    sem_extensao = [nome for nome in saida.split("\0") if nome and "." not in nome.rsplit("/", 1)[-1]
                    and not nome.startswith(FORA) and (RAIZ / nome).is_file()
                    and (RAIZ / nome).read_bytes().startswith(b"#!")]
    return sorted(arquivos_publicos(EXTENSOES_DE_CODIGO) + sem_extensao)


def erros_do_codigo(nome, texto):
    return erros_de_lingua(nome, ESCAPES_DO_CODIGO.sub(" ", texto))


def sem_as_excecoes(nome, texto):
    for arquivo, trecho in EXCECOES_DE_LINGUA:
        texto = texto.replace(trecho, "") if arquivo == nome else texto
    return texto


class AsSeisFormasNovas(unittest.TestCase):

    def achados(self, frase):
        return len(erros_de_lingua("x.md", frase))

    def test_cada_forma_reprova_em_minusculas_e_com_maiuscula(self):
        for frase in ("vai noutro lugar", "Noutro lugar", "noutra seção", "noutros textos", "os píxeis", "um píxel",
                      "a secção nova", "Secção nova", "as secções", "arrastar e largar o item", "Arrastar e largar",
                      "ficou a meio", "o trabalho a meio de outra sessão", "parar a meio do teste", "A meio do plano",
                      "abra a consola", "na consola do navegador", "Na consola", "à consola", "nas consolas",
                      "a mãe a consola"):  # o último é o custo conhecido da forma da consola
            with self.subTest(frase=frase):
                self.assertEqual(self.achados(frase), 1)

    def test_o_que_existe_no_brasil_passa(self):
        for frase in ("a meio caminho", "meio a meio", "vamos dividir meio a meio", "a bandeira a meio mastro", "a meio pau",
                      "a meio-termo", "ela consola o amigo", "no outro lugar", "a seção nova", "um pixel", "arrastar e soltar",
                      "o estágio", "a consolação", "para correr"):
            with self.subTest(frase=frase):
                self.assertEqual(self.achados(frase), 0)

    def test_as_formas_tiradas_nao_voltam(self):
        """`estagiar` e `arrancar` existem no Brasil. Isto prova que não voltaram à lista, não que a fronteira funcione."""
        for frase in ("vou estagiar numa empresa", "arranca o curativo"):
            with self.subTest(frase=frase):
                self.assertEqual(self.achados(frase), 0)


class OTextoPublicoEmPortuguesDoBrasil(unittest.TestCase):
    maxDiff = None  # a falha mostra todas as mensagens

    def test_o_teste_le_o_repositorio_de_verdade(self):
        arquivos = arquivos_de_texto_publico()
        self.assertGreater(len(arquivos), 100)
        self.assertIn("AGENTS.md", arquivos)
        self.assertIn("skills/orquestrando-sessoes/SKILL.md", arquivos)
        um_de_cada_lugar_e_extensao = {"FONTES.md", "projetos/erp-de-servicos/o-que-se-mediu.md", "biblia-akita/leituras.md",
                                       "skills/nextjs-react/evals/trigger-eval.json", "manual/pessoas-citaveis.txt",
                                       ".github/ISSUE_TEMPLATE/2-sugestao.yml"}
        self.assertLessEqual(um_de_cada_lugar_e_extensao, set(arquivos))
        self.assertFalse([nome for nome in arquivos if nome.startswith(FORA)])

    def test_nenhum_texto_publico_tem_forma_de_portugal(self):
        erros = []
        for nome in arquivos_de_texto_publico():
            texto = sem_as_excecoes(nome, (RAIZ / nome).read_text(encoding="utf-8-sig", errors="replace"))
            erros += erros_de_lingua(nome, texto)
        self.assertEqual(erros, [], "troque pela forma do Brasil; uma citação fiel entra em EXCECOES_DE_LINGUA")

    def test_a_excecao_da_citacao_e_exata_e_esta_a_vista(self):
        for nome, trecho in EXCECOES_DE_LINGUA:
            texto = (RAIZ / nome).read_text(encoding="utf-8-sig")
            self.assertIn(trecho, texto)
            self.assertEqual(len(erros_de_lingua(nome, texto)), 1, "sem a exceção o trecho é acusado")
            self.assertEqual(erros_de_lingua(nome, sem_as_excecoes(nome, texto)), [])


class OCodigoForaDosTestesEmPortuguesDoBrasil(unittest.TestCase):
    maxDiff = None

    def test_le_o_codigo_de_verdade(self):
        arquivos = arquivos_de_codigo()
        self.assertGreater(len(arquivos), 30)
        um_de_cada_extensao_e_lugar = {"modelos/claude/hooks/guarda_do_git.py", "modelos/testes-ts/linha-de-base.ts",
                                       "scripts/testar.sh", ".githooks/verificar-lista-negra.sh",
                                       "modelos/git/hooks/pre-commit", ".githooks/commit-msg"}
        self.assertLessEqual(um_de_cada_extensao_e_lugar, set(arquivos))
        # Um nome escrito por extenso: se o FORA perder uma pasta, esta linha falha mesmo com a pasta limpa.
        self.assertFalse({"prova/oraculos/correr.mjs", "tests/lingua_do_brasil.py"} & set(arquivos))

    def test_um_escape_nao_vira_palavra_e_a_palavra_ainda_reprova(self):
        for frase in ('texto = "Uma.\\nOutra linha"', "x = 'a\\noutro'", "y = 'a\\tOutra'"):
            with self.subTest(frase=frase):
                self.assertEqual(erros_do_codigo("x.py", frase), [])
        for frase in ("# fica noutra pasta", "msg = '--no-verify salta os portões'", "// o trabalho a meio",
                      'texto = "linha\\nnoutra pasta"'):
            with self.subTest(frase=frase):
                self.assertEqual(len(erros_do_codigo("x.py", frase)), 1)

    def test_nenhum_codigo_tem_forma_de_portugal(self):
        erros = []
        for nome in arquivos_de_codigo():
            erros += erros_do_codigo(nome, (RAIZ / nome).read_text(encoding="utf-8-sig", errors="replace"))
        self.assertEqual(erros, [], "troque pela forma do Brasil, também nas mensagens e nos testes que as conferem")


if __name__ == "__main__":
    unittest.main()
