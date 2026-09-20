from datetime import datetime, timezone
from typing import Any


def asset_document(name: str, description: str, price: float, created_by: str) -> dict[str, Any]:
    return {
        "name": name.strip(),
        "description": description.strip(),
        "price": price,
        "created_by": created_by,
        "owner_id": None,
        "purchased_at": None,
        "created_at": datetime.now(timezone.utc),
    }


def serialize_asset(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "description": doc["description"],
        "price": doc["price"],
        "created_by": doc["created_by"],
        "owner_id": str(doc["owner_id"]) if doc.get("owner_id") else None,
        "purchased_at": doc["purchased_at"].isoformat() if doc.get("purchased_at") else None,
        "created_at": doc["created_at"].isoformat(),
    }
