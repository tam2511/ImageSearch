from fastapi import FastAPI, File, UploadFile
from fastapi_pagination import paginate, add_pagination, LimitOffsetPage
from pydantic import BaseModel

from src.handler import Handler

handler = Handler()

app = FastAPI()


class ImageResult(BaseModel):
    id: str
    image_path: str
    score: float


class UploadZipResult(BaseModel):
    added_count: int


@app.post("/upload_zip", response_model=UploadZipResult)
async def upload_zip(zip_file: UploadFile = File(...)):
    added_count = handler.upload(zip_file.file.read())
    return {"added_count": added_count}


@app.post("/search", response_model=LimitOffsetPage[ImageResult])
async def search(image: UploadFile = File(...)):
    result = paginate(handler.search(image.file.read()))
    return result


add_pagination(app)
