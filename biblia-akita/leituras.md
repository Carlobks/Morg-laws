# Leituras recomendadas pelo livro

Artigos do blog do autor que *Competente o Suficiente*, de Fabio Akita, indica como as fontes originais dos seus capítulos (secção «Fontes», pp. 433–455). A data é a da publicação; o resumo é nosso, feito ao reler cada artigo em 2026-11-04, e cada um tem a sua entrada no [FONTES.md](../FONTES.md).

## Por onde começar

- [Por que as LLMs não te dão o resultado esperado | Por que eu prefiro Claude Code hoje](https://akitaonrails.com/2026/04/15/como-falar-com-o-claude-code-efetivamente/) (2026-04-15): como montar o pedido em partes (o objetivo, o que não se quer, como validar, o contexto) e continuar a conversa durante o trabalho.
- [Clean Code pra Agentes de IA](https://akitaonrails.com/2026/04/20/clean-code-para-agentes-de-ia/) (2026-04-20): o código escrito para o agente ler, com arquivos e funções pequenos, nomes que não se confundem e testes que ele roda sozinho, e as regras guardadas no arquivo de instruções.
- [Como me precaver pros meus agentes não apagarem minhas coisas?](https://akitaonrails.com/2026/07/11/como-me-precaver-pros-meus-agentes-nao-apagarem-minhas-coisas/) (2026-07-11): camadas que tornam qualquer engano recuperável: jaula, snapshots automáticos e backup externo com retenção.
- [Dicas e Toolkit de IA do Akita: ai-jail, ai-memory, ai-usagebar](https://akitaonrails.com/2026/05/24/dicas-e-toolkit-de-ia-do-akita-ai-jail-ai-memory-ai-usagebar/) (2026-05-24): poucas ferramentas e muita engenharia (testes, CI, refatoração, deploy automático), com cercas de segurança e decisões registradas no git.
- [Desastre no meu NAS! Como quase perdi 90 TB de dados](https://akitaonrails.com/2026/10/06/desastre-no-meu-nas-como-quase-perdi-90-tb-de-dados/) (2026-10-06): discos em espelho não são backup; com discos grandes, duas paridades, e uma cópia separada, fora de casa, do que não tem substituto.
- [Por que LLMs vão falhar na Sua Empresa?](https://akitaonrails.com/2026/06/24/por-que-llms-vao-falhar-na-sua-empresa/) (2026-06-24): pôr IA no processo antigo não chega; é preciso encurtar o ciclo entre decidir, fazer, testar e rever, e voltar a decidir em vez de delegar.
- [Parem de inventar desculpas e façam mais deploy! Com a IA, a premissa mudou. Entendam.](https://akitaonrails.com/2026/09/22/parem-de-inventar-desculpas-e-facam-mais-deploy-a-premissa-mudou/) (2026-09-22): entregar mais vezes, com a base já montada (testes, CI, voltar atrás de verdade, observação e um ambiente de testes).
- [O código fonte do Claude Code vazou. O que achamos dentro.](https://akitaonrails.com/2026/03/31/codigo-fonte-do-claude-code-vazou-o-que-achamos-dentro/) (2026-03-31): o que o vazamento mostra sobre memória, compactação e limites de leitura, e as verificações que um processo de publicação devia ter.

## Método e verificação

- [Vibe Code: Do Zero à Produção em 6 DIAS | The M.Akita Chronicles](https://akitaonrails.com/2026/02/16/vibe-code-do-zero-a-producao-em-6-dias-the-m-akita-chronicles/) (2026-02-16): o agente como um programador dedicado que precisa de instruções claras, com você no papel de produto, liderança técnica e qualidade: plano antes do código, testes, CI e commits pequenos.
- [Testes de Integração em MonoRepo | Bastidores do The M.Akita Chronicles](https://akitaonrails.com/2026/02/20/testes-de-integracao-em-monorepo-bastidores-do-the-m-akita-chronicles/) (2026-02-20): os dublês de teste não apanham a quebra do contrato entre aplicações; testar o caminho inteiro com dados de verdade, e controlar o custo das chamadas pagas.
- [Software Nunca Está 'Pronto' — 4 Projetos, a Vida Pós-Deploy, e Por Que One-Shot Prompt É Mito](https://akitaonrails.com/2026/03/01/software-nunca-esta-pronto-4-projetos-a-vida-pos-deploy-e-por-que-one-shot-prompt-e-mito/) (2026-03-01): o software melhora com voltas depois de entrar em uso, com alguém experiente no comando, testes, CI e entregas pequenas.
- [Como Driveclub e shadPS4 Quase Derrotaram a IA e a Mim: Como Aprender](https://akitaonrails.com/2026/04/23/driveclub-shadps4-e-ia-como-aprender/) (2026-04-23): não aceitar o remendo sem a causa, e entrar num assunto novo como iniciante, por etapas, descartando hipóteses.
- [LLM Benchmark: Devo usar o que tem nota maior?](https://akitaonrails.com/2026/07/19/llm-benchmark-devo-usar-o-que-tem-nota-maior/) (2026-07-19): ler um ranking como grupos de qualidade e escolher dentro do grupo bom pelo custo, pela velocidade e pela ferramenta, com um teste próprio.
- [Novo LLM Benchmark v4: retestando TODOS os principais LLMs (Parte 1)](https://akitaonrails.com/2026/09/15/novo-llm-benchmark-v4-retestando-todos-llms-parte-1/) (2026-09-15): cada nota só vale para o método que a produziu; repetir o teste num problema parecido com o seu.
- [Ensinando a questionar notícias | Frank Investigator](https://akitaonrails.com/2026/03/27/ensinando-a-questionar-noticias-frank-investigator/) (2026-03-27): comparar fontes diferentes, ver o que foi omitido, ir à fonte primária, e usar a IA com perguntas estruturadas em vez de abertas.

## Antes de comprar

- [Hot take: Harness, Loop Engineering, Graph Engineering são Bullshit](https://akitaonrails.com/2026/08/18/hot-take-harness-loop-engineering-graph-engineering-sao-bullshit/) (2026-08-18): em vez de cursos de moda, a base da engenharia de software; o conhecimento do projeto fica no projeto, não preso a uma ferramenta.
- [Você é um idiota se acredita nas propagandas enganosas da OpenAI, Anthropic, NVIDIA. Entenda](https://akitaonrails.com/2026/09/09/propagandas-enganosas-da-openai-anthropic-nvidia/) (2026-09-09): antes de acreditar num anúncio dramático, perguntar quem lucra com ele e pedir provas que se possam conferir.
