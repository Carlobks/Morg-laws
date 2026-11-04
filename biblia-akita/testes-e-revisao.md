# Testes, verificação e revisão

Resumo com palavras nossas de *Competente o Suficiente*, de Fabio Akita. A página é a impressa. A barreira diz como impor o item: **texto** (regra escrita) ou **máquina** (permissão, hook, teste, CI, configuração). «Onde aplicar» diz que skill do Morg-laws já o aplica, ou «ainda nenhuma». O que o livro diz em forma de proibição está no [nao-faca.md](nao-faca.md) e não se repete aqui.

## 1. Um juiz de fora

- Dê ao agente algo de fora que diga se acertou: um teste, uma medida da realidade, uma comparação lado a lado com uma referência. Sem isso, o ciclo de tentar e corrigir gira sem chegar a lado nenhum. Dê-lhe também os meios de executar e de medir. (pp. 43, 50, 112–114) · **máquina** (testes) · onde aplicar: `testes-e-provas`
- A fonte primária decide, não a maioria dos modelos. Antes de dizer que alguém inventou uma coisa, vá à fonte. (pp. 57, 150–151) · **texto** · onde aplicar: `orquestrando-sessoes`
- Meça onde está o custo em vez de o adivinhar. (p. 114) · **texto** · onde aplicar: `testes-e-provas`

## 2. Testes que enganam

- Contar testes diz pouco: veja o que cada um verifica. Um teste verde é o programa falando bem de si mesmo. (p. 153) · **texto** · onde aplicar: `testes-e-provas`
- Pergunte quem escreveu a verificação: um substituto falso criado pelo próprio modelo pode aprovar um comando que nem existe. (pp. 165–167) · **texto** · onde aplicar: `testes-e-provas`
- Os dublês de teste enganam: teste também o sistema inteiro ligado, com serviços e dados que tenham as manias do mundo real (letras de outros alfabetos, nomes que colidem, formatos locais de data e número, limites dos serviços de terceiros). (pp. 81–82, 93–94, 409) · **máquina** (testes de integração) · onde aplicar: ainda nenhuma
- Use controles negativos: um programa vazio tem de reprovar, sair «com sucesso» sem acabar não conta, e uma edição vazia não é uma correção. (pp. 423–424) · **máquina** · onde aplicar: `testes-e-provas`
- Guarde do agente uma parte dos testes de aceitação. Separe os exemplos da prova por unidade inteira, e mantenha a prova final fechada. (pp. 186, 188, 432) · **máquina** · onde aplicar: ainda nenhuma
- Para as regras críticas, escreva propriedades que valem sempre e verifique-as, incluindo as que atravessam várias operações seguidas: é aí que até os bons modelos tropeçam. (pp. 430–433) · **máquina** (testes de propriedade) · onde aplicar: ainda nenhuma
- Diga ao modelo a data de hoje e o que ele não sabe. (pp. 97–98) · **texto** · onde aplicar: ainda nenhuma
- Um modelo pode dizer que os testes passaram sem tê-los rodado. «Parece certo» e «está certo» são degraus diferentes: num caso medido, quase todas as respostas erradas pareciam perfeitas. (pp. 191–193) · **máquina** (o CI roda os testes) · onde aplicar: `testes-e-provas`
- Uma métrica que vira prêmio acaba contornada, por pessoas ou por modelos. (p. 164) · **texto** · onde aplicar: ainda nenhuma

## 3. Conferir a entrega

- Confira qual modelo e qual ferramenta fizeram de fato o trabalho. (pp. 40–41, 165) · **texto** · onde aplicar: ainda nenhuma
- Teste o objetivo final e não só a etapa. Não marque como terminado antes de usar de verdade; o que só aparece na tela confere-se na tela, e avalia-se o percurso inteiro de quem usa. (pp. 90, 191–192, 304, 424) · **texto** · onde aplicar: `testes-e-provas`

