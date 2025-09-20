import httpx
from typing import Any, Optional, Dict

from shared.settings import settings
from shared.utils import encode_tag as e
from services.coc.types import ClanInfo, CurrentWar


class CoCClient:
    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url="https://api.clashofclans.com/v1/",
            headers={"Authorization": f"Bearer {settings.COC_TOKEN}"},
        )

    async def close(self):
        await self._client.aclose()

    async def api_get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        response = await self._client.get(endpoint, params=params)
        response.raise_for_status()
        return response

    async def current_war(self, clan_tag: str = settings.CLAN_TAG) -> CurrentWar:
        endpoint = f"clans/{e(clan_tag)}/currentwar"
        return CurrentWar.model_validate((await self.api_get(endpoint)).json())

    async def current_raid(self, clan_tag: str = settings.CLAN_TAG) -> Dict[str, Any]:
        endpoint = f"clans/{e(clan_tag)}/capitalraidseasons"
        return (await self.api_get(endpoint)).json()

    async def clan_info(self, clan_tag: str = settings.CLAN_TAG) -> ClanInfo:
        endpoint = f"clans/{e(clan_tag)}"
        return ClanInfo.model_validate((await self.api_get(endpoint)).json())

    async def player_info(self, player_tag: str) -> Dict[str, Any]:
        endpoint = f"players/{e(player_tag)}"
        return (await self.api_get(endpoint)).json()
