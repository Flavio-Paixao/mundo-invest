from fastapi import FastAPI
from app.database import engine, Base
from app.routes import clientes, webhooks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mundo Invest — Client Management API",
    description="API para gerenciamento de clientes e integracao com o Pipefy.",
    version="1.0.0",
)

app.include_router(clientes.router)
app.include_router(webhooks.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "Mundo Invest API", "version": "1.0.0"}
