from pydantic import BaseModel, Field


class AssetCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str = Field(min_length=1, max_length=2000)
    price: float = Field(gt=0, le=100000000)
