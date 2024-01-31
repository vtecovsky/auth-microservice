from abc import abstractmethod, ABC

from src.schemas.users import CreateUser, ViewUser


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(self, user: CreateUser) -> ViewUser:
        ...

    @abstractmethod
    async def read(self, **params) -> ViewUser:
        ...
