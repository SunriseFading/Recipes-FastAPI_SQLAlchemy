from app.models.steps import Step as m_Step
from app.schemas.steps import Step as s_Step
from app.utils.messages import messages
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession


class StepCRUD:
    @staticmethod
    async def bulk_create(
        recipe_id: int, steps_schema: list[s_Step], session: AsyncSession
    ):
        steps = [
            m_Step(
                number=number,
                name=step_schema.name,
                time=step_schema.time,
                description=step_schema.description,
                recipe_id=recipe_id,
            )
            for number, step_schema in enumerate(steps_schema, start=1)
        ]
        return await m_Step.bulk_create(instances=steps, session=session)

    @staticmethod
    async def get(id: int, session: AsyncSession):
        step = await m_Step.get(id=id, session=session)
        if step is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=messages.STEP_NOT_FOUND
            )
        return step

    @classmethod
    async def upload_photo(cls, id: int, photo: UploadFile, session: AsyncSession):
        step = await cls.get(id=id, session=session)
        await step.upload_photo(photo=photo, session=session)

    @classmethod
    async def download_photo(cls, id: int, session: AsyncSession):
        step = await cls.get(id=id, session=session)
        return step.download_photo()
