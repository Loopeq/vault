import uuid
from typing import Annotated

import aiofiles
from fastapi import UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CURRENT_ACTIVE_USER
from api.v1.strategy import router
from api.v1.crud.strategy import StrategyRepo
from fastapi import Path as RPath

from core.db.db_helper import db_helper
from core.exceptions.db_exceptions import DatabaseException
from core.schemas.strategy import StrategyInDB
from core.managers.file_manager import FileManager


@router.patch("/update/{file_uuid}")
async def update_strategy(
    file_uuid: Annotated[
        uuid.UUID, RPath(description="The UUID of the file you need")
    ],
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

        strategy_out = await StrategyRepo.update_strategy(
            strategy_in=strategy_in, strategy_uuid=file_uuid, session=session
        )

        abs_path = FileManager.get_file_path(
            user_uuid=current_user.uuid, file_uuid=file_uuid
        )

        async with aiofiles.open(abs_path, "wb") as f:
            await f.write(f"#{file_uuid}\n\n".encode())
            while content := await file.read(1024 * 1024):
                await f.write(content)

        await session.commit()
        return strategy_out
    except DatabaseException as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'Unexpected error while updating strategy (UUID {file_uuid})')

