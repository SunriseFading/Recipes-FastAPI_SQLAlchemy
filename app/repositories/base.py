from collections.abc import Iterable

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, model):
        self.model = model

    async def create(self, instance, session: AsyncSession):
        session.add(instance)
        await session.flush()
        await session.commit()
        return instance

    async def bulk_create(self, instances: list, session: AsyncSession):
        session.add_all(instances)
        await session.flush()
        await session.commit()
        return instances

    def get_filters(self, query, kwargs: dict[str, str] | None = None):
        filters = []
        if kwargs:
            for field, value in kwargs.items():
                if value:
                    try:
                        if field.endswith("__gt"):
                            model_field = getattr(self.model, field[:-4])
                            filters.append(model_field > value)
                        elif field.endswith("__gte"):
                            model_field = getattr(self.model, field[:-5])
                            filters.append(model_field >= value)
                        elif field.endswith("__lt"):
                            model_field = getattr(self.model, field[:-4])
                            filters.append(model_field < value)
                        elif field.endswith("__lte"):
                            model_field = getattr(self.model, field[:-5])
                            filters.append(model_field <= value)
                        else:
                            model_field = getattr(self.model, field)
                            filters.append(model_field == value)
                    except AttributeError:
                        return None
            query = query.filter(and_(*filters))
        return query

    def get_order_by(self, query, order_by: str | None = None):
        if order_by:
            if order_by[0] == "-":
                order_by_field = getattr(self.model, order_by[1:]).desc()
            else:
                order_by_field = getattr(self.model, order_by)
            query = query.order_by(order_by_field)
        return query

    async def get(self, session: AsyncSession, **kwargs):
        query = select(self.model)
        query = self.get_filters(query=query, kwargs=kwargs)
        if result := await session.execute(query):
            return result.scalars().first()

    async def get_or_create(self, instance, session: AsyncSession):
        instance_dict = {
            field: value
            for field, value in instance.__dict__.items()
            if field != "_sa_instance_state"
        }
        created_instance = await self.get(**instance_dict, session=session)
        return created_instance or await self.create(instance=instance, session=session)

    async def all(self, session: AsyncSession):
        query = select(self.model)
        if result := await session.execute(query):
            return result.scalars().all()

    async def filter(
        self, session: AsyncSession, order_by: str | None = None, **kwargs
    ):
        query = select(self.model)
        query = self.get_filters(query=query, kwargs=kwargs)
        query = self.get_order_by(query=query, order_by=order_by)
        if result := await session.execute(query):
            return result.scalars().all()

    async def update(self, instance, session: AsyncSession):
        await session.merge(instance)
        await session.commit()
        return instance

    async def delete(self, instance, session: AsyncSession):
        await session.delete(instance)
        await session.commit()

    async def bulk_delete(self, instances: list | object, session: AsyncSession):
        if isinstance(instances, Iterable):
            for instance in instances:
                await session.delete(instance)
        else:
            await session.delete(instances)
        await session.commit()
