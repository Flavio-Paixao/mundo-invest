from sqlalchemy.orm import Session
from app.models import Cliente, WebhookEvento
from app.schemas import ClienteCreate, WebhookPayload
from app.services.pipefy import build_create_card_mutation, build_update_card_field_mutation
from fastapi import HTTPException

LIMIAR_PRIORIDADE_ALTA = 200_000.0

def calcular_prioridade(valor_patrimonio: float) -> str:
    if valor_patrimonio >= LIMIAR_PRIORIDADE_ALTA:
        return "prioridade_alta"
    return "prioridade_normal"

def criar_cliente(db: Session, payload: ClienteCreate) -> Cliente:
    cliente_existente = db.query(Cliente).filter(Cliente.email == payload.cliente_email).first()
    if cliente_existente:
        raise HTTPException(status_code=409, detail=f"Cliente com e-mail '{payload.cliente_email}' já cadastrado.")
    novo_cliente = Cliente(nome=payload.cliente_nome, email=payload.cliente_email, tipo_solicitacao=payload.tipo_solicitacao, valor_patrimonio=payload.valor_patrimonio, status="Aguardando Análise")
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    build_create_card_mutation(nome=payload.cliente_nome, email=payload.cliente_email, tipo_solicitacao=payload.tipo_solicitacao, valor_patrimonio=payload.valor_patrimonio)
    return novo_cliente

def processar_webhook(db: Session, payload: WebhookPayload) -> dict:
    evento_existente = db.query(WebhookEvento).filter(WebhookEvento.event_id == payload.event_id).first()
    if evento_existente:
        raise HTTPException(status_code=409, detail=f"Evento '{payload.event_id}' já foi processado. Ignorando duplicata.")
    cliente = db.query(Cliente).filter(Cliente.email == payload.cliente_email).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente com e-mail '{payload.cliente_email}' não encontrado.")
    prioridade = calcular_prioridade(cliente.valor_patrimonio)
    novo_status = "Processado"
    card_id = cliente.pipefy_card_id or payload.card_id
    build_update_card_field_mutation(card_id=card_id, novo_status=novo_status, prioridade=prioridade)
    cliente.status = novo_status
    cliente.prioridade = prioridade
    db.commit()
    db.refresh(cliente)
    novo_evento = WebhookEvento(event_id=payload.event_id, card_id=payload.card_id, cliente_email=payload.cliente_email)
    db.add(novo_evento)
    db.commit()
    return {"mensagem": "Webhook processado com sucesso.", "cliente_email": cliente.email, "status": cliente.status, "prioridade": cliente.prioridade, "event_id": payload.event_id}
