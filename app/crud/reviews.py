from app.crud.recipes import RecipeCRUD
from app.models.reviews import Review as ReviewModel
from app.models.users import User as UserModel
from app.schemas.reviews import ReviewParams
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class ReviewCRUD:
    @classmethod
    async def create(
        cls,
        id: int,
        params: ReviewParams,
        user_email: str,
        session: AsyncSession,
    ):
        recipe = await RecipeCRUD.get(id=id, session=session)
        user = await UserModel.get(email=user_email, session=session)
        if await ReviewModel.get(user_id=user.id, recipe_id=recipe.id, session=session):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=messages.REVIEW_ALREADY_LEFT,
            )
        review = await ReviewModel(
            rating=params.rating, user_id=user.id, recipe_id=recipe.id
        ).create(session=session)
        await RecipeCRUD.update_rating(
            recipe=recipe, review_rating=review.rating, session=session
        )
        return review
