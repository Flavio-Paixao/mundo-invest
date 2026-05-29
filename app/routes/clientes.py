from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ClienteCreate, ClienteResponse
from app.services.cliente import criar_cliente

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("", response_model=ClienteResponse, status_code=201)
def criar_novo_cliente(payload: ClienteCreate, db: Session = Depends(get_db)):
    return criar_cliente(db, payload)
