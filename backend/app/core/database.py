from pymongo import AsyncMongoClient
from app.core.config import settings

client = AsyncMongoClient(settings.mongodb_url, tz_aware=True)
db = client[settings.database_name]

users_collection = db["users"]
assets_collection = db["assets"]
sessions_collection = db["sessions"]


async def connect_to_mongodb() -> None:
    await client.admin.command("ping")
    await users_collection.create_index("email", unique=True)
    await assets_collection.create_index([("owner_id", 1), ("purchased_at", -1)])
    await assets_collection.create_index([("owner_id", 1), ("created_at", -1)])
    await assets_collection.create_index("created_by")
    await sessions_collection.create_index("token_hash", unique=True)
    await sessions_collection.create_index("expires_at", expireAfterSeconds=0)


async def close_mongodb() -> None:
    await client.close()
