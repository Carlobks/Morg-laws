# Instalar só algumas skills

Passos rodados numa pasta temporária fora de qualquer repositório, sem `-g`, com a pasta pessoal, as pastas de configuração e o cache trocados por pastas descartáveis, em 2026-11-14.

## `--skill` traz só as skills citadas, e a trava só guarda essas

**O que aconteceu:** o comando `npx skills add Carlobks/Morg-laws -a claude-code -y` com nove `--skill` copiou só essas nove para `.claude/skills/`. O `skills-lock.json` ficou com nove chaves, cada uma com a origem, o caminho e o hash. Comparando arquivo a arquivo com o repositório, 0 diferenças. Com `--list` no lugar do `add`, a ferramenta mostrou as 13 e não gravou nada na pasta.
**Por que:** com `-y` e sem `--skill`, a ferramenta instala todas. Com os nomes, ela instala só os citados e registra só o que instalou.
**Como fazer:** cite cada skill com o seu próprio `--skill`, e use `--list` antes para ver o que existe.
**Versão:** pacote `skills` 1.8.1, em 2026-11-14.

## Somar, atualizar e tirar

**O que aconteceu:** um segundo `add` com `--skill sql-postgres --skill supabase` somou as duas às nove, e as entradas das nove ficaram idênticas. O `npx skills update -p -y` conferiu as onze e não trouxe as outras duas do repositório. O `npx skills remove supabase -y` tirou a pasta e a chave da trava. O `add` sem `--skill` instalou as 13, iguais ao repositório, `evals/` incluídos.
**Por que:** o `update` olha só o que a trava lista, e o `remove` mexe nas duas pontas, a pasta e a chave. Apagar a pasta à mão deixa a chave na trava, e o teste das regras do molde reprova.
**Como fazer:** para somar uma skill, rode outro `add` com o nome dela. Para tirar, use `npx skills remove <nome>`; não apague a pasta.
**Versão:** pacote `skills` 1.8.1.

## O que a ferramenta grava fora do projeto

**O que aconteceu:** com a pasta pessoal trocada por uma descartável, os 656 arquivos gravados nela estavam todos no cache do `npm`, que o `npx` usa; na pasta temporária ficou só um cache do próprio Node. Nada foi para as pastas de configuração, de dados, de estado ou de cache da ferramenta. Na pasta pessoal verdadeira, nada que citasse `skills` mudou, e a instalação pessoal ficou igual.
**Por que:** sem `-g`, a ferramenta escreve só na pasta do projeto (e baixa o repositório numa pasta temporária que apaga).
**Como fazer:** não use `-g` para um projeto: o teste das regras do molde lê as pastas do projeto e não veria skills instaladas na pasta pessoal.
**Versão:** pacote `skills` 1.8.1.

## Para o Codex, o destino é outro

**O que aconteceu:** com `-a codex`, a skill foi para `.agents/skills/` e nenhuma pasta `.claude/` nasceu.
**Por que:** para o Codex, a ferramenta grava em `.agents/skills/`, a pasta onde ele procura as skills.
**Como fazer:** para o Codex, troque `claude-code` por `codex` no comando.
**Versão:** pacote `skills` 1.8.1.
