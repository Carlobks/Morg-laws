"""Quem instala o Morg-laws recebe só a pasta de cada skill e o molde do AGENTS.md: um caminho do repositório citado
sem link aponta, no projeto, para um arquivo que não existe. Por isso o CI confere:

1. nenhuma skill (`skills/**/*.md`) cita, sem link, um arquivo ou pasta do Morg-laws que não venha com ela: um caminho
   com pasta que existe a partir da raiz, um arquivo da raiz (`FONTES.md`) ou um script de outra pasta pelo nome
   (`test_docs_indices.py`). O que está na pasta da própria skill (`references/…`) vem com ela. Os nomes que todo
   projeto tem (`CLAUDE.md`, `AGENTS.md`, `README.md`, `.gitignore`…) falam do arquivo do projeto e não contam;
2. cada link para o próprio repositório, nas skills e nos moldes do AGENTS.md e do CLAUDE.md, aponta para a `main`, para
   um arquivo que o git conhece e, quando tem âncora, para um título que existe nesse arquivo.
As funções recebem a raiz e a lista de arquivos, para os casos de erro serem provados numa pasta temporária.
"""

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from carregar_modelos import RAIZ

ENDERECO = "https://github.com/Carlobks/Morg-laws"
MOLDES_COPIADOS = ("modelos/documentos/AGENTS.md", "modelos/documentos/CLAUDE.md")
NOMES_QUE_TODO_PROJETO_TEM = frozenset({"AGENTS.md", "CLAUDE.md", "README.md", "LICENSE", ".gitignore",
                                        ".gitattributes"})
SCRIPTS = (".py", ".sh", ".mjs")
LINK_PROPRIO = re.compile(r"\[[^\]]*\]\(" + re.escape(ENDERECO) + r"[^)\s]*\)")
ENDERECO_PROPRIO = re.compile(re.escape(ENDERECO) + r"/(blob|tree)/([^/\s)]+)/([^)\s#>`]+)(?:#([^)\s>`]+))?")
URL = re.compile(r"https?://\S+")
ENTRE_CRASES = re.compile(r"`([^`\s]+)`")
SOLTO = re.compile(r"(?<![\w./`-])((?:[\w.-]+/)+[\w.-]*|[\w.-]+\.(?:md|py|sh|mjs))(?![\w/`])")


def ler(caminho):
    return caminho.read_text(encoding="utf-8")


def candidatos(texto):
    """Os caminhos citados fora de um link para o próprio repositório: entre crases ou soltos na prosa."""
    sem_links = URL.sub(" ", LINK_PROPRIO.sub(" ", texto))
    soltos = SOLTO.findall(ENTRE_CRASES.sub(" ", sem_links))
    return {c.removeprefix("./").rstrip("/") for c in ENTRE_CRASES.findall(sem_links) + soltos} - {""}


def no_morg_laws(caminho, pasta_da_skill, raiz, scripts_por_nome):
    """O caminho no Morg-laws de um arquivo ou pasta citado que não vem com a skill, ou None."""
    if "://" in caminho or caminho in NOMES_QUE_TODO_PROJETO_TEM or (pasta_da_skill / caminho).exists():
        return None
    if "/" in caminho or (raiz / caminho).exists():
        return caminho if (raiz / caminho).exists() else None
    return scripts_por_nome.get(caminho) if caminho.endswith(SCRIPTS) else None


def caminhos_sem_link(raiz, arquivos):
    """Mensagens para cada caminho do Morg-laws citado sem link numa skill."""
    scripts_por_nome = {Path(nome).name: nome for nome in arquivos if not nome.startswith("skills/")}
    erros = []
    for nome in sorted(a for a in arquivos if a.startswith("skills/") and a.endswith(".md")):
        pasta_da_skill = raiz / Path(nome).parts[0] / Path(nome).parts[1]
        for citado in sorted(candidatos(ler(raiz / nome))):
            caminho = no_morg_laws(citado, pasta_da_skill, raiz, scripts_por_nome)
            if caminho:
                tipo = "tree" if (raiz / caminho).is_dir() else "blob"
                erros.append(f"{nome}: `{citado}` — não vem com a skill; escreva o link completo "
                             f"[`{citado}`]({ENDERECO}/{tipo}/main/{caminho})")
    return erros


def ancora(titulo):
    """A âncora que o GitHub dá a um título: minúsculas, sem pontuação, espaços trocados por hífens."""
    return re.sub(r"[^\w\- ]", "", titulo.strip().lower()).replace(" ", "-")


def ancoras(texto):
    return {ancora(linha.lstrip("#")) for linha in texto.splitlines() if re.match(r"#{1,6} ", linha)}


def erro_do_link(raiz, conhecidos, ref, caminho, ancora_do_link):
    """O que está errado num link para o próprio repositório, ou None."""
    if ref != "main":
        return f"aponta para `{ref}`; aponte para a `main`, a que o leitor vê"
    if caminho not in conhecidos and not any(nome.startswith(caminho.rstrip("/") + "/") for nome in conhecidos):
        return "o arquivo não existe no git"
    if ancora_do_link and ancora_do_link not in ancoras(ler(raiz / caminho)):
        return f"a âncora #{ancora_do_link} não é de nenhum título de {caminho}"
    return None


