from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from routes.data import data_router
from typing import Any, cast

app = FastAPI(title="FARM API")

# Allow your React dev server to hit the API
app.add_middleware(cast(Any, FastAPICORSMiddleware),
    allow_origins=["*"],  # adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
