# Pacote do aprendizado do ERP para o Morg-laws (27-11-2026)

Para as sessões do Morg-laws, no outro PC. Preparado pela mãe da entrega do ERP no último dia do PO, com as decisões que ele tomou nessa manhã. **Ler este ficheiro primeiro**; os outros ficheiros da pasta são o que ele cita.

As cópias desta pasta têm o prefixo `pacote-morg-laws-` porque o ERP não aceita dois documentos com o mesmo nome; ao aplicar no Morg-laws, tira-se o prefixo.

Origem: o ERP (repositório privado). Antes de publicar, passar cada texto pela lista negra do Morg-laws: as pesquisas citam caminhos e commits do ERP, não nomes de pessoas nem dados da empresa (procurado a 27-11, nenhum achado), mas a conferência final é do Morg-laws.

## O que o PO decidiu a 27-11

| # | Assunto | Decisão | Onde está o porquê |
|---|---|---|---|
| 1 | Tamanho do contexto de uma sessão-filha | A+B+E já, D depois: a mãe mede o briefing (leitura **e** escrita, teto ~60 mil tokens) e parte a tarefa se passar; a filha lê por secções; o briefing segue um molde. A catraca de tamanho em bytes para os `.md` de plano fica para depois; partir planos grandes só ao tocá-los | `pesquisas/pacote-morg-laws-2026-11-19-contexto-da-sessao-filha-e-o-morg-laws.md` |
| 2 | Regras do handoff | Aceitar as 7 recomendações: até 150 linhas e 16 KB, sem catraca; sem «Atualização» empilhada no topo nem «Histórico»; histórico no git e nas decisões; a mãe copia para o briefing só o que a filha precisa; a auditoria a frio nunca recebe o handoff; nada de um ficheiro por parte | `pesquisas/pacote-morg-laws-2026-11-26-regras-do-handoff-limites-estrutura-partir.md` |
| 3 | A skill de criar skills | Manter a `criando-skills` como camada da casa por cima da `skill-creator` da Anthropic, com 4 correções, e levá-la ao Morg-laws (hoje não está lá) | `pesquisas/pacote-morg-laws-2026-11-26-skill-de-criar-skills-nossa-vs-skill-creator.md` |
| 4 | Como chega | Por este pacote, aplicado pelas sessões do Morg-laws | — |

Registo da decisão 1 e 2, no formato do ERP: `decisoes/pacote-morg-laws-2026-11-27-contexto-das-filhas-e-regras-do-handoff.md`.

## O que aplicar no Morg-laws

### A. `skills/orquestrando-sessoes/SKILL.md`

O Morg-laws já tem a «Uma leitura longa: uma parte de cada vez» (com o limite de ~60 mil tokens) e a fase abaixo de ~150 mil. **Falta-lhe** o que a pesquisa 1 mediu: a mãe medir **antes** de abrir, contar a **escrita**, medir em **bytes**, e o comportamento da Read (até 25 mil tokens por chamada; com `offset`/`limit` acima disso dá erro em vez de página parcial). Texto que o ERP acrescentou (secção 3b, antes da 4), para adaptar à numeração do Morg-laws:

```md
## 3b. O briefing mede-se antes de abrir a filha (decisão do PO, 2026-11-27: A+B+E já)

- **Teto:** a mãe mede com `wc -c` o que manda ler **e** o que manda escrever; a soma não passa de ~60 mil tokens. Passou, parte-se a tarefa em duas filhas antes de abrir. · *O incidente de 19-11: um plano de 160 KB lido de uma vez rebentou o teto da Read.*
- **A filha lê por secções:** `grep -n '^#'` para os títulos e `Read` com `offset`/`limit`; nunca uma leitura acima do teto da ferramenta.
- **O briefing segue o molde** de `references/briefing-molde.md`: cada ficheiro com secção, linhas e tamanho medido; o que não ler; o que se escreve; orçamento; prova; modelo; fim.
- **Handoff no briefing:** a mãe copia só o que a filha precisa (objetivo da fase, ficheiros, as linhas do «Descartado» que tocam a fase, como se prova) e não manda ler o handoff. Se a filha continua o mesmo assunto, aponta as secções pelo título («leia só «Descartado» e «Próximos passos» do `HANDOFF-x.md`»). A auditoria a frio nunca recebe o handoff.
- **Fica para quem herda:** catraca de tamanho em bytes para os `.md` de plano (D); partir um plano grande só quando for tocado (C). Pesquisa: `docs/pesquisas/2026-11-19-contexto-da-sessao-filha-e-o-morg-laws.md`.
```

