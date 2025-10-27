from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware

from db.base import init_db
from models.secret_key import SecretKeyIndex
from routes import alert_router
from typing import Any, cast

from models.alerts import BaseAlert
from decouple import config

DB_URL = config('MONGO_DB_CONNECTION_STRING')
DB_NAME = config('MONGO_DB_NAME')


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here (e.g., connect to DB)
    app.client = await init_db(DB_URL, DB_NAME, models=[BaseAlert, SecretKeyIndex])

    yield
    # Shutdown code here (e.g., close DB connection)
    app.client.close()

app = FastAPI(title="FARM API", lifespan=lifespan)

# CORS: allow React dev server only
app.add_middleware(
    FastAPICORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(alert_router)

@app.get('/')
async def root():
    return {"message": "FARM API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}
