"""Ler um texto do repositório e listar os arquivos que o git conhece: uma só fonte para os testes do Morg-laws."""

import subprocess


def ler(caminho):
    """O texto em UTF-8, sem o BOM se houver."""
    return caminho.read_text(encoding="utf-8-sig")


def arquivos_do_git(raiz, *padroes):
    # Só os arquivos que o git conhece: um arquivo novo é conferido depois do `git add`, e um link para um arquivo
    # por commitar não chega a quem lê no GitHub.
    return subprocess.run(["git", "ls-files", *padroes], cwd=raiz, capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout.splitlines()
