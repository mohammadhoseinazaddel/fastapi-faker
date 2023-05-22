import asyncio
import os
import motor.motor_asyncio

from system.config import settings


class MongoDB:
    db_client: motor.motor_asyncio.AsyncIOMotorClient = None

    def get_db(self, db=None) -> motor.motor_asyncio.AsyncIOMotorClient:
        if db is None:
            db = settings.MONGODB_DBNAME
        return self.db_client.db

    async def connect_db(self):
        """Create database connection."""
        self.db_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
        self.db_client.get_io_loop = asyncio.get_running_loop
        print('MongoDB connected')

    async def close_db(self):
        """Close database connection."""
        self.db_client.close()

    async def drop_collection(self, collection_name):
        await self.db_client.drop_collection(collection_name)


mongodb = MongoDB()
