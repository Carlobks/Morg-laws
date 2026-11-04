# Bíblia do Akita

Notas de leitura do livro **_Competente o Suficiente_**, de **Fabio Akita**, sobre como trabalhar com IA e agentes de código.

## O que é e o que não é

- É um **resumo com palavras nossas**, organizado para consulta. Cada item leva a página do livro, para quem quiser ler o original.
- **Não** reproduz o texto do livro. Para o raciocínio completo, os exemplos e o contexto, leia o livro.
- As páginas são as **impressas** (as do rodapé do livro).
- Cada conselho aparece uma vez só: o que o livro diz em forma de proibição fica no `nao-faca.md`, e os arquivos de tema não o repetem.

## Arquivos

| Arquivo | O que tem |
|---|---|
| [nao-faca.md](nao-faca.md) | Os "não faça" do livro (76 itens, das 83 notas de leitura e da revisão da leitura inteira), agrupados por tema |
| [seguranca.md](seguranca.md) | Segurança com agentes: acesso, segredos, injeção de instruções, terceiros, auditoria, dados pessoais e golpes |
| [backups-e-infraestrutura.md](backups-e-infraestrutura.md) | Backup e restauro, operações destrutivas, tarefas automáticas, entregas e continuidade dos fornecedores |
| [arquivo-de-regras.md](arquivo-de-regras.md) | O arquivo que o agente lê em todo pedido: quando, com que forma, o que vai dentro, como cresce, skills e camadas |
| [documentacao-e-memoria.md](documentacao-e-memoria.md) | O que o agente lembra, onde guardar o que se aprende e como escrever documentos que se mantêm certos |
| [testes-e-revisao.md](testes-e-revisao.md) | O juiz de fora, os testes que enganam, conferir a entrega, revisão e o processo de testes |
| [pedidos-e-sessoes.md](pedidos-e-sessoes.md) | Como montar um pedido, conduzir o trabalho e escolher que trabalho dar ao agente |
| [aprender-com-agentes.md](aprender-com-agentes.md) | Como estudar com IA, o que não perde valor e o que esperar de verdade dos agentes |
| [equipe-e-empresa.md](equipe-e-empresa.md) | O cuidado à medida do risco, quem decide, como a equipe se organiza e as pessoas |
| [modelos-e-medicao.md](modelos-e-medicao.md) | Como ler promessas, tabelas e anúncios, como escolher um modelo e o que há dentro dele |
| [custos-e-limites.md](custos-e-limites.md) | Tokens e cota, as contas de custo que enganam e o que reaproveitar |
| [leituras.md](leituras.md) | Os 17 artigos do blog do autor que o livro indica como fontes, com a data e para que serve cada um |

## Como cada conselho vira regra

Cada conselho diz que tipo de barreira o pode impor:

- **texto:** só uma regra escrita (num `AGENTS.md`, numa skill ou num guia da equipe);
- **máquina:** uma barreira automática (permissão negada ao agente, hook, teste, CI ou configuração da conta).

E diz **onde aplicar**: a skill do Morg-laws que já o aplica, ou «ainda nenhuma». Um conselho com «ainda nenhuma» é um candidato a entrar numa skill.

Pelo que o próprio livro ensina, o que importa muito deve ter barreira de máquina: uma regra só escrita depende de alguém lembrar dela. Por isso o formato desta pasta também é conferido no CI (`tests/test_biblia.py`): cada conselho tem a página, a barreira e uma skill que existe (ou «ainda nenhuma»), e cada arquivo está nesta tabela.
