import abc
import asyncio
import logging
from typing import TYPE_CHECKING, Iterable

from apscheduler.triggers.interval import IntervalTrigger

from services.proxy.client import client
from shared.settings import settings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


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
        return IntervalTrigger(seconds=settings.POLLING_PLAYER_SYNC)

    async def _update_one(self, session: "AsyncSession", tag: str) -> None:
        # ----------------------------------------------
        # TODO: Poniższy kod jest do refaktoru pod kątem np optymalizacji liczby zapytań do bazy

        # TODO: dokończyć gdy będzie pyd model Player
        data = await client.player_info(tag)
        log.error(f"Updating player {tag} with data: {data}")
        # result = await session.execute(select(Player).where(Player.tag == tag))
        # player = result.scalars().first()
        # if not player:
        #     player = Player(tag=tag)
        #     session.add(player)

    async def run(self) -> None:
        player_tags = [x.tag for x in (await client.clan_info()).member_list]
        # async with DatabaseManager.session(settings.POSTGRES_URL) as session:
        await self.gather_all(
            [
                self._update_one(
                    # session,
                    tag
                )
                for tag in player_tags
            ]
        )
        # await session.commit()
        # ----------------------------------------------
