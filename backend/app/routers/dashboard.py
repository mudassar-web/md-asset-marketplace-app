from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models.asset import serialize_asset
from app.services.assets import AssetService

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])
service = AssetService()


@router.get("/assets")
async def list_available_assets():
    assets = await service.assets.find_available()
    return {"assets": [serialize_asset(doc) for doc in assets]}


@router.post("/assets/{asset_id}/buy")
async def buy_asset(asset_id: str, user: dict = Depends(get_current_user)):
    asset = await service.buy(asset_id, user["_id"])
    return {"message": "Asset purchased successfully", "asset": serialize_asset(asset)}


@router.get("/my-assets")
async def my_assets(user: dict = Depends(get_current_user)):
    assets = await service.assets.find_by_owner(user["_id"])
    return {"assets": [serialize_asset(doc) for doc in assets]}
