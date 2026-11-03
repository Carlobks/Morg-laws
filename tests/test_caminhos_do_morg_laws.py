"""Quem instala o Morg-laws recebe só a pasta de cada skill e o molde do AGENTS.md: um caminho do repositório citado
sem link aponta, no projeto, para um arquivo que não existe. Por isso o CI confere:

1. nenhuma skill (`skills/**/*.md`) cita, sem link completo, um arquivo ou pasta do Morg-laws que não venha com ela:
   - um caminho cuja primeira pasta só existe neste repositório (`modelos/`, `pesquisas/`…);
   - um pedaço do fim de um caminho dessas pastas (`documentos/handoff.md`);
   - o nome solto de um arquivo de fora de `skills/` (`FONTES.md`, `test_docs_indices.py`);
   - um link Markdown relativo que sai da pasta da skill (`../../FONTES.md`) ou que não chega a nada.
   O que está na pasta da própria skill (`references/…`) vem com ela. As pastas e os nomes que todo projeto tem
   (`tests/`, `scripts/`, `skills/`, `CLAUDE.md`, `settings.json`…) falam do projeto do leitor e não contam;
2. cada link para o próprio repositório (com `http` ou `https`, com qualquer caixa), nas skills e nos moldes do
   AGENTS.md e do CLAUDE.md, aponta para a `main`, para um arquivo que o git conhece e, quando tem âncora, para um
   título que existe nesse arquivo.
As funções recebem a raiz e a lista de arquivos, para os casos de erro serem provados numa pasta temporária.
"""

import re
import tempfile
import unittest
from pathlib import Path

from carregar_modelos import RAIZ
from leitura_do_repositorio import arquivos_do_git, ler

ENDERECO = "https://github.com/Carlobks/Morg-laws"
MOLDES_COPIADOS = ("modelos/documentos/AGENTS.md", "modelos/documentos/CLAUDE.md")
PASTAS_SO_DO_MORG_LAWS = ("modelos", "pesquisas", "aprendizados", "biblia-akita", "prova")
NOMES_QUE_TODO_PROJETO_TEM = frozenset({"AGENTS.md", "CLAUDE.md", "README.md", "LICENSE", ".gitignore",
                                        ".gitattributes", "settings.json", "pre-commit", "commit-msg", "pre-push"})
# Um projeto de exemplo dentro do repositório: os nomes dos arquivos dele (package.json…) são os de qualquer projeto.
PROJETO_DA_PROVA = "prova/projeto-teste/"
_PROPRIO = r"https?://github\.com/Carlobks/Morg-laws"
LINK_PROPRIO = re.compile(r"\[[^\]]*\]\(" + _PROPRIO + r"[^)\s]*\)", re.IGNORECASE)
ENDERECO_PROPRIO = re.compile(_PROPRIO + r"/(blob|tree)/([^/\s)]+)/([^)\s#>`]+)(?:#([^)\s>`]+))?", re.IGNORECASE)
LINK_RELATIVO = re.compile(r"\]\((?![a-z][a-z0-9+.-]*:|#)([^)\s]+)\)", re.IGNORECASE)
URL = re.compile(r"https?://\S+")
ENTRE_CRASES = re.compile(r"`([^`\s]+)`")
SOLTO = re.compile(r"(?<![\w./`-])((?:[\w.-]+/)+[\w.-]*|[\w.-]+\.(?:md|py|sh|mjs))(?![\w/`])")


def candidatos(texto):
    """Os caminhos citados fora de um link: entre crases ou soltos na prosa. A barra final diz que é pasta."""
    sem_links = URL.sub(" ", LINK_RELATIVO.sub(" ", LINK_PROPRIO.sub(" ", texto)))
    soltos = SOLTO.findall(ENTRE_CRASES.sub(" ", sem_links))
    return {c.removeprefix("./") for c in ENTRE_CRASES.findall(sem_links) + soltos} - {""}


def indice_do_repositorio(arquivos):
    """{nome solto: caminho} dos arquivos de fora de skills/, e os caminhos das pastas só do Morg-laws."""
    fora = sorted(nome for nome in arquivos if not nome.startswith(("skills/", PROJETO_DA_PROVA)))
    por_nome = {}
    for nome in fora:
        por_nome.setdefault(Path(nome).name, nome)
    so_do_morg = [nome for nome in fora if nome.split("/")[0] in PASTAS_SO_DO_MORG_LAWS]
    return por_nome, so_do_morg