def links_quebrados(raiz, arquivos):
    """Mensagens para cada link do próprio repositório, nas skills e nos moldes, que não chega ao destino."""
    conhecidos = set(arquivos)
    lidos = [a for a in arquivos if (a.startswith("skills/") and a.endswith(".md")) or a in MOLDES_COPIADOS]
    erros = []
    for nome in sorted(lidos):
        for ref, caminho, ancora_do_link in sorted({m[1:] for m in ENDERECO_PROPRIO.findall(ler(raiz / nome))}):
            erro = erro_do_link(raiz, conhecidos, ref, caminho, ancora_do_link)
            if erro:
                erros.append(f"{nome}: {ENDERECO}/…/{caminho} — {erro}")
    return erros


def arquivos_do_git(raiz):
    # Só os arquivos que o git conhece: um link para um arquivo por commitar não chega a quem lê no GitHub.
    return subprocess.run(["git", "ls-files"], cwd=raiz, capture_output=True, text=True, encoding="utf-8",
                          check=True).stdout.splitlines()


class CaminhosDoMorgLaws(unittest.TestCase):
    maxDiff = None  # a falha mostra todas as mensagens, cada uma com o que fazer

    def test_as_skills_citam_o_repositorio_so_com_link(self):
        self.assertEqual(caminhos_sem_link(RAIZ, arquivos_do_git(RAIZ)), [])

    def test_os_links_para_o_repositorio_chegam_ao_destino(self):
        self.assertEqual(links_quebrados(RAIZ, arquivos_do_git(RAIZ)), [])


class NumaPastaTemporaria(unittest.TestCase):
    """Os casos da prova do plano, numa pasta temporária, nunca nos arquivos do repositório."""

    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.raiz = Path(pasta.name)
        for nome, texto in {"FONTES.md": "# Fontes\n\n## Banco de dados (PostgreSQL, Supabase)\n",
                            "modelos/documentos/handoff.md": "# H\n", "modelos/testes/test_docs_indices.py": "",
                            "skills/x/references/tetos.md": "# T\n"}.items():
            self.escrever(nome, texto)

    def escrever(self, nome, texto):
        (self.raiz / nome).parent.mkdir(parents=True, exist_ok=True)
        (self.raiz / nome).write_text(texto, encoding="utf-8")

    def arquivos(self):
        return sorted(c.relative_to(self.raiz).as_posix() for c in self.raiz.rglob("*") if c.is_file())

    def erros_da_skill(self, texto):
        self.escrever("skills/x/SKILL.md", texto)
        return caminhos_sem_link(self.raiz, self.arquivos())

    def test_ver_fontes_sem_link(self):
        self.assertEqual(self.erros_da_skill("## Fontes\n\nVer `FONTES.md`.\n"),
                         [(f"skills/x/SKILL.md: `FONTES.md` — não vem com a skill; escreva o link completo "
                           f"[`FONTES.md`]({ENDERECO}/blob/main/FONTES.md)")])

    def test_pasta_do_repositorio_e_script_pelo_nome_sem_link(self):
        erros = self.erros_da_skill("O molde está em `modelos/documentos/handoff.md`, ver modelos/ e o "
                                    "`test_docs_indices.py`.\n")
        self.assertEqual([erro.split(" — ")[0] for erro in erros],
                         ["skills/x/SKILL.md: `modelos`", "skills/x/SKILL.md: `modelos/documentos/handoff.md`",
                          "skills/x/SKILL.md: `test_docs_indices.py`"])
        self.assertIn(f"({ENDERECO}/tree/main/modelos)", erros[0])
        self.assertIn(f"({ENDERECO}/blob/main/modelos/testes/test_docs_indices.py)", erros[2])

    def test_tipos_de_arquivo_o_que_vem_com_a_skill_e_o_link_passam(self):
        texto = (f"Um `CLAUDE.md` ou AGENTS.md, o `.gitignore` e `.context/HANDOFF-x.md`. Ver `references/tetos.md`, "
                 f"[`FONTES.md`]({ENDERECO}/blob/main/FONTES.md) e o `lockfile.c` do git.\n")
        self.assertEqual(self.erros_da_skill(texto), [])

    def erros_dos_links(self, texto):
        self.escrever("skills/x/SKILL.md", texto)
        return links_quebrados(self.raiz, self.arquivos())

    def test_link_para_arquivo_que_nao_existe_ancora_errada_e_outro_ramo(self):
        texto = (f"[a]({ENDERECO}/blob/main/NAO-EXISTE.md) [b]({ENDERECO}/blob/main/FONTES.md#segurança) "
                 f"[c]({ENDERECO}/blob/v1/FONTES.md)\n")
        self.assertEqual([erro.split(" — ")[1] for erro in self.erros_dos_links(texto)],
                         ["a âncora #segurança não é de nenhum título de FONTES.md",
                          "o arquivo não existe no git",
                          "aponta para `v1`; aponte para a `main`, a que o leitor vê"])

    def test_links_certos_com_ancora_e_pasta_passam(self):
        texto = (f"[a]({ENDERECO}/blob/main/FONTES.md#banco-de-dados-postgresql-supabase) "
                 f"[b]({ENDERECO}/tree/main/modelos/documentos) [c]({ENDERECO})\n")
        self.assertEqual(self.erros_dos_links(texto), [])
        self.escrever("modelos/documentos/AGENTS.md", f"[d]({ENDERECO}/blob/main/sumiu.md)\n")
        self.assertEqual(len(links_quebrados(self.raiz, self.arquivos())), 1)


if __name__ == "__main__":
    unittest.main()
