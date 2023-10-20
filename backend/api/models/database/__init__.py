from datetime import datetime

from pydash import snake_case
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.schema import FetchedValue
from sqlalchemy.sql import functions


class Base(DeclarativeBase):
    """Define a series of common elements that may be applied to mapped classes
    using this class as a base class."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return snake_case(cls.__name__).lower()

    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=functions.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_onupdate=FetchedValue(for_update=True),
        onupdate=functions.now(),
    )
