from fastapi import Depends, HTTPException, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from starlette import status

from jwt.exceptions import InvalidTokenError

from src.api.auth.utils import validate_password, decode_jwt
from src.api.dependencies import Dependencies
from src.repositories.users.abc import AbstractUserRepository
from src.schemas.users import ViewUser

bearer_scheme = HTTPBearer(
    scheme_name="Bearer",
    description="Your JSON Web Token (JWT)",
    bearerFormat="JWT",
    auto_error=True,
)


def get_current_token_payload(bearer: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> ViewUser:
    try:
        token = bearer and bearer.credentials
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token error: {e}")
    return payload


async def get_current_user(payload: dict = Depends(get_current_token_payload)) -> ViewUser:
    email: str | None = payload.get("email")
    user_repository = Dependencies.get(AbstractUserRepository)
    if not (user := await user_repository.read(email=email)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user


def get_current_active_user(user: ViewUser = Depends(get_current_user)):
    if user.is_active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")


async def validate_auth_user(
        email: str = Form(),
        password: str = Form()
):
    unauthorized_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Invalid username or password")
    user_repository = Dependencies.get(AbstractUserRepository)
    if not (user := await user_repository.read(email=email)):
        raise unauthorized_exception

    if validate_password(password, user.password):
        return user

    raise unauthorized_exception
