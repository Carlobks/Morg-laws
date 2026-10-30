---
name: nextjs-react
description: Guia um agente a escrever Next.js (App Router) e React sem os erros que só aparecem em produção — Server Actions e rotas que conferem a sessão por si, redirect que não se engole num catch, arquivos 'use server' sem re-exports, variáveis NEXT_PUBLIC estáticas, cache revalidado num só lugar, listas indexadas pelo id, atualização otimista, modais com portal e mudanças atrás de um interruptor. Usar ao escrever ou rever componentes React, Server Actions, rotas de API, middleware ou configuração do Next.js, ao corrigir uma tela que pisca, perde a seleção ou mostra o registro errado, ou antes de apagar uma página. Não usar para o banco e o RLS (é a supabase) nem para provar no navegador que a tela está certa (é a testes-e-provas).
---

# Next.js e React

Muitos dos erros desta lista passam pelo compilador, pelo lint e pelos testes, e só aparecem no navegador ou no build de produção. Cada regra tem o motivo.

## 1. Servidor: segurança e fluxo

- **Toda Server Action e toda rota `/api` confere a sessão e a permissão por si.** Uma Server Action é um endpoint público: qualquer pessoa a chama de fora da tela. O middleware não é barreira: a CVE-2025-29927 deixava saltá-lo com um cabeçalho interno em apps com servidor próprio, e a própria Vercel recomenda não o usar como única proteção das rotas.
- **`unstable_rethrow(err)` é a primeira linha de qualquer `catch` genérico.** `redirect()`, `notFound()` e o erro de render dinâmico funcionam por `throw`: um `catch` que engole tudo engole também o redirect. Os mocks nos testes têm de imitar este comportamento.
- **Arquivo `'use server'` não tem re-exports nem exporta constantes.** O `tsc` não acusa, mas o build falha (num projeto real, deu erro 500 em produção duas vezes). As constantes vão para um arquivo sem a diretiva.
- **Mantenha o Next e o React atualizados.** A falha React2Shell (CVE-2025-55182 no React e CVE-2025-66478 no Next, nota 10 de 10) permitia executar código no servidor, sem login, através dos Server Components. Depois vieram mais falhas nos mesmos pacotes. A correção é só atualizar: regras de firewall não substituem a atualização.

## 2. Build e ambiente

- **`process.env.NEXT_PUBLIC_*` só com acesso estático** (`process.env.NEXT_PUBLIC_URL`). O build substitui o texto literal; um acesso dinâmico (`process.env[nome]`) fica `undefined` no navegador. Num projeto real, isso derrubou todas as páginas do cliente.
- **Não rode `next build` com o servidor de desenvolvimento ligado:** os dois partilham a pasta `.next` e o build estraga o servidor. E não mate o servidor de desenvolvimento de outra pessoa.
- **Bibliotecas de ícones em `optimizePackageImports`** no `next.config`. Sem isso, a biblioteca inteira entra no pacote.
- Com o Turbopack, alguns ícones de bibliotecas grandes já derrubaram páginas em produção. Ícone novo: prefira um que o projeto já usa, ou confirme com um build.

## 3. Cache

- **`revalidatePath` e `revalidateTag` num helper central.** Chamadas espalhadas pelo código acabam por esquecer uma rota. As tags vivem num arquivo único.
- `revalidatePath` só quando um Server Component lê os dados que mudaram.

## 4. Listas e estado

- **A chave de uma lista é o id do registro, nunca o que se mostra.** Seleção, mapas, `key` e exclusões indexados pelo nome colidem no dia em que dois registros partilham o nome (num projeto real: centenas de pessoas e um nome a menos que pessoas).
- **`key={index}` é proibido** em listas que mudam de ordem ou de tamanho.
- **Guarde o id selecionado, não a linha.** Uma linha guardada no estado congela no momento do clique e mostra dados velhos depois de uma edição. Derive a linha a partir da prop. Ao corrigir um caso, procure os gêmeos (`grep "useState<.*Row"`).
- **Ação repetida usa atualização otimista** com um instantâneo para desfazer. O "carregando…" só aparece na primeira carga; o sinal de "salvando" fica no controle que mudou. Recarregar a lista inteira a cada clique faz a tela piscar.

## 5. Componentes

- **Modal com `position: fixed` usa `createPortal(…, document.body)`**, com uma guarda de montagem e o Escape para fechar. Sem portal, um `transform` num ancestral (as animações deixam um) quebra o posicionamento.
- **Modais encadeados:** só o do topo reage ao teclado, e fechar com alterações por salvar pede confirmação.
- **Props tipadas com o tipo real da linha**, nunca `Record<string, any>`. Um campo que "nunca mostrou nada" pode simplesmente não existir.
- **Cruze os campos que a tela de detalhe lê com os campos que o formulário edita.** Uma coluna que existe e se mostra, mas não tem input, nunca é preenchida.
- **Uma fonte única que alguém desenha à mão não é fonte única.** Se uma constante governa várias telas, um teste afirma que todas a usam.
- **Nada de `_prefixo` para calar uma prop não usada:** é funcionalidade morta escondida. Use a prop ou tire-a.
- **Nada de setas nativas em `<input type="number">`:** são minúsculas e inacessíveis. Use botões próprios.
- **Duas classes Tailwind da mesma propriedade no mesmo elemento:** ganha a ordem do CSS gerado, não a da string. Use uma classe por propriedade.
- **Tamanho de letra em `rem`**, nunca em `px` fixo, para respeitar o tamanho que o usuário escolhe.

## 6. Mudar uma tela que as pessoas usam

- **Antes de ligar um componente existente a um lugar novo**, veja o que ele **escreve** (as actions que chama). Um modal com nome inocente pode apagar ou demitir.
- **Antes de apagar uma página**, procure três coisas: o que ela escreve ao carregar, que textos e links mandam para lá, e que testes passam por lá. Os testes reapontam-se; não se apagam.
- **Mudança que altera o que a pessoa já faz** (fluxo, lugar, botão que some) entra atrás de um interruptor: liga-se primeiro para um grupo de teste e só depois para todos. O código antigo sai só depois de "todos" ficar ligado sem queixas. Acrescentar (botão novo, aviso) não precisa de interruptor.

## Fontes

Ver `FONTES.md`: avisos do Next.js (CVE-2025-29927) e do React (React2Shell).
