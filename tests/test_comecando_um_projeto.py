"""O molde do documento do projeto (`modelos/documentos/projeto.md`) guarda o que a primeira conversa com um projeto
precisa, conferido sem rede e sobre o texto:

- tem as dez seções, na ordem: O que é, Para quem, Por que começar, O que já existe, O que faz, O que não faz,
  Restrições, Arquitetura, Palavras do dono e Perguntas em aberto;
- leva a marca «ronda dispensada pelo dono» em «Por que começar»;
- não leva palavras nem construções do português de Portugal.
E a skill `comecando-um-projeto`:
- tem as seções do plano, na ordem; as nove rondas da tabela da seção 3, na ordem, e nela a marca «ronda dispensada
  pelo dono»; os sete destinos do que escreve no projeto na tabela da seção 4; e, em «Procurar o que já existe», as
  frases «sem baixar, instalar nem rodar nada» e «Nunca invente um candidato»;
- cada cópia de `assets/` é igual, byte a byte, ao seu molde; nenhum arquivo de `assets/` fica fora do mapa; nenhum
  arquivo de `skills/` se chama `AGENTS.md`, `CLAUDE.md` nem `CLAUDE.local.md` (a ferramenta o carregaria como regra);
- o `SKILL.md` e o `evals/` não levam palavras nem construções do português de Portugal (as cópias de `assets/` ficam
  de fora: são iguais aos moldes).
E a mensagem inicial, a seção «Primeira mensagem num projeto» do README:
- tem os dois blocos iguais aos da seção 6 da skill, com o mesmo corpo depois do prefixo (`/` no Claude Code, `$` no
  Codex), o rótulo certo antes de cada um e o nome da skill no prefixo;
- fica depois do bloco do `npx skills add` e antes de «Para quem contribui»;
- não leva palavras nem construções do português de Portugal.
As funções recebem o texto ou a raiz, para os casos de erro serem provados sem tocar no repositório.
"""

import re
import shutil
import tempfile
import unittest
from pathlib import Path

from carregar_modelos import MODELOS, RAIZ
from leitura_do_repositorio import ler
from lingua_do_brasil import erros_de_lingua

MOLDE_DO_PROJETO = MODELOS / "documentos" / "projeto.md"
PASTA_DA_SKILL = "skills/comecando-um-projeto"
SECOES_DA_SKILL = ("Começando um projeto", "1. Quando usar e o que deixa", "2. Projeto novo ou projeto que já existe",
                   "3. As rondas", "4. O que se escreve", "5. Escolhas grandes viram ADR", "6. Mensagem inicial",
                   "7. O que entregar no fim", "8. Procurar o que já existe", "Fontes")
RONDAS_DA_SKILL = ("0. Ler", "1. O que é e para quem", "2. Vale a pena começar?", "3. O que faz e não faz",
                   "4. Restrições", "5. Arquitetura", "6. Regras", "7. Confirmar e escrever", "8. Primeiro plano")
SECAO_DAS_RONDAS = "## 3. As rondas"
SECAO_DA_BUSCA = "## 8. Procurar o que já existe"
MARCA_DA_DISPENSA = "ronda dispensada pelo dono"
FRASES_DA_BUSCA = ("sem baixar, instalar nem rodar nada", "Nunca invente um candidato")
DESTINOS_DA_SKILL = ("docs/projeto.md", "docs/README.md", "AGENTS.md", "CLAUDE.md", "docs/regras-e-barreiras.md",
                     "docs/planos/", "docs/decisoes/")
COPIAS_DOS_MOLDES = {f"assets/molde-{nome}.md": f"modelos/documentos/{nome}.md"
                     for nome in ("projeto", "AGENTS", "CLAUDE", "regras-e-barreiras", "plano", "adr")}
NOMES_QUE_AS_FERRAMENTAS_CARREGAM = ("AGENTS.md", "CLAUDE.md", "CLAUDE.local.md")
SECAO_DO_README = "### Primeira mensagem num projeto"
SECAO_DA_SKILL = "## 6. Mensagem inicial"
SECAO_DOS_DESTINOS = "## 4. O que se escreve"
ROTULO_E_PREFIXO = re.compile(r"^(No Claude Code|No Codex):\n\n```text\n(.)", re.MULTILINE)
ROTULOS_ESPERADOS = [("No Claude Code", "/"), ("No Codex", "$")]
INSTALACAO = "npx skills add"
PROXIMA_SECAO_DO_README = "## Para quem contribui"
BLOCO_DE_TEXTO = re.compile(r"```text\n(.*?)\n```", re.DOTALL)
SECOES_DO_PROJETO = ("O que é", "Para quem", "Por que começar", "O que já existe", "O que faz", "O que não faz",
                     "Restrições", "Arquitetura", "Palavras do dono", "Perguntas em aberto")


