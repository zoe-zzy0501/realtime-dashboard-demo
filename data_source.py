import random
from datetime import timedelta


def get_new_bar(symbol, last_price, last_time):
    """返回一条新的行情数据。

    现在先用随机数模拟。接入真实行情后，只需要修改这个函数，
    保持返回字段不变，app.py 不需要改。
    """

    open_price = last_price
    close_price = max(1, open_price + random.randint(-8, 8))
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
