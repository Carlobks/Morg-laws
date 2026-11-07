# Catálogo de projetos

Aqui ficam projetos reais, anonimizados, de onde saíram as regras do Morg-laws: o que o sistema faz, que regra nasceu de que incidente, a barreira que a faz ser cumprida e onde ela está neste repositório. Serve para ver de onde vem cada regra, não para copiar o código de ninguém.

## Projetos

| Projeto | O que é |
|---|---|
| [erp-de-servicos](erp-de-servicos/) | um sistema web de gestão para duas empresas de serviços |

## O formato

Cada projeto é uma pasta com os mesmos quatro arquivos, de até 500 linhas cada:

- `README.md`: o projeto em uma página (o que é, para quem, a pilha, desde quando, como se trabalha com agentes);
- `modulos-e-fluxos.md`: o que o sistema faz, módulo a módulo, e os fluxos principais;
- `regras-e-incidentes.md`: cada regra, o incidente que a fez nascer, a barreira e onde está neste repositório;
- `o-que-se-mediu.md`: os números, cada um com o mês e o comando que o deu.

A tabela acima e as pastas têm de bater: o teste confere.

## A regra de anonimato

Vale em toda a pasta. O que o projeto de origem tem e o que o catálogo escreve no lugar:

| No projeto de origem | No catálogo |
|---|---|
| o nome do sistema e das empresas, siglas e números fiscais | o nome da pasta do projeto, «Empresa A» e «Empresa B» |
| pessoas: o dono, gerentes, a equipe | o papel («o dono», «a equipe do Financeiro», «a gerência»); um papel nunca é o sujeito de um erro |
| país, leis, nomes de documentos, de impostos e da forma jurídica | nada, ou um termo genérico («número fiscal», «a lei do trabalho») |
| plataformas de terceiros de um só mercado | «uma plataforma de documentação» |
| mudança de nome ou de sigla de uma empresa | nada |
| datas dos incidentes | o mês, nunca o dia |
| domínios, e-mails, IDs de serviços, UUIDs | nada; se for preciso, `example.com` ou `<id>` |
| hashes de commit, números de migração, de chamado e de decisão | nada |
| valores em dinheiro | nada; só a ordem de grandeza de volume técnico (GB, horas, arquivos) |
| caminhos e nomes de arquivos | o papel («a constante das empresas», «o arquivo de regras»); a exceção são os nomes genéricos de pasta que aparecem dentro de um comando de `o-que-se-mediu.md`, porque o comando só prova se for reproduzível |
| contagens do repositório, de regras, de bugs (só o total por área) e de catracas | entram, exatas, com o mês e o comando que as deu, menos as que falam de defeitos abertos |

## O que barra cada commit

- A lista negra local (os nomes que não podem vazar), no `pre-commit` e no `commit-msg`, em todo o repositório.
- O teste `tests/test_projetos_sem_dados.py`, no `pre-commit` de todos os commits: lê o que está preparado (e não o disco) em `projetos/` e na lista de palavras, e recusa caminhos de pasta pessoal, e-mails, documentos, IBAN, UUID, hashes, IDs de serviço, domínios, dinheiro e qualquer palavra com maiúscula, também dentro de crases, que não esteja em `tests/palavras-com-maiuscula.txt`; só arquivos `.md` entram na pasta, e qualquer outro tipo é recusado sem ser lido.
- O CI roda o mesmo teste sobre cada commit do intervalo do push que mexe em `projetos/` (e não só sobre o último), e o gitleaks sobre a história inteira.

## Os limites

- O CI não vê a lista negra, que fica fora do repositório: um nome em minúsculas, ou que já esteja na lista de palavras por ser também uma palavra comum, passa no CI; só a lista negra local o apanha.
- Quem conhece o dono do repositório reconhece o projeto. O anonimato serve para que o nome da empresa não apareça numa pesquisa ao lado dos incidentes.
- Um nome de pessoa nunca entra na lista de palavras: troca-se pelo papel.
- O teste só varre `projetos/`: o resto do repositório só tem a lista negra e o gitleaks.
- Os commits feitos pelo site do GitHub não passam pelos hooks; o CI os apanha depois, mas já públicos.
- Um link para outro arquivo do catálogo ou do repositório usa caminho relativo (`./`, `../` ou um `.md` sem `://`); qualquer endereço de internet continua sendo domínio.
- O código e os nomes de arquivo escrevem-se entre crases: fora delas, todo nome com ponto é tratado como domínio, e dentro delas só é domínio o que acaba num país (duas letras) ou num final comum, e um nome de arquivo com `.md`, `.py` ou `.sh` e um ponto só passa, mesmo que também seja um domínio.
- Um termo da lista negra com uma classe como `[[:alpha:]]` ou com sintaxe só do `grep` (`\<`, `\>`) é acusado como «não compila» e tem de ser reescrito.
- Os casos que o teste não apanha, e que a leitura de cada subfase cobre: dinheiro por extenso sem algarismo ou abreviado em minúsculas, identificador de serviço com prefixo, com maiúsculas misturadas ou com mais de 20 caracteres, hash curto só de dígitos e número de cartão em grupos de quatro.
