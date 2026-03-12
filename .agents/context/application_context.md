# Contexto Geral da Aplicacao

## Proposito
Construir uma aplicacao de web scraping para consultar dados de contratos no portal de transparencia e-publica e expor o resultado em uma API REST JSON.

O portal alvo nesta fase e:
`https://transparencia.e-publica.net/epublica-portal/#/palmeira/portal/compras/contratoView?params=%7B%22id%22:%22MV8yMDMy%22,%22mode%22:%22INFO%22%7D`

A aplicacao deve receber como entrada:
- cidade: `palmeira`
- params: `{"id":"MV8yMDMy","mode":"INFO"}`

## Objetivo Funcional
Extrair e retornar em JSON, no minimo:
- nome da prefeitura
- valor total do contrato em reais
- objeto ou descricao do contrato
- data de assinatura
- data de inicio da vigencia
- vencimento do contrato
- fornecedor
- filial
- numero ou codigo da licitacao
- responsaveis juridicos
- gestores
- fiscais
- itens do contrato

Cada item do contrato deve conter:
- numero
- denominacao
- quantidade
- unidade de medida
- valor unitario
- valor total

## Regras de Saida
- A API REST deve devolver o resultado final em JSON
- A consulta deve simular persistencia imediata em banco local de teste
- A solicitacao deve simular envio de email para `vitorfelipep@dmmv-tech.com`
- O email deve registrar data, hora, cliente solicitante, titulo e descricao da consulta

## Tecnologia Base
- Python
- Playwright para navegacao e captura de conteudo dinamico
- API REST com FastAPI
- Estrutura de testes com pytest
- Persistencia de teste em banco local ou documental em memoria

## Arquitetura
Usar arquitetura hexagonal com separacao clara entre:
- dominio
- aplicacao
- portas
- adaptadores
- infraestrutura

Aplicar:
- Clean Code
- SOLID
- responsabilidade unica
- tipagem explicita
- componentes testaveis

## Diretriz de Persistencia
Nesta fase, persistencia e apenas de teste.
Preferir uma abordagem simples e local:
- banco em memoria
- ou banco documental local para simular indexacao por documento

A escolha deve ser documentada no codigo, deixando claro que nao e ambiente produtivo.

## Diretriz para Agentes
Todos os agentes devem ler este arquivo antes de propor mudancas.
Esse contexto define:
- finalidade da aplicacao
- requisitos minimos de dados
- stack tecnica
- padrao arquitetural
- integracoes simuladas

## Diretriz de Branching
Antes de iniciar qualquer demanda em uma branch nova:
- executar `git checkout main`
- executar `git pull origin main`
- confirmar que a branch local de trabalho parte da `main` mais recente
- so depois criar a branch `feature/...`

Se houver conflito ou divergencia com a `main`, resolver isso antes de abrir ou atualizar o PR.

## Diretriz de Descoberta de Trabalho
Quando o usuario nao informar explicitamente qual demanda deve ser executada:
- consultar o GitHub do repositorio com `gh`
- listar ou inspecionar issues abertas
- priorizar issues prontas para desenvolvimento
- usar a issue selecionada como fonte oficial da tarefa
- so iniciar implementacao depois de identificar claramente qual issue sera atendida

Se houver ambiguidade entre varias issues abertas, apresentar a selecao ao usuario antes de implementar.
