from sqlalchemy import String, Date, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Publicacao(Base):
    __tablename__ = "publicacoes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(500), unique=True, index=True, nullable=False)
    competencia: Mapped[str] = mapped_column(String(7), index=True, nullable=False)  # Ex: "2025-07"
    data_publicacao: Mapped[Date] = mapped_column(Date, nullable=False)


    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
