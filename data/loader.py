import tushare as ts
import pandas as pd

from config import TUSHARE_TOKEN


ts.set_token(TUSHARE_TOKEN)
pro = ts.pro_api()



def load_stock(symbol="600033"):

    if symbol.startswith("6"):
        ts_code = symbol + ".SH"
    else:
        ts_code = symbol + ".SZ"

    df = pro.daily(
        ts_code=ts_code,
        start_date="20240101",
        end_date="20261231"
    )

    df = df.sort_values("trade_date")

    df = df.rename(columns={
        "trade_date": "timestamp",
        "vol": "volume"
    })

    cols = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount"
    ]

    for col in cols:
        df[col] = pd.to_numeric(df[col])

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df