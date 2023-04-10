from app.models.reviews import Review as ReviewModel
from app.repositories.reviews import review_repository
from app.schemas.reviews import ReviewParams as ReviewParamsSchema
from app.services.recipes import recipe_service
from app.services.users import user_service
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class ReviewService:
    def __init__(self, review_repository, recipe_service, user_service):
        self.review_repository = review_repository
        self.recipe_service = recipe_service
        self.user_service = user_service

    async def create(
        self,
        id: int,
        params: ReviewParamsSchema,
        user_email: str,
        session: AsyncSession,
    ):
        recipe = await self.recipe_service.get(id=id, session=session)
        user = await self.user_service.get(email=user_email, session=session)
        if await self.review_repository.get(
            user_id=user.id, recipe_id=recipe.id, session=session
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=messages.REVIEW_ALREADY_LEFT,
            )
        review = ReviewModel(rating=params.rating, user_id=user.id, recipe_id=recipe.id)
        await self.review_repository.create(instance=review, session=session)
        await self.recipe_service.update_rating(
            recipe=recipe, review_rating=review.rating, session=session
        )
        return review


review_service = ReviewService(
    review_repository=review_repository,
    recipe_service=recipe_service,
    user_service=user_service,
)
