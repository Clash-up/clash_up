from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.polling.managers import scheduler
from services.proxy.client import client
from shared.database import DatabaseManager, init_models
from shared.models import Player
from shared.pyd_models import PlayerRead
from shared.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = await DatabaseManager.get_engine(settings.POSTGRES_URL)
    await init_models(engine)
    scheduler.start()
    client.start()
    try:
        yield
    finally:
        await client.close()
        scheduler.shutdown()
        await DatabaseManager.dispose_engine(settings.POSTGRES_URL)


app = FastAPI(title="CoC API Gateway", lifespan=lifespan, docs_url="/api/docs")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter(prefix="/api")


@api.get("/healthz")
async def healthz():
    return {"ok": True}


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with DatabaseManager.session(settings.POSTGRES_URL) as session:
        yield session


@api.get("/players", response_model=list[PlayerRead])
async def list_players(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Player).options(selectinload(Player.cw_attacks)))
    players = result.scalars().all()
    return [PlayerRead.model_validate(p) for p in players]


@api.get("/wip")
async def wip():
    # potrzebuje przeiterowac po modelu playera,
    # dowiedziec sie ile dni jest afk, jesli pow 1 to go zwraca w liscie z przypisanym powodem
    # dalej przeiterowac po jego statach z wojen jesli nie zaatakowal to zwrocic z przypisanym powodem i statami na wojnach poszczegolnych
    ...


app.include_router(api)
