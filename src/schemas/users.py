from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    firstname: str
    lastname: str
    password: str
    email: EmailStr
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class ViewUser(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    password: bytes
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