def secoes_do_molde(texto):
    """Os títulos `## …` do texto, na ordem em que aparecem."""
    return re.findall(r"^## (.+?)\s*$", texto, re.MULTILINE)


def erros_do_molde(texto):
    achadas = secoes_do_molde(texto)
    erros = [f"falta a seção «{titulo}»" for titulo in SECOES_DO_PROJETO if titulo not in achadas]
    ordem = [titulo for titulo in achadas if titulo in SECOES_DO_PROJETO]
    if not erros and ordem != list(SECOES_DO_PROJETO):
        erros.append(f"as seções estão fora da ordem: {ordem}")
    if MARCA_DA_DISPENSA not in texto:
        erros.append(f"falta no molde a frase «{MARCA_DA_DISPENSA}»")
    return erros


def erros_da_skill(texto):
    """As seções, as rondas e as frases de «Procurar o que já existe» em falta ou fora da ordem, e os destinos que o
    corpo da skill não cita."""
    achadas = re.findall(r"^#{1,2} (.+?)\s*$", texto, re.MULTILINE)
    erros = [f"falta a seção «{titulo}»" for titulo in SECOES_DA_SKILL if titulo not in achadas]
    ordem = [titulo for titulo in achadas if titulo in SECOES_DA_SKILL]
    if not erros and ordem != list(SECOES_DA_SKILL):
        erros.append(f"as seções estão fora da ordem: {ordem}")
    tabela = secao_de(texto, SECAO_DOS_DESTINOS)
    erros += [f"falta o destino `{destino}` na tabela da seção 4" for destino in DESTINOS_DA_SKILL
              if not re.search(rf"^\| `{re.escape(destino)}", tabela, re.MULTILINE)]
    return erros + erros_das_rondas(texto) + erros_da_busca(texto)


def erros_das_rondas(texto):
    """As rondas da tabela da seção 3 em falta ou fora da ordem, e a marca da dispensa que a seção tem de guardar."""
    secao = secao_de(texto, SECAO_DAS_RONDAS)
    achadas = re.findall(r"^\| (\d\. [^|]+?) \|", secao, re.MULTILINE)
    erros = [f"falta a ronda «{nome}»" for nome in RONDAS_DA_SKILL if nome not in achadas]
    ordem = [nome for nome in achadas if nome in RONDAS_DA_SKILL]
    if not erros and ordem != list(RONDAS_DA_SKILL):
        erros.append(f"as rondas estão fora da ordem: {ordem}")
    if MARCA_DA_DISPENSA not in secao:
        erros.append(f"falta no §3 da skill a frase «{MARCA_DA_DISPENSA}»")
    return erros


def erros_da_busca(texto):
    """As frases de segurança que a seção 8 tem de guardar."""
    busca = secao_de(texto, SECAO_DA_BUSCA)
    return [f"falta no §8 a frase «{frase}»" for frase in FRASES_DA_BUSCA if frase not in busca]


def erros_das_copias(raiz):
    """Cópia em falta ou diferente do molde, arquivo de `assets/` fora do mapa e nome que a ferramenta carregaria."""
    pasta = raiz / PASTA_DA_SKILL
    erros = []
    for copia, molde in COPIAS_DOS_MOLDES.items():
        if not (pasta / copia).is_file():
            erros.append(f"falta a cópia {copia}")
        elif (pasta / copia).read_bytes() != (raiz / molde).read_bytes():
            erros.append(f"{copia} difere de {molde}")
    achados = {p.relative_to(pasta).as_posix() for p in (pasta / "assets").rglob("*") if p.is_file()}
    erros += [f"{extra} está em assets/ e fora do mapa" for extra in sorted(achados - set(COPIAS_DOS_MOLDES))]
    nomes = [p for p in (raiz / "skills").rglob("*") if p.name in NOMES_QUE_AS_FERRAMENTAS_CARREGAM]
    return erros + [f"{p.relative_to(raiz).as_posix()} seria carregado como regra da sessão" for p in nomes]


def secao_de(texto, titulo):
    """O texto da seção que começa em `titulo`, até o próximo título do mesmo nível ou acima; vazio se não existe."""
    inicio = texto.find(titulo + "\n")
    if inicio < 0:
        return ""
    nivel = len(titulo.split()[0])
    fim = re.search(rf"^#{{1,{nivel}}} ", texto[inicio + len(titulo):], re.MULTILINE)
    return texto[inicio:] if not fim else texto[inicio:inicio + len(titulo) + fim.start()]


