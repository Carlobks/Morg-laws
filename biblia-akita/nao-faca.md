# Os "não faça" do livro

Resumo com palavras nossas de *Competente o Suficiente*, de Fabio Akita. A página é a impressa. `#n` é o número da nota de leitura de origem (de 1 a 83); o item sem `#n` veio da revisão da leitura inteira. A barreira diz como impor o item: **texto** (regra escrita) ou **máquina** (permissão, hook, teste, CI, configuração). «Onde aplicar» diz que skill do Morg-laws já o aplica, ou «ainda nenhuma».

## 1. Adotar ferramentas, modelos e cursos

- Não adotar uma ferramenta, um plano pago ou um modelo novo só porque foi anunciado. Antes, pergunte: serve para quê, quem conferiu e quanto custa. (p. 5) #1 · **texto** · onde aplicar: ainda nenhuma
- Não decidir com base na demonstração do fabricante: o exemplo mostrado pode ser o melhor de várias tentativas (no anúncio contado na página, de dez). Teste no seu caso. (p. 17) #2 · **texto** · onde aplicar: ainda nenhuma
- Não pagar por uma "memória que aprende sozinha" sem saber onde e como ela guarda o texto. (pp. 37, 39) #9 · **texto** · onde aplicar: ainda nenhuma
- Não trocar de modelo por causa de um ranking. Pergunte que prova foi usada, como se mediu, quantas vezes, contra quem e a que custo. Na compra, distinga o que foi medido de forma independente, o que só o vendedor afirma e o que ainda está por provar. (pp. 152, 400–401) #36 #82 · **texto** · onde aplicar: ainda nenhuma
- Não supor que a versão nova de um modelo é melhor: no caso contado, uma saiu quinze pontos abaixo da anterior. (p. 160) #39 · **texto** · onde aplicar: ainda nenhuma
- Não pagar formação ou consultoria com nome de disciplina nova sem ver o que ela ensina de concreto. Muitas vezes é uma prática antiga com nome novo. (p. 209) #45 · **texto** · onde aplicar: ainda nenhuma
- Não comprar por medo de ficar para trás nem no mês do anúncio. Espere, e pergunte a quem vende onde estão os projetos reais que melhoraram com aquilo. (pp. 210, 213–214, 327–328) #46 #48 #69 · **texto** · onde aplicar: ainda nenhuma
- Não distribuir licenças de IA à equipe com a ordem "sejam mais produtivos" e nenhuma outra instrução. O volume de uso não mostra o que chegou ao cliente. (p. 284) #65 · **texto** · onde aplicar: ainda nenhuma

## 2. Verdade e fontes

- Não aceitar do agente uma lei, uma data ou uma obra sem a conferir: ele inventa com o mesmo à-vontade com que fala do que existe, e não tem como saber se é verdade. (pp. 17–18) #3 · **texto** · onde aplicar: ainda nenhuma
- Não aceitar a explicação do agente sobre uma decisão passada sem a fonte. Ele pode criar um motivo plausível para o que não lembra. (p. 32) #7 · **texto** · onde aplicar: `testes-e-provas`
- Não usar um chat sem busca para decidir sobre saúde, dinheiro ou lei. Prefira a fonte primária e compare modelos. (p. 51) #11 · **texto** · onde aplicar: ainda nenhuma
- Não pedir validação com uma pergunta que já traz a resposta ("isto está certo, não está?"). Pergunte quais são os problemas, ou peça uma coisa fechada: as falácias, o contexto que falta. (pp. 52–54, 56) #12 · **texto** · onde aplicar: `orquestrando-sessoes`
- Não pôr num documento oficial uma citação, um estudo ou um número que o agente trouxe sem abrir a fonte. O tom seguro não prova nada. (pp. 55–56) #13 · **texto** · onde aplicar: ainda nenhuma
- Não aceitar um "zero" ou uma data de um relatório do agente sem perguntar se ele mediu ou só não encontrou. (p. 99) #27 · **texto** · onde aplicar: `testes-e-provas`
- Não pôr a sua conclusão dentro do pedido de pesquisa. Se dois modelos concordam com a ideia que você já pôs no pedido, isso é eco, não confirmação. (p. 211) #47 · **texto** · onde aplicar: `orquestrando-sessoes`
- Não enviar a terceiros um relatório ou achado do agente sem conferir cada afirmação. (pp. 245–246) #57 · **texto** · onde aplicar: `orquestrando-sessoes`
- Não aceitar a explicação do agente sobre **como** verificou algo sem outra prova: a explicação é a mais provável para a pergunta, e o que ele fez por dentro é outra coisa. (p. 357) #71 · **texto** · onde aplicar: `testes-e-provas`

