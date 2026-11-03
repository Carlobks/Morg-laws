"""Motor das catracas com linha de base (Morg-laws: não piorar). Usado por test_tamanho_dos_arquivos.py,
test_nomes_unicos.py e test_testes_saltados.py.

Cada catraca mede, por arquivo, o EXCESSO sobre a regra (`{"src/a.py": {"linhasAcima": 12}}`; zero não aparece)
e compara-o com a linha de base em `tests/linhas-de-base/<regra>.json`. O formato é o mesmo dos moldes TypeScript
(`linha-de-base.mjs`), e as três verificações também, cada uma num teste:
- não piora: nenhuma métrica passa da base; um arquivo fora da base nasce limpo;
- sem folga: a base não deixa mais do que existe hoje (quem corrige desce a base no mesmo commit);
- só encolhe: a base do índice não tem entrada nova nem valor maior do que a do último commit.
Lê do índice do git (o que vai no commit), nunca do disco: o trabalho a meio de outra sessão na mesma pasta não
trava o commit desta. Um arquivo novo conta depois do `git add`.
Projeto que já viola: rode uma vez com MORG_CRIAR_LINHA_DE_BASE=1. A base que falta é criada com os valores de
hoje, e o teste falha até ela entrar no git. Uma base que já existe nunca é reescrita.
Instalar: copiar para `tests/` do projeto, ao lado do carregar_por_caminho.py.
"""

import json
import os
import subprocess

from carregar_por_caminho import RAIZ

# Ajuste ao projeto.
PASTA_DAS_LINHAS_DE_BASE = "tests/linhas-de-base"


def correr_git(argumentos, entrada=b""):
    return subprocess.run(["git", *argumentos], cwd=RAIZ, input=entrada, capture_output=True, check=True).stdout


def arquivos_do_indice():
    """Os caminhos que o índice do git conhece (o que vai no próximo commit)."""
    return [caminho for caminho in correr_git(["ls-files", "-z"]).decode("utf-8").split("\0") if caminho]


def ler_do_git(caminhos, origem=":"):
    """{caminho: texto} dos arquivos pedidos, como estão em `origem` (":" é o índice; "HEAD:", o último commit)."""
    saida = correr_git(["cat-file", "--batch"], "".join(f"{origem}{caminho}\n" for caminho in caminhos).encode())
    textos, posicao = {}, 0
    for caminho in caminhos:
        fim = saida.index(b"\n", posicao)
        cabecalho = saida[posicao:fim].decode("utf-8")
        if cabecalho.endswith(" missing"):
            posicao = fim + 1
            continue
        tamanho = int(cabecalho.split(" ")[2])
        textos[caminho] = saida[fim + 1:fim + 1 + tamanho].decode("utf-8", errors="replace").removeprefix("﻿")
        posicao = fim + 1 + tamanho + 1
    return textos


def caminho_da_base(regra):
    return f"{PASTA_DAS_LINHAS_DE_BASE}/{regra}.json"


def ler_linha_de_base(regra, origem=":"):
    """Os valores da linha de base da regra em `origem`; None se ela não existir lá."""
    texto = ler_do_git([caminho_da_base(regra)], origem).get(caminho_da_base(regra))
    return None if texto is None else json.loads(texto).get("valores", {})


def acima_de(valores, teto, frase):
    """Mensagens de cada métrica de `valores` que passa do mesmo valor em `teto` (o que falta conta como 0)."""
    return [f"{caminho}: {metrica} {valor} ({frase} {teto.get(caminho, {}).get(metrica, 0)})"
            for caminho, metricas in sorted(valores.items()) for metrica, valor in sorted(metricas.items())
            if valor > teto.get(caminho, {}).get(metrica, 0)]


def criar_se_faltar(regra, atuais):
    """Com MORG_CRIAR_LINHA_DE_BASE=1, grava a base que ainda não existe; devolve a mensagem, ou None."""
    destino = RAIZ / caminho_da_base(regra)
    if os.environ.get("MORG_CRIAR_LINHA_DE_BASE") != "1" or destino.exists() or ler_linha_de_base(regra) is not None:
        return None
    destino.parent.mkdir(parents=True, exist_ok=True)
    valores = {caminho: dict(sorted(metricas.items())) for caminho, metricas in sorted(atuais.items())}
    destino.write_bytes((json.dumps({"regra": regra, "valores": valores}, indent=2, ensure_ascii=False) + "\n")
                        .encode("utf-8"))
    return f"linha de base criada em {caminho_da_base(regra)}: confira-a e faça git add"


class TresVerificacoesDaCatraca:
    """Mistura para um unittest.TestCase: defina REGRA, CONSELHO, `medir()` e `julga(caminho, metrica)`."""

    def conferir(self):
        # Uma medição por classe: os três testes julgam o mesmo estado do índice.
        if not hasattr(type(self), "_conferido"):
            atuais = self.medir()
            criada = criar_se_faltar(self.REGRA, atuais)
            type(self)._conferido = (atuais, ler_linha_de_base(self.REGRA) or {},
                                     ler_linha_de_base(self.REGRA, "HEAD:"), criada)
        return type(self)._conferido

    def test_nao_piora(self):
        atuais, base, _, criada = self.conferir()
        self.assertEqual(([criada] if criada else []) + acima_de(atuais, base, "a base deixa"), [], self.CONSELHO)

    def test_a_linha_de_base_nao_tem_folga(self):
        atuais, base, _, _ = self.conferir()
        sobras = {caminho: {metrica: valor for metrica, valor in metricas.items() if self.julga(caminho, metrica)}
                  for caminho, metricas in base.items()}
        self.assertEqual(acima_de(sobras, atuais, "hoje há"), [], "desça a linha de base no mesmo commit")

    def test_a_linha_de_base_so_encolhe(self):
        _, base, do_ultimo_commit, _ = self.conferir()
        novas = [] if do_ultimo_commit is None else acima_de(base, do_ultimo_commit, "o último commit deixava")
        self.assertEqual(novas, [], "a linha de base só desce: corrija o código em vez de a subir")