def erros_da_ordem_no_readme(readme):
    """A seção da mensagem fica depois do bloco do `npx skills add` e antes de «Para quem contribui»."""
    posicoes = [readme.find(INSTALACAO), readme.find(SECAO_DO_README + "\n"), readme.find(PROXIMA_SECAO_DO_README)]
    if min(posicoes) < 0:
        return ["falta no README o bloco da instalação, a seção da mensagem ou «Para quem contribui»"]
    return [] if posicoes == sorted(posicoes) else ["a seção da mensagem está fora do lugar no README"]


def erros_dos_prefixos(blocos, nome):
    """Dois blocos: `/nome corpo` e `$nome corpo`, com o mesmo corpo."""
    if len(blocos) != 2:
        return [f"esperava 2 blocos de texto na mensagem, achei {len(blocos)}"]
    corpos = [bloco.removeprefix(prefixo + nome + " ") for bloco, prefixo in zip(blocos, "/$")]
    erros = [f"o bloco {n} não começa por {prefixo}{nome} " for n, prefixo in enumerate("/$", 1)
             if not blocos[n - 1].startswith(prefixo + nome + " ")]
    return erros or ([] if corpos[0] == corpos[1] else ["o corpo difere entre o Claude Code e o Codex"])


def erros_dos_rotulos(secao, onde):
    """O rótulo «No Claude Code:» vem antes do bloco que começa por `/`, e «No Codex:» antes do que começa por `$`."""
    achados = ROTULO_E_PREFIXO.findall(secao)
    return [] if achados == ROTULOS_ESPERADOS else [f"os rótulos {onde} não casam com os prefixos: {achados}"]


def erros_da_mensagem(readme, skill):
    """Os blocos do README iguais aos da skill, na ordem certa, com o rótulo e o nome da skill no prefixo."""
    secao_do_readme = secao_de(readme, SECAO_DO_README)
    secao_da_skill = secao_de(skill, SECAO_DA_SKILL)
    no_readme = BLOCO_DE_TEXTO.findall(secao_do_readme)
    na_skill = BLOCO_DE_TEXTO.findall(secao_da_skill)
    nome = re.search(r"^name: (.+)$", skill, re.MULTILINE).group(1)
    erros = [] if no_readme == na_skill else ["os blocos do README diferem dos da seção 6 da skill"]
    erros += erros_dos_rotulos(secao_do_readme, "no README") + erros_dos_rotulos(secao_da_skill, "na skill")
    return erros + erros_da_ordem_no_readme(readme) + erros_dos_prefixos(no_readme, nome)


def erros_de_lingua_da_mensagem(readme):
    return erros_de_lingua("README.md", secao_de(readme, SECAO_DO_README))


def erros_de_lingua_da_skill(raiz):
    pasta = raiz / PASTA_DA_SKILL
    return [erro for arquivo in ("SKILL.md", "evals/trigger-eval.json")
            for erro in erros_de_lingua(arquivo, ler(pasta / arquivo))]


class MoldeDoProjeto(unittest.TestCase):
    def setUp(self):
        self.texto = ler(MOLDE_DO_PROJETO)

    def assertErro(self, texto, trecho):
        erros = erros_do_molde(texto)
        self.assertTrue(any(trecho in erro for erro in erros), f"esperava «{trecho}» em {erros}")

    def test_o_molde_passa(self):
        self.assertEqual([], erros_do_molde(self.texto))

    def test_sem_o_que_nao_faz_reprova(self):
        self.assertErro(self.texto.replace("## O que não faz", "## Outra coisa"), "falta a seção «O que não faz»")

    def test_sem_o_que_ja_existe_reprova(self):
        self.assertErro(self.texto.replace("## O que já existe", "## Outra"), "falta a seção «O que já existe»")

    def test_secoes_trocadas_de_ordem_reprovam(self):
        trocado = self.texto.replace("## O que faz\n", "## @@\n").replace("## O que não faz\n", "## O que faz\n")
        self.assertErro(trocado.replace("## @@\n", "## O que não faz\n"), "fora da ordem")

    def test_palavra_de_portugal_no_molde_reprova(self):
        erros = erros_de_lingua("projeto.md", self.texto + "\nO ficheiro do projeto.\n")
        self.assertIn("ficheiro", erros[0])

    def test_o_molde_esta_em_portugues_do_brasil(self):
        self.assertEqual([], erros_de_lingua("projeto.md", self.texto))


