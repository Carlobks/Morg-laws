"""Monta, numa pasta temporária, um projeto de exemplo só com os modelos do Morg-laws (regras, docs, hooks,
portões, testes e skills), num repositório git com identidade fictícia. Usado pelos testes de ponta a ponta."""

import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from carregar_modelos import MODELOS, RAIZ
from leitura_do_repositorio import ler

# Todas, como instala o `npx skills add`: o índice do molde AGENTS.md cita todas.
SKILLS = tuple(sorted(pasta.name for pasta in (RAIZ / "skills").iterdir() if (pasta / "SKILL.md").is_file()))
COPIAS = {
    "documentos/AGENTS.md": "AGENTS.md",
    "documentos/CLAUDE.md": "CLAUDE.md",
    "documentos/regras-e-barreiras.md": "docs/regras-e-barreiras.md",
    "documentos/plano.md": "docs/planos/0001-exemplo.md",
    "documentos/armadilhas.md": "docs/armadilhas.md",
    "documentos/adr.md": "docs/decisoes/0001-exemplo.md",
    "documentos/handoff.md": ".context/HANDOFF-exemplo.md",
    "claude/settings.json": ".claude/settings.json",
    "claude/hooks": ".claude/hooks",
    "git/hooks": ".githooks",
    "git/portoes": "scripts/portoes",
    "testes": "tests",
    "changelog/juntar_changelog.py": "scripts/changelog/juntar_changelog.py",
    "changelog/changelog.d": "changelog.d",
    "github": ".github",
}
INDICE_DOS_DOCS = ("# Docs\n\n- [regras-e-barreiras.md](regras-e-barreiras.md)\n- [armadilhas.md](armadilhas.md)\n"
                   "- [planos/](planos/)\n- [decisoes/](decisoes/) · [0001](decisoes/0001-exemplo.md)\n")
IGNORADOS = ["." + "env", "." + "env.*", "*.pem", "*.key", "__pycache__/"]


def escrever(caminho, texto):
    """Grava em UTF-8 com LF (o write_text do Windows trocaria por CRLF)."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(texto.encode("utf-8"))


def git(pasta, *args, **opcoes):
    return subprocess.run(["git", *args], cwd=pasta, capture_output=True, text=True, encoding="utf-8",
                          check=opcoes.pop("check", True), **opcoes)


def apagar(pasta):
    """Apaga a pasta; os objetos do git são só de leitura no Windows."""
    def _liberar(funcao, caminho, _):
        os.chmod(caminho, stat.S_IWRITE)
        funcao(caminho)
    shutil.rmtree(pasta, onerror=_liberar)


def indice_so_com(texto, skills):
    """O molde AGENTS.md com o índice só das `skills`: tira o nome das outras e a linha que ficar sem nenhuma."""
    antes, marca, depois = texto.partition("## Índice: quando ler o quê")
    cabeca, fim = depois.split("\n## ", 1) if "\n## " in depois else (depois, None)
    linhas = []
    for linha in cabeca.splitlines():
        if linha.startswith("| ") and "`" in linha:
            linha_nova = _linha_so_com(linha, skills)
            linhas += [linha_nova] if linha_nova else []
        else:
            linhas.append(linha)
    return antes + marca + "\n".join(linhas) + ("\n\n## " + fim if fim is not None else "\n")


def _linha_so_com(linha, skills):
    """A linha da tabela só com os nomes de `skills` (None se não sobra nenhum)."""
    situacao, _, nomes = linha.rstrip(" |").rpartition(" | ")
    ficam = [nome for nome in re.findall(r"`([a-z0-9-]+)`", nomes) if nome in skills]
    return f"{situacao} | {', '.join(f'`{nome}`' for nome in ficam)} |" if ficam else None


def copiar_modelos(pasta, skills):
    for origem, destino in COPIAS.items():
        alvo = pasta / destino
        alvo.parent.mkdir(parents=True, exist_ok=True)
        (shutil.copytree if (MODELOS / origem).is_dir() else shutil.copy2)(MODELOS / origem, alvo)
    for skill in skills:
        shutil.copytree(RAIZ / "skills" / skill, pasta / ".claude" / "skills" / skill)


def montar(skills=None):
    """Cria o projeto de exemplo e devolve a pasta (apague-a com `apagar`). Sem `skills`, instala todas e deixa o
    índice do molde como está; com uma parte delas, o índice leva só as instaladas."""
    pasta = Path(tempfile.mkdtemp(prefix="morg-exemplo-"))
    copiar_modelos(pasta, SKILLS if skills is None else skills)
    if skills is not None:
        escrever(pasta / "AGENTS.md", indice_so_com(ler(MODELOS / "documentos" / "AGENTS.md"), skills))
    escrever(pasta / "docs" / "README.md", INDICE_DOS_DOCS)
    escrever(pasta / ".gitignore", "\n".join(IGNORADOS) + "\n")
    escrever(pasta / ".gitattributes", "* text=auto eol=lf\n*.ps1 text eol=crlf\n")
    escrever(pasta / "src" / "total_do_pedido.py", 'def total_do_pedido(itens):\n    """Soma."""\n    return sum(itens)\n')
    git(pasta, "init", "-q")
    for chave, valor in (("user.email", "1+ana@users.noreply.github.com"), ("user.name", "Ana"),
                         ("core.autocrlf", "false"), ("core.hooksPath", ".githooks"), ("morg.listaNegra", "")):
        git(pasta, "config", "--local", chave, valor)
    git(pasta, "add", "--", ".")
    return pasta


def rodar_testes(pasta, padrao="test*.py", verboso=False):
    """Roda os testes-modelo (ou só os arquivos que `padrao` pede) no projeto de exemplo; devolve (código de saída,
    saída do unittest). Verboso, a saída diz cada teste e o motivo de cada salto."""
    resultado = subprocess.run([sys.executable, "-I", "-m", "unittest", "discover", "-s", "tests", "-p", padrao,
                                *(["-v"] if verboso else [])],
                               cwd=pasta,
                               capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
                               timeout=300)
    return resultado.returncode, resultado.stderr
