# Manual de uso do Morg-laws

Um manual prático para quem está começando a trabalhar com agentes de código. É trabalho de um não profissional, escrito
em Markdown nesta pasta e feito para ser lido como PDF.

## As partes

| Arquivo | O que tem |
|---|---|
| `00-antes-de-comecar.md` | Quem escreveu, e como ler o manual |
| `01-o-que-e-o-morg-laws.md` | O que é, para que serve, o que tem cada pasta |
| `03-instalar.md` | Instalar as skills, pôr as regras, ligar as barreiras |
| `04-pedir.md` | Como pedir: as quatro partes, o oráculo, a tarefa pequena, pôr o plano à prova |
| `05-sessoes.md` | Continuar, compactar, abrir uma sessão filha, várias sessões na mesma pasta |
| `06-o-ciclo-de-uma-mudanca.md` | O plano, o commit por caminho, o hook que recusa, o push |
| `07-as-regras.md` | As regras, cada uma com o porquê e a fonte |
| `08-como-se-garante.md` | Como o texto vira barreira |
| `09-quando-da-errado.md` | O que fazer quando o agente diz “pronto” sem prova, ou esquece o combinado |
| `10-glossario.md` | Cada termo numa frase, com a parte que o explica |
| `11-pedidos-prontos.md` | Os pedidos que se copiam |
| `12-como-este-manual-foi-feito.md` | O posfácio |

Por enquanto só as partes `00-antes-de-comecar.md`, `01-o-que-e-o-morg-laws.md`, `03-instalar.md`, `04-pedir.md`, `05-sessoes.md`, `06-o-ciclo-de-uma-mudanca.md`, `07-as-regras.md`, `08-como-se-garante.md`, `09-quando-da-errado.md`, `10-glossario.md` e `11-pedidos-prontos.md` existem. Falta só a `12-como-este-manual-foi-feito.md`, que vem por último.

Os procedimentos (P1 a P24) vão em páginas duplas: na página par, **Na prática**; na ímpar, **Por quê e fonte**.

## Gerar o PDF

Instale o Typst (`sudo pacman -S typst` no Arch Linux, `winget install --id Typst.Typst` no Windows; para as outras
máquinas, veja a [instalação oficial](https://github.com/typst/typst#installation)); o git você já tem. Na
raiz do repositório, o mesmo comando serve no `sh` e no PowerShell:

`typst compile --root . --font-path manual/fontes --ignore-system-fonts --input commit="$(git describe --always --dirty)" manual/manual.typ manual/manual.pdf`

Na primeira vez o Typst baixa o pacote [`cmarker`](https://typst.app/universe/package/cmarker/), que lê o Markdown. A fonte dos títulos vem em `manual/fontes/`, com a
licença; nada se instala no sistema. O PDF não entra no git. Se um par não couber numa página, a compilação falha e diz
qual é.

O molde da página é o `manual.typ`; as partes em Markdown são o conteúdo.
