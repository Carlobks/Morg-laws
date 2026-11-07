"""Nenhum dado pessoal ou identificador em `projetos/`, a pasta do catálogo publicado (anonimizado).

O que lê depende de onde corre:
- no `pre-commit` (MORG_LER_DO_INDICE=1): o conteúdo preparado (`git add`) de `projetos/` e da lista de palavras, lido
  do índice e não do disco;
- no CI (MORG_BASE_DE_COMPARACAO): cada commit do intervalo que mexe em `projetos/`, e não só a ponta: um dado
  num commit do meio fica na história pública; sem base utilizável (só zeros), todos os commits;
- à mão (`sh scripts/testar.sh`): a árvore commitada de `projetos/` mais os arquivos novos.
Procura caminhos de pasta pessoal, e-mails, documentos, IBAN, UUID, hash, ID de serviço, domínios, dinheiro, nomes
próprios fora de `tests/palavras-com-maiuscula.txt` e os termos da lista negra local (`git config morg.listaNegra`,
nunca impressos: só «termo n.º N»). O CI não vê a lista negra: ela vive fora do repositório.
"""

import os
import unittest

import dados_do_catalogo as catalogo
from carregar_modelos import RAIZ

# A estrutura confere o catálogo inteiro; no pre-commit, um projeto novo chega arquivo a arquivo.
SO_FORA_DO_PRE_COMMIT = unittest.skipIf(os.environ.get("MORG_LER_DO_INDICE") == "1", "o commit do meio não tem os quatro arquivos")


class CatalogoSemDados(unittest.TestCase):
    maxDiff = None  # a falha mostra todas as mensagens

    def test_nada_que_identifique_pessoas_ou_empresas(self):
        mensagens = catalogo.problemas(catalogo.conteudos_a_verificar(RAIZ), catalogo.molde.termos_da_lista_negra())
        self.assertEqual(mensagens, [], "troque o dado pelo papel («o dono», «Empresa A») ou por um marcador")

    def test_a_lista_de_palavras_esta_bem_formada(self):
        texto = (RAIZ / catalogo.PALAVRAS).read_text(encoding="utf-8-sig")
        self.assertEqual(catalogo.ler_palavras(texto)[2], ())


@SO_FORA_DO_PRE_COMMIT
class EstruturaDoCatalogo(unittest.TestCase):

    def test_tabela_pastas_e_arquivos_batem(self):
        self.assertEqual(catalogo.erros_da_estrutura(RAIZ), [])


if __name__ == "__main__":
    unittest.main()
