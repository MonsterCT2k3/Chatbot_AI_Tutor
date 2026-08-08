import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.services.auth_service import decode_access_token

# auto_error=False so a missing token also flows through our own
# credentials_exception below (same code/message as an invalid one),
# instead of FastAPI's default 403 with a plain-string detail.
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"code": "INVALID_TOKEN", "message": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise credentials_exception

    try:
        user_id = uuid.UUID(decode_access_token(credentials.credentials))
    except (JWTError, ValueError):
        raise credentials_exception

    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user
