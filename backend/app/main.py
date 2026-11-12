import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.connection import ensure_database, wait_for_server
from app.db.schema import ensure_schema
from app.routers import health

settings = get_settings()
logging.basicConfig(level=settings.log_level, format="%(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once on startup, before the first request.
    wait_for_server()
    ensure_schema(ensure_database(settings.arango_db))
    yield
    # Code after yield would run on shutdown.


app = FastAPI(
    title="Auto Diagnostic Knowledge Base",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
