# Código morto: como achá-lo sempre do mesmo jeito, e o que a ferramenta não vê

Data: 2026-11-03 e 2026-11-04 (as medições). A documentação do knip foi lida em 2026-11-06.

## Pergunta

Quando uma funcionalidade nova abre para todos, o ramo antigo e o interruptor que escolhia entre os dois devem
sair. Como achar, de forma repetível, o código que ficou para trás (arquivos que ninguém importa, exports sem uso,
pacotes parados), sem confiar só na ferramenta e sem tocar no projeto antes de saber o que morre em cadeia?

## Fontes

Lidas em 2026-11-06. As páginas não dizem a que versão do knip se referem; nesse dia, a versão publicada no npm era
a 6.44.1, de 2026-10-31 (`npm view knip version`).

- **knip — página inicial** — https://knip.dev — Entrada no `FONTES.md`.
- **knip — modo de produção** — https://knip.dev/features/production-mode — Entrada no `FONTES.md`.
- **knip — plugins** — https://knip.dev/explanations/plugins — Entrada no `FONTES.md`.
- **knip — arquivos de entrada** — https://knip.dev/explanations/entry-files — Entrada no `FONTES.md`.
- **knip — plugin do Next.js** — https://knip.dev/reference/plugins/next — Entrada no `FONTES.md`.
- **knip — configuração** — https://knip.dev/reference/configuration — Entrada no `FONTES.md`.
- **knip — tratar os achados** — https://knip.dev/guides/handling-issues — Entrada no `FONTES.md`.
- **knip — problemas conhecidos** — https://knip.dev/reference/known-issues — Entrada no `FONTES.md`.

## O que se mediu

As medições foram feitas num projeto Next.js real (App Router, vitest e testes de ponta a ponta), com o **knip
5.88.1**. Os números do projeto não entram aqui: só o método e o que vale fora dele.

**Avaliar a ferramenta antes de a instalar.**

- Instalar o pacote numa pasta isolada e procurar no código dele chamadas de rede e telemetria (`fetch`, `http`,
  `https`). No 5.88.1 não havia nenhuma.
- Fixar a versão exata (`npm i -D -E`), com a impressão digital no lockfile.
- Rodar o `npm audit` depois (e antes, para comparar), e conferir se algum aviso cai num pacote da ferramenta.
- Ler o diff do lockfile: a instalação também mudou de lado dependências opcionais que já existiam (subiram de
  versão sem ninguém pedir).

**O risco do `.env`.** O knip **executa** os arquivos de configuração do projeto para ler o que eles exportam: a
página dos plugins diz que os carrega «dinamicamente», e a do plugin do Next.js diz que carrega o `next.config`. No
projeto medido, um desses arquivos (o da ferramenta de testes de ponta a ponta) carregava o `.env` com o dotenv.
Resultado: as variáveis de ambiente, com as chaves, ficavam na memória do processo do knip. Conferiu-se que o
pacote não tem código de rede e que não escreveu nada no projeto (`git status` limpo); o `.env` não foi aberto.
A página dos problemas conhecidos trata a variável que falta como um erro de carga e sugere carregar o `.env` para o
knip: a escolha de não o fazer é do projeto, não da ferramenta. O risco vale para qualquer ferramenta que «só lê»
mas carrega as configurações.

**A afinação contra os falsos positivos.** A primeira corrida acusou como mortos arquivos que estavam vivos. Cada
grupo ganhou uma linha na configuração:

| Falso positivo | Correção |
|---|---|
| Scripts que rodam à mão (`node script.mjs`) | declarados como entradas |
| Protótipos e arquivos de configuração soltos | ignorados |
| Arquivos que o framework carrega por convenção e que o plugin não cobria | declarados como entradas de produção |
| Exports usados só dentro do próprio arquivo | `ignoreExportsUsedInFile` |

**O falso negativo.** O erro maior era o contrário: um arquivo que só os testes importam parece vivo. O modo
`--production` deixa os testes de fora e apanha-o. A página do modo de produção diz o mesmo: como os testes importam
o código de produção, um arquivo pode parecer usado sem o ser.

