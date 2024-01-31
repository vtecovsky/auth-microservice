from asyncpg import UniqueViolationError, IntegrityConstraintViolationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.utils import hash_password
from src.exceptions import UserExists
from src.repositories.crud import CRUD
from src.repositories.users.abc import AbstractUserRepository
from src.schemas.users import ViewUser, CreateUser
from src.storage.sql import AbstractSQLAlchemyStorage
from src.storage.sql.models.users import User as UserModel

crud = CRUD(UserModel, CreateUser, ViewUser)


class SqlUserRepository(AbstractUserRepository):
    storage: AbstractSQLAlchemyStorage

    def __init__(self, storage: AbstractSQLAlchemyStorage):
        self.storage = storage

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def create(self, user: CreateUser) -> ViewUser:
        user.password = hash_password(user.password)
        try:
            async with self._create_session() as session:
                return await crud.create(session, user)
        except IntegrityError:
            raise UserExists()

    async def read(self, **params) -> ViewUser:
        async with self._create_session() as session:
            return await crud.read(session, **params)

    async def update(self, **params) -> ViewUser:
        async with self._create_session() as session:
            return await crud.update(session, **params)
