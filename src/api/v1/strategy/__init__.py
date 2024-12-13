from fastapi import APIRouter

router = APIRouter(prefix="/strategy", tags=["Strategy"])

from . import strategy_upload  # noqa
from . import strategy_execute  # noqa
from . import strategy_delete  # noqa
from . import strategy_me  # noqa
