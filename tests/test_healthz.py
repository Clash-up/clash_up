import pytest
from tests.fixtures import ClientFixture


class TestHealthz(ClientFixture):
    @pytest.mark.asyncio
    async def test_healthz(self, async_client):
        response = await async_client.get("/healthz")

        assert response.status_code == 200
        assert response.json() == {"ok": True}
