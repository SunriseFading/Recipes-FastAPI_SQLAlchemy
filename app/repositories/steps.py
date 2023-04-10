from app.models.steps import Step as StepModel
from app.repositories.base import BaseRepository
from app.repositories.photo import PhotoRepository


class StepRepository(BaseRepository, PhotoRepository):
    def __init__(self):
        super().__init__(model=StepModel)


step_repository = StepRepository()
