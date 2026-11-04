"""Motor das catracas com linha de base (Morg-laws: não piorar). Usado pelos seis testes prontos da forma do código
(tamanho de arquivo e de função, nomes genéricos e únicos, alarmes e testes saltados).

Cada catraca mede, por arquivo, o EXCESSO sobre a regra (`{"src/a.py": {"linhasAcima": 12}}`; zero não aparece)
e compara-o com a linha de base em `tests/linhas-de-base/<regra>.json`. O formato é o mesmo dos moldes TypeScript
(`linha-de-base.ts`), e as três verificações também, cada uma num teste:
- não piora: nenhuma métrica passa da base; um arquivo fora da base nasce limpo;
- sem folga: a base não deixa mais do que existe hoje (quem corrige desce a base no mesmo commit);
- só encolhe: a base não tem entrada nova nem valor maior do que a da base de comparação. Na máquina, a de
  comparação é a do último commit (HEAD). No CI e numa PR, o índice é o próprio commit: MORG_BASE_DE_COMPARACAO diz
  com que commit comparar (a ponta anterior do ramo de destino), e o checkout precisa do histórico (fetch-depth: 0).
  Uma regra pode deixar a base subir com uma linha na mensagem do commit (MARCA_PARA_SUBIR; a dos alarmes é
  `Alarme-novo:`): na máquina quem a confere é o commit-msg (o pre-commit corre antes da mensagem); no CI, este
  teste confere-a commit a commit (a base em C^ contra a de C, e a marca na mensagem de C). Se a base de comparação
  não for um commit que o git conheça (os 40 zeros de um ramo novo, um push forçado, um nome errado), o teste salta,
  com o motivo escrito, em vez de passar calado.
Lê do índice do git (o que vai no commit), nunca do disco: o trabalho a meio de outra sessão na mesma pasta não
trava o commit desta. Um arquivo novo conta depois do `git add`.
Projeto que já viola: rode uma vez com MORG_CRIAR_LINHA_DE_BASE=1. A base que falta é criada com os valores de
hoje; uma que existe no índice mas ainda não no último commit ganha as métricas que lhe faltam (o caso de um projeto
com as duas línguas, que partilham a pasta). O teste falha até ela entrar no git. Uma base já commitada nunca muda.
Limites conhecidos: mudar de caminho um arquivo que está na base (`git mv`) conta como entrada nova; corrija-o ou
faça um commit só da base, revisto. Apagar a base e criá-la de novo: o commit que a apaga com o código ainda a
violar falha no «não piora», e no CI os dois commits no mesmo push são apanhados; só passa com o primeiro feito sem
os hooks e os dois enviados em pushes separados, e aí só a revisão do histórico o apanha.
Instalar: copiar para `tests/` do projeto, ao lado do carregar_por_caminho.py.
"""

import json
import os
import re
import subprocess

from carregar_por_caminho import RAIZ

# Ajuste ao projeto.
PASTA_DAS_LINHAS_DE_BASE = "tests/linhas-de-base"


def correr_git(argumentos, entrada=b"", check=True):
    return subprocess.run(["git", *argumentos], cwd=RAIZ, input=entrada, capture_output=True, check=check).stdout


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


def base_de_comparacao():
    """O commit com que o «só encolhe» compara: MORG_BASE_DE_COMPARACAO (no CI) ou o último commit."""
    return os.environ.get("MORG_BASE_DE_COMPARACAO") or "HEAD"


def commit_conhecido(commit):
    """True se o git conhece este commit (num ramo novo o CI dá 40 zeros; um push forçado tira o de antes)."""
    return subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}"], cwd=RAIZ,
                          capture_output=True, check=False).returncode == 0


def subidas_sem_marca(regra, commit, marca):
    """Commit a commit de `commit..HEAD`: os que sobem a base face ao commit de antes sem a marca na própria mensagem."""
    commits = correr_git(["rev-list", "--reverse", f"{commit}..HEAD"]).decode("utf-8").split()
    erros = []
    for atual in commits:
        antes, depois = ler_linha_de_base(regra, f"{atual}^:"), ler_linha_de_base(regra, f"{atual}:")
        mensagem = correr_git(["log", "-1", "--format=%B", atual]).decode("utf-8", errors="replace")
        subiu = antes is not None and depois is not None and acima_de(depois, antes, "")
        if subiu and not re.search(rf"^{re.escape(marca)} *\S", mensagem, re.MULTILINE):
            erros.append(f"{atual[:10]} «{mensagem.splitlines()[0]}» sobe a base sem a linha '{marca} <motivo>'")
    return erros


