"""Portão do git (commit-msg): a mensagem segue o formato do Morg-laws (skill git-e-commits).

- título `tipo(área): …` (a área é opcional), com até 72 caracteres e sem ponto final;
- linha em branco entre o título e o corpo; fix, feat e refactor levam corpo com o que mudou e porquê;
- um fix sem nenhum arquivo de teste (padrão TESTE) leva a linha `Sem-teste: <motivo>`;
- um feat ou fix que mexa no que se publica para quem usa (PUBLICADO) leva um fragmento changelog.d/*.md ou a
  linha `Sem-changelog: <motivo>`;
- um commit que tira ou muda linhas de um teste que já existia leva `Teste-mudado: <motivo>` (acrescentar casos
  não pede nada): um teste afrouxado fica verde e deixa de proteger;
- uma versão lançada do CHANGELOG.md não muda sem `Changelog-corrigido: <motivo>`, e o VERSION só muda no
  lançamento (versao_lancada.py).
Os títulos que o próprio git escreve (Merge …, Revert "…") passam. As linhas com # são do git e não contam.
Uso: python -I scripts/portoes/mensagem_commit.py <arquivo da mensagem>   Sai com 1 se recusar.
"""

import re
import subprocess
import sys
from pathlib import Path

# Com `-I` a pasta do script não entra no sys.path: sem isto o import seguinte falhava.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lista_negra
import versao_lancada

# Ajuste ao projeto: o que conta como teste, e o que chega a quem usa (vazio: o changelog não é exigido).
TESTE = re.compile(r"(?:^|/)tests?/|\.(?:test|spec)\.[^/]+$|(?:^|/)test_[^/]+\.py$")
PUBLICADO = ()  # ex.: ("src/", "instalador/")

TIPOS = ("feat", "fix", "docs", "test", "refactor", "chore", "build", "ci", "perf", "style")
EXIGEM_CORPO = ("feat", "fix", "refactor")
MAXIMO_DO_TITULO = 72
TITULO_DO_COMMIT = re.compile(r"^(?P<tipo>[a-z]+)(?:\([a-z0-9-]+\))?: \S")
TITULOS_DO_GIT = ("Merge ", 'Revert "')
# Linhas finais de metadados: não contam como corpo.
RODAPE = re.compile(r"^(?:Co-Authored-By|Signed-off-by|Sem-teste|Sem-changelog|Teste-mudado|Changelog-corrigido):",
                    re.IGNORECASE)
TESTE_MUDADO = re.compile(r"^Teste-mudado: *\S", re.MULTILINE)
SEM_TESTE = re.compile(r"^Sem-teste: *\S", re.MULTILINE)
SEM_CHANGELOG = re.compile(r"^Sem-changelog: *\S", re.MULTILINE)
FRAGMENTO = re.compile(r"^changelog\.d/[^/]+\.md$")


def linhas_da_mensagem(texto):
    """Linhas da mensagem sem os comentários do git e sem as linhas vazias do fim."""
    linhas = [linha.rstrip() for linha in texto.splitlines() if not linha.startswith("#")]
    while linhas and not linhas[-1]:
        linhas.pop()
    return linhas


def erros_do_titulo(titulo):
    """Motivos para recusar o título; o tipo vem em segundo (None se o formato estiver errado)."""
    motivos = []
    if len(titulo) > MAXIMO_DO_TITULO:
        motivos.append(f"ERRO: o título tem {len(titulo)} caracteres (máximo {MAXIMO_DO_TITULO}).")
    formato = TITULO_DO_COMMIT.match(titulo)
    if not formato or formato["tipo"] not in TIPOS:
        motivos.append(f"ERRO: o título tem de começar por tipo(área): … com um destes tipos: {', '.join(TIPOS)}.")
        return motivos, None
    if titulo.endswith("."):
        motivos.append("ERRO: o título não leva ponto final.")
    return motivos, formato["tipo"]


