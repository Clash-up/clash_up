import re
import uuid
from collections import defaultdict

from pydantic import NonNegativeFloat, NonNegativeInt
from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database import Base
from shared.types import Role


class ClashBaseDBModel(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    __abstract__ = True

    def __init_subclass__(cls, **kwargs):
        if not hasattr(cls, "__tablename__"):
            cls.__tablename__ = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        super().__init_subclass__(**kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"


class WarEntry(ClashBaseDBModel):
    war_id: Mapped[uuid.UUID] = mapped_column(  # maybe later ForeignKey
        postgresql.UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    stars: Mapped[NonNegativeInt | None] = mapped_column(Integer, nullable=True)
    destruction_percentage: Mapped[NonNegativeFloat | None] = mapped_column(Integer, nullable=True)
    duration: Mapped[NonNegativeInt | None] = mapped_column(Integer, nullable=True)

    player_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("player.id", ondelete="CASCADE"), nullable=False
    )
    player: Mapped["Player"] = relationship(back_populates="cw_attacks")


class Player(ClashBaseDBModel):
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    tag: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    trophies: Mapped[NonNegativeInt] = mapped_column(Integer, nullable=False)
    donations: Mapped[NonNegativeInt] = mapped_column(Integer, nullable=False)
    donations_received: Mapped[NonNegativeInt] = mapped_column(Integer, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    town_hall_level: Mapped[NonNegativeInt] = mapped_column(Integer, nullable=False)
    # Transformowane na out jako lista list zgrupowana po war_id (w praktyce max 2 elementy)
    cw_attacks: Mapped[list["WarEntry"]] = relationship(
        back_populates="player", cascade="all, delete-orphan"
    )
    # TODO: przechowywanie cwl_attacks

    @property
    def cw_attacks_grouped(self) -> list[list[WarEntry]]:
        grouped = defaultdict(list)
        for entry in self.cw_attacks:
            grouped[entry.war_id].append(entry)
        return list(grouped.values())
