from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware

from db.base import init_db
from routes.data import data_router
from typing import Any, cast

from core.constants import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here (e.g., connect to DB)
    app.client = init_db(settings.MONGO_DB_CONNECTION_STRING, settings.MONGO_DB_NAME)
    yield
    # Shutdown code here (e.g., close DB connection)
    app.client.close()

app = FastAPI(title="FARM API")

# Allow your React dev server to hit the API
app.add_middleware(cast(Any, FastAPICORSMiddleware),
    allow_origins=["*"],  # adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(data_router)

@app.get('/')
async def root():
    return {"message": "FARM API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}