class SkillComecandoUmProjeto(unittest.TestCase):
    def setUp(self):
        self.texto = ler(RAIZ / PASTA_DA_SKILL / "SKILL.md")

    def copia_do_repositorio(self):
        """Uma pasta temporária só com a skill, os moldes e a pasta `skills/`, para as mutações."""
        raiz = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, raiz)
        shutil.copytree(RAIZ / "skills", raiz / "skills")
        shutil.copytree(MODELOS / "documentos", raiz / "modelos" / "documentos")
        return raiz

    def test_a_skill_passa(self):
        self.assertEqual([], erros_da_skill(self.texto))

    def test_sem_a_secao_das_escolhas_grandes_reprova(self):
        mutado = self.texto.replace("## 5. Escolhas grandes viram ADR", "## 5. Outra")
        self.assertIn("falta a seção «5. Escolhas grandes viram ADR»", erros_da_skill(mutado))

    def test_secoes_fora_de_ordem_reprovam(self):
        mutado = self.texto.replace("## 6. Mensagem inicial", "## @@").replace("## 7. O que entregar no fim",
                                                                                "## 6. Mensagem inicial")
        erros = erros_da_skill(mutado.replace("## @@", "## 7. O que entregar no fim"))
        self.assertTrue(any("fora da ordem" in erro for erro in erros), erros)

    def test_sem_a_secao_do_que_ja_existe_reprova(self):
        mutado = self.texto.replace("## 8. Procurar o que já existe", "## 8. Outra")
        self.assertIn("falta a seção «8. Procurar o que já existe»", erros_da_skill(mutado))

    def test_sem_a_ronda_vale_a_pena_reprova(self):
        linhas = self.texto.splitlines()
        sem_a_ronda = "\n".join(linha for linha in linhas if not linha.startswith("| 2. Vale a pena começar?"))
        trocada = [linha for linha in linhas if linha.startswith(("| 2. ", "| 3. "))]
        fora_de_ordem = self.texto.replace(trocada[0], "@@").replace(trocada[1], trocada[0]).replace("@@", trocada[1])
        casos = {"em falta": (sem_a_ronda, "falta a ronda «2. Vale a pena começar?»"),
                 "fora de ordem": (fora_de_ordem, "as rondas estão fora da ordem")}
        for nome, (mutado, trecho) in casos.items():
            with self.subTest(caso=nome):
                self.assertTrue(any(trecho in erro for erro in erros_da_skill(mutado)), erros_da_skill(mutado))

    def test_sem_a_frase_de_seguranca_reprova(self):
        trocas = {"Nunca invente um candidato": "Evite inventar", "sem baixar, instalar nem rodar nada": "sem pressa"}
        for frase, outra in trocas.items():
            with self.subTest(frase=frase):
                self.assertIn(f"falta no §8 a frase «{frase}»", erros_da_skill(self.texto.replace(frase, outra)))

    def test_sem_a_marca_da_dispensa_reprova(self):
        molde = ler(MOLDE_DO_PROJETO)
        casos = {"na skill": (erros_da_skill(self.texto.replace(MARCA_DA_DISPENSA, "outra marca")), "no §3 da skill"),
                 "no molde": (erros_do_molde(molde.replace(MARCA_DA_DISPENSA, "outra marca")), "no molde")}
        for nome, (erros, onde) in casos.items():
            with self.subTest(caso=nome):
                self.assertTrue(any(f"falta {onde}" in erro and MARCA_DA_DISPENSA in erro for erro in erros), erros)

    def test_sem_um_destino_reprova(self):
        erros = erros_da_skill(self.texto.replace("docs/decisoes/", "docs/outra/"))
        self.assertIn("falta o destino `docs/decisoes/` na tabela da seção 4", erros)

    def test_sem_a_linha_do_agents_na_tabela_reprova(self):
        sem_a_linha = "\n".join(linha for linha in self.texto.splitlines() if not linha.startswith("| `AGENTS.md`"))
        self.assertEqual(["falta o destino `AGENTS.md` na tabela da seção 4"], erros_da_skill(sem_a_linha))

    def test_as_copias_sao_iguais_aos_moldes(self):
        self.assertEqual([], erros_das_copias(RAIZ))

    def test_uma_copia_mudada_reprova(self):
        raiz = self.copia_do_repositorio()
        copia = raiz / PASTA_DA_SKILL / "assets" / "molde-AGENTS.md"
        copia.write_text(copia.read_text(encoding="utf-8") + "\numa linha a mais\n", encoding="utf-8")
        self.assertEqual(["assets/molde-AGENTS.md difere de modelos/documentos/AGENTS.md"], erros_das_copias(raiz))

    def test_uma_copia_em_falta_reprova(self):
        raiz = self.copia_do_repositorio()
        (raiz / PASTA_DA_SKILL / "assets" / "molde-adr.md").unlink()
        self.assertEqual(["falta a cópia assets/molde-adr.md"], erros_das_copias(raiz))

    def test_um_arquivo_a_mais_em_assets_reprova(self):
        raiz = self.copia_do_repositorio()
        (raiz / PASTA_DA_SKILL / "assets" / "sobra.md").write_text("x", encoding="utf-8")
        self.assertEqual(["assets/sobra.md está em assets/ e fora do mapa"], erros_das_copias(raiz))

    def test_uma_copia_com_o_nome_que_a_ferramenta_carrega_reprova(self):
        for nome in NOMES_QUE_AS_FERRAMENTAS_CARREGAM:
            with self.subTest(nome=nome):
                raiz = self.copia_do_repositorio()
                (raiz / PASTA_DA_SKILL / nome).write_text("x", encoding="utf-8")
                self.assertEqual([f"{PASTA_DA_SKILL}/{nome} seria carregado como regra da sessão"],
                                 erros_das_copias(raiz))

    def test_a_skill_esta_em_portugues_do_brasil(self):
        self.assertEqual([], erros_de_lingua_da_skill(RAIZ))

    def test_palavra_de_portugal_na_skill_reprova(self):
        raiz = self.copia_do_repositorio()
        arquivo = raiz / PASTA_DA_SKILL / "SKILL.md"
        arquivo.write_text(arquivo.read_text(encoding="utf-8") + "\nO ficheiro do projeto.\n", encoding="utf-8")
        self.assertIn("ficheiro", erros_de_lingua_da_skill(raiz)[0])


