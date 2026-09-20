from fastapi import APIRouter, Cookie, Depends, Response, status
from app.core.config import settings
from app.dependencies import get_current_user
from app.models.user import serialize_user
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/api/users", tags=["Users"])
service = AuthService()
REFRESH_COOKIE = "refresh_token"


def set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE,
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        path="/api/users",
    )


def clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(key=REFRESH_COOKIE, path="/api/users")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest):
    user = await service.register(payload.name, payload.email, payload.password)
    return {"message": "User registered successfully", "user": serialize_user(user)}


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, response: Response):
    user = await service.authenticate(payload.email, payload.password)
    access, refresh = await service.create_session(user)
    set_refresh_cookie(response, refresh)
    return service.public_response(user, access)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(response: Response, refresh_token: str | None = Cookie(default=None)):
    if not refresh_token:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Refresh session not found")
    user, access, new_refresh = await service.refresh_session(refresh_token)
    set_refresh_cookie(response, new_refresh)
    return service.public_response(user, access)


@router.post("/logout", status_code=204)
async def logout(response: Response, refresh_token: str | None = Cookie(default=None)):
    if refresh_token:
        await service.logout(refresh_token)
    clear_refresh_cookie(response)


@router.get("/me")
async def me(user: dict = Depends(get_current_user)):
    return {"user": serialize_user(user)}
