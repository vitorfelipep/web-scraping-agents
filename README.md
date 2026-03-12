# web-scraping

Projeto base para extracao de contratos do portal e-publica com API REST, persistencia de teste em memoria e orquestracao por skills e agentes.

## Objetivo
Este projeto foi estruturado para criar features com apoio de agentes especializados. O caso de uso inicial e consultar um contrato no portal de transparencia da cidade de `palmeira`, extrair seus dados e responder em JSON.

Entrada esperada do caso inicial:
- cidade: `palmeira`
- `params={"id":"MV8yMDMy","mode":"INFO"}`

URL de referencia:
- [Portal de contratos](https://transparencia.e-publica.net/epublica-portal/#/palmeira/portal/compras/contratoView?params=%7B%22id%22:%22MV8yMDMy%22,%22mode%22:%22INFO%22%7D)

## Escopo funcional da aplicacao
A aplicacao deve expor uma API REST que:
- recebe a cidade e o payload `params`
- consulta o portal com Playwright
- extrai os dados do contrato
- persiste a resposta em um banco local de teste
- simula o envio de email confirmando a solicitacao
- devolve tudo em JSON

Campos minimos da resposta:
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

Cada item do contrato deve incluir:
- numero
- denominacao
- quantidade
- unid. medida
- valor unitario
- valor total

## Arquitetura
O projeto deve seguir arquitetura hexagonal.

Camadas previstas:
- `domain/`: entidades, objetos de valor e regras de negocio
- `application/`: casos de uso, DTOs e portas de entrada/saida
- `infrastructure/`: configuracao, persistencia, scraping, notificacoes e entrypoints HTTP

Diretrizes obrigatorias:
- Clean Code
- SOLID
- type hints
- componentes coesos e testaveis
- isolamento entre regras de negocio e infraestrutura

## Contexto compartilhado dos agentes
O contexto funcional e tecnico comum do projeto fica em:
- [.agents/context/application_context.md](/Users/vitorcosta/codex-agents-study/agent-skill-projetc/portal-web-scraping/.agents/context/application_context.md)

Esse arquivo deve ser considerado a fonte base para qualquer feature nova. As definicoes dos agentes ja apontam para ele em `context_files`.

## Estrutura do projeto
```text
web-scraping/
├── docs/
│   └── technical_decisions.md
├── pyproject.toml
├── src/
│   └── web_scraping/
│       ├── application/
│       │   ├── dto/
│       │   ├── ports/
│       │   └── use_cases/
│       ├── domain/
│       │   └── entities/
│       └── infrastructure/
│           ├── config/
│           ├── entrypoints/
│           ├── notifications/
│           ├── persistence/
│           └── scraping/
├── tests/
├── .agents/
│   ├── context/
│   │   └── application_context.md
│   ├── skills/
│   │   ├── python_senior_dev.md
│   │   ├── qa_engineer.md
│   │   └── git_ops.md
│   ├── agents/
│   │   ├── dev_agent.json
│   │   ├── qa_agent.json
│   │   └── orchestrator.json
│   └── workflows/
│       └── feature_pipeline.json
└── agent_runner.py
```

Decisoes tecnicas e dependencias iniciais:
- [technical_decisions.md](/Users/vitorcosta/codex-agents-study/agent-skill-projetc/portal-web-scraping/docs/technical_decisions.md)

Versao local de Python registrada para esta base:
- `Python 3.14.3`

## Como os agentes devem trabalhar
### 1. Orchestrator
- carrega o workflow principal
- garante que todos os agentes compartilhem o contexto global
- coordena a ordem entre implementacao e validacao

### 2. Dev Agent
- usa a skill `python_senior_dev`
- implementa a feature seguindo arquitetura hexagonal
- cria codigo e testes no mesmo fluxo

### 3. QA Agent
- usa a skill `qa_engineer`
- valida regressao, criterios de aceite e consistencia dos dados extraidos

### 4. Git Ops
- apoia revisao de diff, organizacao de commits e seguranca operacional

## Pipeline de criacao de features
Fluxo esperado para cada feature:

1. Ler o contexto compartilhado em `.agents/context/application_context.md`
2. Identificar o caso de uso e os contratos de entrada/saida
3. Modelar a feature em termos de dominio, aplicacao e infraestrutura
4. Implementar a feature no `src/`
5. Criar ou atualizar testes no `tests/`
6. Validar o workflow com `agent_runner.py`
7. Revisar diff e preparar integracao

## Contrato inicial da API
Exemplo de objetivo para a primeira API:

`GET /contracts/{city}?params={"id":"MV8yMDMy","mode":"INFO"}`

Resposta JSON esperada, em alto nivel:
```json
{
  "request": {
    "city": "palmeira",
    "params": {
      "id": "MV8yMDMy",
      "mode": "INFO"
    }
  },
  "contract": {
    "municipality_name": "Prefeitura ...",
    "total_value_brl": "R$ 0,00",
    "description": "...",
    "signature_date": "...",
    "start_date": "...",
    "expiration_date": "...",
    "supplier": "...",
    "branch": "...",
    "bid_reference": "...",
    "legal_responsibles": [],
    "managers": [],
    "inspectors": [],
    "items": [
      {
        "number": "1",
        "denomination": "...",
        "quantity": 1,
        "unit_measure": "UN",
        "unit_value_brl": "R$ 0,00",
        "total_value_brl": "R$ 0,00"
      }
    ]
  },
  "persistence": {
    "mode": "test-only",
    "backend": "in-memory"
  },
  "notification": {
    "status": "simulated",
    "recipient": "vitorfelipep@dmmv-tech.com"
  }
}
```

## Persistencia de teste
Nesta fase, a persistencia deve ser simples e explicitamente nao produtiva.

Opcoes aceitaveis:
- armazenamento em memoria
- banco documental local

O objetivo e deixar claro o fluxo de persistencia e indexacao sem adicionar complexidade de infraestrutura definitiva.

## Simulacao de email
A aplicacao deve simular um envio de email registrando:
- data e hora da solicitacao
- cliente solicitante
- titulo da consulta
- descricao da consulta
- remetente/destinatario fixo: `vitorfelipep@dmmv-tech.com`

## Como usar o runner de agentes
Executar:

```bash
python3 agent_runner.py
```

Saida esperada:
- validacao das skills
- validacao dos agentes
- validacao do workflow
- exibicao do pipeline resolvido

## Como evoluir o projeto
- adicionar novos modulos hexagonais dentro de `src/`
- implementar o adaptador Playwright para o portal e-publica
- modelar o documento do contrato e seus itens
- adicionar repositorio de teste em memoria
- criar o caso de uso da consulta de contrato
- expor a API REST com FastAPI
- adicionar simulacao de notificacao por email
- ampliar testes unitarios e de integracao

## Observacao
O projeto esta preparado para evolucao orientada por agentes. O contexto base do negocio e da tecnologia deve permanecer centralizado no arquivo de contexto compartilhado para evitar perda de consistencia entre features.

## Setup local
Instalar dependencias:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e .[dev]
python3 -m playwright install
```

Subir a API:

```bash
uvicorn web_scraping.infrastructure.entrypoints.api.app:app --reload
```
