"""O código do próprio Morg-laws segue o limite que ensina: roda o modelo modelos/testes/test_tamanho_das_funcoes.py
contra este repositório (funções novas até 20 linhas; as antigas, se houvesse, na linha de base em
tests/linhas-de-base/tamanho-de-funcao.json, pelo motor modelos/testes/linha_de_base.py)."""

import sys
import types
import unittest

from carregar_modelos import PASTA_TESTES_MODELO, RAIZ, carregar

# O modelo importa RAIZ de carregar_por_caminho (e o motor linha_de_base); aqui a raiz é a deste repositório.
sys.modules["carregar_por_caminho"] = types.SimpleNamespace(RAIZ=RAIZ)
sys.modules["linha_de_base"] = carregar(PASTA_TESTES_MODELO / "linha_de_base.py", "linha_de_base")
modelo = carregar(PASTA_TESTES_MODELO / "test_tamanho_das_funcoes.py", "test_tamanho_das_funcoes_modelo")
del sys.modules["carregar_por_caminho"], sys.modules["linha_de_base"]


class FuncoesDoMorgLaws(modelo.TamanhoDasFuncoes):
    """As regras do modelo (o limite e as três verificações da linha de base), aplicadas aqui."""

    def test_o_limite_e_o_da_decisao_do_dono(self):
        self.assertEqual(modelo.LIMITE_POR_FUNCAO, 20)


del modelo.TamanhoDasFuncoes  # senão o unittest roda a classe do modelo uma segunda vez

if __name__ == "__main__":
    unittest.main()
