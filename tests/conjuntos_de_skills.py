"""Os conjuntos de skills do P1 do manual: uma só fonte para os testes e para o projeto de exemplo.

Os comandos `npx skills add Carlobks/Morg-laws … --skill …` do P1 (`manual/03-instalar.md`) são a lista: o primeiro
traz as skills gerais, e cada um dos seguintes soma as de uma tecnologia. O README repete só o das gerais.
"""

import re

from leitura_do_repositorio import ler

PREFIXO_DO_COMANDO = "npx skills add Carlobks/Morg-laws"
CAMINHO_DO_P1 = "manual/03-instalar.md"


def _linhas_de_comando(texto):
    return [linha for linha in texto.splitlines() if linha.startswith(PREFIXO_DO_COMANDO) and "--skill" in linha]


def _secao_do_p1(texto):
    depois_do_p1 = re.split(r"^## P1\b", texto, flags=re.MULTILINE)[-1]
    return re.split(r"^## P2\b", depois_do_p1, flags=re.MULTILINE)[0]


def comandos_do_p1(texto):
    """Os nomes de cada comando de skills do P1, na ordem em que aparecem (uma tupla por comando)."""
    return [tuple(re.findall(r"--skill (\S+)", linha)) for linha in _linhas_de_comando(_secao_do_p1(texto))]


def gerais(raiz):
    """Os nomes do primeiro comando do P1: as skills que servem a qualquer projeto."""
    return comandos_do_p1(ler(raiz / CAMINHO_DO_P1))[0]


def _erros_dos_nomes(comandos, na_pasta):
    todos = [nome for comando in comandos for nome in comando]
    erros = [f"a skill {nome} não está em nenhum comando do P1: ponha-a num conjunto"
             for nome in sorted(na_pasta - set(todos))]
    erros += [f"a skill {nome} está em mais de um comando do P1" for nome in sorted(set(todos)) if todos.count(nome) > 1]
    erros += [f"o P1 cita a skill {nome}, que não existe em skills/" for nome in sorted(set(todos) - na_pasta)]
    erros += ["o P1 tem um comando com supabase sem sql-postgres" for c in comandos
              if "supabase" in c and "sql-postgres" not in c]
    return erros


def erros_dos_conjuntos(raiz):
    """Uma mensagem por problema: skill fora de todos os comandos, repetida, inexistente, Supabase sem SQL e o README."""
    texto_do_p1 = ler(raiz / CAMINHO_DO_P1)
    na_pasta = {pasta.parent.name for pasta in (raiz / "skills").glob("*/SKILL.md")}
    erros = _erros_dos_nomes(comandos_do_p1(texto_do_p1), na_pasta)
    do_p1 = _linhas_de_comando(_secao_do_p1(texto_do_p1))[:1]
    do_readme = _linhas_de_comando(ler(raiz / "README.md"))[:1]
    if do_p1 != do_readme:
        erros.append("o comando das gerais do README é diferente do primeiro comando do P1")
    return erros
