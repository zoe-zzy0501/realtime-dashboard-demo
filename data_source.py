"""Simulated OHLCV data source used by the dashboard demo."""

import random
from datetime import datetime, timedelta


PRICE_MOVE_RANGE = (-8, 8)
PRICE_PADDING_RANGE = (1, 5)
VOLUME_RANGE = (60, 260)


def get_new_bar(symbol: str, last_price: int, last_time: datetime) -> dict:
    """生成一条模拟 K 线；接入真实行情时可保持相同的返回字段。"""

    open_price = last_price
    price_change = random.randint(*PRICE_MOVE_RANGE)
    close_price = max(1, open_price + price_change)
    high_price = max(open_price, close_price) + random.randint(*PRICE_PADDING_RANGE)
    low_price = min(open_price, close_price) - random.randint(*PRICE_PADDING_RANGE)
    volume = random.randint(*VOLUME_RANGE)

    return {
        "时间": last_time + timedelta(minutes=1),
        "开": open_price,
        "高": high_price,
        "低": low_price,
        "收": close_price,
        "成交量": volume,
    }
