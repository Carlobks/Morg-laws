"""Nenhum dado pessoal no repositório público (Morg-laws: nunca dados reais em testes, exemplos ou commits).

Três verificações sobre os arquivos de texto do repositório (os guardados e os novos ainda por guardar):
- caminhos de uma pasta pessoal (`C:\\Users\\<conta>`, `/home/<conta>`, `/Users/<conta>`) com uma conta que não
  seja de CONTAS_DE_EXEMPLO; marcadores como `<conta>`, `{{HOME}}` ou `%USERPROFILE%` são aceitos;
- endereços de e-mail que não sejam o noreply do GitHub ou da Anthropic, ou um domínio de exemplo (uma versão npm
  como `pacote@1.2.3` não conta);
- os termos da lista negra, que fica FORA do repositório (os nomes não podem estar aqui, nem no teste que os
  procura): `git config morg.listaNegra <arquivo>`, um termo por linha, `#` para comentários.
Números de documento (CPF, NIF, IBAN, telefone…) não são procurados por padrão: o formato muda de país para país.
Ligue os do projeto em DOCUMENTOS, cada um com a sua expressão; nos exemplos, use um marcador como `<NIF>`.
Instalar: copiar para `tests/` do projeto e ajustar o bloco abaixo.
"""

import re
import subprocess
import unittest
from pathlib import Path

from carregar_por_caminho import RAIZ

# Ajuste ao projeto. As contas fictícias dos exemplos (o nome fictício do Morg-laws é "Ana").
CONTAS_DE_EXEMPLO = ("ana", "nome", "conta", "public", "default")
EXTENSOES_BINARIAS = (".ttf", ".woff2", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".pdf", ".exe", ".zip")
CAMINHOS_EXCLUIDOS = ("vendor/", "package-lock.json")
# Números de documento que o projeto não pode ter: nome -> expressão regular (ex.: {"CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"}).
DOCUMENTOS = {}

CONTA_EM_CAMINHO = re.compile(r"(?:[A-Za-z]:[\\/]+Users|(?<![\w.])/(?:home|Users))[\\/]+([^\s\\/<{%$`'\"();,:]+)",
                              re.IGNORECASE)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}\b")
EMAILS_ACEITOS = re.compile(r"@(?:users\.noreply\.github\.com|anthropic\.com|example\.(?:com|org|net))$",
                            re.IGNORECASE)


def arquivos_do_repositorio():
    """Caminhos (relativos) dos arquivos de texto guardados e dos novos que o .gitignore não esconde."""
    saida = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=RAIZ,
                           capture_output=True, text=True, encoding="utf-8", check=True).stdout
    return [caminho for caminho in dict.fromkeys(saida.splitlines())
            if (RAIZ / caminho).is_file()
            and not caminho.lower().endswith(EXTENSOES_BINARIAS)
            and not any(excluido in caminho for excluido in CAMINHOS_EXCLUIDOS)]


def termos_da_lista_negra():
    """Termos do arquivo em `git config morg.listaNegra`; lista vazia se não houver."""
    saida = subprocess.run(["git", "config", "--get", "morg.listaNegra"], cwd=RAIZ,
                           capture_output=True, text=True, encoding="utf-8", check=False).stdout.strip()
    if not saida:
        return []
    linhas = Path(saida).expanduser().read_text(encoding="utf-8-sig").splitlines()
    return [linha.strip() for linha in linhas if linha.strip() and not linha.lstrip().startswith("#")]


def achados(padrao, aceito=lambda achado: False):
    """{arquivo: [linhas]} onde o padrão aparece (menos os achados que `aceito` deixa passar)."""
    resultado = {}
    for caminho in arquivos_do_repositorio():
        texto = (RAIZ / caminho).read_text(encoding="utf-8-sig", errors="replace")
        for numero, linha in enumerate(texto.splitlines(), 1):
            if any(not aceito(achado) for achado in padrao.finditer(linha)):
                resultado.setdefault(caminho, []).append(numero)
    return resultado


def conta_de_exemplo(achado):
    """True se o caminho da pasta pessoal usa uma das contas fictícias."""
    return achado.group(1).lower() in CONTAS_DE_EXEMPLO


def email_aceito(achado):
    """True se o e-mail é o noreply do GitHub/Anthropic ou de um domínio de exemplo."""
    return bool(EMAILS_ACEITOS.search(achado.group(0)))


class SemDadosPessoais(unittest.TestCase):

    def test_ha_arquivos_para_verificar(self):
        self.assertGreater(len(arquivos_do_repositorio()), 0)

    def test_sem_caminhos_de_pastas_pessoais(self):
        self.assertEqual(achados(CONTA_EM_CAMINHO, conta_de_exemplo), {},
                         "use %USERPROFILE%, ~, {{HOME}} ou uma conta de exemplo")

    def test_sem_emails_pessoais(self):
        self.assertEqual(achados(EMAIL, email_aceito), {}, "só o noreply do GitHub/Anthropic ou example.com")

    def test_sem_numeros_de_documentos(self):
        for nome, expressao in DOCUMENTOS.items():
            with self.subTest(documento=nome):
                self.assertEqual(achados(re.compile(expressao)), {}, "número de documento: troque por um marcador")

    def test_sem_termos_da_lista_negra(self):
        for numero, termo in enumerate(termos_da_lista_negra(), 1):
            padrao = re.compile(r"(?<!\w)" + re.escape(termo) + r"(?!\w)", re.IGNORECASE)
            with self.subTest(termo=f"termo n.º {numero} da lista negra"):
                self.assertEqual(achados(padrao), {}, "dado pessoal: troque pelo nome fictício ou por um papel")


if __name__ == "__main__":
    unittest.main()
