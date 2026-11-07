# ERP de serviços

Um sistema web de gestão feito para duas empresas de serviços (a Empresa A e a Empresa B), que compartilham a mesma equipe interna. Este é o projeto de onde saíram as regras do Morg-laws.

## Para quem é

Para a equipe interna: o RH, o Financeiro e a gerência. Quem trabalha no dia a dia usa o sistema no navegador; a gerência decide, por perfil, quem vê e quem altera o quê.

## O que faz

Do cadastro de uma pessoa ao pagamento do que se deve a ela, e do pedido de um serviço à conclusão da tarefa, tudo no mesmo lugar: funcionários e contratos, folha e pagamentos, contas a pagar e a receber, caixa e bancos, documentos e PDFs, inventário e frota, tarefas e avisos, lista de espera, acessos e permissões. O arquivo [`modulos-e-fluxos.md`](modulos-e-fluxos.md) conta cada um em palavras.

## Como é feito

| Camada | O que usa |
|---|---|
| interface e servidor | Next.js com React, rotas e ações de servidor no mesmo projeto |
| dados | Postgres com RLS, o controle de acesso por linha, ligado em todas as tabelas da aplicação (medido em novembro de 2026) |
| hospedagem | serverless, com publicação a partir da branch principal |
| testes | testes unitários, testes de ponta a ponta no navegador e catracas que impedem o passivo de crescer |

A interface e a documentação interna são em português.

## Desde quando

O primeiro commit é de março de 2026. O histórico, as contagens e os comandos que as deram estão em `o-que-se-mediu.md`.

## Como se trabalha com agentes

O projeto é conduzido por um dono de produto que não escreve o código: pede, aprova e confere, e os agentes de IA propõem e implementam. Daí vêm as regras que o Morg-laws reúne. O ciclo é sempre o mesmo:

1. **Plano primeiro.** O agente lê, mede e propõe; nada se escreve sem o «sim» do dono, e um plano que mexe numa tela ou em muitos arquivos leva uma página visual de antes e depois.
2. **Uma sessão por fase.** A sessão principal orquestra; cada fase roda numa sessão nova, para o contexto não crescer até o agente perder o fio.
3. **Auditoria a frio.** Quem audita não é quem implementou, e lê o resultado sem a conversa que o gerou.
4. **Portões que rodam sozinhos.** Tipos, lint, testes do que mudou e catracas rodam em cada commit, e um hook que recusa não se contorna: se corrige.
5. **Provar medindo.** Um «pronto» leva o comando e a saída, a tela vista ou a consulta feita, e diz o que não se verificou.

## Os outros arquivos

- [`modulos-e-fluxos.md`](./modulos-e-fluxos.md): o que o sistema faz, módulo a módulo, e os fluxos principais.
- [`o-que-se-mediu.md`](./o-que-se-mediu.md): os números, cada um com o mês e o comando.
- [`regras-e-incidentes.md`](./regras-e-incidentes.md): cada regra, o incidente que a fez nascer e a barreira; chega em outra etapa.
