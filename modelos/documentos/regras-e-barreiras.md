# Regras e barreiras

Cada regra do `CLAUDE.md` e o que a obriga. Texto é conselho; o que tem de ser cumprido vira hook, teste ou CI
(skill `escrevendo-regras-de-agente`). O `tests/test_regras.py` exige que cada título do `CLAUDE.md` tenha aqui uma
linha, e que cada caminho citado exista.

**Tipos de barreira:**
- **hook:** um hook do Claude Code em `.claude/hooks/` (trava o agente; um commit feito à mão não passa por ele);
- **git:** um hook do git em `.githooks/` (vale para o agente e para quem commita à mão);
- **teste:** um teste do comando único de testes, que roda em cada commit;
- **permissão:** uma regra em `.claude/settings.json` (o `ask` sozinho não pergunta no modo automático);
- **CI:** uma verificação no GitHub; vale também para quem desligou os hooks do git;
- **texto:** só a regra escrita (não há máquina que a decida; o motivo está ao lado);
- **por fazer (<fase>):** a barreira tem fase marcada no plano; o teste falha quando a fase fica feita.

| Regra | Barreira | Onde |
|---|---|---|
| <O PERIGO MAIS CARO> | por fazer (F1) | <o hook ou teste que vai obrigá-la> |
| PLANO ANTES DE MEXER | teste; texto | `tests/test_docs_indices.py`: os planos têm "Fora do escopo" e a prova; o "sim" do dono é texto |
| DECISÃO É DO DONO | texto | nenhuma máquina sabe o que é uma decisão do dono; skill `pondo-o-plano-a-prova` |
| COMMIT SEM PEDIDO, PUSH COM O SIM | hook | `.claude/hooks/perguntar_antes.py` pergunta antes de cada push e PR |
| OS HOOKS SÃO A REDE | hook + CI | `.claude/hooks/guarda_do_git.py` (`--no-verify`, `core.hooksPath`); o CI pega quem saltar à mão |
| NÃO PIORAR | teste | catracas: `tests/test_tamanho_das_funcoes.py`, `tests/test_alarmes.py` |
| SEM SILENCIAR ALARME | teste | `tests/test_alarmes.py` (motivo, contagem, só regras ligadas) |
| BUG TRAZ TESTE | git | `.githooks/commit-msg` → `scripts/portoes/mensagem_commit.py` (fix sem teste exige `Sem-teste:`) |
| PROVAR MEDINDO | git; texto | `.githooks/pre-commit` roda os testes; dizer o que não se verificou é texto |
| NOMES PESQUISÁVEIS | teste | `tests/test_nomes.py` (arquivos, pastas e identificadores) |
| TEXTO VIRA BARREIRA | teste | `tests/test_regras.py` (este mapa) |
| SEM DADOS REAIS | teste + git | `tests/test_dados_pessoais.py`; `.githooks/pre-commit` e `commit-msg` com a lista negra |
| SEM SEGREDOS | permissão + hook + git | `.claude/settings.json` (deny), `.claude/hooks/bloquear_segredos.py`, `.githooks/pre-push` (gitleaks) |
| SÓ O PRÓPRIO TRABALHO | hook | `.claude/hooks/guarda_do_git.py` (`add -A`, `.`, `commit -a`, commit sem caminhos, `git stash`) |
