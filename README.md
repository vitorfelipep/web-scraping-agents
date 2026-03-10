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
- `application/`: casos de uso e contratos de entrada/saida
- `ports/`: interfaces para scraping, repositorio e notificacao
- `adapters/`: implementacoes para portal web, banco local e email
- `entrypoints/`: API REST

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
├── src/
├── tests/
├── .github/
│   ├── CODEOWNERS
│   ├── pull_request_template.md
│   ├── ISSUE_TEMPLATE/
│   │   ├── feature_request.md
│   │   └── config.yml
│   └── workflows/
│       └── ci.yml
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

## Governanca no GitHub
O projeto foi preparado para um fluxo controlado por Pull Request.

Arquivos adicionados:
- [.github/CODEOWNERS](/Users/vitorcosta/codex-agents-study/agent-skill-projetc/portal-web-scraping/.github/CODEOWNERS): solicita sua revisao em qualquer alteracao
- [.github/pull_request_template.md](/Users/vitorcosta/codex-agents-study/agent-skill-projetc/portal-web-scraping/.github/pull_request_template.md): padroniza o conteudo dos PRs
- [.github/ISSUE_TEMPLATE/feature_request.md](/Users/vitorcosta/codex-agents-study/agent-skill-projetc/portal-web-scraping/.github/ISSUE_TEMPLATE/feature_request.md): padroniza a abertura de demandas
- [.github/workflows/ci.yml](/Users/vitorcosta/codex-agents-study/agent-skill-projetc/portal-web-scraping/.github/workflows/ci.yml): valida o runner e executa os testes em PR e push para `main`

Fluxo esperado:
1. Abrir uma issue de feature
2. Atualizar a `main` local com `git checkout main` e `git pull origin main`
3. Criar branch `feature/...` somente a partir da `main` atualizada
4. Verificar divergencias ou conflitos com a `main` antes de iniciar a implementacao
5. Implementar a mudanca na branch
6. Abrir PR para `main`
7. Aguardar sua revisao e aprovacao
8. Fazer merge apenas apos aprovacao

## Identidade dos agentes nos commits
Os agentes podem assinar commits com nomes proprios, enquanto a aprovacao e o merge continuam sob sua conta no GitHub.

Convencao atual:
- `dev_agent` -> `DMMV Dev Agent`
- `qa_agent` -> `DMMV QA Agent`
- `orchestrator` -> `DMMV Orchestrator`

Metadados de Git configurados nos JSONs dos agentes:
- `display_name`
- `git_name`
- `git_email`

Email padrao definido:
- `vitorfelipep@gmail.com`

Isso significa:
- o autor do commit pode aparecer como agente
- o aprovador continua sendo `@vitorfelipep` via GitHub
- `CODEOWNERS` continua representando revisao humana, nao agentes

## Como configurar isso no GitHub
Depois de subir estes arquivos para o repositrio, configure a branch `main`.

Passo a passo:
1. Acesse `Settings` do repositrio
2. Entre em `Rules` ou `Branches`, dependendo da UI da sua conta
3. Crie uma regra para a branch `main`
4. Defina o alvo como `Branch name pattern = main`
5. Ative `Require a pull request before merging`
6. Ative `Require approvals`
7. Configure `1` aprovacao minima
8. Ative `Dismiss stale pull request approvals when new commits are pushed`
9. Ative `Require conversation resolution before merging`
10. Ative `Require status checks to pass before merging`
11. Selecione o check da workflow `CI` quando ele aparecer apos o primeiro push

Com isso, a `main` fica protegida e o merge passa a depender da sua aprovacao.

## Significado do warning da rule
Mensagem:

`This ruleset does not target any resources and will not be applied.`

Isso significa que a regra foi criada sem apontar para nenhum alvo real. Em geral acontece quando:
- voce criou um ruleset sem definir o pattern da branch
- o pattern nao bate com nenhuma branch existente
- a regra foi criada para um tipo de recurso errado

Para corrigir:
- escolha `Branches` como alvo
- informe `main` em `Branch name pattern`
- confirme que a branch `main` ja existe no repositrio remoto

Se a branch ainda nao existir no GitHub, faca o primeiro push da `main` antes de criar a regra.

## Comandos Git para o fluxo de features
Criar uma branch de feature:

```bash
git checkout main
git pull origin main
git checkout -b feature/nome-da-feature
```

Essa ordem e obrigatoria. Nao crie `feature/...` a partir de uma branch desatualizada.

Antes de abrir o PR, confira se a branch continua alinhada com `main` e resolva conflitos localmente se necessario.

Enviar a branch:

```bash
git push -u origin feature/nome-da-feature
```

Depois, abra o PR no GitHub da branch `feature/nome-da-feature` para `main`.

## Como trocar a autoria Git para um agente
Para commits de implementacao do agente dev:

```bash
git config user.name "DMMV Dev Agent"
git config user.email "vitorfelipep@gmail.com"
```

Para commits do agente de QA:

```bash
git config user.name "DMMV QA Agent"
git config user.email "vitorfelipep@gmail.com"
```

Para voltar sua identidade pessoal no repositorio:

```bash
git config user.name "Vitor Felipe"
git config user.email "vitorfelipep@gmail.com"
```

Para conferir a identidade ativa:

```bash
git config --get user.name
git config --get user.email
```

## Fluxo sugerido de trabalho
- voce cria a issue no GitHub
- o agente atualiza a `main` local antes de criar a branch
- o agente implementa em uma branch `feature/...` criada a partir da `main` atualizada
- o agente abre ou prepara o PR
- voce revisa e aprova
- o merge para `main` acontece so depois da sua aprovacao

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
3. Modelar a feature em termos de dominio, aplicacao, portas e adaptadores
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
- adicionar os modulos hexagonais dentro de `src/`
- implementar o adaptador Playwright para o portal e-publica
- modelar o documento do contrato e seus itens
- adicionar repositorio de teste em memoria
- criar o caso de uso da consulta de contrato
- expor a API REST com FastAPI
- adicionar simulacao de notificacao por email
- ampliar testes unitarios e de integracao

## Observacao
O projeto esta preparado para evolucao orientada por agentes. O contexto base do negocio e da tecnologia deve permanecer centralizado no arquivo de contexto compartilhado para evitar perda de consistencia entre features.
