from app.config import jwt_settings
from app.crud.recipes import RecipeCRUD
from app.database import get_session
from app.schemas.recipes import Ingredient as IngredientSchema
from app.schemas.recipes import Recipe as RecipeSchema
from app.schemas.recipes import RecipeParams as RecipeParamsSchema, RecipeResponse as RecipeResponseSchema
from app.utils.messages import messages
from fastapi import APIRouter, Depends, Security, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/recipes", tags=["recipes"], responses={404: {"description": "Not found"}}
)

security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.get("/get", status_code=status.HTTP_200_OK, summary="Get all recipes")
async def get_all(
    params: RecipeParamsSchema = Depends(),
    session: AsyncSession = Depends(get_session),
):
    if recipes := await RecipeCRUD.get_all(
        params=params, session=session
    ):
        return [RecipeResponseSchema.from_orm(recipe) for recipe in recipes]


@router.post(
    "/get_by_ingredients",
    status_code=status.HTTP_200_OK,
    summary="Get recipes by ingredients list",
)
async def get_by_ingredients(
    ingredients: list[IngredientSchema],
    session: AsyncSession = Depends(get_session),
):
    if recipes := await RecipeCRUD.get_by_ingredients(
        ingredients=ingredients, session=session
    ):
        return [RecipeResponseSchema.from_orm(recipe) for recipe in recipes]


@router.get("/get/{id}", status_code=status.HTTP_200_OK, summary="Get recipe by id")
async def get(id: int, session: AsyncSession = Depends(get_session)):
    if recipe := await RecipeCRUD.get(id=id, session=session):
        return RecipeResponseSchema.from_orm(recipe)


@router.post("/create", status_code=status.HTTP_201_CREATED, summary="Create recipe")
async def create(
    recipe_schema: RecipeSchema,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    await RecipeCRUD.create(recipe_schema=recipe_schema, session=session)
    return {"detail": messages.RECIPE_CREATED}


@router.post(
    "/upload/{id}", status_code=status.HTTP_200_OK, summary="Upload recipe photo"
)
async def upload_photo(
    id: int,
    photo: UploadFile,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    await RecipeCRUD.upload_photo(id=id, photo=photo, session=session)
    return {"detail": messages.RECIPE_PHOTO_UPLOADED}


@router.post(
    "/download/{id}", status_code=status.HTTP_200_OK, summary="Download recipe photo"
)
async def download_photo(
    id: int,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    return FileResponse(await RecipeCRUD.download_photo(id=id, session=session))


@router.post(
    "/update/{id}", status_code=status.HTTP_202_ACCEPTED, summary="Update recipe"
)
async def update(
    id: int,
    recipe_schema: RecipeSchema,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    await RecipeCRUD.update(id=id, recipe_schema=recipe_schema, session=session)
    return {"detail": messages.RECIPE_UPDATED}


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK, summary="Delete recipe")
async def delete(
    id: int,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    await RecipeCRUD.delete(id=id, session=session)
    return {"detail": messages.RECIPE_DELETED}
