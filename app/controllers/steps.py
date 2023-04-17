from app.models.steps import Step as StepModel
from app.repositories.steps import step_repository
from app.schemas.steps import Step as StepSchema
from app.utils.messages import messages
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession


class StepController:
    def __init__(self, step_repository):
        self.step_repository = step_repository

    async def bulk_create(
        self, recipe_id: int, steps_schema: list[StepSchema], session: AsyncSession
    ):
        steps = [
            StepModel(
                number=number,
                name=step_schema.name,
                time=step_schema.time,
                description=step_schema.description,
                recipe_id=recipe_id,
            )
            for number, step_schema in enumerate(steps_schema, start=1)
        ]
        return await self.step_repository.bulk_create(instances=steps, session=session)

    async def get(self, id: int, session: AsyncSession):
        step = await step_repository.get(id=id, session=session)
        if step is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=messages.STEP_NOT_FOUND
            )
        return step

    async def bulk_delete(self, steps: list[StepModel], session: AsyncSession):
        await self.step_repository.bulk_delete(instances=steps, session=session)

    async def upload_photo(self, id: int, photo: UploadFile, session: AsyncSession):
        step = await self.get(id=id, session=session)
        await self.step_repository.upload_photo(
            instance=step, photo=photo, session=session
        )

    async def download_photo(self, id: int, session: AsyncSession):
        step = await self.get(id=id, session=session)
        return self.step_repository.download_photo(instance=step)


step_controller = StepController(step_repository=step_repository)
