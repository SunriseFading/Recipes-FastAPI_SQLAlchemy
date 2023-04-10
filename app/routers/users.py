from app.config import jwt_settings
from app.database import get_session
from app.schemas.users import User as UserSchema
from app.services.users import user_service
from app.utils.messages import messages
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/accounts", tags=["accounts"], responses={404: {"description": "Not found"}}
)


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    summary="User register",
)
async def register(user_schema: UserSchema, session: AsyncSession = Depends(get_session)):
    if user := await user_service.get(email=user_schema.email, session=session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=messages.USER_ALREADY_EXISTS
        )
    await user_service.create(user_schema=user_schema, session=session)
    return {"detail": messages.USER_CREATED}


@router.post("/login/", status_code=status.HTTP_200_OK, summary="User login")
async def login(
    user_schema: UserSchema,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    user = await user_service.get(email=user_schema.email, session=session)
    if not user.verify_password(unhashed_password=user_schema.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.WRONG_PASSWORD
        )
    return {
        "access_token": authorize.create_access_token(subject=user.email),
        "refresh_token": authorize.create_refresh_token(subject=user.email),
    }


@router.delete("/logout/", status_code=status.HTTP_200_OK, summary="User logout")
async def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return {"detail": messages.USER_LOGOUT}
