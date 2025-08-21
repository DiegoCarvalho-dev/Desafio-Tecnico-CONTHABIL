# local_server.py
import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
from pathlib import Path

app = FastAPI(title="Diarios Oficiais Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("../data") / "public_pdfs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(400, "Apenas arquivos PDF são permitidos")

        safe_filename = file.filename.replace(" ", "_").replace("/", "_")
        file_path = UPLOAD_DIR / safe_filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_url = f"http://localhost:8000/files/{safe_filename}"

        return {
            "message": "Upload realizado com sucesso",
            "filename": safe_filename,
            "url": file_url,
            "size": os.path.getsize(file_path)
        }

    except Exception as e:
        raise HTTPException(500, f"Erro no upload: {str(e)}")


@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(404, "Arquivo não encontrado")

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename
    )


@app.get("/health")
async def health_check():
    return {"status": "online", "service": "diarios_server"}


if __name__ == "__main__":
    print(" Servidor local iniciando...")
    print(" PDFs disponíveis em: http://localhost:8001/files/nome_do_arquivo.pdf")
    uvicorn.run(app, host="0.0.0.0", port=8001)