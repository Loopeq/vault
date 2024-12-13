from sqlalchemy.exc import IntegrityError
from api.v1.strategy.validation import validate_file
from core.managers.s3_manager import s3_manager
from api.v1.strategy import router
from typing import Annotated
from fastapi import UploadFile, HTTPException, Depends, Path as RPath
from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies import CURRENT_ACTIVE_USER
from api.v1.crud.strategy import StrategyRepo
from core.db.db_helper import db_helper
from core.schemas.strategy import StrategyOut, StrategyInDB
from core.logger import logging

logger = logging.getLogger(__name__)


@router.post("/upload_strategy/", response_model=StrategyOut)
async def upload_strategy(
    file: UploadFile,
    current_user: CURRENT_ACTIVE_USER,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    validate_file(file=file)
    try:
        strategy = await StrategyRepo.get_strategy_by_name(user_uuid=current_user.uuid,
                                                           name=file.filename,
                                                           session=session)
        if strategy is None:
            strategy_in = StrategyInDB(
                name=file.filename, user_uuid=current_user.uuid
            )
            strategy = await StrategyRepo.insert_strategy(
                strategy_in, session=session
            )
        await s3_manager.upload_file(
            file=file,
            user_uuid=strategy.user_uuid,
            file_uuid=strategy.uuid,
        )
        await session.commit()

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"File with name {file.filename} already exist.",
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to save file.")

    return strategy
