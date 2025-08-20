from fastapi import FastAPI

app = FastAPI(title="Desafio Conthabil")

@app.get("/")
def root():
    return {"message": "API do Desafio Conthabil rodando 🚀"}