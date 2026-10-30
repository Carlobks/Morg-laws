# TypeScript

## Zero `any`, sem exceção escondida

**O que aconteceu:** uma regra antiga dizia "`any` proibido, salvo com um comentário `eslint-disable` a explicar". Na prática, criou uma lista de exceções que só crescia.
**Por que:** um comentário que desliga o alarme é uma exceção que ninguém revê.
**Como fazer:** zero `any`, sem comentário que o libere. Para dados de fora, use `unknown` e valide com um schema (por exemplo, Zod).

## `useParams()` devolve mais do que uma string

**O que aconteceu:** `const { id } = useParams()` passado para uma função que espera `string` dá erro de tipo, e `id ?? ''` não resolve.
**Por que:** o tipo é `string | string[] | undefined`. O `??` tira o `undefined`, mas o `string[]` continua.
**Como fazer:**
```ts
const registroId = (Array.isArray(id) ? id[0] : id) ?? ''
```

## `as const` só em literais

**O que aconteceu:** `['a', 'b'].join(', ') as const` dá erro TS1355.
**Por que:** a asserção `const` só se aplica a literais, não ao resultado de uma chamada.
**Como fazer:** escreva o literal direto (`'a, b' as const`) ou tire o `as const`.

## Derive o tipo da função que consome o dado

**O que aconteceu:** um hook importava um tipo de linha de outro arquivo, que mudou e deixou os dois desalinhados.
**Como fazer:** derive o tipo da fonte da verdade:
```ts
type ClientesParam = Parameters<typeof sincronizar>[0]['clientes']
```

## Fábrica sem tipo de retorno é interface por verificar

**O que aconteceu:** uma função que monta objetos declarava uma interface, mas não a usava como tipo de retorno. Os objetos tinham campos a mais ou a menos, e o compilador não acusava.
**Como fazer:** declare o tipo de retorno (`function criar(): Modelo`), ou use `satisfies Modelo` em cada objeto.

## Limites de tamanho (exemplo de um projeto real)

Não são lei universal; são números que funcionaram, impostos por catracas:

- arquivo `.tsx` com até 400 linhas, `.ts` até 300, Server Actions até 200;
- função nova com até 20 linhas (era 50 e foi apertado depois de medir);
- arquivo de Server Action com mais de 3 funções exportadas nasce partido.

O livro *Competente o Suficiente*, de Fabio Akita, defende funções curtas. O número exato é escolha de cada projeto.
