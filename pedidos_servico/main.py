from fastapi import FastAPI
from routes import router

app = FastAPI(title="API de Pedidos")

# Incluindo as rotas
app.include_router(router)

# Rota de verificação
@app.get("/status")
def verificar_status():
    return {"status": "ok"}