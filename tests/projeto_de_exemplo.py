"""Monta, numa pasta temporária, um projeto de exemplo só com os modelos do Morg-laws (regras, docs, hooks,
portões, testes e skills), num repositório git com identidade fictícia. Usado pelos testes de ponta a ponta."""

import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from carregar_modelos import MODELOS, RAIZ

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


def copiar_modelos(pasta):
    for origem, destino in COPIAS.items():
        alvo = pasta / destino
        alvo.parent.mkdir(parents=True, exist_ok=True)
        (shutil.copytree if (MODELOS / origem).is_dir() else shutil.copy2)(MODELOS / origem, alvo)
    for skill in SKILLS:
        shutil.copytree(RAIZ / "skills" / skill, pasta / ".claude" / "skills" / skill)


def montar():
    """Cria o projeto de exemplo e devolve a pasta (apague-a com `apagar`)."""
    pasta = Path(tempfile.mkdtemp(prefix="morg-exemplo-"))
    copiar_modelos(pasta)
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


def rodar_testes(pasta):
    """Roda os testes-modelo no projeto de exemplo; devolve (código de saída, saída do unittest)."""
    resultado = subprocess.run([sys.executable, "-I", "-m", "unittest", "discover", "-s", "tests"], cwd=pasta,
                               capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
                               timeout=300)
    return resultado.returncode, resultado.stderr
