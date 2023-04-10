from app.models.reviews import Review as ReviewModel
from app.repositories.base import BaseRepository


class ReviewRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=ReviewModel)


review_repository = ReviewRepository()
