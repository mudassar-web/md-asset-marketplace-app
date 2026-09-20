from datetime import datetime, timezone
from app.core.database import sessions_collection


class SessionRepository:
    async def create(self, user_id, token_hash: str, expires_at: datetime):
        document = {
            "user_id": user_id,
            "token_hash": token_hash,
            "expires_at": expires_at,
            "created_at": datetime.now(timezone.utc),
        }
        await sessions_collection.insert_one(document)
        return document

    async def find_valid(self, token_hash: str):
        return await sessions_collection.find_one({
            "token_hash": token_hash,
            "expires_at": {"$gt": datetime.now(timezone.utc)},
        })

    async def delete(self, token_hash: str):
        await sessions_collection.delete_one({"token_hash": token_hash})
