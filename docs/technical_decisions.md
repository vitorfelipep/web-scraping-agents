# Decisoes Tecnicas Iniciais

## Stack escolhida
- `FastAPI` para a API REST inicial
- `Playwright` para scraping de conteudo dinamico
- `Pydantic` e `pydantic-settings` para contratos e configuracao
- `pytest` para testes automatizados

## Arquitetura
- Estrutura base em arquitetura hexagonal
- Separacao entre dominio, aplicacao e infraestrutura
- Portas ficam na camada de aplicacao
- Configuracao, persistencia, scraping, notificacao e API ficam em infraestrutura
- Dependencias fluem de fora para dentro

## Persistencia
- Persistencia em memoria para simular um banco local de teste
- O objetivo e validar o fluxo de armazenamento antes da escolha de infraestrutura definitiva

## Notificacao
- Envio de email apenas simulado
- O adaptador registra um recibo simples de notificacao

## Python local validado
- Ambiente local verificado em: `Python 3.14.3`

## Observacao
- O scraping real do portal ainda sera implementado em feature posterior
- Esta entrega prepara a base do projeto para esse desenvolvimento
