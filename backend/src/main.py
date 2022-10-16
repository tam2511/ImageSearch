from fastapi import FastAPI, File, UploadFile
from fastapi_pagination import paginate, add_pagination, LimitOffsetPage
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.handler import Handler

handler = Handler()

app = FastAPI()


origins = [
    "http://localhost:22222",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
