"""Os testes-modelo (modelos/testes/) rodam num projeto montado só com os modelos, e pegam o que devem pegar.

Verde: o projeto de exemplo, como sai dos modelos, passa. Vermelho: cada estrago típico faz falhar o teste certo.
Os estragos que mexem em arquivos diferentes e caem em testes diferentes juntam-se numa só corrida, e cada um é
conferido pelo nome do teste que falha e pelo caminho que a falha cita. Num ensaio real, a primeira corrida deu dois
vermelhos verdadeiros: arquivos gravados com CRLF pelo write_text do Windows e uma skill instalada fora do índice.
"""

import json
import os
import subprocess
import sys
import unittest
from unittest import mock

from projeto_de_exemplo import apagar, escrever, git, montar, rodar_testes

FUNCAO_COM_COMENTARIOS_NO_FIM = ("def com_notas():\n" + "".join(f"    passo_{i} = {i}\n" for i in range(19))
                                 + "    # uma nota\n    # outra\n    # e mais uma\n")
DOIS_METODOS_COM_O_MESMO_NOME = ("class Caixa:\n    def correr(self):\n" + "".join(f"        p{i} = {i}\n" for i in range(26))
                                 + "\n\nclass Fila:\n    def correr(self):\n        pass\n")
# Os estragos que se juntam numa corrida: (arquivo, texto, teste que falha, trecho que a falha cita).
ESTRAGOS = [
    ("src/pedido.py", "x = 1\r\n", "test_no_disco_crlf_so_no_que_o_windows_roda", "src/pedido.py"),
    ("src/utils.py", "x = 1\n", "test_nao_piora (test_nomes.", "src/utils.py: caminhoGenerico"),
    ("src/carregar.py", "data, erro = ler()\n", "test_nao_piora (test_nomes.", "src/carregar.py: nomesGenericos"),
    ("src/campos.py", "class Pedido(TypedDict):\n    info: str\n", "test_nao_piora (test_nomes.",
     "src/campos.py: nomesGenericos"),
    ("src/calado.py", "# TODO ver depois\nimport os  # noqa: F401\n", "test_cada_alarme_tem_motivo", "src/calado.py:2"),
    ("src/tela.tsx", "const a = <div>{/* @ts-expect-error — tipo da lib */}</div>;\n", "test_nao_piora (test_alarmes.",
     "src/tela.tsx:1"),
    ("docs/contato.md", "Fale com ana@correio-ficticio.net\n", "test_sem_emails_pessoais", "docs/contato.md"),
    ("src/grande.py", "x = 1\n" * 501, "test_nao_piora (test_tamanho_dos_arquivos.", "src/grande.py: linhasAcima 1"),
    ("src/caixa.py", "def total_do_pedido(itens):\n    return 0\n", "test_nao_piora (test_nomes_unicos.",
     "src/caixa.py: nomesDeTopoRepetidos"),
    ("tests/test_pedido.py", ("import unittest\n\n\nclass Pedido(unittest.TestCase):\n    @unittest.skip('lento')\n"
                              "    def test_soma(self):\n        pass\n"),
     "test_nao_piora (test_testes_saltados.", "tests/test_pedido.py"),
    ("src/notas.py", FUNCAO_COM_COMENTARIOS_NO_FIM, "test_nao_piora (test_tamanho_das_funcoes.",
     "src/notas.py: funcoesAcima 1"),
    ("src/filas.py", DOIS_METODOS_COM_O_MESMO_NOME, "test_nao_piora (test_tamanho_das_funcoes.",
     "src/filas.py: funcoesAcima 1"),
]
SEM_TESTES_NO_COMMIT = {**os.environ, "MORG_A_TESTAR": "1"}
# Os estragos do workflow, um de cada vez: (trecho certo, trecho estragado ou None para tirar a linha, teste que falha).
ESTRAGOS_DO_CI = [
    ("actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1", "actions/checkout@v7",
     "test_cada_action_fixada_por_sha_com_a_versao"),
    ("sha256sum -c", None, "test_nada_baixado_direto_para_uma_shell"),
    # O bloco do topo continua só de leitura; o job ganha escrita por baixo dele.
    ("    timeout-minutes: 10\n", "    timeout-minutes: 10\n    permissions:\n      contents: write\n",
     "test_o_token_so_le_e_o_checkout_nao_guarda_a_credencial"),
    ("  segredos:\n", "  segredos:\n    permissions: write-all\n", "test_o_token_so_le_e_o_checkout_nao_guarda_a_credencial"),
    ("          tar -xzf", '          sh -c "$(curl -sSfL https://exemplo.com/x)"\n          tar -xzf',
     "test_nada_baixado_direto_para_uma_shell"),
    ("          tar -xzf", "          curl -sSfL https://exemplo.com/f.tar.gz > f.tar.gz\n          tar -xzf",
     "test_nada_baixado_direto_para_uma_shell"),
    ("          tar -xzf", "          curl -sSfL --output f.tar.gz https://exemplo.com/f.tar.gz\n          tar -xzf",
     "test_nada_baixado_direto_para_uma_shell"),
]


