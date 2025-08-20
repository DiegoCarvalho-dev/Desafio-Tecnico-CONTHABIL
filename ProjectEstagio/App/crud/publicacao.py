from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.publicacao import Publicacao
from app.schemas.publicacao import PublicacaoCreate

def criar_publicacao(db: Session, dados: PublicacaoCreate) -> Publicacao:

    existe = db.scalar(select(Publicacao).where(Publicacao.url == str(dados.url)))
    if existe:
        return existe
    entidade = Publicacao(
        url=str(dados.url),
        competencia=dados.competencia,
        data_publicacao=dados.data_publicacao
    )
    db.add(entidade)
    db.commit()
    db.refresh(entidade)
    return entidade

def listar_publicacoes(db: Session, limit: int = 100, offset: int = 0) -> List[Publicacao]:
    stmt = select(Publicacao).order_by(Publicacao.data_publicacao.desc()).limit(limit).offset(offset)
    return list(db.execute(stmt).scalars().all())

def filtrar_por_competencia(db: Session, competencia: str, limit: int = 100, offset: int = 0) -> List[Publicacao]:
    stmt = (
        select(Publicacao)
        .where(Publicacao.competencia == competencia)
        .order_by(Publicacao.data_publicacao.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.execute(stmt).scalars().all())

def obter_por_id(db: Session, pub_id: int) -> Optional[Publicacao]:
    return db.get(Publicacao, pub_id)