from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from api.models.database import Base


class District(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    division_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    bn_name: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    long: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<District(id={self.id}, name={self.name})>"
