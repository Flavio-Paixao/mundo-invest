from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class ClienteCreate(BaseModel):
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float

    @field_validator("cliente_nome")
    @classmethod
    def nome_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("Nome do cliente não pode ser vazio.")
        return v.strip()

    @field_validator("tipo_solicitacao")
    @classmethod
    def tipo_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("Tipo de solicitação não pode ser vazio.")
        return v.strip()

    @field_validator("valor_patrimonio")
    @classmethod
    def patrimonio_positivo(cls, v):
        if v < 0:
            raise ValueError("Valor do patrimônio não pode ser negativo.")
        return v


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: Optional[str]
    pipefy_card_id: Optional[str]
    criado_em: Optional[datetime]

    model_config = {"from_attributes": True}


class WebhookPayload(BaseModel):
    event_id: str
    card_id: str
    cliente_email: EmailStr
    timestamp: datetime

    @field_validator("event_id")
    @classmethod
    def event_id_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("event_id não pode ser vazio.")
        return v.strip()

    @field_validator("card_id")
    @classmethod
    def card_id_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("card_id não pode ser vazio.")
        return v.strip()


class WebhookResponse(BaseModel):
    mensagem: str
    cliente_email: str
    status: str
    prioridade: str
    event_id: str
