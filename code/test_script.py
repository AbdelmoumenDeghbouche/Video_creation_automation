from fastapi import FastAPI, File, UploadFile
from typing import Optional

app = FastAPI()


@app.post("/uploadfile/")
async def upload_file(
    file: UploadFile = File(None),
    description: Optional[str] = None,
    username: str = "anonymous",
):
    print("hellooooooo")
    return {
        "filename": "No file uploaded",
        "description": description,
        "username": username,
    }
