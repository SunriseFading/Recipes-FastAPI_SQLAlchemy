from app.config import jwt_settings
from app.database import get_session
from app.controllers.steps import step_controller
from app.utils.messages import messages
from fastapi import APIRouter, Depends, Security, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/steps", tags=["steps"], responses={404: {"description": "Not found"}}
)

security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.post(
    "/upload/{id}", status_code=status.HTTP_200_OK, summary="Upload step photo"
)
async def upload_photo(
    id: int,
    photo: UploadFile,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    await step_controller.upload_photo(id=id, photo=photo, session=session)
    return {"detail": messages.STEP_PHOTO_UPLOADED}


@router.post(
    "/download/{id}", status_code=status.HTTP_200_OK, summary="Download step photo"
)
async def download_photo(
    id: int,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    if photo := await step_controller.download_photo(id=id, session=session):
        return FileResponse(photo)