class MensagemInicial(unittest.TestCase):
    def setUp(self):
        self.readme = ler(RAIZ / "README.md")
        self.skill = ler(RAIZ / PASTA_DA_SKILL / "SKILL.md")

    def assertErro(self, readme, trecho):
        erros = erros_da_mensagem(readme, self.skill)
        self.assertTrue(any(trecho in erro for erro in erros), f"esperava «{trecho}» em {erros}")

    def test_a_mensagem_passa(self):
        self.assertEqual([], erros_da_mensagem(self.readme, self.skill))

    def test_uma_palavra_trocada_no_readme_reprova(self):
        self.assertErro(self.readme.replace("me faça as perguntas em rondas", "me faça as perguntas em etapas", 1),
                        "diferem")

    def test_a_secao_depois_de_para_quem_contribui_reprova(self):
        secao = secao_de(self.readme, SECAO_DO_README)
        movido = self.readme.replace(secao, "").rstrip("\n") + "\n\n" + secao
        self.assertErro(movido, "fora do lugar")

    def test_a_secao_antes_da_instalacao_reprova(self):
        secao = secao_de(self.readme, SECAO_DO_README)
        movido = self.readme.replace(secao, "").replace("## Como usar num projeto", secao + "## Como usar num projeto")
        self.assertErro(movido, "fora do lugar")

    def test_o_nome_errado_no_prefixo_do_codex_reprova(self):
        errado = self.readme.replace("$comecando-um-projeto", "$comecando-o-projeto")
        self.assertErro(errado, "não começa por $comecando-um-projeto")

    def troca_os_rotulos(self, texto):
        return (texto.replace("No Claude Code:", "@@").replace("No Codex:", "No Claude Code:")
                .replace("@@", "No Codex:"))

    def test_os_rotulos_trocados_no_readme_reprovam(self):
        self.assertErro(self.troca_os_rotulos(self.readme), "os rótulos no README")

    def test_os_rotulos_trocados_na_skill_reprovam(self):
        erros = erros_da_mensagem(self.readme, self.troca_os_rotulos(self.skill))
        self.assertTrue(any("os rótulos na skill" in erro for erro in erros), erros)

    def test_a_mensagem_esta_em_portugues_do_brasil(self):
        self.assertEqual([], erros_de_lingua_da_mensagem(self.readme))

    def test_palavra_de_portugal_na_mensagem_reprova(self):
        mutado = self.readme.replace("confirme comigo", "partilhe comigo", 1)
        self.assertIn("partilhe", erros_de_lingua_da_mensagem(mutado)[0])


if __name__ == "__main__":
    unittest.main()
