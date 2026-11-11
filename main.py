from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import engine, Base
from models.orden import Orden
from models.mecanico import Mecanico
from models.repuesto import Repuesto
from routers import ordenes, mecanicos, repuestos

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Taller de Motos API", lifespan=lifespan)

app.include_router(ordenes.router)
app.include_router(mecanicos.router)
app.include_router(repuestos.router)

@app.get("/")
async def root():
    return {"mensaje": "API del Taller de Motos funcionando"}