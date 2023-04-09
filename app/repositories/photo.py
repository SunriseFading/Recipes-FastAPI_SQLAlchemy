import os

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


class PhotoRepository:
    async def upload_photo(self, photo: UploadFile, session: AsyncSession):
        cls = type(self)
        if os.path.exists(self.photo):
            os.remove(self.photo)
        photo_path = os.path.join(
            "media", cls.__name__.lower(), self.name, photo.filename
        )
        if not os.path.exists(os.path.dirname(photo_path)):
            os.makedirs(os.path.dirname(photo_path))
        with open(photo_path, "wb") as buffer:
            buffer.write(await photo.read())
        self.photo = photo_path
        await self.update(session=session)

    def download_photo(self):
        if os.path.exists(self.photo):
            return self.photo
