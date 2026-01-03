# app/utils/file_utils.py
import os
from fastapi import UploadFile
from pathlib import Path
import shutil

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)

def save_upload_file(upload_file: UploadFile, dest_folder: str | None = None) -> str:
    """
    Save UploadFile to disk inside app/data/ and return path string.
    """
    dest_folder = dest_folder or str(DATA_DIR)
    os.makedirs(dest_folder, exist_ok=True)
    filename = upload_file.filename or "uploaded_file"
    safe_path = os.path.join(dest_folder, filename)

    # If filename already exists, append a numeric suffix
    base, ext = os.path.splitext(safe_path)
    counter = 1
    while os.path.exists(safe_path):
        safe_path = f"{base}_{counter}{ext}"
        counter += 1

    # Write file to disk
    with open(safe_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)

    return safe_path
