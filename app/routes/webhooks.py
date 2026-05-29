from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import WebhookPayload, WebhookResponse
from app.services.cliente import processar_webhook

router = APIRouter(prefix="/webhooks/pipefy", tags=["Webhooks"])


@router.post("/card-updated", response_model=WebhookResponse)
def card_atualizado(payload: WebhookPayload, db: Session = Depends(get_db)):
    return processar_webhook(db, payload)
