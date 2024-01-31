from typing import TypeVar, Type
from pydantic import BaseModel as PydanticModel
from sqlalchemy import insert, and_, select, ColumnElement, inspect
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.sql.models import Base

ViewType = TypeVar("ViewType", bound=PydanticModel)
CreateType = TypeVar("CreateType", bound=PydanticModel)
UpdateType = TypeVar("UpdateType", bound=PydanticModel)

ModelType = TypeVar("ModelType", bound=Base)


class CRUD:
    def __init__(self, model: Type[ModelType], CreateScheme: Type[CreateType], ViewScheme: Type[ViewType]):
        self._Model = model
        self._CreateScheme = CreateScheme
        self._ViewScheme = ViewScheme
        # self._UpdateScheme = UpdateScheme

    async def create(self, session: AsyncSession, data: CreateType):
        insert_query = insert(self._Model).values(data.model_dump()).returning(self._Model)
        obj = await session.scalar(insert_query)
        await session.commit()
        return self._ViewScheme.from_orm(obj)

    async def read(self, session: AsyncSession, **columns):
        query = select(self._Model).where(*[getattr(self._Model, column) == value for column, value in columns.items()])
        obj = await session.scalar(query)
        return self._ViewScheme.from_orm(obj) if obj else None
