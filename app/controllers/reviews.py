from app.models.reviews import Review as ReviewModel
from app.repositories.reviews import review_repository
from app.schemas.reviews import ReviewParams as ReviewParamsSchema
from app.controllers.recipes import recipe_controller
from app.controllers.users import user_controller
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class ReviewController:
    def __init__(self, review_repository, recipe_controller, user_controller):
        self.review_repository = review_repository
        self.recipe_controller = recipe_controller
        self.user_controller = user_controller

    async def create(
        self,
        id: int,
        params: ReviewParamsSchema,
        user_email: str,
        session: AsyncSession,
    ):
        recipe = await self.recipe_controller.get(id=id, session=session)
        user = await self.user_controller.get(email=user_email, session=session)
        if await self.review_repository.get(
            user_id=user.id, recipe_id=recipe.id, session=session
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=messages.REVIEW_ALREADY_LEFT,
            )
        review = ReviewModel(rating=params.rating, user_id=user.id, recipe_id=recipe.id)
        await self.review_repository.create(instance=review, session=session)
        await self.recipe_controller.update_rating(
            recipe=recipe, review_rating=review.rating, session=session
        )
        return review


review_controller = ReviewController(
    review_repository=review_repository,
    recipe_controller=recipe_controller,
    user_controller=user_controller,
)
