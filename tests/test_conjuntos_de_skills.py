"""Os conjuntos de skills do P1 do manual, conferidos sem rede:

- cada skill de `skills/` está em exatamente um comando do P1, e o P1 não cita skill que não existe;
- o Supabase nunca vem sem a skill de SQL no mesmo comando;
- o comando das gerais do README é igual, letra a letra, ao primeiro do P1.
Cada erro tem o seu caso, numa cópia temporária de `skills/`, `manual/` e `README.md`.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from carregar_modelos import RAIZ
from conjuntos_de_skills import CAMINHO_DO_P1, erros_dos_conjuntos, gerais
from leitura_do_repositorio import ler


class ConjuntosDeSkills(unittest.TestCase):
    def setUp(self):
        self.raiz = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.raiz)
        shutil.copytree(RAIZ / "skills", self.raiz / "skills")
        (self.raiz / "manual").mkdir()
        shutil.copy(RAIZ / CAMINHO_DO_P1, self.raiz / CAMINHO_DO_P1)
        shutil.copy(RAIZ / "README.md", self.raiz / "README.md")

    def trocar(self, arquivo, antigo, novo):
        caminho = self.raiz / arquivo
        texto = ler(caminho)
        self.assertIn(antigo, texto)
        caminho.write_text(texto.replace(antigo, novo, 1), encoding="utf-8")

    def assertErro(self, trecho):
        erros = erros_dos_conjuntos(self.raiz)
        self.assertTrue(any(trecho in erro for erro in erros), f"esperava «{trecho}» em {erros}")

    def test_o_repositorio_passa(self):
        self.assertEqual(erros_dos_conjuntos(RAIZ), [])
        self.assertEqual(len(gerais(RAIZ)), 9)

    def test_skill_nova_fora_de_um_conjunto_reprova(self):
        (self.raiz / "skills" / "exemplo-nova").mkdir()
        (self.raiz / "skills" / "exemplo-nova" / "SKILL.md").write_text("---\nname: exemplo-nova\n---\n", encoding="utf-8")
        self.assertErro("a skill exemplo-nova não está em nenhum comando do P1")

    def test_skill_em_dois_comandos_reprova(self):
        self.trocar(CAMINHO_DO_P1, "--skill sql-postgres --skill supabase", "--skill sql-postgres --skill supabase --skill git-e-commits")
        self.assertErro("a skill git-e-commits está em mais de um comando")

    def test_nome_que_nao_existe_reprova(self):
        self.trocar(CAMINHO_DO_P1, "--skill nextjs-react", "--skill nextjs-react --skill nao-existe")
        self.assertErro("o P1 cita a skill nao-existe, que não existe")

    def test_supabase_sem_sql_reprova(self):
        self.trocar(CAMINHO_DO_P1, "--skill sql-postgres --skill supabase", "--skill supabase")
        self.assertErro("supabase sem sql-postgres")

    def test_readme_diferente_do_p1_reprova(self):
        self.trocar("README.md", " --skill testes-e-provas", "")
        self.assertErro("o comando das gerais do README é diferente")


if __name__ == "__main__":
    unittest.main()
