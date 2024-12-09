import uuid
from typing import Annotated

from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.exceptions.db_exceptions import DatabaseException
from core.managers.file_manager import FileManager
from api.dependencies import CURRENT_ACTIVE_USER
from api.v1.crud.strategy import StrategyRepo
from api.v1.strategy import router
from core.db.db_helper import db_helper


@router.delete("/delete/{strategy_uuid}")
async def delete_strategy(
    strategy_uuid: Annotated[
        uuid.UUID, Path(description="UUID of file to delete")
    ],
    current_user: CURRENT_ACTIVE_USER,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    try:
        strategy_to_remove = await StrategyRepo.remove_strategy(
            strategy_uuid=strategy_uuid, session=session
        )
        FileManager.remove_file(
            user_uuid=current_user.uuid, file_uuid=strategy_uuid
        )
        await session.commit()

    except DatabaseException as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=e.msg)
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Can't remove the strategy with uuid {strategy_uuid}",
        )
    return strategy_to_remove