## 4. Revisão

- Use mais de um revisor, com modelos e ferramentas diferentes. Uma segunda revisão às cegas acha o que a primeira deixou escapar. (pp. 49, 156) · **texto** · onde aplicar: `orquestrando-sessoes`
- Numa contribuição de fora, audite o código. A IA pode fazer a triagem; a decisão é de uma pessoa, e nenhum código fica isento de revisão. (pp. 127, 247–248) · **texto** · onde aplicar: `orquestrando-sessoes`
- Depois de entrar um lote de mudanças, faça uma segunda auditoria do que se mexeu nesse dia (regressões, código duplicado, código morto) e use-o de verdade. (p. 248) · **texto** · onde aplicar: ainda nenhuma
- Audite a sua própria auditoria, e desconfie dos seus testes quando o resultado sai mau. (pp. 48, 416) · **texto** · onde aplicar: `testes-e-provas`
- Avalie as entregas por faixas, não com uma nota exata: pronta, falta uma ou duas horas, precisa de retrabalho, vai para o lixo. (pp. 152–153) · **texto** · onde aplicar: ainda nenhuma
- Contra o código feito com pressa pela IA, o único remédio é rever à mão cada pacote de mudanças. A rapidez com que foi escrito não diz nada da qualidade. (pp. 135–136) · **texto** · onde aplicar: ainda nenhuma

## 5. O processo de testes

- Comece pelo teste, prenda cada bug com um teste, só junte à linha principal com tudo verde e feche uma brecha de segurança no mesmo commit que a corrige. (pp. 80–81) · **máquina** (hooks e CI) · onde aplicar: `testes-e-provas`, `git-e-commits`
- Antes de uma troca grande, tenha testes. Refatore pouco e muitas vezes, protegido pelos testes que já existem. (pp. 67, 84–85) · **texto** · onde aplicar: `codigo-legivel`
- Os testes rodam com um só comando, sem configuração à mão e com uma saída previsível. (pp. 125–126) · **máquina** · onde aplicar: `codigo-legivel`
- Em sistemas de dinheiro ou regulados, os cenários de teste são mais pesados e há mais de uma trava para cada forma de falhar: voltar o código atrás não devolve um pagamento. (pp. 292–293) · **texto** · onde aplicar: ainda nenhuma
- Antes de ir para produção, alguém responde: pode ir? aguenta a carga? é seguro? é fácil de manter? conversa com o resto? resolve o problema certo? (pp. 282–283) · **texto** · onde aplicar: ainda nenhuma
- Quem usa de verdade é a revisão mais forte, desde que a mudança chegue pequena, atrás de um interruptor e com volta. Um projeto que ninguém usa está morto. (pp. 133–134, 294) · **máquina** (interruptor) · onde aplicar: `nextjs-react`
- Ao depurar: reproduza em todas as tentativas antes de testar correções, procure pelo histórico o commit que estragou (dividindo ao meio), espalhe medições para conhecer o terreno, liste os suspeitos e o que mudou, e isole uma variável de cada vez antes de concluir. (pp. 67, 108–110, 171–172, 410–411) · **texto** · onde aplicar: `testes-e-provas`
- Operações sobre caracteres (contar letras, trocar acentos) fazem-se com uma ferramenta, não de cabeça. (p. 349) · **texto** · onde aplicar: ainda nenhuma
- Para conferir um documento: leitores simulados com perfis reais (que leem, não que editam) e regras para juntar as críticas; rodadas até os problemas deixarem de voltar; outro modelo, de um fabricante diferente, checando cada frase na origem; e retirar o que ainda não foi verificado. (pp. 300, 336–337, 344, 407–408) · **texto** · onde aplicar: ainda nenhuma
- Os bugs não foram inventados pela IA, e nenhum verificador geral prova que um programa não tem bugs. (pp. 246, 427) · **texto** · onde aplicar: ainda nenhuma
