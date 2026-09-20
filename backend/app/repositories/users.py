from bson import ObjectId
from app.core.database import users_collection


class UserRepository:
    async def find_by_email(self, email: str):
        return await users_collection.find_one({"email": email.lower().strip()})

    async def find_by_id(self, user_id: ObjectId):
        return await users_collection.find_one({"_id": user_id})

    async def create(self, document: dict):
        result = await users_collection.insert_one(document)
        document["_id"] = result.inserted_id
        return document

    async def list_all(self):
        cursor = users_collection.find({}, {"password_hash": 0}).sort("created_at", -1)
        return [doc async for doc in cursor]
