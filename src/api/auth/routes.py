from fastapi import APIRouter, Depends

from src.api.auth.utils import Token, encode_jwt, hash_password
from src.api.dependencies import Dependencies
from src.repositories.users.abc import AbstractUserRepository
from src.schemas.users import ViewUser, CreateUser
from src.api.auth.dependencies import get_current_active_user, validate_auth_user

router = APIRouter(prefix="/users", tags=["Auth"])


@router.post("/login/", response_model=Token)
async def login(user: ViewUser = Depends(validate_auth_user)):
    jwt_payload = {
        "sub": user.id,
        "email": user.email,
    }
    access_token = encode_jwt(payload=jwt_payload)
    return Token(
        access_token=access_token,
        token_type="Bearer",
    )


@router.post("/")
async def register(user: CreateUser) -> ViewUser:
    user_repository = Dependencies.get(AbstractUserRepository)
    user = await user_repository.create(user)

    return user


@router.get("/me/")
async def auth_user_me(user: ViewUser = Depends(get_current_active_user)):
    return {
        "id": user.id,
        "email": user.email
    }


@router.post("/reset-password/{token}/")
async def reset_password(new_password: str, user: ViewUser = Depends(get_current_active_user)):
    user_repository = Dependencies.get(AbstractUserRepository)
    new_password = hash_password(new_password)
    await user_repository.update(email=user.email, password=new_password)
