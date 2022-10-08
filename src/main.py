from fastapi import FastAPI, File, UploadFile
from pydantic import BaseSettings
from fastapi.middleware.cors import CORSMiddleware

from src.handler import Handler

handler = Handler()


class Settings(BaseSettings):
    # ... The rest of our FastAPI settings

    BASE_URL = "http://localhost:8000"
    USE_NGROK = True


settings = Settings()


def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload_zip")
async def upload_zip(zip_file: UploadFile = File(...)):
    handler.upload(zip_file.file.read())
    return {"message": f"Successfully uploaded {zip_file.filename}"}


@app.post("/search")
async def upload_zip(image: UploadFile = File(...), number_images: int = 10):
    result = handler.search(image.file.read(), number_images)
    return result
