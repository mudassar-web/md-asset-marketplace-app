from fastapi import HTTPException
from bson import ObjectId
from app.models.asset import asset_document
from app.repositories.assets import AssetRepository


class AssetService:
    def __init__(self):
        self.assets = AssetRepository()

    @staticmethod
    def object_id(value: str) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise HTTPException(status_code=400, detail="Invalid asset id")
        return ObjectId(value)

    async def create(self, name: str, description: str, price: float, admin_id: ObjectId):
        return await self.assets.create(asset_document(name, description, price, str(admin_id)))

    async def buy(self, asset_id: str, user_id: ObjectId):
        object_id = self.object_id(asset_id)
        asset = await self.assets.purchase_if_available(object_id, user_id)
        if not asset:
            raise HTTPException(status_code=409, detail="Asset is unavailable or already purchased")
        return asset
