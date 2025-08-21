from fastapi import FastAPI
from app.database import engine, Base
from app.routes.publicacao import router as publicacao_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Desafio Conthabil")

@app.get("/")
def root():
    return {"message": "API do Desafio Conthabil rodando "}


app.include_router(publicacao_router, prefix="/api")
