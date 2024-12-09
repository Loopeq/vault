from datetime import date
from core.logger import logging
from core.enums.unit_time import UnitTime
from core.enums.symbols import Symbols
import vectorbt as vbt
from core.utils.utils import get_freq
logger = logging.getLogger(__name__)


class DataManager:
    @staticmethod
    def get_data(symbol: Symbols,
                 start_d: date,
                 unit_time: UnitTime,
                 periods: int) -> tuple[dict, dict]:
        window = 4
        pair_data = vbt.YFData.download(f"{symbol}-USD").get(column='Close')
        if pair_data.index.tzinfo is not None:
            pair_data.index = pair_data.index.tz_convert(None)
        freq = get_freq(unit_time=unit_time)
        filtered_close = pair_data.loc[start_d:].resample(freq).last().iloc[:periods]
        rsi = vbt.RSI.run(filtered_close, window=window)
        rsi_np = rsi.rsi.to_numpy()[window:]

        return rsi_np, {1, 2, 3, 4, 5}

