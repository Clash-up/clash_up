from contextlib import asynccontextmanager
from fastapi import FastAPI
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
