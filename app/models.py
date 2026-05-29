from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    tipo_solicitacao = Column(String, nullable=False)
    valor_patrimonio = Column(Float, nullable=False)
    status = Column(String, default="Aguardando Análise")
    prioridade = Column(String, nullable=True)
    pipefy_card_id = Column(String, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())


class WebhookEvento(Base):
    __tablename__ = "webhook_eventos"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True, nullable=False)
    card_id = Column(String, nullable=False)
    cliente_email = Column(String, nullable=False)
    processado = Column(Boolean, default=True)
    processado_em = Column(DateTime(timezone=True), server_default=func.now())
