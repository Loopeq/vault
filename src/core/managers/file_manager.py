import re
import uuid
from pathlib import Path

from fastapi import UploadFile, HTTPException

from core.constants import ROOT_PATH


class FileManager:
    MAX_SIZE = 2e7
    MAX_SIZE_MB = MAX_SIZE / 1024 / 1024

    @staticmethod
    def validate_file(file: UploadFile):
        if not file.filename.endswith(".py"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Only .py files are allowed",
            )
        if file.size > FileManager.MAX_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds the allowed limit. {FileManager.MAX_SIZE_MB}",
            )
        if not re.match(r"^[\w,-]{1,50}\.[A-Za-z]{2,4}$", file.filename):
            raise HTTPException(
                status_code=400,
                detail="Invalid file name. Only alphanumeric characters, underscores, and hyphens are allowed.",
            )

    @staticmethod
    def check_file_structure(user_uuid: uuid.UUID):
        try:
            user_folder = ROOT_PATH / str(user_uuid)
            user_folder.mkdir(exist_ok=True)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error while creating file structure: {str(e)}",
            )

    @staticmethod
    def get_file_path(user_uuid: uuid.UUID, file_uuid: uuid.UUID) -> Path:
        return ROOT_PATH / str(user_uuid) / f"{file_uuid}.py"

    @staticmethod
    def remove_file(user_uuid: uuid.UUID, file_uuid: uuid.UUID) -> bool:
        path = FileManager.get_file_path(
            user_uuid=user_uuid, file_uuid=file_uuid
        )
        if path.exists():
            path.unlink()
        else:
            raise ValueError("No file with this UUID")
