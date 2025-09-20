import uuid

from pydantic import NonNegativeInt
from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base
from shared.types import Role


class BaseClashModel(Base):
    __abstract__ = True
    id: Mapped[uuid.UUID] = mapped_column(
        uuid.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )


class Player(BaseClashModel):
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    tag: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    trophies: Mapped[NonNegativeInt] = mapped_column(Integer, nullable=False)
    donations: Mapped[NonNegativeInt] = mapped_column(Integer, nullable=False)
    donations_received: Mapped[NonNegativeInt] = mapped_column(Integer, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    town_hall_level: Mapped[NonNegativeInt] = mapped_column(Integer, nullable=False)
