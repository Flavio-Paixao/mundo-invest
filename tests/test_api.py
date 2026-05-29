import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine_test = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)

client = TestClient(app)

CLIENTE_VALIDO = {
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000
}

WEBHOOK_VALIDO = {
    "event_id": "evt_123",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2026-05-18T12:00:00Z"
}

def test_criar_cliente_payload_valido():
    response = client.post("/clientes", json=CLIENTE_VALIDO)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "João Silva"
    assert data["status"] == "Aguardando Análise"

def test_criar_cliente_email_invalido():
    payload = {**CLIENTE_VALIDO, "cliente_email": "email-invalido"}
    response = client.post("/clientes", json=payload)
    assert response.status_code == 422

def test_criar_cliente_campos_obrigatorios_ausentes():
    response = client.post("/clientes", json={"cliente_nome": "João"})
    assert response.status_code == 422

def test_criar_cliente_duplicado():
    client.post("/clientes", json=CLIENTE_VALIDO)
    response = client.post("/clientes", json=CLIENTE_VALIDO)
    assert response.status_code == 409
    assert "já cadastrado" in response.json()["detail"]

def test_criar_cliente_patrimonio_negativo():
    payload = {**CLIENTE_VALIDO, "valor_patrimonio": -1000}
    response = client.post("/clientes", json=payload)
    assert response.status_code == 422

def test_webhook_prioridade_alta_patrimonio_igual_limite():
    payload_cliente = {**CLIENTE_VALIDO, "valor_patrimonio": 200000}
    client.post("/clientes", json=payload_cliente)
    response = client.post("/webhooks/pipefy/card-updated", json=WEBHOOK_VALIDO)
    assert response.status_code == 200
    assert response.json()["prioridade"] == "prioridade_alta"

def test_webhook_prioridade_alta_patrimonio_acima_limite():
    client.post("/clientes", json=CLIENTE_VALIDO)
    response = client.post("/webhooks/pipefy/card-updated", json=WEBHOOK_VALIDO)
    assert response.status_code == 200
    assert response.json()["prioridade"] == "prioridade_alta"

def test_webhook_prioridade_normal_patrimonio_abaixo_limite():
    payload_cliente = {**CLIENTE_VALIDO, "valor_patrimonio": 150000}
    client.post("/clientes", json=payload_cliente)
    response = client.post("/webhooks/pipefy/card-updated", json=WEBHOOK_VALIDO)
    assert response.status_code == 200
    assert response.json()["prioridade"] == "prioridade_normal"

def test_webhook_atualiza_status_cliente():
    client.post("/clientes", json=CLIENTE_VALIDO)
    response = client.post("/webhooks/pipefy/card-updated", json=WEBHOOK_VALIDO)
    assert response.status_code == 200
    assert response.json()["status"] == "Processado"

def test_webhook_idempotencia_event_id_duplicado():
    client.post("/clientes", json=CLIENTE_VALIDO)
    response1 = client.post("/webhooks/pipefy/card-updated", json=WEBHOOK_VALIDO)
    assert response1.status_code == 200
    response2 = client.post("/webhooks/pipefy/card-updated", json=WEBHOOK_VALIDO)
    assert response2.status_code == 409
    assert "já foi processado" in response2.json()["detail"]

def test_webhook_diferentes_event_ids_sao_processados():
    payload_cliente = {**CLIENTE_VALIDO, "cliente_email": "maria@example.com"}
    client.post("/clientes", json=payload_cliente)
    webhook1 = {**WEBHOOK_VALIDO, "cliente_email": "maria@example.com", "event_id": "evt_001"}
    response1 = client.post("/webhooks/pipefy/card-updated", json=webhook1)
    assert response1.status_code == 200

def test_webhook_cliente_nao_encontrado():
    webhook = {**WEBHOOK_VALIDO, "cliente_email": "naoexiste@example.com"}
    response = client.post("/webhooks/pipefy/card-updated", json=webhook)
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]
