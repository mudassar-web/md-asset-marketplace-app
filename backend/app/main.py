from contextlib import asynccontextmanager
import logging
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError
from app.core.config import settings
from app.core.database import connect_to_mongodb, close_mongodb, users_collection
from app.core.logging import configure_logging
from app.core.security import hash_password
from app.models.user import user_document
from app.routers import auth, dashboard, admin
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    await connect_to_mongodb()
    # Bootstrap is idempotent. The password is never stored in plaintext.
    admin_email = settings.admin_email.lower().strip()
    if not await users_collection.find_one({"email": admin_email}):
        try:
            await users_collection.insert_one(
                user_document(admin_email, hash_password(settings.admin_password), "System Admin", "admin")
            )
            logger.info("Bootstrap admin created: %s", admin_email)
        except DuplicateKeyError:
            pass
    yield
    await close_mongodb()


app = FastAPI(title="Asset Marketplace API", version="2.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Unhandled exception request_id=%s path=%s", request_id, request.url.path)
        response = JSONResponse(status_code=500, content={"detail": "Internal server error", "request_id": request_id})
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(Exception)
async def unhandled_exception(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.exception("Unhandled exception request_id=%s", request_id, exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "request_id": request_id})


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "environment": settings.app_env, "currentTimestamp": datetime.now(timezone.utc)}


@app.get("/ready", tags=["Health"])
async def ready():
    from app.core.database import client
    await client.admin.command("ping")
    return {"status": "ready"}


app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(admin.router)
