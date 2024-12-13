import re

from fastapi import UploadFile, HTTPException


def validate_file(file: UploadFile):
    max_size = 2e7
    max_size_mb = max_size / 1024 / 1024
    if not file.filename.endswith(".py"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only .py files are allowed",
        )
    if file.size > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the allowed limit. {max_size_mb}",
        )
    if not re.match(r"^[\w,-]{1,50}\.[A-Za-z]{2,4}$", file.filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file name. Only alphanumeric characters, underscores, and hyphens are allowed.",
        )
