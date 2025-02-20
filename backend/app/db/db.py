import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from settings import settings

MONGO_URI = settings.MONGO_URI
DB_NAME = settings.DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
database: Database = client[DB_NAME]

def get_collection(collection_name: str):
    return database[collection_name]