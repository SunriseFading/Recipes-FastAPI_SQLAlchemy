from app.crud.recipes import RecipeCRUD
from app.models.reviews import Review as m_Review
from app.models.users import User as m_User
from app.schemas.reviews import ReviewParams
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class ReviewCRUD:
    @classmethod
    async def create(
        cls,
        id: int,
        review_params: ReviewParams,
        user_email: str,
        session: AsyncSession,
    ):
        recipe = await RecipeCRUD.get(id=id, session=session)
        user = await m_User.get(email=user_email, session=session)
        if await m_Review.get(user_id=user.id, recipe_id=recipe.id, session=session):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=messages.REVIEW_ALREADY_LEFT,
            )
        review = await m_Review(
            rating=review_params.rating, user_id=user.id, recipe_id=recipe.id
        ).create(session=session)
        await RecipeCRUD.update_rating(
            recipe=recipe, review_rating=review.rating, session=session
        )
        return review
