"""Hook aviso_da_pausa (modelos/claude/hooks/aviso_da_pausa.py): avisa o agente depois de mais de uma hora parada.

Os testes usam um registro de conversa falso, em JSON por linha, nunca um real.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest import mock

from carregar_modelos import PASTA_HOOKS, carregar_hook, correr_como_script

pausa = carregar_hook("aviso_da_pausa")
HOOK_DA_PAUSA = PASTA_HOOKS / "aviso_da_pausa.py"
AGORA = datetime(2026, 11, 13, 12, 0, tzinfo=UTC)


def entrada(tipo, minutos_atras, agora=None):
    """Uma linha do registro falso: o tipo e o timestamp (formato ISO com Z) de tantos minutos atrás."""
    hora = (agora or datetime.now(UTC)) - timedelta(minutes=minutos_atras)
    return json.dumps({"type": tipo, "timestamp": hora.strftime("%Y-%m-%dT%H:%M:%S.000Z")})


class CasoComRegistro(unittest.TestCase):

    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.registro = Path(pasta.name) / "conversa.jsonl"

    def gravar(self, *linhas):
        self.registro.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    def mensagem(self):
        """Roda o hook inteiro como script, com a entrada JSON do evento."""
        pedido = {"hook_event_name": "UserPromptSubmit", "prompt": "oi", "transcript_path": str(self.registro)}
        return correr_como_script(HOOK_DA_PAUSA, json.dumps(pedido).encode("utf-8"))


class OAvisoDaPausa(CasoComRegistro):

    def avisou(self):
        codigo, saida, erro = self.mensagem()
        self.assertEqual((codigo, erro), (0, ""))
        if not saida:
            return False
        especifico = json.loads(saida)["hookSpecificOutput"]
        self.assertEqual(especifico["hookEventName"], "UserPromptSubmit")
        self.assertEqual(especifico["additionalContext"], pausa.TEXTO_DO_AVISO)
        return True

    def test_a_61_minutos_avisa(self):
        self.gravar(entrada("user", 62), entrada("assistant", 61))
        self.assertTrue(self.avisou())

    def test_a_59_minutos_nao_diz_nada(self):
        self.gravar(entrada("user", 62), entrada("assistant", 59))
        self.assertFalse(self.avisou())

    def test_nos_60_minutos_exatos_nao_avisa(self):
        self.gravar(entrada("assistant", 60, AGORA))
        self.assertFalse(pausa.passou_da_pausa(self.registro, AGORA))
        self.gravar(entrada("assistant", 61, AGORA))
        self.assertTrue(pausa.passou_da_pausa(self.registro, AGORA))

    def test_entradas_recentes_de_outros_tipos_nao_enganam(self):
        # O caso real que derrubou a ideia de ler a hora do arquivo: fila, anexo e fronteira de compactação
        # chegam depois da última resposta do assistente.
        self.gravar(entrada("assistant", 300), entrada("queue-operation", 1), entrada("attachment", 1),
                    entrada("system", 1))
        self.assertTrue(self.avisou())

    def test_a_ultima_resposta_e_a_que_vale(self):
        self.gravar(entrada("assistant", 500), entrada("assistant", 5), entrada("user", 1))
        self.assertFalse(self.avisou())

    def test_o_texto_diz_sessao_nova_e_nao_compacte(self):
        self.assertIn("sessão nova", pausa.TEXTO_DO_AVISO)
        self.assertIn("não compacte", pausa.TEXTO_DO_AVISO)

    def test_um_turno_que_o_dono_nao_escreveu_avisa_assim_mesmo(self):
        # Limite conhecido, não resolvido: nenhum campo separa a mensagem do dono de uma iteração de `/loop`, de
        # uma tarefa agendada ou da mensagem de outra sessão. Com a última resposta a mais de uma hora, avisa.
        pedido = {"hook_event_name": "UserPromptSubmit", "prompt": "/loop 2h verifique o deploy",
                  "transcript_path": str(self.registro)}
        self.gravar(entrada("assistant", 120))
        codigo, saida, _ = correr_como_script(HOOK_DA_PAUSA, json.dumps(pedido).encode("utf-8"))
        self.assertEqual(codigo, 0)
        self.assertIn("sessão nova", saida)


class OAvisoQueSomeCalado(CasoComRegistro):
    """Se o registro não tem o formato esperado, o aviso some: nunca avisa e nunca quebra a mensagem."""

    def test_registro_vazio(self):
        self.registro.write_text("", encoding="utf-8")
        self.assertEqual(self.mensagem(), (0, "", ""))

    def test_registro_ilegivel(self):
        self.registro.write_bytes(b"\xff\xfe\x00 isto n\xe3o \x80 \xc3 \n{partido")
        self.assertEqual(self.mensagem(), (0, "", ""))

    def test_registro_sem_entrada_do_assistente(self):
        self.gravar(entrada("user", 500), entrada("system", 400))
        self.assertEqual(self.mensagem(), (0, "", ""))

    def test_registro_de_outro_formato(self):
        for outro in ('{"role": "assistant", "time": "2020-01-01"}', "[1, 2]", '"texto"', "42",
                      '{"type": "assistant"}', '{"type": "assistant", "timestamp": "ontem"}',
                      '{"type": "assistant", "timestamp": 1700000000}'):
            with self.subTest(linha=outro):
                self.gravar(outro)
                self.assertEqual(self.mensagem(), (0, "", ""))

    def test_caminho_que_nao_existe(self):
        self.assertEqual(self.mensagem(), (0, "", ""))

    def test_sem_transcript_path(self):
        self.assertEqual(correr_como_script(HOOK_DA_PAUSA, b'{"prompt": "oi"}'), (0, "", ""))

    def test_hora_sem_fuso_conta_como_utc(self):
        antiga = (datetime.now(UTC) - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S")
        self.gravar(json.dumps({"type": "assistant", "timestamp": antiga}))
        self.assertIn("sessão nova", self.mensagem()[1])

    def test_so_o_fim_do_arquivo_e_lido(self):
        # Uma conversa maior que o trecho lido: a primeira linha do trecho vem cortada e é ignorada.
        enchimento = json.dumps({"type": "user", "texto": "x" * 5000})
        self.gravar(entrada("assistant", 500), *[enchimento] * 3)
        with mock.patch.object(pausa, "BYTES_DO_FIM", 7000):
            self.assertEqual(len(pausa.fim_do_registro(self.registro)), 2)
            self.assertIsNone(pausa.ultima_resposta(self.registro))

    def test_o_texto_na_pasta_do_registro_que_e_um_diretorio(self):
        pedido = {"transcript_path": str(self.registro.parent)}
        self.assertEqual(correr_como_script(HOOK_DA_PAUSA, json.dumps(pedido).encode("utf-8")), (0, "", ""))


class HookQuebrado(unittest.TestCase):

    def test_no_python_isolado_de_verdade_a_entrada_ruim_sai_com_falha(self):
        # É o que o `continue` do settings deixa passar: só o hook quebrado, nunca a mensagem, fica sem efeito.
        resultado = subprocess.run([sys.executable, "-I", str(HOOK_DA_PAUSA)], input="isto não é JSON",
                                   capture_output=True, text=True, encoding="utf-8", check=False, timeout=30,
                                   env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        self.assertNotIn(resultado.returncode, (0, 2))
        self.assertIn("Traceback", resultado.stderr)


if __name__ == "__main__":
    unittest.main()
