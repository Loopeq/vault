from sqlalchemy.exc import IntegrityError

from core.managers.file_manager import FileManager
from api.v1.strategy import router
from typing import Annotated
from fastapi import UploadFile, HTTPException, Depends
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies import CURRENT_ACTIVE_USER
from api.v1.crud.strategy import StrategyRepo
from core.db.db_helper import db_helper
from core.schemas.strategy import StrategyOut, StrategyInDB


@router.post("/upload_strategy/", response_model=StrategyOut)
async def upload_strategy(
    file: UploadFile,
    current_user: CURRENT_ACTIVE_USER,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    FileManager.validate_file(file=file)
    FileManager.check_file_structure(user_uuid=current_user.uuid)

    try:
        strategy_in = StrategyInDB(
            name=file.filename, user_uuid=current_user.uuid
        )
        strategy_out = await StrategyRepo.insert_strategy(
            strategy_in, session=session
        )
        abs_path = FileManager.get_file_path(
            user_uuid=current_user.uuid, file_uuid=strategy_out.uuid
        )

        async with aiofiles.open(abs_path, "wb") as f:
            await f.write(f"#{strategy_out.uuid}\n\n".encode())
            while content := await file.read(1024 * 1024):
                await f.write(content)

        await session.commit()

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"File with name {file.filename} already exist.",
        )
    except:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to save file.")

    return strategy_out
