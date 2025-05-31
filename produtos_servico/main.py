from fastapi import FastAPI
from routes import router

app = FastAPI(title="API Produtos")

app.include_router(router)

@app.get("/status")
def verificar_status():
    return {"status": "ok"}
