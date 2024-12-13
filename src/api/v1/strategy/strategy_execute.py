import datetime

from api.dependencies import CURRENT_ACTIVE_USER
from api.v1.strategy import router
import uuid
from typing import Annotated, Callable
from fastapi import Path as RPath, Query, HTTPException
from core.enums.unit_time import UnitTime
from core.managers.data_manager import DataManager
from core.managers.s3_manager import s3_manager
from core.enums.symbols import Symbols


@router.get("/run/{file_uuid}")
async def execute_strategy(
    file_uuid: Annotated[
        uuid.UUID, RPath(description="The UUID of the file you need")
    ],
    symbol: Annotated[
        Symbols, Query(description="Currency symbol (BTC for example)")
    ],
    periods: Annotated[
        int,
        Query(description="How much <unit time> include since <time_period>"),
    ],
    unit_time: Annotated[UnitTime, Query(description="Unit of <periods>")],
    start_dt: Annotated[
        str, Query(description="Start time to run [example: 2024-11-25]")
    ],
    current_active_user: CURRENT_ACTIVE_USER,
):
    try:
        start_dt = datetime.date.fromisoformat(start_dt)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. User format <2000-12-30>",
        )

    content = await s3_manager.get_file(
        user_uuid=current_active_user.uuid, file_uuid=file_uuid
    )

    exec_globals = {
        '__builtins__': {
            'print': print,
            'len': len,
            'range': range,
            'enumerate': enumerate,
        }
    }
    exec(content, exec_globals)
    strategy: Callable = exec_globals.get('strategy')

    if strategy is None:
        raise ValueError("Strategy function not found.")

    data = DataManager.get_data(
        symbol=symbol,
        start_d=start_dt,
        unit_time=unit_time,
        periods=periods,
    )
    signals = strategy(data)
    return {'signals': signals}


