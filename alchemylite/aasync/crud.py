from typing import Any

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.inspection import inspect


class AsyncCrudOperation:
    def __init__(self, async_session_factory: async_sessionmaker, model, base):
        self.async_session_factory = async_session_factory
        self.model = model
        self.base = base

    def validate_params(self, params: dict[str, Any]) -> bool:
        model_columns = {column.name: column.type for column in inspect(self.model).columns}
        for key, value in params.items():
            if key not in model_columns:
                raise ValueError(f'Parameter {key} is not a valid column name')
        return True

    async def create(self, params: dict[str, Any]) -> None:
        async with self.async_session_factory() as session:
            model = self.model(**params)
            session.add(model)
            await session.commit()

    async def read(self) -> tuple:
        async with self.async_session_factory() as session:
            query = select(self.model)
            result = await session.execute(query)
            result = result.all()
            return result

    async def update_by_id(self, condition: dict[str, int], params: dict[str, Any]) -> None:
        self.validate_params(params)
        if 'id' not in params:
            raise ValueError(f'Parameter "id" is missing')
        id = condition['id']
        if type(id) is not int:
            raise ValueError(f'Parameter "id" must be an integer')

        async with self.async_session_factory() as session:
            stmt = update(self.model).where(self.model.id == id).values(params)
            await session.execute(stmt)
            await session.commit()

    async def delete_by_id(self, condition: dict[str, Any]) -> None:
        if 'id' not in condition:
            raise ValueError(f'Parameter "id" is missing')
        id = condition['id']
        if type(id) is not int:
            raise ValueError(f'Parameter "id" must be an integer')

        async with self.async_session_factory() as session:
            stmt = delete(self.model).where(self.model.id == id)
            await session.execute(stmt)
            await session.commit()

    async def create_all_tables(self) -> None:
        async with self.async_session_factory() as session:
            self.base.metadata.create_all(bind=session.get_bind())

    async def delete_all_tables(self) -> None:
        async with self.async_session_factory() as session:
            self.base.metadata.drop_all(bind=session.get_bind())