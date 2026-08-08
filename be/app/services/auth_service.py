from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest

JWT_ALGORITHM = "HS256"


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> str:
    """Returns the user_id encoded in the token. Raises jose.JWTError on an expired or invalid token."""
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return payload["sub"]


async def register_user(db: AsyncSession, payload: SignupRequest) -> User:
    existing = await db.scalar(select(User).where(User.email == payload.email))
    if existing is not None:
        raise EmailAlreadyRegisteredError()

    user = User(email=payload.email, hashed_password=hash_password(payload.password), name=payload.name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, payload: LoginRequest) -> User:
    user = await db.scalar(select(User).where(User.email == payload.email))
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise InvalidCredentialsError()
    return user
