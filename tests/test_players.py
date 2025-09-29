import pytest
from tests.fixtures import ClientFixture

class TestPlayers(ClientFixture):
    @pytest.mark.asyncio
    async def test_list_players_with_initial_data(self, async_client):
        response = await async_client.get("/players")
        
        assert response.status_code == 200
        assert response.json() == []

