"""Nenhum texto dos hooks de compactação sugere compactar fora das frases desta lista fechada.

No fim do dia, ou numa pausa de mais de uma hora, não se compacta: grava-se o handoff e para-se. Nenhum hook sabe
quando é o fim do dia, por isso nenhum texto deles pode puxar para compactar. Cada frase com o radical «compact» tem
de estar na lista; uma frase nova falha até entrar nela, às claras.
"""

import re
import unittest

from carregar_modelos import carregar_hook

# O hook e as constantes com o texto que ele mostra (ao usuário ou ao agente).
TEXTOS_POR_HOOK = {"lembrar_o_handoff": ("TEXTO_DA_PARADA",), "retomar_pelo_handoff": ("TEXTO_DA_RETOMADA",),
                   "aviso_da_pausa": ("TEXTO_DO_AVISO",)}
FRASES_COM_COMPACT = {
    "A conversa foi compactada.",
    "Compactação parada (Morg-laws): o /compact não aponta para um .context/HANDOFF-<assunto>.md gravado e commitado.",
    "Grave o handoff com a skill passando-o-trabalho e use o /compact que ela entrega.",
    "Se vai parar (fim do dia ou pausa de mais de uma hora), não compacte: grave o handoff e pare.",
    "Para compactar mesmo assim, ponha «sem handoff».",
    ("Antes de responder, diga ao usuário: se o trabalho continua, grave o handoff (skill `passando-o-trabalho`) e "
     "abra uma sessão nova que o lê; não compacte."),
}
FIM_DE_FRASE = re.compile(r"(?<=[.?!])\s+")


def frases_com_compact(texto):
    """As frases do texto que têm o radical «compact», sem diferença de maiúsculas."""
    return [frase.strip() for frase in FIM_DE_FRASE.split(texto) if "compact" in frase.lower()]


class FimDoDia(unittest.TestCase):

    def test_so_as_frases_da_lista(self):
        for nome, constantes in TEXTOS_POR_HOOK.items():
            hook = carregar_hook(nome)
            for constante in constantes:
                for frase in frases_com_compact(getattr(hook, constante)):
                    with self.subTest(hook=nome, frase=frase):
                        self.assertIn(frase, FRASES_COM_COMPACT, "frase nova com «compact»: confira a regra do fim do dia")

    def test_a_lista_nao_tem_frase_morta(self):
        usadas = {frase for nome, constantes in TEXTOS_POR_HOOK.items() for constante in constantes
                  for frase in frases_com_compact(getattr(carregar_hook(nome), constante))}
        self.assertEqual(FRASES_COM_COMPACT - usadas, set())

    def test_a_parada_diz_para_nao_compactar(self):
        self.assertIn("não compacte", carregar_hook("lembrar_o_handoff").TEXTO_DA_PARADA)

    def test_a_retomada_manda_ler_e_nao_continuar(self):
        texto = carregar_hook("retomar_pelo_handoff").TEXTO_DA_RETOMADA
        self.assertIn("leia o", texto)
        self.assertNotIn("continu", texto.lower())


if __name__ == "__main__":
    unittest.main()