def subcaminho(citado, so_do_morg):
    """O arquivo das pastas só do Morg-laws de cujo caminho `citado` é o fim, ou None."""
    return next((nome for nome in so_do_morg if ("/" + nome).endswith("/" + citado)), None)


def no_morg_laws(citado, pasta_da_skill, raiz, indice):
    """O caminho no Morg-laws de um arquivo ou pasta citado que não vem com a skill, ou None."""
    por_nome, so_do_morg = indice
    if "://" in citado or citado in NOMES_QUE_TODO_PROJETO_TEM or (pasta_da_skill / citado).exists():
        return None
    if "/" not in citado:
        return por_nome.get(citado)
    if citado.split("/")[0] in PASTAS_SO_DO_MORG_LAWS:
        return citado.rstrip("/") if (raiz / citado).exists() else None
    return subcaminho(citado, so_do_morg)


def link_completo(raiz, caminho):
    tipo = "tree" if (raiz / caminho).is_dir() else "blob"
    return f"{ENDERECO}/{tipo}/main/{caminho}"


def links_relativos_quebrados(raiz, nome, texto, pasta_da_skill):
    """Mensagens para cada link Markdown relativo que sai da pasta da skill ou não chega a nada."""
    erros = []
    for alvo in sorted(set(LINK_RELATIVO.findall(texto))):
        destino = ((raiz / nome).parent / alvo.split("#")[0]).resolve()
        if not destino.is_relative_to(pasta_da_skill.resolve()):
            dentro = destino.is_relative_to(raiz.resolve()) and destino.exists()
            completo = link_completo(raiz, destino.relative_to(raiz.resolve()).as_posix()) if dentro else "…"
            erros.append(f"{nome}: ({alvo}) — sai da pasta da skill, que é tudo o que se instala; escreva o link "
                         f"completo ({completo})")
        elif not destino.exists():
            erros.append(f"{nome}: ({alvo}) — link relativo para o que não existe")
    return erros


def caminhos_sem_link(raiz, arquivos):
    """Mensagens para cada caminho do Morg-laws citado sem link completo numa skill."""
    indice = indice_do_repositorio(arquivos)
    erros = []
    for nome in sorted(a for a in arquivos if a.startswith("skills/") and a.endswith(".md")):
        pasta_da_skill = raiz / Path(nome).parts[0] / Path(nome).parts[1]
        texto = ler(raiz / nome)
        for citado in sorted(candidatos(texto)):
            caminho = no_morg_laws(citado, pasta_da_skill, raiz, indice)
            if caminho:
                erros.append(f"{nome}: `{citado}` — não vem com a skill; escreva o link completo "
                             f"[`{citado}`]({link_completo(raiz, caminho)})")
        erros += links_relativos_quebrados(raiz, nome, texto, pasta_da_skill)
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


class CaminhosDoMorgLaws(unittest.TestCase):
    maxDiff = None  # a falha mostra todas as mensagens, cada uma com o que fazer

    def test_as_skills_citam_o_repositorio_so_com_link(self):
        self.assertEqual(caminhos_sem_link(RAIZ, arquivos_do_git(RAIZ)), [])

    def test_os_links_para_o_repositorio_chegam_ao_destino(self):
        self.assertEqual(links_quebrados(RAIZ, arquivos_do_git(RAIZ)), [])


