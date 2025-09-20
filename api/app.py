from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from services.coc.client import CoCClient
from services.coc.types import ClanInfo, CurrentWar
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


def get_coc_client() -> CoCClient:
    return app.state.coc


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with DatabaseManager.session(settings.POSTGRES_URL) as session:
        yield session


@api.get("/current_war", response_model=CurrentWar)
async def current_war(client: CoCClient = Depends(get_coc_client)):
    return await client.current_war()


@api.get("/clan_info", response_model=ClanInfo)
async def clan_info(client: CoCClient = Depends(get_coc_client)):
    return await client.clan_info()


@api.get("/zolta_kartka")
async def zolta_kartka(client: CoCClient = Depends(get_coc_client)):
    # potrzebuje przeiterowac po modelu playera,
    # dowiedziec sie ile dni jest afk, jesli pow 1 to go zwraca w liscie z przypisanym powodem
    # dalej przeiterowac po jego statach z wojen jesli nie zaatakowal to zwrocic z przypisanym powodem i statami na wojnach poszczegolnych
    ...


app.include_router(api)
