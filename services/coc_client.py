import httpx
from typing import Any, Optional, Dict

from shared import settings

class CoCClient:
    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url="https://api.clashofclans.com/v1/",
            headers={"Authorization": f"Bearer {settings.COC_TOKEN}"},
        )

    async def __aenter__(self) -> "CoCClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self._client.aclose()

    async def api_get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        response = await self._client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()