## 3. Decisões que são de pessoas

- Não deixar o agente decidir sozinho uma regra de negócio ou legal (interpretar uma lei, abrir uma exceção, dizer como a empresa deve funcionar). Ele fica com o trabalho repetitivo. (p. 21) #4 · **texto** · onde aplicar: `pondo-o-plano-a-prova`
- Não decidir com base num chatbot um assunto que tem um profissional responsável (médico, contador, advogado). (pp. 58–59) #15 · **texto** · onde aplicar: ainda nenhuma
- Não trocar a leitura de um contrato pelo resumo feito por IA: o resumo pode omitir a cláusula que importa. Contas com datas pedem o cálculo passo a passo, refeito numa planilha. (p. 59) #16 · **texto** · onde aplicar: ainda nenhuma
- Não acusar alguém de ter usado IA com base num "detector de texto de IA". (p. 60) #18 · **texto** · onde aplicar: ainda nenhuma
- Não pedir uma tela ou um cálculo novo para um problema de negócio sem antes descobrir, com quem usa, qual é a regra certa. Às vezes a solução é menos software. (p. 304) #67 · **texto** · onde aplicar: ainda nenhuma

## 4. Conferir o trabalho do agente

- Não tratar um "nenhuma falha de segurança encontrada" como garantia: o modelo acha alguns problemas, sem garantia nenhuma de que são todos. (p. 21) #5 · **texto** · onde aplicar: `auditoria-de-seguranca`
- Não aprovar só porque o agente disse "pronto": o "pronto" da tela e o trabalho certo são coisas diferentes, e o segundo só se vê abrindo a caixa. (p. 47) #10 · **texto + máquina** (hooks com os portões) · onde aplicar: `testes-e-provas`, `git-e-commits`
- Não olhar para o trabalho do agente só quando ele diz «sucesso»: o que ficou por dentro pode estar mal arrumado mesmo com tudo a funcionar na tela. (p. 64) #19 · **texto** · onde aplicar: ainda nenhuma
- Não deixar o agente a fazer e desfazer no mesmo lugar sem avançar. Pare e mude a pergunta. (p. 67) #20 · **texto** · onde aplicar: ainda nenhuma
- Não tratar um sistema que outras pessoas usam como "feito só pela IA". Um programador experiente revê o que importa. (p. 72) #22 · **texto** · onde aplicar: ainda nenhuma
- Não ler a falta de objeções do agente como "a ideia é boa e segura": ele quase nunca diz não. Pergunte que proteção se esqueceu de pedir. (p. 80) #24 · **texto** · onde aplicar: ainda nenhuma
- Não aceitar "os testes passam" quando os testes foram escritos pelo próprio agente junto com o código: com IA, os testes pesam mais, não menos. (p. 81) #25 · **texto** · onde aplicar: `testes-e-provas`
- Não aprovar um plano sem as perguntas incômodas: e se a operação parar a meio? E se os dados corromperem? E se a máquina de quem usa for mais fraca? E se alguém mudar milhares de arquivos de lugar? (p. 92) #26 · **texto** · onde aplicar: `pondo-o-plano-a-prova`
- Não continuar a pedir "mais um ajuste" quando cada ajuste quebra outra coisa. Pare e repense. (p. 105) #28 · **texto** · onde aplicar: `testes-e-provas`
- Não chamar solução a uma mitigação: se parar sem ter achado a causa, diga que é mitigação. (pp. 108–109) #29 · **texto + máquina** (o commit `fix` exige a causa) · onde aplicar: `testes-e-provas`, `git-e-commits`
- Não mandar um pedido importante sem dizer o que fica de fora e qual é o critério de pronto. (p. 120) #30 · **texto** · onde aplicar: `pondo-o-plano-a-prova`
- Não aprovar uma contribuição pela descrição de quem a escreveu: ela diz o que o autor julga ter feito. Audite o código. (pp. 127, 129) #31 · **texto** · onde aplicar: `orquestrando-sessoes`
- Não liberar para todos um programa que "ficou pronto rápido e os testes passam": só o tempo, quem usa e a revisão mostram se ele presta. (pp. 135–136) #33 · **máquina** (interruptor + grupo de teste) · onde aplicar: `nextjs-react`
- Não aceitar "tudo feito" sem a prova de cada exigência: na prova do autor, o modelo revia uma a uma e apontava a prova, e admitir uma falha contava mais do que inventar um sucesso. (p. 157) #37 · **texto** · onde aplicar: `testes-e-provas`
- Não aceitar uma mudança que altera um teste existente para ele passar sem perguntar porquê. O agente pega o que quebra, não o que só está errado. (pp. 160–161) #38 · **máquina** (aviso no hook) · onde aplicar: `git-e-commits`
- Não largar o volante, mas também não virar fiscal de vírgula: o equilíbrio está em testes, integração contínua, revisão e mudanças pequenas. (p. 272) #63 · **texto** · onde aplicar: ainda nenhuma
- Não aprovar o que não consegue ler, nem uma mudança cujo porquê não saberia explicar sem o agente. (pp. 280, 331) #64 #70 · **texto** · onde aplicar: ainda nenhuma