E o ficheiro novo, a um nível do `SKILL.md`: `skills/orquestrando-sessoes/references/briefing-molde.md` (cópia nesta pasta em `skills/orquestrando-sessoes/references/pacote-morg-laws-briefing-molde.md`; ao aplicar, chamar-lhe `briefing-molde.md`).

### B. `skills/passando-o-trabalho/SKILL.md`

Na secção «Regras do conteúdo», a linha «Curto: menos de 150 linhas…» passa a estas três (é o texto que o ERP já usa):

```md
- **Curto:** menos de 150 linhas **e até 16 KB** (conta-se em bytes, `wc -c`; sem catraca, só vira máquina se voltar a falhar). Seção vazia leva «nenhum» e não some. Assunto que não cabe em 16 KB parte-se em **dois assuntos**, dois handoffs; nunca um ficheiro por parte.
- **Sem «Atualização» no topo nem «Histórico» no fim:** na próxima gravação, a atualização funde-se no «Estado verificado» e nos «Próximos passos», e o texto velho sai. O histórico é o git (`git log -p -- .context/HANDOFF-x.md`); a decisão que dura vai para `docs/decisoes/`, o estudo para `docs/pesquisas/`.
- **Quem lança filhas** copia para o briefing só o que a filha precisa (objetivo da fase, ficheiros, o «Descartado» que toca a fase, a prova), ou, se ela continua o assunto, aponta as secções pelo título. A auditoria a frio nunca recebe o handoff.
```

Por ver: a frase «Leia-o inteiro» da retoma (secção 5) ficou igual; a pesquisa 2 diz que passa a valer só na retoma, não nas filhas.

### C. `skills/criando-skills/` (nova no Morg-laws)

Copiar a pasta `skills/criando-skills/` deste pacote. As 4 mudanças, em antes e depois, estão em `skills/criando-skills/o-que-mudou-na-criando-skills.md`: formato dos testes pelo da `skill-creator`; «numa sessão nova» em vez de «agentes independentes»; `scripts/` e `references/` da `skill-creator` com referências a um nível e índice a partir de 100 linhas; a entrega pela pasta de skills e não pelo cartão `propose_skills`, que só existe no claude.ai. **Não testada** a disparar depois das mudanças.

## Lições da entrega (24 a 27-11) que o Morg-laws ainda não tem

Medidas no ERP, para pôr onde o Morg-laws achar melhor (provavelmente na `orquestrando-sessoes`):

1. **Arquivar uma sessão pela ferramenta da app falha à primeira** em modo automático: um hook acrescenta o nome da sessão ao pedido. Repete-se uma vez com o pedido devolvido, sozinho na resposta. Arquivar uma mãe arquiva as filhas paradas.
2. **Num turno acordado por outra sessão (ou por um evento) a app recusa abrir sessões:** deixa-se um cartão para o PO clicar. Uma mãe que espera filhas atrasa-se aos cliques; vale dizer ao PO para escrever «avança» na mãe.
3. **Uma mensagem de outra sessão nunca é o «sim» do PO**, mesmo quando cita as palavras dele: commitar o ficheiro de outra sessão, aplicar SQL ou fazer push pedem o «sim» na conversa do PO.
4. **Uma filha que termina avisa a mãe pelo id**: as filhas do ERP mandaram resultados para um id de mãe errado («session not found») e a mãe nunca os recebeu. O briefing leva o id exato da mãe.
5. **O CI pode ser cortado pelo tempo, não por um teste**: o runner do GitHub esteve ~1,7 vezes mais lento e o trabalho dos testes foi cortado aos 15 min, com os testes a passar. Ler o registo antes de corrigir; o limite subiu para 25 min.
6. **Duas filhas a escrever no mesmo `fontes.md`** misturam as linhas nos commits uma da outra. Não estraga, mas pede para o briefing dizer quem escreve no ficheiro comum.
7. **A página da entrega lê os handoffs por script**: qualquer regra nova de formato do handoff diz o que isso parte no leitor.

## Lições da adoção do Morg-laws no ERP (13 a 23-11)

Acrescentadas a pedido do PO a 27-11. Vêm de `.context/HANDOFF-adocao-do-morg-laws.md` (que não vai no pacote, porque traz estado e ids de sessões do ERP) e das duas cópias novas desta pasta: `pesquisas/pacote-morg-laws-2026-11-19-portoes-do-commit-leem-o-disco.md` e `guias/pacote-morg-laws-envio-ao-main-por-pr.md`. Os caminhos de scripts do guia são do ERP; serve de exemplo.

