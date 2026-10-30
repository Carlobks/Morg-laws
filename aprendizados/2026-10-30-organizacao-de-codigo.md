# Organização de código

## Componente que faz tudo → orquestrador

**Sinais:** mais de 5 `useState`, mais de 3 `useEffect`, handlers com mais de 30 linhas, mais de 150 linhas de JSX.
**Como fazer:**
1. Leia o arquivo inteiro e separe os blocos: estado, efeitos, handlers, seções da tela.
2. Extraia primeiro um hook com o estado e os handlers. Isso mostra o que cada parte da tela precisa de receber.
3. Extraia os subcomponentes, das folhas para cima.
4. O arquivo original fica só a montar as peças.
5. Rode o compilador depois de cada extração, não só no fim.

## Server Action que faz tudo → estrela

Um arquivo central com o CRUD e arquivos ao lado por responsabilidade:

```
pedidos-crud.ts       ← criar, ler, atualizar, apagar
pedidos-helpers.ts    ← funções puras (limpar payload, validar)
pedidos-leitura.ts    ← consultas de leitura complexas
pedidos-efeitos.ts    ← o que mexe fora do banco (e-mail, arquivos)
```

## Mover um arquivo sem partir quem o importa

1. Copie para o destino novo.
2. No lugar antigo, deixe um arquivo que reexporta o novo, marcado com `@deprecated`.
3. Atualize os importadores aos poucos.
4. Apague o antigo só quando ninguém o importar.

Atenção: num arquivo `'use server'`, reexportar parte o build (ver a skill `nextjs-react`).

## Organização por tipo (exemplo)

Tipos partilhados numa pasta própria (`lib/types/`) e Server Actions numa pasta própria (`app/actions/`), em vez de espalhados pelas pastas de cada funcionalidade. Facilita achar e evita importações circulares. É uma escolha, não lei.

## Operações independentes em paralelo

```ts
const resultados = await Promise.allSettled(ids.map((id) => mover(id)))
const movidos = resultados.filter((r) => r.status === 'fulfilled').length
```

O `allSettled` não para no primeiro erro e diz quantas operações deram certo. Um `for` com `await` faz uma de cada vez.
