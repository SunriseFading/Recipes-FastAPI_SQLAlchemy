from app.config import jwt_settings
from app.database import get_session
from app.schemas.reviews import ReviewParams as ReviewParamsSchema
from app.controllers.reviews import review_controller
from app.utils.messages import messages
from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/reviews", tags=["reviews"], responses={404: {"description": "Not found"}}
)

security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.post("/create/{id}", status_code=status.HTTP_200_OK, summary="Create review")
async def create(
    id: int,
    params: ReviewParamsSchema = Depends(),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    user_email = authorize.get_jwt_subject()
    await review_controller.create(
        id=id, params=params, user_email=user_email, session=session
    )
    return {"detail": messages.REVIEW_SAVED}