**Os pontos cegos.** Três coisas que o knip 5.88.1 não mostrou, e uma por verificar, com o que a documentação lida
em 2026-11-06 diz de cada uma:

| O que não se viu | Visto no | O que a documentação diz |
|---|---|---|
| Um `export default` que ficou sem chamador | 5.88.1, ao apagar código de verdade | Nada: as páginas da configuração e dos achados não falam de `export default`. Não se sabe se é um limite geral ou do caso. |
| Um ramo morto dentro de um arquivo vivo (um `if` que já não se toma) | 5.88.1 | Nada sobre ramos: a página inicial fala de arquivos, exports e dependências. Tira-se à mão, lendo o código. |
| Uma rota HTTP (`route.ts`) que ninguém chama | 5.88.1 | O plugin do Next.js põe `app/**/route` entre as entradas, e por omissão os exports das entradas não se acusam, nem com o `includeEntryExports` ligado, porque é uma entrada do plugin. Uma rota sem chamador acha-se pelo endereço dela, com `git grep`. |
| Um import montado a partir de texto (o caminho numa variável) | não procurado (knip 5.88.1) | A página dos achados diz que o caminho calculado de um `import()` não se resolve e que o montado com *template string* pode ser ignorado. O efeito é o contrário de um ponto cego: um arquivo vivo acusado de morto. Declara-se como entrada. |

**A simulação numa cópia.** Para saber o que morre em cadeia ao apagar um ramo antigo, sem tocar no projeto:

1. `git archive HEAD` para uma pasta fora do projeto;
2. o knip na cópia, antes;
3. apagar o ramo antigo na cópia;
4. o knip na cópia, depois;
5. a diferença entre as duas saídas é o que morre junto.

No projeto medido, um ramo antigo arrastou muitos arquivos que só ele usava, e outro não arrastou nenhum: o
tamanho da cadeia só se sabe simulando.

**Conferir cada arquivo antes de apagar.** Para cada arquivo que o knip acusa:

- procurar quem o importa **pelo caminho**, e não pelo nome solto: o nome dá falsos positivos (`env` aparece dentro
  de `dotenv`);
- ver o que ele escreve no banco e que textos o citam;
- procurar os testes que o importam em todo o lado: os testes podem viver fora da pasta `__tests__/`, ao lado do
  código;
- depois de apagar, o verificador de tipos (`tsc --noEmit`) é a rede que apanha o import que escapou.

## O que não se verificou

- **A versão 6 do knip** (a 6.44.1 era a publicada em 2026-11-06) não foi rodada. Os três pontos cegos foram vistos
  no 5.88.1; a coluna da documentação é da leitura de 2026-11-06, que não diz a versão.
- O porquê do `export default` calado: a documentação lida não fala dele, e não se fez um caso mínimo para o provar.
- Os imports montados a partir de texto não foram procurados no projeto medido.
- A lista inteira dos exports sem uso não foi lida um a um: só uma amostra, em que todos eram reais.
- O tempo de uma corrida no CI não foi medido.
- Nenhuma outra ferramenta de código morto foi rodada para comparar.

## Conclusão

1. **Antes de instalar:** ler o pacote (rede e telemetria), fixar a versão, rodar o `npm audit` antes e depois, ler o
   diff do lockfile.
2. **Antes de rodar:** saber que as configurações do projeto vão ser executadas e o que elas carregam, o `.env`
   incluído.
3. **Afinar** os falsos positivos na configuração (scripts à mão, protótipos, convenções do framework, exports só
   internos) e rodar também com `--production`.
4. **Não confiar só na ferramenta:** o `export default` sem uso, o ramo morto dentro de um arquivo vivo e a rota sem
   chamador procuram-se à mão; o import montado a partir de texto vira entrada declarada.
5. **Simular numa cópia** (`git archive`) antes de apagar um ramo antigo, para ver a cadeia inteira.
6. **Conferir pelo caminho**, com o verificador de tipos como rede final.
7. **Travar o que já está limpo:** a saída da ferramenta vira uma linha de base que só encolhe, como as outras
   catracas (skill `codigo-legivel` §4).

Estes fatos são de uma versão de uma ferramenta: antes de os usar numa versão nova, rode-a de novo num caso pequeno.
