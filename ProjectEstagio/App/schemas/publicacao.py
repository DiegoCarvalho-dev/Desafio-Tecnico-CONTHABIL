from datetime import date
from pydantic import BaseModel, HttpUrl, Field, field_validator

class PublicacaoBase(BaseModel):
    url: HttpUrl = Field(..., description="URL pública do PDF no 0x0.st")
    competencia: str = Field(..., pattern=r"^\d{4}-\d{2}$", description="Competência no formato YYYY-MM")
    data_publicacao: date

    @field_validator("competencia")
    @classmethod
    def valida_competencia(cls, v: str) -> str:
        # valida 01-12
        ano, mes = v.split("-")
        m = int(mes)
        if m < 1 or m > 12:
            raise ValueError("competencia deve ser no formato YYYY-MM e mês entre 01 e 12")
        return v

class PublicacaoCreate(PublicacaoBase):
    pass

class PublicacaoOut(PublicacaoBase):
    id: int

    class Config:
        from_attributes = True
