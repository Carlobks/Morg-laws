# Modelos de issue e de PR no GitHub

Data: 2026-11-08.

## Pergunta

Que modelos de issue e de PR o GitHub aceita, como se pede a prova sem deixá-la fugir e como se manda a segurança
para um canal privado num repositório público mantido por uma pessoa? A resposta sustenta o que está em `.github/`
(os formulários, o `config.yml`, o modelo de PR e o `SECURITY.md`) e os testes que o conferem.

## Fontes

As 12 páginas da documentação do GitHub, todas relidas em 2026-11-08 com o `WebFetch` (um modelo pequeno resume cada
página, e as frases e a contagem dos erros vêm desse resumo). Cada uma tem a sua entrada no `FONTES.md`:

- **Formulários de issue:** a sintaxe dos formulários —
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
  — e o esquema deles —
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema
- **O seletor e os modelos:** configurar os modelos de issue —
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
  —, sobre os modelos de issue e de PR —
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates
  — e o modelo de pull request —
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
- **Os erros do GitHub:** os erros comuns de validação —
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/common-validation-errors-when-creating-issue-forms
- **Segurança:** os arquivos de saúde da comunidade —
  https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file
  —, a política de segurança —
  https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository
  —, ligar o aviso privado —
  https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configuring-private-vulnerability-reporting-for-a-repository
  —, reportar em privado —
  https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately
  — e a divulgação coordenada —
  https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/about-coordinated-disclosure-of-security-vulnerabilities
- **Links com o formulário escolhido:** criar uma issue —
  https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue

## O que se mediu

A primeira tabela é o estado do repositório no GitHub, consultado em 2026-11-08 só com leitura (`gh label list`, `gh repo view`,
`gh api -X GET …` e um `curl` sem login):

| O quê | Resultado |
|---|---|
| Etiquetas que existem | as 10 de fábrica: `accessibility`, `bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix` |
| Repositório | público; issues ligadas; Discussions desligadas |
| Aviso privado | `{"enabled":false}`: ainda desligado |
| Política de segurança | `isSecurityPolicyEnabled: false` |
| Perfil da comunidade | saúde de 28 %; `issue_template` e `pull_request_template` ainda `null` (nada foi enviado) |
| Link do aviso privado sem login | `302` para a página de login do GitHub, com o endereço de volta |

A segunda é o que o repositório local tem, contado nos arquivos:

| O quê | Resultado |
|---|---|
| Formulários em `.github/ISSUE_TEMPLATE/` | quatro (problema numa regra, sugestão, correção de fonte e pedir um contato de segurança) e o `config.yml` |
| Testes que os conferem | `tests/test_esquema_dos_formularios.py` (a forma, incluindo a do molde `modelos/github/ISSUE_TEMPLATE/erro.yml`) e `tests/test_modelos_do_github.py` (o conteúdo, o `config.yml`, o modelo de PR, a política, a língua e os endereços) |
| PyYAML | não há pacote para o Python 3.15 local; instalou-se compilando a partir do código-fonte, num ambiente descartável, e o CI fixa a versão 6.0.3 |

O que as páginas dizem, lido hoje e posto em forma de regra do desenho:

- **Formulário ou modelo em Markdown.** O formulário mostra campos e deixa marcar os obrigatórios; o modelo em
  Markdown só orienta. Por isso a prova (o comando e a saída) vai num campo obrigatório. O `required` só vale em
  repositório público, e este é.
- **O `config.yml`.** Com `blank_issues_enabled: false`, quem só lê não vê a issue em branco e ninguém foge da prova;
  quem escreve vê a opção marcada «Maintainers only». Os `contact_links` levam `name`, `url` e `about`. A ordem do
  seletor é alfabética, e um número na frente do nome do arquivo a fixa.
- **O que o GitHub recusa.** A página dos erros lista 21 casos. Os que mais pesam no desenho: `body` vazio ou sem
  nenhum campo que não seja `markdown`, `label`s repetidos ou parecidos demais, opções repetidas, a palavra `None`
  e valores que o YAML lê como booleanos (`Yes`, `No`).
- **Onde fica o `SECURITY.md`.** Em `.github`, na raiz ou em `docs`, e o GitHub procura nessa ordem. A página da
  política de segurança não diz isso; vem da página dos arquivos de saúde da comunidade.
- **Segurança em privado.** Quem é dono ou administrador liga o aviso privado em Settings → Advanced Security. Quem
  recebe o aviso são os administradores e os gestores de segurança que seguem o repositório (All Activity, ou Custom
  com Security alerts). Sem política de segurança, a divulgação coordenada manda abrir uma issue a pedir um contato,
  sem detalhe nenhum, porque ela fica pública na hora.
- **Links que abrem o formulário.** O parâmetro `template` da URL escolhe o formulário, e uma URL com parâmetros
  inválidos dá 404.

## O que não se verificou

- **O seletor do «New issue» com os modelos:** só depois do push. A ordem dos quatro formulários e a marca «Maintainers
  only» também. A vista de quem não é dono precisaria de uma segunda conta.
- **O endereço `…/security/advisories/new`** não está escrito em nenhuma das páginas lidas, que falam do botão «Report
  a vulnerability». Sem login, medi o `302`. Com login e o aviso desligado, não sei o que ele mostra, e a página de
  reportar em privado não diz se a opção some ou fica desabilitada.
- **Onde o GitHub mostra o erro de um formulário inválido.** A página dos erros diz que aparece ao criar, guardar ou
  ver o formulário, sem dizer onde. Também não sei se a API de GraphQL lista os formulários `.yml`, nem se uma PR aberta
  pelo `gh pr create` sem corpo usa o modelo de PR.
- **A sintaxe dos formulários está em *public preview*** e pode mudar. O teste local confere o que a página diz hoje;
  só a conferência depois do push mostra se o GitHub aceita cada formulário.
- **A ordem das chaves de topo.** A página manda o arquivo começar por `name`, `description` e `body`, e o exemplo
  completo dela escreve `title`, `labels`, `projects`, `assignees` e `type` antes do `body`. O teste local exige só que
  essas três existam e que `name` venha primeiro; qual das duas leituras o GitHub aplica não se verificou.
- **As palavras proibidas nos rótulos.** A página dá só «password» como exemplo; a lista inteira não é pública, e o
  teste não a confere.
- **O título do formulário de contato de segurança é livre:** o aviso pede para não pôr detalhes nele, mas nada o
  impede.
- **Os resumos das páginas** vêm de um modelo pequeno, não da leitura da página inteira por uma pessoa.
- **A eficácia dos formulários no uso real.** As regras saíram de um projeto real e ninguém as mediu; nada aqui mede
  se os formulários melhoram os relatos que chegam.

## Conclusão

Formulários `.yml` com a prova num campo obrigatório; um quarto, só para pedir um contato de segurança sem nenhum
detalhe; a issue em branco desligada; o `SECURITY.md` em `.github/`, a apontar para esse quarto quando o aviso privado
não abre; e um teste local do esquema que vale também para o molde `erro.yml`. O aviso privado é ligado à mão pelo dono,
antes do push. As regras saíram de um projeto real e ninguém as mediu: o caso que alguém viveu é a prova que conta.
