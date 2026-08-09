import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest

JWT_ALGORITHM = "HS256"


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidRefreshTokenError(Exception):
    pass


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
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


def _hash_refresh_token(raw_token: str) -> str:
    # Plain SHA-256 is enough here: the input is a 256-bit random string,
    # not a low-entropy human password, so slow hashing (bcrypt) or a
    # secret-keyed HMAC would add complexity without adding real protection.
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


async def create_refresh_token(db: AsyncSession, user_id: uuid.UUID) -> str:
    raw_token = secrets.token_urlsafe(32)
    refresh_token = RefreshToken(
        user_id=user_id,
        token_hash=_hash_refresh_token(raw_token),
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(refresh_token)
    await db.commit()
    return raw_token


async def verify_refresh_token(db: AsyncSession, raw_token: str) -> RefreshToken:
    token_hash = _hash_refresh_token(raw_token)
    record = await db.scalar(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
    if record is None or record.revoked or record.expires_at < datetime.now(timezone.utc):
        raise InvalidRefreshTokenError()
    return record


async def revoke_refresh_token(db: AsyncSession, user_id: uuid.UUID, raw_token: str) -> None:
    record = await verify_refresh_token(db, raw_token)
    if record.user_id != user_id:
        # Same error as "doesn't exist" — don't reveal that a token valid
        # for someone else exists at all.
        raise InvalidRefreshTokenError()
    record.revoked = True
    await db.commit()
