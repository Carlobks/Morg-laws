# Segurança com agentes

Resumo com palavras nossas de *Competente o Suficiente*, de Fabio Akita. A página é a impressa. A barreira diz como impor o item: **texto** (regra escrita) ou **máquina** (permissão, hook, teste, CI, configuração). «Onde aplicar» diz que skill do Morg-laws já o aplica, ou «ainda nenhuma». O que o livro diz em forma de proibição está no [nao-faca.md](nao-faca.md) e não se repete aqui.

## 1. Acesso e isolamento

- Lembre-se de que o agente trabalha com as permissões de quem o abriu: tudo o que a sua conta apaga, ele também apaga. (p. 227) · **máquina** (permissões do agente) · onde aplicar: `auditoria-de-seguranca`
- Para cada comando que podia causar uma perda sem volta, pergunte porque ele é possível e retire esse poder. A meta é que o pior engano do agente custe, no máximo, uma tarde. (pp. 229, 236) · **máquina** · onde aplicar: ainda nenhuma
- Mantenha os agentes longe da produção: nada de senha do banco, chave de administrador ou acesso aos servidores. Num ambiente de testes, o agente escreve as mudanças como receitas versionadas; uma pessoa revê e promove. (pp. 234–235, 386–387) · **máquina** (papel só de leitura) · onde aplicar: `sql-postgres`
- Rode o agente numa jaula: só a pasta do projeto pode ser escrita; chaves de servidores, credenciais de nuvem e perfis do navegador ficam de fora; a rede fica desligada ou filtrada; nada de atalhos para serviços que rodam como administrador (o Docker é um deles). Para código suspeito, uma máquina virtual descartável. (pp. 229–231, 381–382, 388–389) · **máquina** · onde aplicar: ainda nenhuma
- Leia o que a sua proteção promete de verdade: uma «proteção contra acidentes» não é uma fronteira de segurança. Cada camada precisa de quem a audite, senão é só enfeite. (pp. 230–231) · **texto** · onde aplicar: `auditoria-de-seguranca`
- Use o Git como rede de segurança: commits pequenos e frequentes, uma cópia remota, e o envio sempre na mão de uma pessoa. (pp. 230, 382) · **máquina** (hooks e `pre-push`) · onde aplicar: `git-e-commits`

## 2. Segredos e o que se publica

- Guarde senhas e chaves num gestor de senhas. Se uma vazar, troque-a: limpar o histórico do repositório não chega. (p. 386) · **texto** · onde aplicar: ainda nenhuma
- Antes de publicar um pacote ou um deploy, confira o que vai dentro e ponha uma verificação automática curta no caminho. Um mapa de código-fonte esquecido já expôs o código inteiro de uma ferramenta conhecida. (pp. 28–29, 39) · **máquina** (verificação no CI) · onde aplicar: ainda nenhuma
- Procure no código publicado os atalhos de teste esquecidos e os segredos que entram por variáveis de ambiente. Tudo o que chega ao navegador ou ao aplicativo do cliente pode ser lido. (pp. 232, 253) · **máquina** · onde aplicar: `auditoria-de-seguranca`, `nextjs-react`
- Não conte com esconder como forma de proteger: o que está escondido acaba por ser achado. (pp. 244–245) · **texto** · onde aplicar: ainda nenhuma
- Rode no CI uma bateria fixa: estilo, dependências com falhas conhecidas, análise estática de segurança e os testes. (pp. 408–409) · **máquina** (CI) · onde aplicar: `auditoria-de-seguranca`

## 3. Injeção de instruções e conteúdo de fora

- Trate tudo o que o agente lê (páginas, e-mails, PDFs, projetos baixados, mensagens) como entrada de um estranho: pode trazer ordens escondidas. (pp. 239–240) · **texto** · onde aplicar: ainda nenhuma
- Reduza o risco da injeção: marque o conteúdo de fora como tal, tire os caracteres invisíveis, limite o tamanho, dê só as ferramentas daquela tarefa e peça aprovação humana antes de apagar ou de mandar dados para fora. As duas últimas protegem mesmo quando o modelo obedece à ordem escondida. (pp. 240–241, 251) · **máquina** (aprovação nas permissões) · onde aplicar: ainda nenhuma
- Conte que, mais cedo ou mais tarde, chegarão ao agente ordens escondidas no que ele lê (mensagens, sites, e-mails): limite-o ao acesso que o trabalho exige e prefira ferramentas que confirmam com você antes de apagar ou enviar. (p. 251) · **texto** · onde aplicar: ainda nenhuma

## 4. Software de terceiros

- Faça o inventário dos componentes de terceiros (SDKs, bibliotecas): é por eles que entram a recolha de dados e boa parte do risco. (p. 258) · **máquina** (lista de dependências conferida) · onde aplicar: `auditoria-de-seguranca`
- Cumpra a licença do que usa ou adapta: mantenha os avisos de autoria e diga de onde veio. (pp. 169–170) · **texto** · onde aplicar: ainda nenhuma

