from datetime import datetime, timezone
from bson import ObjectId
from app.core.database import assets_collection


class AssetRepository:
    async def create(self, document: dict):
        result = await assets_collection.insert_one(document)
        document["_id"] = result.inserted_id
        return document

    async def find_available(self):
        cursor = assets_collection.find({"owner_id": None}).sort("created_at", -1)
        return [doc async for doc in cursor]

    async def find_by_id(self, asset_id: ObjectId):
        return await assets_collection.find_one({"_id": asset_id})

    async def purchase_if_available(self, asset_id: ObjectId, user_id: ObjectId):
        purchased_at = datetime.now(timezone.utc)
        result = await assets_collection.update_one(
            {"_id": asset_id, "owner_id": None},
            {"$set": {"owner_id": user_id, "purchased_at": purchased_at}},
        )
        if result.modified_count != 1:
            return None
        return await self.find_by_id(asset_id)

    async def find_by_owner(self, owner_id: ObjectId):
        cursor = assets_collection.find({"owner_id": owner_id}).sort("purchased_at", -1)
        return [doc async for doc in cursor]

    async def list_all(self):
        cursor = assets_collection.find({}).sort("created_at", -1)
        return [doc async for doc in cursor]
