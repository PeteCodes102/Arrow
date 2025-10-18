# from fastapi import Depends, Request
# from motor.motor_asyncio import AsyncIOMotorDatabase
# from app.domain.data.repository import MotorDataRepo
# from app.domain.data.service import DataService
#
# def get_db(request: Request) -> AsyncIOMotorDatabase:
#     return request.app.state.db   # set in lifespan
#
# def get_data_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> DataService:
#     return DataService(MotorDataRepo(db))
import pandas as pd
from fastapi import Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from routes.data import DataService, DataRepository

# Dependency for FastAPI

def get_db(request: Request) -> AsyncIOMotorDatabase:
    return request.app.state.db   # set in lifespan

async def get_service() -> DataService:
    repo = DataRepository()
    return DataService(repo)


