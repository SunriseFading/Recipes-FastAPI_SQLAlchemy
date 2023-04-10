import os

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


class PhotoRepository:
    async def upload_photo(self, instance, photo: UploadFile, session: AsyncSession):
        cls = type(instance)
        if os.path.exists(instance.photo):
            os.remove(instance.photo)
        photo_path = os.path.join(
            "media", cls.__name__.lower(), instance.name, photo.filename
        )
        if not os.path.exists(os.path.dirname(photo_path)):
            os.makedirs(os.path.dirname(photo_path))
        with open(photo_path, "wb") as buffer:
            buffer.write(await photo.read())
        instance.photo = photo_path
        await self.update(instance=instance, session=session)

    def download_photo(self, instance):
        if os.path.exists(instance.photo):
            return instance.photo
