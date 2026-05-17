import os
import uuid
from pathlib import Path
from fastapi import UploadFile

BASE_UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_upload_file(file: UploadFile, subfolder: str = "") -> str:
    folder = BASE_UPLOAD_DIR / subfolder
    folder.mkdir(parents=True, exist_ok=True)
    extension = Path(file.filename).suffix or ".bin"
    filename = f"{uuid.uuid4().hex}{extension}"
    target_path = folder / filename
    with target_path.open("wb") as buffer:
        buffer.write(file.file.read())
    return f"/uploads/{subfolder}/{filename}".replace("\\", "/")
