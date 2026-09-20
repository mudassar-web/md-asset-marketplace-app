from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, hash_token
from app.models.user import user_document, serialize_user
from app.repositories.users import UserRepository
from app.repositories.sessions import SessionRepository


class AuthService:
    def __init__(self):
        self.users = UserRepository()
        self.sessions = SessionRepository()

    async def register(self, name: str, email: str, password: str):
        email = email.lower().strip()
        if await self.users.find_by_email(email):
            raise HTTPException(status_code=409, detail="Email is already registered")
        try:
            return await self.users.create(user_document(email, hash_password(password), name))
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail="Email is already registered")

    async def authenticate(self, email: str, password: str):
        user = await self.users.find_by_email(email)
        if not user or not verify_password(password, user["password_hash"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        return user

    async def create_session(self, user: dict):
        access = create_access_token(str(user["_id"]), user["role"])
        refresh, refresh_hash, expires_at = create_refresh_token()
        await self.sessions.create(user["_id"], refresh_hash, expires_at)
        return access, refresh

    async def refresh_session(self, refresh_token: str):
        session = await self.sessions.find_valid(hash_token(refresh_token))
        if not session:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        user = await self.users.find_by_id(session["user_id"])
        if not user:
            await self.sessions.delete(hash_token(refresh_token))
            raise HTTPException(status_code=401, detail="User no longer exists")
        # Rotate the refresh token so a used token cannot be replayed.
        await self.sessions.delete(hash_token(refresh_token))
        access, new_refresh = await self.create_session(user)
        return user, access, new_refresh

    async def logout(self, refresh_token: str):
        await self.sessions.delete(hash_token(refresh_token))

    @staticmethod
    def public_response(user: dict, access_token: str) -> dict:
        return {"access_token": access_token, "token_type": "bearer", "user": serialize_user(user)}
