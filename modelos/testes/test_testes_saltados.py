"""Nenhum teste desligado para sempre (Morg-laws: não piorar; um teste saltado deixa de proteger).

Um teste saltado sem condição nunca mais corre, e ninguém volta a ele. Nos arquivos de teste Python, é recusado:
- `@unittest.skip(…)` e `@pytest.mark.skip(…)`: saltam sempre, mesmo com motivo;
- `@unittest.skipIf/skipUnless(condição, motivo)` e `@pytest.mark.skipif(condição, reason=…)` sem o motivo escrito
  (um texto literal que não está vazio);
- `self.skipTest(…)`, `pytest.skip(…)` e `raise SkipTest(…)` fora de um `if` ou de um `except`, ou sem o motivo
  escrito.
A forma certa diz quando e porquê: `@unittest.skipIf(sys.platform == "win32", "o hook só corre em sh")`,
`if not instalado: self.skipTest("sem o ruff não há o que conferir")`, ou `except ImportError:` com o `skipTest`
(uma dependência opcional). É a mesma regra do molde TypeScript testes-saltados.test.ts (`it.skip`, `.only`,
`it.skipIf(condição)`, `contexto.skip` num `if` ou num `catch`).
Limites conhecidos: uma condição constante (`skipIf(True, "x")`) passa; `pytestmark = pytest.mark.skip` (o salto de
um módulo inteiro) não é visto; um `.skip(…)` de outra coisa num arquivo de teste (`leitor.skip(3)`) é recusado.
Linha de base: tests/linhas-de-base/testes-saltados.json (linha_de_base.py).
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import ast
import re
import unittest

from linha_de_base import TresVerificacoesDaCatraca, arquivos_do_indice, ler_do_git

# Ajuste ao projeto. Arquivo de teste: numa pasta tests/ ou test/, ou com o nome test_*.py ou *_test.py.
ARQUIVO_DE_TESTE_PYTHON = re.compile(r"(?:^|/)tests?/.*\.py$|(?:^|/)(?:test_[^/]*|[^/]*_test)\.py$")
FORA_DOS_TESTES_SALTADOS = ("vendor/", "node_modules/")

SALTA_SEMPRE = "salta sempre: diga a condição (skipIf) ou apague o teste"
SEM_MOTIVO = "falta o motivo escrito"
FORA_DE_UM_IF = "salta sempre: ponha-o dentro de um if com a condição (ou de um except)"


def nome_chamado(no):
    """O último nome de `a.b.skip(…)` ou `skip`: "skip", "skipIf"…; None se não for um nome."""
    alvo = no.func if isinstance(no, ast.Call) else no
    if isinstance(alvo, ast.Attribute):
        return alvo.attr
    return alvo.id if isinstance(alvo, ast.Name) else None


def motivo_escrito(no):
    """True se `no` é um texto literal que não está vazio (também um f-string)."""
    textual = isinstance(no, ast.Constant) and isinstance(no.value, str) and no.value.strip() != ""
    return textual or isinstance(no, ast.JoinedStr)


def argumento_do_motivo(chamada, posicao):
    """O motivo de uma chamada: o argumento `reason=`, ou o da posição dada; None se não houver."""
    if not isinstance(chamada, ast.Call):
        return None
    nomeados = {argumento.arg: argumento.value for argumento in chamada.keywords}
    return nomeados.get("reason", chamada.args[posicao] if len(chamada.args) > posicao else None)


def erro_do_decorador(decorador):
    """Porque este decorador desliga o teste; None se não o desligar ou se o fizer com condição e motivo."""
    nome = nome_chamado(decorador)
    if nome == "skip":
        return SALTA_SEMPRE
    if nome in ("skipIf", "skipUnless", "skipif"):
        return None if motivo_escrito(argumento_do_motivo(decorador, 1)) else SEM_MOTIVO
    return None


def erro_da_chamada(chamada, dentro_de_um_if):
    """Porque esta chamada no corpo salta o teste para sempre; None se for condicional e com motivo."""
    if nome_chamado(chamada) not in ("skipTest", "skip", "SkipTest"):
        return None
    if not dentro_de_um_if:
        return FORA_DE_UM_IF
    return None if motivo_escrito(argumento_do_motivo(chamada, 0)) else SEM_MOTIVO


def percorrer(no, dentro_de_um_if, achados):
    """Junta em `achados` (linha, motivo) de cada salto proibido debaixo de `no`."""
    if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        achados += [(d.lineno, erro) for d in no.decorator_list if (erro := erro_do_decorador(d))]
        filhos = no.body
    else:
        filhos = list(ast.iter_child_nodes(no))
    if isinstance(no, ast.Call) and (erro := erro_da_chamada(no, dentro_de_um_if)):
        achados.append((no.lineno, erro))
    for filho in filhos:
        percorrer(filho, dentro_de_um_if or isinstance(no, (ast.If, ast.ExceptHandler)), achados)
    return achados


def saltos_proibidos(fonte):
    """[(linha, motivo)] dos saltos proibidos num arquivo de teste Python."""
    return sorted(percorrer(ast.parse(fonte), False, []))


def e_teste_python(caminho):
    return (bool(ARQUIVO_DE_TESTE_PYTHON.search(caminho))
            and not any(caminho.startswith(fora) or f"/{fora}" in caminho for fora in FORA_DOS_TESTES_SALTADOS))


class DetectorDeSaltos(unittest.TestCase):

    def test_recusa_o_que_salta_sempre_ou_sem_motivo(self):
        # Cada arroba abre um texto: colada a uma letra, a arroba pareceria um e-mail ao test_dados_pessoais.py.
        fonte = ("@unittest.skip('lento')\ndef test_a(): pass\n"
                 "@pytest.mark.skip\ndef test_b(): pass\n"
                 "@unittest.skipIf(x, '')\ndef test_c(): pass\n"
                 "@pytest.mark.skipif(x)\ndef test_d(): pass\n"
                 "def test_e(self):\n    self.skipTest('sempre')\n"
                 "def test_f(self):\n    if x:\n        pytest.skip(motivo)\n")
        self.assertEqual(saltos_proibidos(fonte), [(1, SALTA_SEMPRE), (3, SALTA_SEMPRE), (5, SEM_MOTIVO),
                                                   (7, SEM_MOTIVO), (10, FORA_DE_UM_IF), (13, SEM_MOTIVO)])

    def test_deixa_o_que_tem_condicao_e_motivo(self):
        fonte = ("@unittest.skipIf(x, 'sem rede')\ndef test_a(): pass\n"
                 "@pytest.mark.skipif(x, reason='só sh')\ndef test_b(): pass\n"
                 "def test_c(self):\n    if not y:\n        self.skipTest(f'falta {y}')\n"
                 "    if z:\n        raise unittest.SkipTest('sem dados')\n")
        self.assertEqual(saltos_proibidos(fonte), [])

    def test_o_salto_com_motivo_num_except_vale_como_num_if(self):
        # A forma do unittest para uma dependência opcional; no TypeScript, o contexto.skip num catch.
        fonte = ("def test_a(self):\n    try:\n        import numpy\n    except ImportError:\n"
                 "        self.skipTest('sem numpy')\n"
                 "def test_b(self):\n    try:\n        pass\n    except ImportError:\n        self.skipTest('')\n")
        self.assertEqual(saltos_proibidos(fonte), [(10, SEM_MOTIVO)])

    def test_so_julga_os_arquivos_de_teste(self):
        self.assertEqual([e_teste_python(c) for c in ("tests/x.py", "src/test_y.py", "src/y_test.py", "src/y.py")],
                         [True, True, True, False])


class TestesSaltados(TresVerificacoesDaCatraca, unittest.TestCase):
    REGRA = "testes-saltados"
    CONSELHO = "diga a condição e o motivo (skipIf) ou apague o teste"

    def medir(self):
        textos = ler_do_git([caminho for caminho in arquivos_do_indice() if e_teste_python(caminho)])
        return {caminho: {"testesSaltados": len(saltos)} for caminho, texto in textos.items()
                if (saltos := saltos_proibidos(texto))}

    def julga(self, caminho, metrica):
        return e_teste_python(caminho)


if __name__ == "__main__":
    unittest.main()
