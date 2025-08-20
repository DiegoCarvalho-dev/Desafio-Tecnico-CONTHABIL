from fastapi import FastAPI
from app.database import engine, Base
from app.routes import publicacoes_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Desafio Conthabil")

@app.get("/")
def root():
    return {"message": "API do Desafio Conthabil rodando "}


app.include_router(publicacoes_router)
