# Módulos e fluxos

O que o sistema faz, em palavras. Não há aqui nomes de tabelas, rotas ou telas, regras de cálculo, prazos legais nem o que cada perfil enxerga: isso é detalhe do projeto de origem, e parte dele seria um mapa para quem quisesse atacá-lo.

## Os módulos

O painel de administração tem 12 pastas de módulo (acessos e permissões são duas delas, juntas na tabela), e o Financeiro se divide em cinco partes (a contagem e o comando estão em `o-que-se-mediu.md`).

| Módulo | O que faz |
|---|---|
| Funcionários | A ficha de cada pessoa, o contrato e os seus períodos, a admissão, o desligamento e a recontratação; o acesso pelo celular e a validação dos documentos de identificação. |
| Férias | As férias das pessoas da equipe, numa tela própria. |
| Financeiro, pessoal | As horas trabalhadas, a folha, os pagamentos e os recibos de cada pessoa. |
| Financeiro, contas a pagar | As faturas de fornecedor, os impostos, os alojamentos e as rendas, os veículos; a fila do que se deve pagar e a baixa de cada pagamento. |
| Financeiro, contas a receber | A faturação aos clientes e o acompanhamento do que ainda não entrou. |
| Financeiro, caixa e bancos | O saldo de cada conta, os movimentos e a conciliação com o extrato. |
| Financeiro, relatórios | As visões consolidadas para a gerência. |
| Clientes | O cadastro dos clientes e a ficha de cada um. |
| Documentos | A guarda dos documentos de funcionários, clientes, empresas e itens do inventário, a geração de PDF (contratos, cartas, declarações, recibos) e a tradução quando é preciso. |
| Inventário e frota | O que a empresa tem, onde está e com quem; os veículos próprios e alugados ligados ao inventário; a expedição. |
| Tarefas e avisos | O quadro de tarefas da equipe, a mobilização, os avisos por tela e um bloco de rascunho para capturar uma tarefa antes de a organizar. |
| Lista de espera | Os candidatos que aguardam, organizados por profissão, com um formulário de entrada e um relatório. |
| Empresas | A ficha de cada uma das duas empresas, usada nos documentos e nos pagamentos. |
| Acessos e permissões | Quem entra, com que perfil e o que cada perfil pode fazer; a gerência concede e retira, também o acesso pelo celular. |
| Definições | As opções gerais do sistema, numa tela própria. |

## Os fluxos principais

### Admissão, contrato e desligamento

1. O RH abre a ficha da pessoa e preenche os dados; os números dos documentos de identificação são validados no formulário.
2. O contrato é gerado em PDF a partir do modelo da empresa que contrata, e fica guardado nos documentos da pessoa.
3. Enquanto o contrato dura, a pessoa aparece nas horas e na folha, e pode pedir férias.
4. No desligamento, o RH registra a saída; a ficha fica no histórico, e o que já foi pago continua nele.
5. Uma recontratação reabre a ficha da mesma pessoa, e não cria outra.

### Horas, folha, pagamento e recibo

1. As horas de cada pessoa entram por período.
2. A folha calcula o que se deve a cada pessoa.
3. O Financeiro confere a folha e paga; o pagamento é registrado.
4. O recibo é gerado em PDF e distribuído à pessoa.

### Fatura de fornecedor, conta a pagar e pagamento

1. A fatura entra e fica ligada ao fornecedor.
2. Vira uma conta a pagar, que entra numa fila.
3. O Financeiro paga a partir da fila, abrindo a conta em contexto; o pagamento fica registrado contra a conta e o banco.
4. A conciliação confere os movimentos do banco com o que foi pago.

### Pedido, tarefa e conclusão

1. Um pedido da equipe vira uma tarefa, que nasce no bloco de rascunho ou direto no quadro.
2. A tarefa tem um responsável e um estado, e o quadro mostra o que está parado.
3. Ao concluir, a tarefa sai do quadro.

### Lista de espera

1. O candidato entra pelo formulário, escolhendo a profissão.
2. A equipe acompanha a lista e o relatório por profissão.
3. Quem é escolhido segue para o fluxo de admissão.
