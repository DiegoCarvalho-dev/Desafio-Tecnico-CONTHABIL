from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PublicacaoCreate, PublicacaoOut
from app.crud import (
    criar_publicacao,
    listar_publicacoes,
    filtrar_por_competencia,
    obter_por_id,
)

router = APIRouter(prefix="/publicacoes", tags=["publicações"])

@router.post("/", response_model=PublicacaoOut, status_code=status.HTTP_201_CREATED)
def post_publicacao(payload: PublicacaoCreate, db: Session = Depends(get_db)):

    pub = criar_publicacao(db, payload)
    return pub

@router.get("/", response_model=List[PublicacaoOut])
def get_publicacoes(
    competencia: Optional[str] = Query(default=None, pattern=r"^\d{4}-\d{2}$", description="YYYY-MM"),
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):

    if competencia:
        return filtrar_por_competencia(db, competencia, limit, offset)
    return listar_publicacoes(db, limit, offset)

@router.get("/{pub_id}", response_model=PublicacaoOut)
def get_publicacao(pub_id: int, db: Session = Depends(get_db)):
    pub = obter_por_id(db, pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")
    return pub