def erros(texto, arquivos, testes_mudados=()):
    """Lista dos motivos para recusar a mensagem (vazia se estiver certa).

    `arquivos` são os do commit; `testes_mudados`, os testes que já existiam e perdem ou mudam linhas.
    """
    linhas = linhas_da_mensagem(texto)
    if not linhas:
        return ["ERRO: a mensagem do commit está vazia."]
    if linhas[0].startswith(TITULOS_DO_GIT):
        return []
    motivos, tipo = erros_do_titulo(linhas[0])
    return motivos + erros_do_corpo(linhas, tipo) + erros_das_linhas_de_motivo(texto, tipo, arquivos, testes_mudados)


def erros_do_corpo(linhas, tipo):
    """Linha em branco depois do título, e corpo nos tipos que o exigem (os rodapés não contam como corpo)."""
    motivos = []
    if len(linhas) > 1 and linhas[1]:
        motivos.append("ERRO: falta a linha em branco entre o título e o corpo.")
    corpo = [linha for linha in linhas[1:] if linha and not RODAPE.match(linha)]
    if tipo in EXIGEM_CORPO and not corpo:
        motivos.append(f"ERRO: um commit {tipo} leva corpo com o que mudou e porquê.")
    return motivos


def erros_das_linhas_de_motivo(texto, tipo, arquivos, testes_mudados):
    """As linhas Sem-teste, Sem-changelog e Teste-mudado que os arquivos do commit exigem e faltam."""
    motivos = []
    if tipo == "fix" and not any(TESTE.search(a) for a in arquivos) and not SEM_TESTE.search(texto):
        motivos.append("ERRO: um fix traz o teste que pega o bug ou a linha 'Sem-teste: <motivo concreto>'.")
    if tipo in ("feat", "fix") and falta_changelog(texto, arquivos):
        motivos.append(f"ERRO: um {tipo} que mexe no que se publica leva um fragmento "
                       "changelog.d/AAAA-MM-DD-assunto.md ou a linha 'Sem-changelog: <motivo concreto>'.")
    if testes_mudados and not TESTE_MUDADO.search(texto):
        motivos.append(f"ERRO: o commit tira ou muda linhas de testes que já existiam ({', '.join(testes_mudados)}): "
                       "diga por quê na linha 'Teste-mudado: <motivo>'.")
    return motivos


def falta_changelog(texto, arquivos):
    """True se o commit mexe no que se publica sem fragmento do changelog nem `Sem-changelog:`."""
    mexe = bool(PUBLICADO) and any(a.startswith(PUBLICADO) for a in arquivos)
    return mexe and not any(FRAGMENTO.match(a) for a in arquivos) and not SEM_CHANGELOG.search(texto)


def arquivos_do_commit(correr=None):
    """Arquivos do commit em curso (o git dá aos hooks o índice certo, também num commit por caminho)."""
    saida = (correr or subprocess.run)(["git", "diff", "--cached", "--name-only"], capture_output=True,
                                       text=True, encoding="utf-8", check=False).stdout
    return saida.splitlines()


def testes_com_linhas_tiradas(correr=None):
    """Testes que já existiam e que o commit deixa com linhas a menos (numstat: tiradas > 0 ou binário)."""
    saida = (correr or subprocess.run)(["git", "diff", "--cached", "--numstat", "--diff-filter=M"],
                                       capture_output=True, text=True, encoding="utf-8", check=False).stdout
    linhas = [linha.split("\t", 2) for linha in saida.splitlines()]
    return [caminho for _, tiradas, caminho in linhas if tiradas != "0" and TESTE.search(caminho)]


def main(argv):
    texto = Path(argv[1]).read_bytes().decode("utf-8", errors="replace")
    arquivos = arquivos_do_commit()
    motivos = erros(texto, arquivos, testes_com_linhas_tiradas()) + versao_lancada.erros_do_commit(texto, arquivos)
    for motivo in motivos:
        lista_negra.escrever_erro(motivo)
    if motivos:
        lista_negra.escrever_erro("Commit recusado: corrija a mensagem (formato no início de mensagem_commit.py).")
    return 1 if motivos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
