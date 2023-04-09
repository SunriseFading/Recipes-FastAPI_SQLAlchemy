from app.config import jwt_settings
from app.database import get_session
from app.models.users import User as UserModel
from app.schemas.users import User as s_User
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
async def register(user_schema: s_User, session: AsyncSession = Depends(get_session)):
    if await UserModel.get(email=user_schema.email, session=session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=messages.USER_ALREADY_EXISTS
        )
    await UserModel(**user_schema.dict()).create(session=session)
    return {"detail": messages.USER_CREATED}


@router.post("/login/", status_code=status.HTTP_200_OK, summary="User login")
async def login(
    user_schema: s_User,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    if (user := await UserModel.get(email=user_schema.email, session=session)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
        )
    print(user)
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
