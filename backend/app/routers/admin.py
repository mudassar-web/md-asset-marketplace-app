from fastapi import APIRouter, Depends, status
from app.dependencies import get_current_admin
from app.models.asset import serialize_asset
from app.models.user import serialize_user
from app.schemas.asset import AssetCreate
from app.services.assets import AssetService
from app.repositories.users import UserRepository

router = APIRouter(prefix="/api/admin", tags=["Admin"])
assets = AssetService()
users = UserRepository()


@router.post("/assets", status_code=status.HTTP_201_CREATED)
async def create_asset(payload: AssetCreate, admin: dict = Depends(get_current_admin)):
    asset = await assets.create(payload.name, payload.description, payload.price, admin["_id"])
    return {"message": "Asset created successfully", "asset": serialize_asset(asset)}


@router.get("/users")
async def list_users(_: dict = Depends(get_current_admin)):
    return {"users": [serialize_user(doc) for doc in await users.list_all()]}


@router.get("/assets")
async def list_all_assets(_: dict = Depends(get_current_admin)):
    return {"assets": [serialize_asset(doc) for doc in await assets.assets.list_all()]}