class ProjetoDeExemplo(unittest.TestCase):

    def setUp(self):
        # A variável do CI do próprio Morg-laws aponta para um commit deste repositório, não do exemplo.
        self.enterContext(mock.patch.dict(os.environ))
        os.environ.pop("MORG_BASE_DE_COMPARACAO", None)
        self.pasta = montar()
        self.addCleanup(apagar, self.pasta)

    def assertFalhaEm(self, teste, padrao="test*.py"):
        git(self.pasta, "add", "--", ".")
        codigo, saida = rodar_testes(self.pasta, padrao)
        self.assertNotEqual(codigo, 0, saida[-2000:])
        self.assertIn(f"FAIL: {teste}", saida)
        return saida

    def assertPassa(self, padrao="test*.py"):
        git(self.pasta, "add", "--", ".")
        codigo, saida = rodar_testes(self.pasta, padrao)
        self.assertEqual(codigo, 0, saida[-3000:])

    def commitar(self, mensagem="chore: base", deve_passar=True):
        git(self.pasta, "add", "--", ".")
        resultado = git(self.pasta, "commit", "-q", "-F", "-", input=mensagem, env=SEM_TESTES_NO_COMMIT, check=False)
        if deve_passar:
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
        return resultado

    def commit_sem_hooks(self, mensagem):
        """Um commit que não passa pelos hooks, como o feito no site do GitHub: o git só os corre no `commit`."""
        git(self.pasta, "add", "--", ".")
        arvore = git(self.pasta, "write-tree").stdout.strip()
        novo = git(self.pasta, "commit-tree", arvore, "-p", "HEAD", "-m", mensagem).stdout.strip()
        git(self.pasta, "update-ref", "HEAD", novo)

    def test_como_sai_dos_modelos_passa(self):
        codigo, saida = rodar_testes(self.pasta)
        self.assertEqual(codigo, 0, saida[-3000:])
        self.assertIn("OK", saida)

    def test_cada_estrago_cai_no_seu_teste(self):
        for caminho, texto, _, _ in ESTRAGOS:
            (self.pasta / caminho).parent.mkdir(parents=True, exist_ok=True)
            (self.pasta / caminho).write_bytes(texto.encode("utf-8"))
        saida = self.assertFalhaEm("test_no_disco_crlf_so_no_que_o_windows_roda")
        for caminho, _, teste, trecho in ESTRAGOS:
            with self.subTest(estrago=caminho):
                self.assertIn(f"FAIL: {teste}", saida)
                self.assertIn(trecho, saida)

    def test_regra_sem_linha_no_mapa(self):
        mapa = self.pasta / "docs" / "regras-e-barreiras.md"
        texto = mapa.read_text(encoding="utf-8")
        escrever(mapa, "".join(linha for linha in texto.splitlines(True) if not linha.startswith("| NÃO PIORAR")))
        self.assertFalhaEm("test_cada_regra_esta_no_mapa_e_o_mapa_nao_tem_regras_a_mais", "test_regras.py")

    def test_o_claude_md_estragado(self):
        for texto, teste in (("## Só no Claude Code\n\nNada.\n", "test_o_claude_md_importa_o_arquivo_de_regras"),
                             ("@AGENTS.md\n\nVer `docs/nao-existe.md`.\n", "test_caminhos_citados_existem"),
                             # Sozinhos, os dois ficam abaixo de 100 linhas; o Claude Code carrega-os juntos.
                             ("@AGENTS.md\n" + "- nota\n" * 60, "test_tamanho")):
            with self.subTest(teste=teste):
                escrever(self.pasta / "CLAUDE.md", texto)
                self.assertFalhaEm(teste, "test_regras.py")

    def test_numero_de_documento_com_o_padrao_ligado(self):
        teste = self.pasta / "tests" / "test_dados_pessoais.py"
        escrever(teste, teste.read_text(encoding="utf-8").replace(
            "DOCUMENTOS = {}", r'DOCUMENTOS = {"CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"}'))
        escrever(self.pasta / "docs" / "cliente.md", "CPF do cliente: 000.000.000-00\n")
        self.assertFalhaEm("test_sem_numeros_de_documentos", "test_dados_pessoais.py")

    def estragar_o_ci(self, antes, depois):
        ci = self.pasta / ".github" / "workflows" / "ci.yml"
        texto = ci.read_text(encoding="utf-8")
        self.assertIn(antes, texto)
        escrever(ci, texto.replace(antes, depois, 1))

    def test_o_ci_estragado(self):
        original = (self.pasta / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        for antes, depois, teste in ESTRAGOS_DO_CI:
            with self.subTest(estrago=depois or antes):
                escrever(self.pasta / ".github" / "workflows" / "ci.yml", original)
                if depois is None:
                    antes, depois = next(linha for linha in original.splitlines(True) if antes in linha), ""
                self.estragar_o_ci(antes, depois)
                self.assertFalhaEm(teste, "test_ci.py")

    def test_juntar_changelog_em_rascunho_mostra_a_secao(self):
        escrever(self.pasta / "CHANGELOG.md", "# Changelog\n")
        escrever(self.pasta / "changelog.d" / "2026-11-01-primeira.md", "Categoria: Adicionado\n\n- Tudo novo.\n")
        resultado = subprocess.run([sys.executable, "-I", "scripts/changelog/juntar_changelog.py", "--rascunho"],
                                   cwd=self.pasta, capture_output=True, check=False, timeout=60)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn(b"## [0.1.0]", resultado.stdout)
        self.assertIn(b"### Adicionado\n\n- Tudo novo.", resultado.stdout.replace(b"\r\n", b"\n"))
        self.assertFalse((self.pasta / "VERSION").exists(), "o rascunho não grava")

    def gravar_base(self, regra, valores):
        escrever(self.pasta / "tests" / "linhas-de-base" / f"{regra}.json",
                 json.dumps({"regra": regra, "valores": valores}, indent=2) + "\n")

    def test_a_base_deixa_passar_o_que_ja_violava_mas_sem_folga(self):
        escrever(self.pasta / "src" / "grande.py", "x = 1\n" * 501)
        self.gravar_base("tamanho-de-arquivo", {"src/grande.py": {"linhasAcima": 1}})
        self.assertPassa("test_tamanho_dos_arquivos.py")
        self.gravar_base("tamanho-de-arquivo", {"src/grande.py": {"linhasAcima": 4}})
        self.assertFalhaEm("test_a_linha_de_base_nao_tem_folga (test_tamanho_dos_arquivos", "test_tamanho_dos_arquivos.py")

    def test_linha_de_base_dos_alarmes_que_nao_desceu(self):
        # Quem tira um alarme desce a base no mesmo commit; senão a folga deixa o próximo entrar calado.
        self.gravar_base("alarmes", {"*": {"eslint-disable": 1}})
        self.assertFalhaEm("test_a_linha_de_base_nao_tem_folga (test_alarmes", "test_alarmes.py")

    def test_entrada_nova_na_base_ja_commitada(self):
        self.gravar_base("tamanho-de-arquivo", {})
        self.commitar()
        escrever(self.pasta / "src" / "grande.py", "x = 1\n" * 501)
        self.gravar_base("tamanho-de-arquivo", {"src/grande.py": {"linhasAcima": 1}})
        self.assertFalhaEm("test_a_linha_de_base_so_encolhe (test_tamanho_dos_arquivos", "test_tamanho_dos_arquivos.py")

    def test_no_ci_a_entrada_nova_ja_commitada_tambem_e_recusada(self):
        # No CI o índice é o último commit: compara-se com a ponta anterior do ramo (MORG_BASE_DE_COMPARACAO).
        self.gravar_base("tamanho-de-arquivo", {})
        self.commitar()
        anterior = git(self.pasta, "rev-parse", "HEAD").stdout.strip()
        escrever(self.pasta / "src" / "grande.py", "x = 1\n" * 501)
        self.gravar_base("tamanho-de-arquivo", {"src/grande.py": {"linhasAcima": 1}})
        self.commitar("feat: entrada nova\n\nSem passar pela revisão.\n")
        with mock.patch.dict(os.environ, {"MORG_BASE_DE_COMPARACAO": anterior}):
            self.assertFalhaEm("test_a_linha_de_base_so_encolhe (test_tamanho_dos_arquivos", "test_tamanho_dos_arquivos.py")

    def test_o_alarme_que_muda_de_arquivo_passa(self):
        alarme = "// eslint-disable-next-line no-console — o CLI escreve no terminal\n"
        escrever(self.pasta / "src" / "a.ts", alarme)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 1}})
        self.commitar()
        git(self.pasta, "rm", "-q", "--", "src/a.ts")
        escrever(self.pasta / "src" / "b.ts", alarme)
        self.assertPassa("test_alarmes.py")

    def test_alarme_novo_so_com_a_linha_alarme_novo(self):
        self.gravar_base("alarmes", {})
        self.commitar()
        anterior = git(self.pasta, "rev-parse", "HEAD").stdout.strip()
        escrever(self.pasta / "src" / "a.ts", "// eslint-disable-next-line no-console — o CLI escreve no terminal\n")
        self.gravar_base("alarmes", {"*": {"eslint-disable": 1}})
        self.assertPassa("test_alarmes.py")  # no índice, a subida fica para o commit-msg
        recusado = self.commitar("feat: alarme\n\nUm alarme novo.\n", deve_passar=False)
        self.assertNotEqual(recusado.returncode, 0)
        self.assertIn("Alarme-novo:", recusado.stderr)
        self.assertEqual(self.commitar("feat: alarme\n\nUm alarme novo.\n\nAlarme-novo: o exemplo importa sem usar\n")
                         .returncode, 0)
        with mock.patch.dict(os.environ, {"MORG_BASE_DE_COMPARACAO": anterior}):
            self.assertPassa("test_alarmes.py")  # no CI, a linha está num commit do intervalo

    def test_no_ci_o_alarme_novo_sem_a_linha_e_recusado(self):
        self.gravar_base("alarmes", {})
        self.commitar()
        anterior = git(self.pasta, "rev-parse", "HEAD").stdout.strip()
        escrever(self.pasta / "src" / "a.ts", "// eslint-disable-next-line no-console — o CLI escreve no terminal\n")
        self.gravar_base("alarmes", {"*": {"eslint-disable": 1}})
        self.commit_sem_hooks("feat: alarme sem a linha")
        with mock.patch.dict(os.environ, {"MORG_BASE_DE_COMPARACAO": anterior}):
            self.assertFalhaEm("test_a_linha_de_base_so_encolhe (test_alarmes", "test_alarmes.py")

    def test_no_ci_cada_subida_dos_alarmes_pede_a_sua_linha(self):
        # Uma linha Alarme-novo: num commit não cobre a subida de outro commit do mesmo push.
        alarme = "// eslint-disable-next-line no-console — o CLI escreve no terminal\n"
        escrever(self.pasta / "src" / "a.ts", alarme)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 1}})
        self.commitar()
        anterior = git(self.pasta, "rev-parse", "HEAD").stdout.strip()
        for numero, mensagem in ((2, "feat: b\n\nAlarme-novo: o CLI escreve no terminal"), (3, "feat: c sem a linha")):
            escrever(self.pasta / "src" / f"{numero}.ts", alarme)
            self.gravar_base("alarmes", {"*": {"eslint-disable": numero}})
            self.commit_sem_hooks(mensagem)
        with mock.patch.dict(os.environ, {"MORG_BASE_DE_COMPARACAO": anterior}):
            saida = self.assertFalhaEm("test_a_linha_de_base_so_encolhe (test_alarmes", "test_alarmes.py")
        self.assertIn("feat: c sem a linha", saida)

    def test_no_ci_apagar_e_recriar_a_base_dos_alarmes_mais_alta_e_recusado(self):
        # Um commit apaga a base, o seguinte recria-a mais alta sem a linha: conta a última base conhecida.
        alarme = "// eslint-disable-next-line no-console — o CLI escreve no terminal\n"
        escrever(self.pasta / "src" / "a.ts", alarme)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 1}})
        self.commitar()
        anterior = git(self.pasta, "rev-parse", "HEAD").stdout.strip()
        git(self.pasta, "rm", "-q", "--", "tests/linhas-de-base/alarmes.json")
        self.commit_sem_hooks("chore: sem a base")
        for numero in (2, 3):
            escrever(self.pasta / "src" / f"{numero}.ts", alarme)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 3}})
        self.commit_sem_hooks("feat: a base de volta, mais alta")
        with mock.patch.dict(os.environ, {"MORG_BASE_DE_COMPARACAO": anterior}):
            self.assertFalhaEm("test_a_linha_de_base_so_encolhe (test_alarmes", "test_alarmes.py")

    def test_numa_pr_a_subida_com_a_linha_passa_pelo_merge_de_teste(self):
        # O CI de uma PR tira o merge de teste (pais: a base e a PR); o merge não traz a linha, e não é acusado.
        alarme = "// eslint-disable-next-line no-console — o CLI escreve no terminal\n"
        escrever(self.pasta / "src" / "a.ts", alarme)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 1}})
        self.commitar()
        base = git(self.pasta, "rev-parse", "HEAD").stdout.strip()
        escrever(self.pasta / "src" / "b.ts", alarme)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 2}})
        self.commit_sem_hooks("feat: alarme\n\nAlarme-novo: o CLI escreve no terminal")
        da_pr = git(self.pasta, "rev-parse", "HEAD").stdout.strip()
        arvore = git(self.pasta, "write-tree").stdout.strip()
        merge = git(self.pasta, "commit-tree", arvore, "-p", base, "-p", da_pr, "-m", "Merge pr into main").stdout.strip()
        git(self.pasta, "update-ref", "HEAD", merge)
        with mock.patch.dict(os.environ, {"MORG_BASE_DE_COMPARACAO": base}):
            self.assertPassa("test_alarmes.py")

    def test_numa_pr_o_merge_que_sobe_a_base_por_si_e_recusado(self):
        # A sobe a 2 com a linha; o merge sobe a 3 por si. O controlo (o merge que não sobe): o teste do merge de teste.
        alarme = "// eslint-disable-next-line no-console — o CLI escreve no terminal\n"
        escrever(self.pasta / "src" / "a.ts", alarme)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 1}})
        self.commitar()
        base = git(self.pasta, "rev-parse", "HEAD").stdout.strip()
        escrever(self.pasta / "src" / "b.ts", alarme)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 2}})
        self.commit_sem_hooks("feat: alarme\n\nAlarme-novo: o CLI escreve no terminal")
        da_pr = git(self.pasta, "rev-parse", "HEAD").stdout.strip()
        escrever(self.pasta / "src" / "c.ts", alarme)
        self.gravar_base("alarmes", {"*": {"eslint-disable": 3}})
        git(self.pasta, "add", "--", ".")
        arvore = git(self.pasta, "write-tree").stdout.strip()
        merge = git(self.pasta, "commit-tree", arvore, "-p", base, "-p", da_pr, "-m", "Merge pr into main").stdout.strip()
        git(self.pasta, "update-ref", "HEAD", merge)
        with mock.patch.dict(os.environ, {"MORG_BASE_DE_COMPARACAO": base}):
            saida = self.assertFalhaEm("test_a_linha_de_base_so_encolhe (test_alarmes", "test_alarmes.py")
        self.assertIn("*: eslint-disable 3", saida)

    def test_a_base_de_comparacao_que_o_git_nao_conhece_salta_com_o_motivo(self):
        # Um ramo novo (40 zeros), um push forçado ou um nome errado: o teste diz que não pôde comparar.
        self.gravar_base("tamanho-de-arquivo", {})
        self.commitar()
        escrever(self.pasta / "src" / "grande.py", "x = 1\n" * 501)
        self.gravar_base("tamanho-de-arquivo", {"src/grande.py": {"linhasAcima": 1}})
        self.commitar("feat: entrada nova\n\nSem passar pela revisão.\n")
        for desconhecida in ("0" * 40, "nao-existe"):
            with self.subTest(base=desconhecida), mock.patch.dict(os.environ, {"MORG_BASE_DE_COMPARACAO": desconhecida}):
                codigo, saida = rodar_testes(self.pasta, "test_tamanho_dos_arquivos.py", verboso=True)
                self.assertEqual(codigo, 0, saida[-2000:])
                # Sem os acentos: o processo filho escreve na página de código da consola do Windows.
                self.assertIn("TamanhoDosArquivos.test_a_linha_de_base_so_encolhe) ... skipped 'a base de compara", saida)
                self.assertIn(f"{desconhecida} n", saida)

    def test_criar_a_base_num_projeto_que_ja_viola(self):
        escrever(self.pasta / "src" / "grande.py", "x = 1\n" * 501)
        with mock.patch.dict(os.environ, {"MORG_CRIAR_LINHA_DE_BASE": "1"}):
            self.assertFalhaEm("test_nao_piora (test_tamanho_dos_arquivos", "test_tamanho_dos_arquivos.py")
        base = json.loads((self.pasta / "tests" / "linhas-de-base" / "tamanho-de-arquivo.json").read_text("utf-8"))
        self.assertEqual(base, {"regra": "tamanho-de-arquivo", "valores": {"src/grande.py": {"linhasAcima": 1}}})
        self.assertPassa()

    def test_permissao_perigosa_no_allow(self):
        settings = self.pasta / ".claude" / "settings.json"
        texto = settings.read_text(encoding="utf-8").replace('"Bash(git status*)"', '"Bash(git push *)"')
        escrever(settings, texto)
        self.assertFalhaEm("test_allow_so_tem_leituras_e_testes", "test_permissoes.py")

    def escolher_so_sessoes(self, teste="True", deny_agent=False):
        """Põe `SO_SESSOES = <teste>` na cópia do test_permissoes.py e, se pedido, `"Agent"` no deny da cópia do settings."""
        permissoes = self.pasta / "tests" / "test_permissoes.py"
        escrever(permissoes, permissoes.read_text(encoding="utf-8").replace("SO_SESSOES = False", f"SO_SESSOES = {teste}"))
        if deny_agent:
            settings = self.pasta / ".claude" / "settings.json"
            escrever(settings, settings.read_text(encoding="utf-8").replace('"deny": [', '"deny": [\n      "Agent",', 1))

    def test_so_sessoes_sem_o_deny_da_ferramenta_agent(self):
        self.escolher_so_sessoes("True")
        self.assertFalhaEm("test_sub_agentes_conforme_a_escolha", "test_permissoes.py")

    def test_so_sessoes_com_o_deny_da_ferramenta_agent(self):
        self.escolher_so_sessoes("True", deny_agent=True)
        self.assertPassa("test_permissoes.py")

    def test_deny_da_ferramenta_agent_sem_a_escolha_escrita(self):
        self.escolher_so_sessoes("False", deny_agent=True)
        self.assertFalhaEm("test_sub_agentes_conforme_a_escolha", "test_permissoes.py")


if __name__ == "__main__":
    unittest.main()
