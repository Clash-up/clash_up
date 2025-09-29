import asyncio
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from shared.database import DatabaseManager
from shared.settings import settings

from api.app import app


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

#TODO: Dokończyć tworzenie nowej sesji to testów
class IsolatedSession:
    @pytest_asyncio.fixture(scope="function")
    async def async_session(self):
        SessionMaker = DatabaseManager.get_async_sessionmaker(settings.POSTGRES_URL)
        async with SessionMaker() as session:
            if (await DatabaseManager.ping(settings.POSTGRES_URL)):

                yield session


class ClientFixture(IsolatedSession):
    @pytest_asyncio.fixture(autouse=True)
    async def async_client(self):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://localhost:8000/api"
        ) as client:
            yield client

