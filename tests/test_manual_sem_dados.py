"""Nenhum dado pessoal ou identificador nos `.md` de `manual/`, o manual de uso publicado.

O que lê depende de onde corre, como o teste do catálogo: no `pre-commit` (MORG_LER_DO_INDICE=1) o que está
preparado (`git add`), lido do índice; no resto, a árvore e os arquivos novos, lidos do disco. Procura o que o
detector do manual procura (`dados_do_manual.py`) e os termos da lista negra local (`git config morg.listaNegra`,
nunca impressos: só «termo n.º N»). O CI não vê a lista negra: lá a barreira é só o detector."""

import unittest

import dados_do_catalogo as catalogo
import dados_do_manual as manual
from carregar_modelos import RAIZ


class ManualSemDados(unittest.TestCase):
    maxDiff = None  # a falha mostra todas as mensagens

    def test_nada_que_identifique_pessoas_ou_empresas(self):
        conteudos, situacao = manual.situacao_do_manual(RAIZ)
        mensagens = manual.problemas(conteudos, situacao, catalogo.molde.termos_da_lista_negra())
        self.assertEqual(mensagens, [], "troque o dado pelo papel («o dono») e ponha os nomes de arquivo em crases")


if __name__ == "__main__":
    unittest.main()
