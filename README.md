# Mundo Invest - Client Management API

API de gerenciamento de clientes com integracao ao Pipefy via GraphQL.

## Arquitetura

- app/main.py - Ponto de entrada da API
- app/database.py - Configuracao do banco de dados
- app/models.py - Tabelas do banco SQLAlchemy
- app/schemas.py - Validacao de dados Pydantic
- app/routes/clientes.py - POST /clientes
- app/routes/webhooks.py - POST /webhooks/pipefy/card-updated
- app/services/cliente.py - Regras de negocio
- app/services/pipefy.py - Integracao GraphQL Pipefy
- tests/test_api.py - 12 testes automatizados

## Stack

- Python 3.13, FastAPI, SQLAlchemy, Pydantic, SQLite, Pytest

## Como Rodar

pip install -r requirements.txt
uvicorn app.main:app --reload
Acesse: http://localhost:8000/docs

## Testes

pytest tests/ -v
12 testes passando.

## Decisoes Tecnicas

- Separacao de responsabilidades: routes delegam, services concentram logica
- Idempotencia: event_id unico, rejeita duplicatas com 409
- Pipefy: mutations GraphQL isoladas em pipefy.py, prontas para producao
- Prioridade: patrimonio >= R200k = prioridade_alta

## Visao AWS em Producao

- API Gateway + Lambda + Mangum
- RDS PostgreSQL
- DynamoDB para idempotencia
- CloudWatch para logs
- Terraform para infraestrutura como codigo

## Autor

Flavio Paixao - github.com/Flavio-Paixao - linkedin.com/in/flaviopx
