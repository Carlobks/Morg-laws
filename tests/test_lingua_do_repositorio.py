"""A língua do Brasil em todo o texto público do repositório: `.md`, `.json`, `.txt` e `.yml` do git, fora de `tests/` e
de `prova/`. Confere a lista de `lingua_do_brasil.py` (as seis formas com fronteira própria) e o texto de cada arquivo.

O texto dentro do código dos moldes (`.py`, `.ts`, `.mjs`, `.sh`) não é lido aqui: mexer nele mexe nos testes que o
conferem e no par Python/TypeScript. Uma citação fiel de uma fonte de Portugal entra em `EXCECOES_DE_LINGUA`, à vista."""

import subprocess
import unittest

from carregar_modelos import RAIZ
from lingua_do_brasil import erros_de_lingua

EXTENSOES = (".md", ".json", ".txt", ".yml")
FORA = ("tests/", "prova/")
# (arquivo, trecho): o trecho exato que o teste não confere. A citação é a mensagem real do projeto de origem.
EXCECOES_DE_LINGUA = frozenset({("projetos/erp-de-servicos/o-que-se-mediu.md", "109 ficheiros por commitar")})


def arquivos_de_texto_publico():
    saida = subprocess.run(["git", "ls-files", "-z"], cwd=RAIZ, capture_output=True, check=True).stdout.decode("utf-8")
    nomes = [nome for nome in saida.split("\0") if nome.endswith(EXTENSOES) and not nome.startswith(FORA)]
    return sorted(nome for nome in nomes if (RAIZ / nome).is_file())


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


if __name__ == "__main__":
    unittest.main()
