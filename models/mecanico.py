from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base

class Mecanico(Base):
    __tablename__ = "mecanicos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    documento: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    nombre_completo: Mapped[str] = mapped_column(String(100), nullable=False)
    especialidad: Mapped[str] = mapped_column(String(50), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)