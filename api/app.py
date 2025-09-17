from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from services.coc.client import CoCClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    coc = CoCClient()
    app.state.coc = coc
    try:
        yield
    finally:
        await coc.close()


app = FastAPI(title="CoC API Gateway", lifespan=lifespan)


@app.get("/healthz")
async def healthz():
    return {"ok": True}

def get_coc_client() -> CoCClient:
    return app.state.coc


@app.get("/current_war")
async def current_war(client: CoCClient = Depends(get_coc_client)):
    return await client.current_war()


@app.get("/clan_info")
async def clan_info(client: CoCClient = Depends(get_coc_client)):
    return await client.clan_info()