class NumaPastaTemporaria(unittest.TestCase):
    """Os casos da prova do plano e da auditoria, numa pasta temporária, nunca nos arquivos do repositório."""

    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.raiz = Path(pasta.name)
        for nome, texto in {"FONTES.md": "# Fontes\n\n## Banco de dados (PostgreSQL, Supabase)\n",
                            "modelos/documentos/handoff.md": "# H\n", "modelos/testes/test_docs_indices.py": "",
                            "modelos/documentos/regras-e-barreiras.md": "# R\n", "modelos/claude/settings.json": "{}",
                            "tests/test_x.py": "", "scripts/testar.sh": "", "skills/x/references/tetos.md": "# T\n"
                            }.items():
            self.escrever(nome, texto)

    def escrever(self, nome, texto):
        (self.raiz / nome).parent.mkdir(parents=True, exist_ok=True)
        (self.raiz / nome).write_text(texto, encoding="utf-8")

    def arquivos(self):
        return sorted(c.relative_to(self.raiz).as_posix() for c in self.raiz.rglob("*") if c.is_file())

    def erros_da_skill(self, texto):
        self.escrever("skills/x/SKILL.md", texto)
        return caminhos_sem_link(self.raiz, self.arquivos())

    def citados_que_reprovam(self, texto):
        return [erro.split(" — ")[0].removeprefix("skills/x/SKILL.md: ") for erro in self.erros_da_skill(texto)]

    def test_ver_fontes_sem_link(self):
        self.assertEqual(self.erros_da_skill("## Fontes\n\nVer `FONTES.md`.\n"),
                         [(f"skills/x/SKILL.md: `FONTES.md` — não vem com a skill; escreva o link completo "
                           f"[`FONTES.md`]({ENDERECO}/blob/main/FONTES.md)")])

    def test_pasta_do_repositorio_e_script_pelo_nome_sem_link(self):
        erros = self.erros_da_skill("O molde está em `modelos/documentos/handoff.md`, ver modelos/ e o "
                                    "`test_docs_indices.py`.\n")
        self.assertEqual([erro.split(" — ")[0] for erro in erros],
                         ["skills/x/SKILL.md: `modelos/`", "skills/x/SKILL.md: `modelos/documentos/handoff.md`",
                          "skills/x/SKILL.md: `test_docs_indices.py`"])
        self.assertIn(f"({ENDERECO}/tree/main/modelos)", erros[0])
        self.assertIn(f"({ENDERECO}/blob/main/modelos/testes/test_docs_indices.py)", erros[2])

    def test_link_relativo_que_sai_da_pasta_da_skill(self):
        # O caso mais provável de voltar: no GitHub o link relativo funciona; depois do `npx skills add`, não.
        erros = self.erros_da_skill("Ver o link relativo [FONTES](../../FONTES.md) e [r](references/nada.md).\n")
        self.assertEqual(erros, [
            (f"skills/x/SKILL.md: (../../FONTES.md) — sai da pasta da skill, que é tudo o que se instala; escreva o "
             f"link completo ({ENDERECO}/blob/main/FONTES.md)"),
            "skills/x/SKILL.md: (references/nada.md) — link relativo para o que não existe"])

    def test_nome_solto_de_documento_e_subcaminho(self):
        self.assertEqual(self.citados_que_reprovam("O mapa `regras-e-barreiras.md` e o molde `documentos/handoff.md` "
                                                   "dos modelos.\n"),
                         ["`documentos/handoff.md`", "`regras-e-barreiras.md`"])
        erros = self.erros_da_skill("O molde `documentos/handoff.md`.\n")
        self.assertIn(f"({ENDERECO}/blob/main/modelos/documentos/handoff.md)", erros[0])

    def test_o_que_todo_projeto_tem_passa(self):
        texto = ("Ponha os testes do projeto em `tests/`. Rode `scripts/testar.sh` do seu projeto. Instaladas em "
                 "`skills/` ou `.claude/skills/`. O `.claude/settings.json` e o `settings.json` do projeto, o "
                 "`pre-commit`, e o `package.json`.\n")
        self.escrever("prova/projeto-teste/package.json", "{}")
        self.assertEqual(self.erros_da_skill(texto), [])

    def test_tipos_de_arquivo_o_que_vem_com_a_skill_e_o_link_passam(self):
        texto = (f"Um `CLAUDE.md` ou AGENTS.md, o `.gitignore` e `.context/HANDOFF-x.md`. Ver `references/tetos.md`, "
                 f"[t](references/tetos.md), [`FONTES.md`]({ENDERECO}/blob/main/FONTES.md), "
                 f"[e](https://example.com/a), [s](#fontes) e o `lockfile.c` do git.\n")
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

    def test_endereco_com_outra_caixa_ou_com_http_tambem_se_confere(self):
        texto = ("[x](https://github.com/carlobks/Morg-laws/blob/main/NAO.md) "
                 "[y](http://github.com/Carlobks/Morg-laws/blob/main/NAO2.md)\n")
        self.assertEqual([erro.split(" — ")[1] for erro in self.erros_dos_links(texto)],
                         ["o arquivo não existe no git", "o arquivo não existe no git"])

    def test_links_certos_com_ancora_e_pasta_passam(self):
        texto = (f"[a]({ENDERECO}/blob/main/FONTES.md#banco-de-dados-postgresql-supabase) "
                 f"[b]({ENDERECO}/tree/main/modelos/documentos) [c]({ENDERECO})\n")
        self.assertEqual(self.erros_dos_links(texto), [])
        self.escrever("modelos/documentos/AGENTS.md", f"[d]({ENDERECO}/blob/main/sumiu.md)\n")
        self.assertEqual(len(links_quebrados(self.raiz, self.arquivos())), 1)


if __name__ == "__main__":
    unittest.main()
