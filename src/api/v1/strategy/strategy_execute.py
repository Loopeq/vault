import datetime

from api.dependencies import CURRENT_ACTIVE_USER
from api.v1.strategy import router
import uuid
from typing import Annotated
from fastapi import Path as RPath, Query, HTTPException

from core.enums.unit_time import UnitTime
from core.managers.data_manager import DataManager

from core.managers.file_manager import FileManager
from core.managers.strategy_manager import StrategyManager
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
        int, Query(description="How much <unit time> include since <time_period>")
    ],
    unit_time: Annotated[
        UnitTime, Query(description="Unit of <periods>")
    ],
    start_dt: Annotated[
        str,
        Query(description="Start time to run [example: 2024-11-25]")
    ],
    current_active_user: CURRENT_ACTIVE_USER,
):

    try:
        start_dt = datetime.date.fromisoformat(start_dt)
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid date format. User format <2000-12-30>')

    result = None

    path = FileManager.get_file_path(current_active_user.uuid, file_uuid)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f'Strategy {file_uuid} not found')

    function = StrategyManager.get_function(file_uuid=file_uuid, path=path)

    if StrategyManager.validate_function(func=function):
        data, params = DataManager.get_data(symbol=symbol, start_d=start_dt,
                                            unit_time=unit_time, periods=periods)
        result = StrategyManager.execute(func=function, data=data, params=params)
    return result