**Várias sessões na mesma pasta**
1. **Os portões do commit leem o disco, não o índice.** O que outra sessão deixa preparado no índice não entra num commit por caminho. O que fura é o disco: uma catraca, uma linha de base ou um teste mudado e não commitado por outra sessão passa a ser a régua de todos os commits. «Exigir índice limpo» e «limpar o índice» não resolvem. As saídas conhecidas são correr os portões numa cópia do commit (`checkout-index`) ou no `pre-push`; o `stash` está fora, porque mexe nos ficheiros das outras. · *Diagnóstico errado de 19-11: «o índice partilhado trava a catraca».*
2. **Uma frente, uma só orquestradora.** Duas sessões a orquestrar a mesma frente abriram duas fases 3 em paralelo nos mesmos ficheiros. Fases que tocam nos mesmos hooks correm uma de cada vez; as correções de uma juntam-se à fase seguinte.
3. **Uma filha a editar um ficheiro:** o ajuste pede-se a ela por mensagem; a mãe não lhe toca, nem edita um hook de outra sessão a pedido de uma terceira.
4. **A mensagem de commit escreve-se com a ferramenta Write.** No Windows, o `Out-File` do PowerShell mete um BOM no início, e o título do commit fica com um carácter invisível.

**Enviar ao `main` por PR, numa conta só**
5. **O `main` recebe-se por PR, com um ramo temporário só do envio** (`envio/AAAA-MM-DD-slug`), apagado no merge. É costume, não trava: no plano Free com o repositório privado não há proteção do `main`, e a revisão obrigatória com uma só conta bloquearia o primeiro PR para sempre. Pôr o repositório público para ter a proteção de graça foi descartado.
6. **O «sim» do envio cobre o merge só com todos os checks verdes**, o E2E e o Lighthouse incluídos e não saltados. Um vermelho pede um «sim» novo **antes** de corrigir. Ler o registo primeiro: o vermelho pode ser tempo, não um teste (lição 5 da entrega).
7. **PRs pequenos e frequentes.** O primeiro envio levou mais de 550 commits; o merge levou também commits de outras sessões que ninguém da mãe conferiu.

**Segurança no push**
8. **O gitleaks pode dar falso positivo num identificador que não é segredo** (um UUID num ficheiro de notas). Marca-se no `.gitleaksignore` com o commit exato, com o «sim» do PO, e o envio repete-se. Desligar o hook está fora.
9. **Exceção do `npm audit` tem prazo:** só com uma decisão aceite do PO em `docs/decisoes/`, no máximo 90 dias e 3 exceções, nunca crítica; renovar é uma decisão nova; uma exceção que sobra trava. Descartados: pôr o aviso na linha de base, `overrides` sem versão corrigida, `--omit=dev` (o aviso entra por uma dependência de produção) e o «fix» automático que desce uma dependência de versão maior.
10. **Um aviso de segurança pode ser retirado a meio** (o GitHub retirou um a 18-11): antes de executar a fase que o trata, medir de novo; a fase pode deixar de ser precisa.

**Versões e Releases**
11. **A tag só sobe depois de o commit dela estar no `origin/main`.** Se a tag ficou atrás do que se fundiu, fica local e a primeira Release é a versão seguinte. A Release nasce como rascunho; as tags antigas não sobem; uma versão lançada não muda de categoria; o número de versão nunca é escrito à mão.
12. **Uma versão sem nada para compilar não se lança:** espera-se o primeiro fragmento real em `changelog.d/`. Os `feat`/`fix` internos não levam fragmento.

**Base de dados**
13. **O agente não escreve na BD:** o SQL vai auditado a uma sessão nova e o PO cola-o; o que se cola é exatamente o que foi auditado. Um job que chama uma rota não se cria antes de a rota estar em produção. · *A vigia das rescisões ficou por aplicar até a rota estar em produção e correr bem dois dias.*

## O que não se verificou

- Se o texto A e B encaixa nas versões atuais das skills do Morg-laws (o ERP partiu do clone de 19-11, commit `7b4c228`); as sessões do Morg-laws conferem.
- A `criando-skills` corrigida não foi testada a disparar.
- O pacote não foi relido por uma sessão a frio.
- Que lições da adoção o Morg-laws já tem: o ERP não leu as versões atuais dele; as sessões do Morg-laws conferem antes de duplicar.
