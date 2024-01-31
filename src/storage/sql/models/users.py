from sqlalchemy.orm import Mapped, mapped_column

from src.storage.sql.__mixin__ import IdMixin
from src.storage.sql.models import Base


class User(Base, IdMixin):
    __tablename__ = 'users'
    firstname: Mapped[str]
    lastname: Mapped[str]
    password: Mapped[bytes]
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool]