## 5. Auditar e endurecer

- Pensar como um invasor não é coisa que o agente faça sozinho: peça o endurecimento por escrito e confira-o. Exemplos: comandos negados de início, com poucos liberados por nome; assinatura conferida em cada mensagem de um serviço externo, com proteção contra repetição; dados cifrados no disco; o dono aprova antes de apagar ou alterar. (pp. 242–243, 262) · **texto** · onde aplicar: `auditoria-de-seguranca`
- Peça auditorias com perguntas concretas, não um «revê a segurança». Por exemplo: um segredo com valor padrão no código, um código de segundo fator que se pode reutilizar, o destino do redirecionamento depois do login, dois pedidos ao mesmo contador ao mesmo tempo. (pp. 89–90) · **texto** · onde aplicar: `auditoria-de-seguranca`
- O agente só encontra as falhas que você sabe mandar procurar. Use listas de falhas reais já catalogadas: dados de um cliente vistos por outro, injeção em consultas, biblioteca vulnerável, teste adulterado, soma errada. (pp. 21, 69, 158) · **texto** · onde aplicar: `auditoria-de-seguranca`
- Faça duas auditorias independentes, a segunda sem ler a primeira, de preferência com agentes de fabricantes diferentes, e corrija a soma das duas listas. Procure também você. Uma auditoria feita por IA e não conferida é um sinal, não a lista certa. (pp. 81, 156, 232, 239) · **texto** · onde aplicar: `orquestrando-sessoes`
- Procure por conta própria os erros silenciosos: o agente apanha o que quebra, mas deixa passar o que só está errado. (pp. 160–161) · **texto** · onde aplicar: `testes-e-provas`
- Um sistema muito bom pode ter um ponto cego que só aparece quando alguém o procura de propósito. (p. 219) · **texto** · onde aplicar: ainda nenhuma
- Retire as funcionalidades que ninguém usa: cada uma a menos é uma porta a menos. (pp. 241–242) · **texto** · onde aplicar: ainda nenhuma
- A barreira de entrada caiu para todos: a mesma IA que ajuda você ajuda quem procura brechas no seu sistema. (p. 266) · **texto** · onde aplicar: ainda nenhuma

## 6. Dados pessoais

- Cifre no banco os dados pessoais sensíveis e não instale rastreadores. (p. 81) · **máquina** · onde aplicar: ainda nenhuma
- Para dados que não podem sair de casa, pense num modelo que roda localmente. (p. 91) · **texto** · onde aplicar: ainda nenhuma
- Saiba o que é a impressão digital de um aparelho e quanto um aplicativo pode recolher além do que precisa. Os SDKs de métricas e de erros costumam vir com a recolha ligada por padrão. (pp. 254–257) · **texto** · onde aplicar: ainda nenhuma
- Imagens de pessoas reais nunca são geradas por IA. Registre a origem, a licença e a autorização de cada foto. (pp. 336, 456–458) · **texto** · onde aplicar: ainda nenhuma
- Separe o que um código consegue fazer do que ele faz: ter a função que lê um dado não prova quando nem para quem ele o envia. (pp. 258–259) · **texto** · onde aplicar: ainda nenhuma

## 7. Golpes

- O golpe de hoje chega num português impecável e com um elogio feito à medida; cai-se por vaidade, medo ou pressa. Diante dele, desacelere. (pp. 260–262, 264) · **texto** · onde aplicar: ainda nenhuma
- Revogue as autorizações que já deu a aplicativos nas suas contas e que já não usa. (pp. 261, 264) · **texto** · onde aplicar: ainda nenhuma
- Combine uma palavra-código para emergências: um vídeo ou um áudio já não provam quem fala. (pp. 264–265) · **texto** · onde aplicar: ainda nenhuma
- Desconfie de quem aparece sem ser chamado a pedir uma reunião, um pagamento ou dados: trate-o como golpe até ter a confirmação. (pp. 262–263) · **texto** · onde aplicar: ainda nenhuma
- Uma marca d'água de texto de IA é um rótulo fraco: some numa reescrita. Não serve de prova em nenhum sentido. (pp. 405–407) · **texto** · onde aplicar: ainda nenhuma

## 8. IA dentro do sistema

- Deixe no código as regras que se podem escrever (limites, gravidade, permissões). O modelo só serve para transformar texto livre em fatos. (pp. 182, 421–422) · **texto** · onde aplicar: ainda nenhuma
- Trate a resposta de um modelo como a entrada de um usuário que não conhece: confira, limite, normalize e avise quando falta um dado. (pp. 98–99) · **texto** · onde aplicar: ainda nenhuma
- Não confie na «certeza» que o modelo declara nem numa trava do fornecedor que pode mandar o pedido para outro modelo sem aviso. (pp. 182, 199–200, 212–213) · **texto** · onde aplicar: ainda nenhuma
