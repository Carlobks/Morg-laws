# Os "não faça" do livro

Resumo com palavras nossas de *Competente o Suficiente*, de Fabio Akita. A página é a impressa. `#n` é o número da nota de leitura de origem (de 1 a 83). A barreira diz como impor o item: **texto** (regra escrita) ou **máquina** (permissão, hook, teste, CI, configuração).

## 1. Adotar ferramentas, modelos e cursos

- Não adotar uma ferramenta, um plano pago ou um modelo novo só porque foi anunciado. Antes, pergunte: serve para quê, quem conferiu e quanto custa. (p. 5) #1 · **texto**
- Não decidir com base na demonstração do fabricante: o exemplo mostrado costuma ser o melhor de muitas tentativas. Teste no seu caso. (p. 17) #2 · **texto**
- Não pagar por uma "memória que aprende sozinha" sem saber onde e como ela guarda o texto. (pp. 37, 39) #9 · **texto**
- Não trocar de modelo por causa de um ranking. Pergunte que prova foi usada, como se mediu, quantas vezes, contra quem e a que custo. Na compra, distinga o que foi medido de forma independente, o que só o vendedor afirma e o que ainda está por provar. (pp. 152, 400–401) #36 #82 · **texto**
- Não passar um trabalho crítico para a versão nova de um modelo sem testá-la antes no seu caso. (p. 160) #39 · **texto**
- Não pagar formação ou consultoria com nome de disciplina nova sem ver o que ela ensina de concreto. Muitas vezes é uma prática antiga com nome novo. (p. 209) #45 · **texto**
- Não comprar por medo de ficar para trás nem no mês do anúncio. Espere, e pergunte a quem vende onde estão os projetos reais que melhoraram com aquilo. (pp. 210, 213–214, 327–328) #46 #48 #69 · **texto**
- Não distribuir licenças de IA à equipe com a ordem "sejam mais produtivos", sem objetivo, métrica nem formação. Meça o que mudou para o cliente, não o volume de uso. (p. 284) #65 · **texto**

## 2. Verdade e fontes

- Não aceitar do agente uma regra legal, fiscal ou trabalhista sem a fonte oficial conferida: o modelo não sabe se o que diz é verdade. (pp. 17–18) #3 · **texto**
- Não aceitar a explicação do agente sobre uma decisão passada sem a fonte (commit, registro de decisão). Ele pode inventar o que não lembra. (p. 32) #7 · **texto**
- Não usar um chat sem busca para decidir sobre saúde, dinheiro ou lei. Prefira a fonte primária e compare modelos. (p. 51) #11 · **texto**
- Não pedir validação com uma pergunta que já traz a resposta ("isto está certo, não está?"). Pergunte o que falha, quais os riscos e quais as alternativas. (pp. 52–54, 56) #12 · **texto**
- Não pôr num documento oficial uma citação, um estudo ou um número que o agente trouxe sem abrir a fonte. O tom seguro não prova nada. (pp. 55–56) #13 · **texto**
- Não aceitar um "zero" ou uma data de um relatório do agente sem perguntar se ele mediu ou só não encontrou. (p. 99) #27 · **texto**
- Não pôr a sua conclusão dentro do pedido de pesquisa. Se dois modelos concordam com a ideia que você já pôs no pedido, isso é eco, não confirmação. (p. 211) #47 · **texto**
- Não enviar a terceiros um relatório ou achado do agente sem conferir cada afirmação. (pp. 245–246) #57 · **texto**
- Não aceitar a explicação do agente sobre **como** verificou algo sem a evidência (comando, saída, consulta). A explicação é a mais provável, não necessariamente o que ele fez. (p. 357) #71 · **texto**

## 3. Decisões que são de pessoas

- Não deixar o agente decidir sozinho uma regra de negócio ou legal (como pagar, quem dispensar, que imposto se aplica). Ele fica com o trabalho repetitivo. (p. 21) #4 · **texto**
- Não decidir com base num chatbot um assunto que tem um profissional responsável (contador, advogado, médico do trabalho). (pp. 58–59) #15 · **texto**
- Não trocar a leitura de um contrato pelo resumo feito por IA: o resumo pode omitir a cláusula que importa. Contas com datas pedem o cálculo passo a passo, refeito numa planilha. (p. 59) #16 · **texto**
- Não acusar alguém de ter usado IA com base num "detector de texto de IA". (p. 60) #18 · **texto**
- Não pedir uma tela ou um cálculo novo para um problema de negócio sem antes descobrir, com quem usa, qual é a regra certa. Às vezes a solução é menos software. (p. 304) #67 · **texto**

## 4. Conferir o trabalho do agente

