from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
from app.database import Database
from app.api.v1 import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """"""
    logger.info("Starting application")
    app.state.db = Database()
    await app.state.db.connect()
    yield
    logger.info("Stopping application")
    await app.state.db.disconnect()


app: FastAPI = FastAPI(
    title="TaskIt API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

app.include_router(router)


@app.get("/", response_model=dict)
async def root():
    """"""
    return {"message": "TaskIt API"}
