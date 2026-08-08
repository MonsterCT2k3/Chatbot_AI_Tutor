from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse, UserResponse
from app.services.auth_service import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    authenticate_user,
    create_access_token,
    register_user,
)

router = APIRouter()


@router.post("/signup", response_model=TokenResponse)
async def signup(payload: SignupRequest, db: AsyncSession = Depends(get_db)):
    try:
        user = await register_user(db, payload)
    except EmailAlreadyRegisteredError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "EMAIL_ALREADY_REGISTERED", "message": "Email already registered"},
        )

    return TokenResponse(access_token=create_access_token(str(user.id)))


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        user = await authenticate_user(db, payload)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Incorrect email or password"},
        )

    return TokenResponse(access_token=create_access_token(str(user.id)))


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    # Stateless JWT: nothing to invalidate server-side. Requiring a valid
    # token here just confirms there was a real session; the frontend is
    # responsible for discarding the token client-side.
    return {}