## 5. Registrar

- Não tomar uma decisão importante só na conversa. Peça para a guardar num arquivo de decisões, que o agente relê na sessão seguinte. (pp. 32–33, 36) #6 · **texto** · onde aplicar: `passando-o-trabalho`
- Não transformar cada falha numa regra logo a seguir: muitas são passageiras (uma senha vencida, a rede em baixo), e regras escritas a cada tropeço viram um monte de superstições. (p. 35) #8 · **texto** · onde aplicar: `escrevendo-regras-de-agente`
- Não pedir uma correção com "não funciona". Dê a mensagem exata, os passos para reproduzir e o que mudou antes. (p. 68) #21 · **texto** (modelo de relato) · onde aplicar: ainda nenhuma
- Não contar que o agente aprendeu com a sessão: na seguinte, acorda sem memória, e o que se aprendeu evapora se ninguém o guardar. (pp. 319, 323) #68 · **máquina** (hook de fim de sessão) · onde aplicar: `passando-o-trabalho`

## 6. Privacidade

- Não colar dados da empresa (extratos, planilhas de clientes, laudos) num chatbot sem anonimizar e sem confirmar que o plano não treina com eles. O que falta nos dados pode virar conclusão. (pp. 56, 59–60) #14 #17 · **texto** · onde aplicar: ainda nenhuma
- Não ligar um pacote de métricas ou de relatórios de erro sem ver o que ele recolhe: muitos já vêm a recolher desde que se instalam. (p. 257) #59 · **máquina** (configuração do SDK + teste) · onde aplicar: ainda nenhuma
- Não encaminhar e-mails a um serviço grátis de análise sem saber quem está do outro lado: quem o opera lê tudo o que chega. (pp. 262–263) #61 · **texto** · onde aplicar: ainda nenhuma
- Não guardar registros de sessões sem antes filtrar deles os dados sensíveis. (p. 394) #80 · **texto** · onde aplicar: ainda nenhuma

## 7. Acesso e permissões do agente

- Não deixar ao alcance do agente o que ele não deve usar (uma senha guardada em texto, a pasta das cópias de segurança, um atalho de que já ninguém se lembra): o que está ao alcance acaba por ser usado. (pp. 164–165) #40 · **máquina** (negar leitura nas permissões) · onde aplicar: `auditoria-de-seguranca`
- Não aprovar commits que acrescentam exceções ao alarme (o aviso de segurança posto na lista de exceções do próprio verificador, um `eslint-disable`, um teste saltado) sem a razão escrita. (p. 165) #41 · **máquina** (catraca) · onde aplicar: `codigo-legivel`
- Não dar ao agente credenciais de escrita em produção. Corte o acesso, não o filtre, e nunca dê a mesma credencial a todos. (pp. 205, 234) #43 #52 · **máquina** (papel só de leitura) · onde aplicar: ainda nenhuma
- Não ligar o agente a um sistema real (uma conta, um servidor, a produção) sem pesar que a responsabilidade do que ele fizer lá é de quem abriu a porta. (pp. 205–206) #44 · **máquina** (permissões por ferramenta) · onde aplicar: ainda nenhuma
- Não usar o modo que salta todas as permissões fora de uma sandbox. (pp. 228, 386) #50 #77 · **máquina** (desligar esse modo nas definições) · onde aplicar: `auditoria-de-seguranca`
- Não contar com a boa vontade do modelo quando ele instala uma biblioteca: se ela foi invadida, o código malicioso roda com as permissões dele, ou seja, as suas. (p. 228) #51 · **máquina** (pedir confirmação para `npm install`) · onde aplicar: ainda nenhuma
- Não instalar a skill de terceiros sem ler tudo. De preferência, escreva a sua. (pp. 128–129, 239) #32 #55 · **texto + máquina** · onde aplicar: `escrevendo-regras-de-agente`
- Não instalar um gateway que recebe mensagens de fora e roda comandos quando o ritmo de mudanças não deixa ver quem revisa: foi a decisão do autor. (pp. 237–239) #54 · **máquina** (lista permitida) · onde aplicar: ainda nenhuma
- Não dar a um agente que leu texto alheio mais mãos do que daria a quem escreveu esse texto: uma instrução lida pode sobreviver à compactação como se fosse ordem sua. (pp. 240–241) #56 · **texto** · onde aplicar: ainda nenhuma
- Não tratar um aplicativo baixado de um site espelho como igual ao da loja oficial: há uma chance, pequena, de ter sido adulterado no caminho. (p. 252) #58 · **texto** · onde aplicar: ainda nenhuma
- Não autorizar um aplicativo de terceiros nas contas da empresa a partir de um link recebido, mesmo que a tela de autorização seja a verdadeira. (p. 261) #60 · **máquina** (lista permitida na consola) · onde aplicar: ainda nenhuma
- Não rodar o agente com acesso à pasta pessoal inteira e às credenciais do usuário. No Windows, considere o WSL2 ou a sandbox do agente. (pp. 381–382) #73 · **máquina** · onde aplicar: ainda nenhuma
- Não aprovar "sim a tudo" por cansaço. Organize as permissões em três colunas: pode sem perguntar, pergunta antes, nunca. (p. 385) #76 · **máquina** · onde aplicar: `auditoria-de-seguranca`
- Não deixar o agente ler o `.env`: dentro da jaula, ele vê os segredos do projeto a menos que se escondam. A configuração vinda do próprio projeto só pode apertar a jaula, nunca afrouxar, salvo se a pasta for marcada como confiável. (p. 389) #79 · **máquina + texto** · onde aplicar: `auditoria-de-seguranca`