def acima_de(valores, teto, frase, detalhe=lambda caminho, metrica: ""):
    """Mensagens de cada métrica de `valores` que passa do mesmo valor em `teto` (o que falta conta como 0)."""
    return [f"{caminho}: {metrica} {valor} ({frase} {teto.get(caminho, {}).get(metrica, 0)}){detalhe(caminho, metrica)}"
            for caminho, metricas in sorted(valores.items()) for metrica, valor in sorted(metricas.items())
            if valor > teto.get(caminho, {}).get(metrica, 0)]


def gravar_base(regra, valores):
    destino = RAIZ / caminho_da_base(regra)
    destino.parent.mkdir(parents=True, exist_ok=True)
    ordenados = {caminho: dict(sorted(metricas.items())) for caminho, metricas in sorted(valores.items()) if metricas}
    destino.write_bytes((json.dumps({"regra": regra, "valores": ordenados}, indent=2, ensure_ascii=False) + "\n")
                        .encode("utf-8"))


def criar_ou_completar(regra, atuais):
    """Com MORG_CRIAR_LINHA_DE_BASE=1, cria a base que falta ou junta-lhe as métricas que lhe faltam, se ela ainda
    não estiver no último commit; devolve a mensagem, ou None se nada mudou."""
    destino = RAIZ / caminho_da_base(regra)
    if os.environ.get("MORG_CRIAR_LINHA_DE_BASE") != "1" or ler_linha_de_base(regra, "HEAD:") is not None:
        return None
    existente = json.loads(destino.read_text(encoding="utf-8"))["valores"] if destino.exists() else {}
    faltam = {caminho: {metrica: valor for metrica, valor in metricas.items() if metrica not in existente.get(caminho, {})}
              for caminho, metricas in atuais.items()}
    if destino.exists() and not any(faltam.values()):
        return None
    gravar_base(regra, {caminho: {**existente.get(caminho, {}), **faltam.get(caminho, {})}
                        for caminho in {*existente, *faltam}})
    return f"linha de base gravada em {caminho_da_base(regra)}: confira-a e faça git add"


class TresVerificacoesDaCatraca:
    """Mistura para um unittest.TestCase: defina REGRA, CONSELHO, `medir()` e `julga(caminho, metrica)`; e, se quiser,
    MARCA_PARA_SUBIR e `detalhe(caminho, metrica)` (o texto que se junta à mensagem de uma métrica que passa)."""

    maxDiff = None  # a falha mostra todas as mensagens, com o caminho de cada uma
    MARCA_PARA_SUBIR = None

    def detalhe(self, caminho, metrica):
        return ""

    def conferir(self):
        # Uma medição por classe: os três testes julgam o mesmo estado do índice.
        if not hasattr(type(self), "_conferido"):
            atuais = self.medir()
            criada = criar_ou_completar(self.REGRA, atuais)
            type(self)._conferido = (atuais, ler_linha_de_base(self.REGRA) or {},
                                     ler_linha_de_base(self.REGRA, f"{base_de_comparacao()}:"), criada)
        return type(self)._conferido

    def test_nao_piora(self):
        atuais, base, _, criada = self.conferir()
        piores = acima_de(atuais, base, "a base deixa", self.detalhe)
        self.assertEqual(([criada] if criada else []) + piores, [], self.CONSELHO)

    def test_a_linha_de_base_nao_tem_folga(self):
        atuais, base, _, _ = self.conferir()
        sobras = {caminho: {metrica: valor for metrica, valor in metricas.items() if self.julga(caminho, metrica)}
                  for caminho, metricas in base.items()}
        self.assertEqual(acima_de(sobras, atuais, "hoje há"), [], "desça a linha de base no mesmo commit")

    def test_a_linha_de_base_so_encolhe(self):
        _, base, da_comparacao, _ = self.conferir()
        commit = base_de_comparacao()
        if commit != "HEAD" and not commit_conhecido(commit):
            self.skipTest(f"a base de comparação {commit} não é um commit que o git conheça (ramo novo, push forçado "
                          "ou nome errado): o «só encolhe» não pôde comparar")
        novas = [] if da_comparacao is None else acima_de(base, da_comparacao, "a base de comparação deixava")
        if novas and self.MARCA_PARA_SUBIR:
            if commit == "HEAD":
                self.skipTest(f"a subida pede a linha '{self.MARCA_PARA_SUBIR}' na mensagem; o commit-msg confere-a")
            novas = subidas_sem_marca(self.REGRA, commit, self.MARCA_PARA_SUBIR)
        self.assertEqual(novas, [], "a linha de base só desce: corrija o código em vez de a subir")