- Não tratar um "nenhuma falha de segurança encontrada" como garantia. Some verificações automáticas e revisão externa. (p. 21) #5 · **texto**
- Não aprovar um commit ou um push só porque o agente disse "pronto" ou "tudo verde". Veja a prova. (p. 47) #10 · **texto + máquina** (hooks com os portões)
- Não deixar uma sessão longa a correr sem conferir os pontos intermédios: o plano, a lista, o diff. (p. 64) #19 · **texto**
- Não deixar o agente insistir mais de duas vezes na mesma correção. Pare e mude a pergunta. (p. 67) #20 · **texto**
- Não tratar um sistema que outras pessoas usam como "feito só pela IA". Um programador experiente revê o que importa. (p. 72) #22 · **texto**
- Não ler a falta de objeções do agente como "a ideia é boa e segura": ele quase nunca diz não. Pergunte que proteção se esqueceu de pedir. (p. 80) #24 · **texto**
- Não aceitar "os testes passam" quando foram escritos na mesma sessão que o código. O teste de regressão tem de falhar antes da correção. (p. 81) #25 · **máquina** (teste de mutação no CI)
- Não aprovar um plano sem as perguntas incômodas: e se a operação parar a meio? E se os dados corromperem? E se duas pessoas fizerem o mesmo ao mesmo tempo? (p. 92) #26 · **texto**
- Não continuar a pedir "mais um ajuste" quando cada ajuste quebra outra coisa. Pare e repense. (p. 105) #28 · **texto**
- Não fechar um bug porque "já não acontece" sem ter a causa escrita. Uma mitigação não é uma solução. (pp. 108–109) #29 · **texto + máquina** (o commit `fix` exige a causa)
- Não mandar um pedido importante sem dizer o que fica de fora e qual é o critério de pronto. (p. 120) #30 · **texto**
- Não aprovar o trabalho de uma sessão pelo resumo que ela própria escreveu. Audite o diff. (pp. 127, 129) #31 · **texto**
- Não liberar para todos uma tela que "ficou pronta rápido e os testes passam" sem uso real por um grupo de teste. (pp. 135–136) #33 · **máquina** (interruptor + grupo de teste)
- Não abrir mais sessões em paralelo do que as que consegue acompanhar com atenção. (p. 136) #34 · **texto**
- Não aceitar "tudo feito" sem a lista dos critérios, cada um com a sua prova. (p. 157) #37 · **texto**
- Não aceitar uma mudança que altera um teste existente para ele passar sem perguntar porquê. O agente pega o que quebra, não o que só está errado. (pp. 160–161) #38 · **máquina** (aviso no hook)
- Não aprovar sem olhar, mas também não gastar o tempo a corrigir o que as verificações automáticas já conferem. (p. 272) #63 · **texto**
- Não aprovar o que não consegue ler nem explicar em duas frases (o que muda, o que pode quebrar). Peça explicação, prova ou uma segunda revisão. (pp. 280, 331) #64 #70 · **texto**

## 5. Registrar

- Não tomar uma decisão importante só na conversa. Escreva-a num arquivo assim que for tomada. (pp. 32–33) #6 · **texto**
- Não transformar cada falha numa regra logo a seguir. Espere ver se ela se repete ou se custou caro, e escreva o porquê. (p. 35) #8 · **texto**
- Não pedir uma correção com "não funciona". Dê a mensagem exata, os passos para reproduzir e o que mudou antes. (p. 68) #21 · **texto** (modelo de relato)
- Não deixar uma sessão longa terminar sem o registro do que se aprendeu. O modelo começa cada sessão sem memória. (p. 319) #68 · **máquina** (hook de fim de sessão)

## 6. Privacidade

- Não colar dados da empresa (salários, extratos, documentos com dados pessoais) num chatbot sem anonimizar e sem confirmar que o plano não treina com eles. O que falta nos dados pode virar conclusão. (pp. 56, 59–60) #14 #17 · **texto**
- Não ligar um serviço de relatórios de erro ou métricas sem configurar a remoção de dados pessoais. (p. 257) #59 · **máquina** (configuração do SDK + teste)
- Não encaminhar e-mails ou documentos da empresa para serviços gratuitos de análise. (pp. 262–263) #61 · **texto**
- Não partilhar transcrições de sessões que consultaram dados de produção. Filtre os dados sensíveis antes de guardar registros de sessões. (p. 394) #80 · **texto**

## 7. Acesso e permissões do agente

