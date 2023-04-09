from collections.abc import Iterable

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    async def create(self, session: AsyncSession):
        session.add(self)
        await session.flush()
        await session.commit()
        return self

    @classmethod
    async def bulk_create(cls, instances: list | object, session: AsyncSession):
        session.add_all(instances)
        await session.flush()
        await session.commit()
        return instances

    @classmethod
    def get_filters(cls, query, kwargs: dict[str, str] | None = None):
        filters = []
        if kwargs:
            for field, value in kwargs.items():
                if value:
                    try:
                        if field.endswith("__gt"):
                            model_field = getattr(cls, field[:-4])
                            filters.append(model_field > value)
                        elif field.endswith("__gte"):
                            model_field = getattr(cls, field[:-5])
                            filters.append(model_field >= value)
                        elif field.endswith("__lt"):
                            model_field = getattr(cls, field[:-4])
                            filters.append(model_field < value)
                        elif field.endswith("__lte"):
                            model_field = getattr(cls, field[:-5])
                            filters.append(model_field <= value)
                        else:
                            model_field = getattr(cls, field)
                            filters.append(model_field == value)
                    except AttributeError:
                        return None
            query = query.filter(and_(*filters))
        return query

    @classmethod
    def get_order_by(cls, query, order_by: str | None = None):
        if order_by:
            if order_by[0] == "-":
                order_by_field = getattr(cls, order_by[1:]).desc()
            else:
                order_by_field = getattr(cls, order_by)
            query = query.order_by(order_by_field)
        return query

    @classmethod
    async def get(cls, session: AsyncSession, **kwargs):
        query = select(cls)
        query = cls.get_filters(query=query, kwargs=kwargs)
        if result := await session.execute(query):
            return result.scalars().first()

    async def get_or_create(self, session: AsyncSession):
        cls = type(self)
        self_dict = {
            field: value
            for field, value in self.__dict__.items()
            if field != "_sa_instance_state"
        }
        instance = await cls.get(session=session, **self_dict)
        return instance or await self.create(session=session)

    @classmethod
    async def all(cls, session: AsyncSession):
        query = select(cls)
        if result := await session.execute(query):
            return result.scalars().all()

    @classmethod
    async def filter(cls, session: AsyncSession, order_by: str | None = None, **kwargs):
        query = select(cls)
        query = cls.get_filters(query=query, kwargs=kwargs)
        query = cls.get_order_by(query=query, order_by=order_by)
        if result := await session.execute(query):
            return result.scalars().all()

    async def update(self, session: AsyncSession):
        await session.merge(self)
        await session.commit()
        return self

    async def delete(self, session: AsyncSession):
        await session.delete(self)
        await session.commit()

    @classmethod
    async def bulk_delete(cls, instances: list | object, session: AsyncSession):
        if isinstance(instances, Iterable):
            for instance in instances:
                await session.delete(instance)
        else:
            await session.delete(instances)
        await session.commit()
