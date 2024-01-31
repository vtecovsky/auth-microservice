from datetime import datetime, timedelta

import bcrypt
import jwt
from pydantic import BaseModel

from src.config import settings


class Token(BaseModel):
    access_token: str
    token_type: str


def encode_jwt(
        payload: dict,
        key=settings.PRIVATE_KEY_PATH.read_text(),
        algorithm=settings.ALGORITHM,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRATION,
        expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire)
    encoded = jwt.encode(to_encode, key, algorithm)

    return encoded


def decode_jwt(token: str | bytes,
               public_key=settings.PUBLIC_KEY_PATH.read_text(),
               algorithm=settings.ALGORITHM):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
        password: str,
        hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