## 8. Dados, lotes e backups

- Não dar por pronto um trabalho em lote sem abrir o resultado final: na dublagem contada na página, os defeitos só apareceram ao escutar os arquivos. (p. 181) #42 · **texto** · onde aplicar: ainda nenhuma
- Não autorizar uma operação destrutiva em lote sem ver antes a contagem do que será protegido e do que será apagado. Uma lista de proteção vazia é um alarme. (pp. 222, 224) #49 · **máquina** (o script exige o número esperado) · onde aplicar: `sql-postgres`
- Não apagar a origem antes de conferir a cópia no destino. (pp. 235–236) #53 · **texto** · onde aplicar: ainda nenhuma
- Não trocar de uma vez um formato de dados que já roda em produção: acrescente o novo sem tirar o velho, espere todos migrarem, e só então remova. (p. 293) #66 · **máquina** (aviso em `DROP`) · onde aplicar: ainda nenhuma
- Não trabalhar com agentes no Windows sem backup externo automático da pasta de trabalho. (pp. 383–384) #74 · **máquina** · onde aplicar: ainda nenhuma
- Não confiar num backup que nunca foi restaurado. Abra alguns arquivos da cópia todo mês. (p. 385) #75 · **máquina** (tarefa recorrente) · onde aplicar: ainda nenhuma
- Não restaurar a partir de um arquivo só porque se chama "último". Confira o hash, o passo exato e o estado guardado: o "último" pode ter voltado no tempo. (p. 423) #83 · **máquina** · onde aplicar: ainda nenhuma

## 9. Dinheiro, custos e fraude

- Não passar a pagar por pedido (API) quando o plano bate no limite, só para continuar. Espalhe o trabalho por dias. (pp. 70–71) #23 · **máquina** (teto de gasto) · onde aplicar: ainda nenhuma
- Não deixar um trabalho em lote a correr sem olhar a cota: no caso contado, o trabalho levou o plano ao teto, e houve uso extra pago além da mensalidade. (pp. 146–147) #35 · **máquina** (configuração da conta) · onde aplicar: ainda nenhuma
- Não mudar dados bancários nem autorizar uma transferência com base só num e-mail, mensagem, áudio ou vídeo. Confirme por um canal que você já conhecia. (p. 264) #62 · **máquina** (segundo aprovador) · onde aplicar: ainda nenhuma

## 10. Aprender e enviar

- Não pedir a solução pronta quando o objetivo é aprender. Tente sozinho primeiro e peça uma pista. (p. 363) #72 · **texto** · onde aplicar: ainda nenhuma
- Não publicar o rascunho só porque ele impressiona: os primeiros esboços dizem pouco sobre o resto, e o trabalho está na leitura, no corte e na correção que vêm depois. A versão fácil recusa-se. (pp. 343–344) · **texto** · onde aplicar: ainda nenhuma
- Não aprovar um push sem ver a lista de arquivos de todos os commits por enviar, incluindo os removidos depois. (p. 386) #78 · **máquina** (`pre-push` com scanner de segredos) · onde aplicar: `auditoria-de-seguranca`, `git-e-commits`