- Não deixar segredos (chaves, `.env`, backups com dados pessoais) onde o agente consegue ler: o que está ao alcance acaba por ser usado. (pp. 164–165) #40 · **máquina** (negar leitura nas permissões)
- Não aprovar commits que acrescentam exceções ao alarme (`eslint-disable`, `@ts-ignore`, testes saltados) sem a razão escrita. (p. 165) #41 · **máquina** (catraca)
- Não dar ao agente credenciais de escrita em produção, nem contando com a confirmação de um hook. Corte o acesso, não o filtre, e nunca dê a mesma credencial a todos. (pp. 205, 234) #43 #52 · **máquina** (papel só de leitura)
- Não ligar um conector novo (banco, e-mail, arquivos) sem decidir por escrito o que o agente fica autorizado a fazer lá. (pp. 205–206) #44 · **máquina** (permissões por ferramenta)
- Não usar o modo que salta todas as permissões fora de uma sandbox. (pp. 228, 386) #50 #77 · **máquina** (desligar esse modo nas definições)
- Não deixar o agente instalar pacotes novos sem aprovação: uma biblioteca invadida roda com as permissões dele. (p. 228) #51 · **máquina** (pedir confirmação para `npm install`)
- Não instalar skill, plugin ou MCP de terceiros sem ler tudo. De preferência, escreva a sua. (pp. 128–129, 239) #32 #55 · **texto + máquina**
- Não instalar gateways, bots ou MCPs que leem mensagens de fora e executam comandos, se ninguém consegue revisar o ritmo de mudanças deles. (pp. 237–239) #54 · **máquina** (lista permitida)
- Não continuar a fazer trabalho com permissões (banco, push, arquivos) na mesma sessão longa depois de o agente ler conteúdo externo não confiável: uma instrução lida pode sobreviver à compactação como se fosse ordem sua. (p. 240) #56 · **texto**
- Não instalar aplicativos baixados de sites espelho. Use a fonte oficial. (p. 252) #58 · **texto**
- Não autorizar um aplicativo de terceiros nas contas da empresa a partir de um link recebido, mesmo que a tela de autorização seja a verdadeira. (p. 261) #60 · **máquina** (lista permitida na consola)
- Não rodar o agente com acesso à pasta pessoal inteira e às credenciais do usuário. No Windows, considere o WSL2 ou a sandbox do agente. (p. 382) #73 · **máquina**
- Não aprovar "sim a tudo" por cansaço. Organize as permissões em três colunas: pode sem perguntar, pergunta antes, nunca. (p. 385) #76 · **máquina**
- Não deixar o agente ler o `.env` nem editar as próprias configurações de segurança. Configurações vindas de dentro do projeto só podem apertar, nunca afrouxar. (p. 389) #79 · **máquina + texto**
- Não colar `curl … | sh` de fontes não oficiais nem sem ler o script. Prefira instaladores que conferem a soma de verificação. (p. 397) #81 · **máquina** (pedir confirmação)

## 8. Dados, lotes e backups

- Não distribuir em lote (documentos, e-mails, recibos) sem abrir uma amostra do resultado final. (p. 181) #42 · **texto**
- Não autorizar uma operação destrutiva em lote sem ver antes a contagem do que será protegido e do que será apagado. Uma lista de proteção vazia é um alarme. (pp. 222, 224) #49 · **máquina** (o script exige o número esperado)
- Não apagar a origem antes de conferir a cópia no destino. (pp. 235–236) #53 · **texto**
- Não remover colunas ou tabelas no mesmo passo em que cria as novas, nem sem backup. Primeiro acrescente, espere todos migrarem, e só então remova. (p. 293) #66 · **máquina** (aviso em `DROP`)
- Não trabalhar com agentes no Windows sem backup externo automático da pasta de trabalho. (p. 383) #74 · **máquina**
- Não confiar num backup que nunca foi restaurado. Abra alguns arquivos da cópia todo mês. (p. 385) #75 · **máquina** (tarefa recorrente)
- Não restaurar a partir de um arquivo só porque se chama "último". Confira a data, o tamanho, o hash e a contagem das tabelas-chave. (p. 423) #83 · **máquina**

## 9. Dinheiro, custos e fraude

- Não passar a pagar por pedido (API) quando o plano bate no limite, só para continuar. Espalhe o trabalho por dias. (pp. 70–71) #23 · **máquina** (teto de gasto)
- Não deixar um trabalho em lote a correr sem saber se o uso extra pago está ligado e com teto. (pp. 146–147) #35 · **máquina** (configuração da conta)
- Não mudar dados bancários nem autorizar uma transferência com base só num e-mail, mensagem, áudio ou vídeo. Confirme por um canal que você já conhecia. (p. 264) #62 · **máquina** (segundo aprovador)

## 10. Aprender e enviar

- Não pedir a solução pronta quando o objetivo é aprender. Tente sozinho primeiro e peça uma pista. (p. 363) #72 · **texto**
- Não aprovar um push sem ver a lista de arquivos de todos os commits por enviar, incluindo os removidos depois. (p. 386) #78 · **máquina** (`pre-push` com scanner de segredos)
