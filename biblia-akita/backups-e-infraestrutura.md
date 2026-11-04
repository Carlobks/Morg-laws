# Backups e infraestrutura

Resumo com palavras nossas de *Competente o Suficiente*, de Fabio Akita. A página é a impressa. A barreira diz como impor o item: **texto** (regra escrita) ou **máquina** (permissão, hook, teste, CI, configuração). «Onde aplicar» diz que skill do Morg-laws já o aplica, ou «ainda nenhuma». O que o livro diz em forma de proibição está no [nao-faca.md](nao-faca.md) e não se repete aqui.

## 1. Backup e restauro

- O backup entra no primeiro dia em que o sistema vai para produção, não depois. (p. 87) · **texto** · onde aplicar: ainda nenhuma
- Tenha snapshots automáticos do disco, no mínimo a cada hora, com um prazo de retenção definido, e aprenda a recuperar um antes de precisar. Antes de uma sessão arriscada, tire um à mão. No Windows, as cópias de sombra são fracas para isto. (pp. 223, 232–234, 382–383) · **máquina** (tarefa agendada) · onde aplicar: ainda nenhuma
- O backup externo precisa de quatro coisas: rodar sozinho, guardar várias versões com uma regra de retenção (por exemplo, 7 diárias, 4 semanais, 6 mensais e 1 anual), estar cifrado e ser testado abrindo arquivos recuperados. E fica onde o agente que mexe no original não chega. (pp. 234, 384) · **máquina** · onde aplicar: ainda nenhuma
- Guarde pelo menos uma cópia noutro lugar físico. Discos em espelho ou com paridade salvam de um disco com defeito, não da perda do aparelho, e a reconstrução pode levar um segundo disco. (pp. 224–225, 234) · **texto** · onde aplicar: ainda nenhuma
- Confira o backup contra uma lista feita a partir da origem, nunca contra o relatório da própria ferramenta de cópia: ela pode pular pastas sem permissão ou arquivos que não reconhece e mesmo assim dizer que deu tudo certo. (pp. 225–226) · **máquina** · onde aplicar: ainda nenhuma
- A conferência não pode usar os mesmos filtros da cópia: o que o filtro esconde da cópia também o esconde da conferência. (p. 226) · **máquina** · onde aplicar: ainda nenhuma
- Que o arquivo exista não prova que está inteiro: compare o tamanho e o conteúdo. (pp. 223–224) · **máquina** (hash) · onde aplicar: ainda nenhuma
- Só desligue o sistema antigo depois de cada parte estar provada no novo. (pp. 226, 236) · **texto** · onde aplicar: ainda nenhuma
- Hábitos para toda a equipe: fazer uma cópia noutro lugar antes de deixar um programa «arrumar» arquivos em massa, saber se o serviço guarda versões e por quanto tempo, e manter o backup longe do original. (pp. 235–236) · **texto** · onde aplicar: ainda nenhuma
- A produção pede backup testado, restauro ensaiado e monitorização. Nada vai para produção sem um caminho de volta conhecido. (p. 235) · **texto** · onde aplicar: ainda nenhuma

## 2. Operações destrutivas e tarefas automáticas

- Ponha uma porta trancada entre planejar e executar: a execução só começa depois de o plano ser aprovado, e nada se apaga da origem. (p. 119) · **máquina** (o script só executa com o plano aprovado) · onde aplicar: ainda nenhuma
- Peça o trabalho longo em etapas numeradas, que se podem repetir e que gravam o progresso. Toda tarefa automática tem de poder rodar duas vezes sem estragar nada. (pp. 99, 119) · **texto** · onde aplicar: ainda nenhuma
- Nunca deixe um erro passar calado: registre o detalhe técnico e avise onde já se olha todos os dias. Muitas vezes a verificação que faltava só nasce depois da falha que ninguém tinha previsto. (pp. 77, 83) · **máquina** (alerta) · onde aplicar: ainda nenhuma
- Ponha uma conferência entre cada etapa de uma cadeia automática: dez etapas que acertam 90% cada uma acertam juntas só cerca de 35%. (p. 209) · **máquina** · onde aplicar: ainda nenhuma
- Decida você o que o sistema faz quando um serviço externo falha, por exemplo cortar as chamadas por um tempo em vez de repetir sem fim. (pp. 94–95) · **texto** · onde aplicar: ainda nenhuma
- Peça a outro agente, ou a outra pessoa, que execute e confira o procedimento que o primeiro escreveu. Ajuste as travas aos dados reais: uma trava exagerada recusa também o que é legítimo. (pp. 223–224) · **texto** · onde aplicar: `orquestrando-sessoes`
- Confira o estado na origem (contar processos, contar linhas), e não pela ferramenta, que pode estar enganada. (p. 226) · **texto** · onde aplicar: `testes-e-provas`, `sql-postgres`
- Garanta que os alertas de saúde dos discos e servidores chegam antes do desastre; comprar na urgência sai mais caro. (p. 225) · **máquina** (alerta) · onde aplicar: ainda nenhuma

## 3. Entregar sem medo

- Antes de acelerar as entregas, monte as travas: testes de lógica e de integração, CI, revisão automática desconfiada, interruptores por funcionalidade, um ambiente de testes, voltar atrás em minutos e monitorização. (p. 292) · **máquina** · onde aplicar: ainda nenhuma
- Garanta que sabe mesmo desfazer uma entrega. O ritmo certo de entregas mede-se pelo preço de um engano no seu ramo. (p. 294) · **texto** · onde aplicar: ainda nenhuma
- Padronize o deploy, as versões e os scripts, para que «faz o deploy» não deixe nada por adivinhar. (p. 127) · **máquina** (script único) · onde aplicar: ainda nenhuma
- Até as ferramentas pequenas (scripts de backup, utilitários) levam testes, versão e configuração no lugar certo. (p. 143) · **máquina** (testes) · onde aplicar: `codigo-legivel`

## 4. Fornecedores e continuidade

- Prepare-se para o dia em que o fornecedor de IA desligar o modelo para todos, e tenha um plano para quando ele recusar um pedido pela política de conteúdo. (pp. 147–148, 200) · **texto** · onde aplicar: ainda nenhuma
- Não ponha tudo numa aposta só: quando uma bolha estoura, as empresas que viviam dela desaparecem e a tecnologia fica. (pp. 24, 365–368) · **texto** · onde aplicar: ainda nenhuma
- Trate os dados da empresa como o patrimônio que o código deixou de ser. (pp. 139–140) · **texto** · onde aplicar: ainda nenhuma
- Pague por um serviço quando ele poupa horas de operação. Compare o tempo, o trabalho de manter e o custo por unidade. (p. 180) · **texto** · onde aplicar: ainda nenhuma
- Só compre hardware para IA local se a máquina já existir ou se os dados não puderem sair. A conta é a memória (o que cabe) vezes a largura de banda (a velocidade), somando os pesos do modelo e a memória da conversa. (pp. 175–176, 183, 417–420) · **texto** · onde aplicar: ainda nenhuma
