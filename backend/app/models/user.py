from datetime import datetime, timezone
from typing import Any


def user_document(email: str, password_hash: str, name: str, role: str = "user") -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    return {
        "email": email.lower().strip(),
        "name": name.strip(),
        "password_hash": password_hash,
        "role": role,
        "created_at": now,
        "updated_at": now,
    }


def serialize_user(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(doc["_id"]),
        "email": doc["email"],
        "name": doc["name"],
        "role": doc["role"],
        "created_at": doc["created_at"].isoformat(),
    }
