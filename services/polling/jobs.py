import abc
import asyncio
import logging
from typing import TYPE_CHECKING, Iterable

from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.proxy.client import coc_client
from shared.database import DatabaseManager
from shared.models import Player
from shared.settings import settings

if TYPE_CHECKING:
    pass


log = logging.getLogger(__name__)


class BaseJob(abc.ABC):
    job_id: str = "base-job"

    @abc.abstractmethod
    async def run(self) -> None: ...
    @abc.abstractmethod
    def build_trigger(self): ...

    async def gather_all(self, coros: Iterable) -> None:
        await asyncio.gather(*coros)


class PlayerSyncJob(BaseJob):
    job_id = "player-sync"

    def build_trigger(self) -> IntervalTrigger:
        return IntervalTrigger(minutes=settings.POLLING_PLAYER_SYNC)

    async def _update_one(self, session: "AsyncSession", tag: str) -> None:
        # ----------------------------------------------
        # TODO: Poniższy kod jest do refaktoru pod kątem np optymalizacji liczby zapytań do bazy
        player_client = await coc_client.player_info(tag)
        player_db = (
            (await session.execute(select(Player).where(Player.tag == tag))).scalars().first()
        )
        if not player_db:
            player_db = Player(tag=tag)
            session.add(player_db)
        player_db.name = player_client.name
        player_db.trophies = player_client.trophies
        player_db.donations = player_client.donations
        player_db.donations_received = player_client.donations_received
        player_db.role = player_client.role
        player_db.town_hall_level = player_client.town_hall_level

    async def run(self) -> None:
        player_tags = [x.tag for x in (await coc_client.clan_info()).member_list]
        async with DatabaseManager.session(settings.POSTGRES_URL) as session:
            await self.gather_all([self._update_one(session, tag) for tag in player_tags])
            await session.commit()
        # ----------------------------------------------
