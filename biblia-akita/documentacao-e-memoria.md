# Documentação e memória

Resumo com palavras nossas de *Competente o Suficiente*, de Fabio Akita. A página é a impressa. A barreira diz como impor o item: **texto** (regra escrita) ou **máquina** (permissão, hook, teste, CI, configuração). «Onde aplicar» diz que skill do Morg-laws já o aplica, ou «ainda nenhuma». O que o livro diz em forma de proibição está no [nao-faca.md](nao-faca.md) e não se repete aqui. A linha do tempo datada dos fatos do ano está no próprio livro (pp. 369–379).

## 1. O que o agente lembra

- O modelo é um arquivo fechado: nada da conversa fica nele. O que precisa ser lembrado guarda-se fora, e deixar o agente trabalhando sozinho não o faz aprender o seu domínio. (pp. 19, 319) · **texto** · onde aplicar: `passando-o-trabalho`
- A cada mensagem, o modelo volta a ler o contexto inteiro. Esse espaço tem tamanho fixo, e enchê-lo custa dinheiro, tempo e precisão: o meio é o que mais se perde. (pp. 19, 29–31) · **texto** · onde aplicar: `passando-o-trabalho`
- Na compactação, o início da conversa encolhe para quase nada. Em vez de perguntar ao agente porque se decidiu algo, pergunte onde a decisão está escrita. (pp. 31–33) · **texto** · onde aplicar: `passando-o-trabalho`
- O agente pode ter lido só uma parte de um arquivo (as leituras vêm em fatias e as saídas grandes são cortadas sem aviso) e responder como se tivesse lido tudo. (pp. 33, 124) · **texto** · onde aplicar: ainda nenhuma

## 2. Onde guardar

- Use três gavetas: as regras do projeto (o arquivo de instruções), as decisões e pesquisas (documentos no git) e o meio do caminho (uma passagem de turno no fim de cada sessão: onde parou, o que deu errado e o que ainda falta). (p. 387) · **texto** · onde aplicar: `passando-o-trabalho`, `escrevendo-regras-de-agente`
- A memória do agente é uma pista: confira no projeto antes de agir. Uma memória errada faz mais mal do que nenhuma. (pp. 34–35, 395) · **texto** · onde aplicar: ainda nenhuma
- Peça ao agente que registre por escrito o trabalho que ficou fora do código: a pesquisa, a decisão e o porquê, a alternativa descartada, a experiência que falhou, o defeito que vai e volta. O conhecimento escrito acumula de sessão para sessão. (pp. 130, 323) · **texto** · onde aplicar: `passando-o-trabalho`, `escrevendo-regras-de-agente`
- Mantenha os documentos numa pasta, em arquivos curtos, um por assunto (arquitetura, decisões, armadilhas). Uma alternativa é um wiki mantido pelo modelo: uma página por conceito, com ligações, contradições assinaladas e revisão de tempos em tempos. (pp. 36–37) · **texto** · onde aplicar: ainda nenhuma
- Guarde a memória em arquivos seus, num formato aberto (Markdown no git, que se lê em qualquer editor ou com `grep`), para que resista quando você mudar de agente, de computador ou de fornecedor. Para mudar de agente, escreva um documento de estado. Não seja você a memória do agente. (pp. 36, 323–324, 392–397) · **texto** · onde aplicar: `passando-o-trabalho`
- Leia e limpe o que a memória das ferramentas guardou. Desligue, por padrão, as funções que reescrevem ou apagam memória sozinhas, e guarde o histórico. Se automatizar, ponha limites (tempo, número de sessões, uma trava) e dê permissão só sobre as próprias notas. (pp. 36, 39, 395, 402–403) · **máquina** (configuração da ferramenta) · onde aplicar: ainda nenhuma
- A memória automática compensa para quem troca de agente, trabalha em várias máquinas, volta a projetos semanas depois ou trabalha em equipe. Fora disso, compactar bem e cuidar de uma pasta de documentos chega. A transcrição bruta é prova; o documento é o conhecimento já arrumado. (p. 396) · **texto** · onde aplicar: ainda nenhuma
- Prefira a busca por palavras e uma janela de contexto grande a um banco vetorial. O vetorial só se justifica com acervos enormes, vocabulário muito diferente entre perguntas e textos, imagem ou áudio, resposta instantânea ou necessidade de auditar o trecho usado; o mais robusto é combinar os dois. (pp. 37–38, 403–405) · **texto** · onde aplicar: ainda nenhuma

## 3. Como escrever

- Escreva datas completas («em março de 2026») e nunca «recentemente»; ponha a data ao lado de cada número. (pp. 7, 9) · **texto** · onde aplicar: ainda nenhuma
- Quando um documento estiver errado, marque-o como obsoleto no topo e mantenha-o; o caminho errado documenta-se como errado. Corrija todas as cópias de um mesmo erro. (pp. 5, 151, 414, 416) · **texto** · onde aplicar: ainda nenhuma
- Diga até onde vai o que provou (o alcance e os limites do teste) e as camadas de incerteza de uma análise feita com IA. Separe fato de opinião, com uma etiqueta em cada um. (pp. 172, 252, 276–277) · **texto** · onde aplicar: `testes-e-provas`
- Escreva o que faria mudar a sua conclusão, em critérios que alguém de fora consiga medir. (pp. 322–323) · **texto** · onde aplicar: ainda nenhuma
- Feche cada projeto com um relatório (decisões, medidas, erros) e publique de tempos em tempos um boletim da estabilidade de cada sistema. Seja honesto sobre o que é de fato mantido. (pp. 132–133, 185, 338) · **texto** · onde aplicar: ainda nenhuma
- Trate um documento importante como um produto: a especificação num lugar só, um verificador automático (referência para nada, o mesmo número diferente em dois lugares, trecho sem origem, frases proibidas), revisões, versões, registro de mudanças e um canal para relatar erros. (pp. 335, 343–344) · **máquina** (verificador no CI) · onde aplicar: ainda nenhuma
- Para reorganizar um acervo com agentes: um inventário selado (com um código do conteúdo de cada arquivo), um formulário fixo por documento, um mapa do que substituiu o quê, um piloto cujas lições viram regras escritas, o registro das contradições entre agentes e a origem marcada em cada trecho. (pp. 333–336) · **texto** · onde aplicar: ainda nenhuma
- Quando dois números seus não batem, descubra porquê e diga o que cada um conta. Quando o resumo e a fonte discordam, vale a fonte. (pp. 336, 344) · **texto** · onde aplicar: `testes-e-provas`
- Diga onde usou IA e assine só o que dirigiu e conferiu. Marque as imagens geradas por IA. (pp. 10, 305–306, 336) · **texto** · onde aplicar: ainda nenhuma
- Registre a origem e a licença dos dados e acervos de terceiros que usa. (p. 218) · **texto** · onde aplicar: `escrevendo-regras-de-agente`
- Desconfie da informação espalhada, sem data ou contraditória, incluindo as suas próprias notas antigas. (p. 410) · **texto** · onde aplicar: ainda nenhuma
