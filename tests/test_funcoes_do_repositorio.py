"""O código do próprio Morg-laws segue o limite que ensina: roda o modelo modelos/testes/test_tamanho_das_funcoes.py
contra este repositório (funções novas até 20 linhas, as antigas congeladas na lista do modelo)."""

import sys
import types
import unittest

from carregar_modelos import PASTA_TESTES_MODELO, RAIZ, carregar

# O modelo importa RAIZ de carregar_por_caminho; aqui a raiz é a deste repositório.
sys.modules["carregar_por_caminho"] = types.SimpleNamespace(RAIZ=RAIZ)
modelo = carregar(PASTA_TESTES_MODELO / "test_tamanho_das_funcoes.py", "test_tamanho_das_funcoes_modelo")
del sys.modules["carregar_por_caminho"]


class FuncoesDoMorgLaws(modelo.TamanhoDasFuncoes):
    """As regras do modelo (limite e catraca das antigas), aplicadas aqui."""

    def test_o_limite_e_o_da_decisao_do_dono(self):
        self.assertEqual(modelo.LIMITE_POR_FUNCAO, 20)


del modelo.TamanhoDasFuncoes  # senão o unittest roda a classe do modelo uma segunda vez

if __name__ == "__main__":
    unittest.main()
