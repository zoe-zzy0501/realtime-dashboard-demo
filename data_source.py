import random
from datetime import timedelta


def get_new_bar(symbol, last_price, last_time):
    """先生成一条模拟 K 线，接真实行情时改这个函数。"""

    open_price = last_price
    price_change = random.randint(-8, 8)
    close_price = max(1, open_price + price_change)
    high_price = max(open_price, close_price) + random.randint(1, 5)
    low_price = min(open_price, close_price) - random.randint(1, 5)
    volume = random.randint(60, 260)

    return {
        "时间": last_time + timedelta(minutes=1),
        "开": open_price,
        "高": high_price,
        "低": low_price,
        "收": close_price,
        "成交量": volume,
    }
