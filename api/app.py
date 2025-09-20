from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import AsyncGenerator
from services.coc.client import CoCClient
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database import DatabaseManager, init_models
from shared.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = await DatabaseManager.get_engine(settings.POSTGRES_URL, echo=True)
    await init_models(engine)
    coc = CoCClient()
    app.state.coc = coc
    try:
        yield
    finally:
        await coc.close()
        await DatabaseManager.dispose_engine(settings.POSTGRES_URL)


app = FastAPI(title="CoC API Gateway", lifespan=lifespan)


@app.get("/healthz")
async def healthz():
    return {"ok": True}


def get_coc_client() -> CoCClient:
    return app.state.coc


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with DatabaseManager.session(settings.POSTGRES_URL) as session:
        yield session


@app.get("/current_war")
async def current_war(client: CoCClient = Depends(get_coc_client)):
    return await client.current_war()


@app.get("/clan_info")
async def clan_info(client: CoCClient = Depends(get_coc_client)):
    return await client.clan_info()
