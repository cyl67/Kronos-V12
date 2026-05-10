import akshare as ak
import pandas as pd

def load_data(symbol="600033", start="20240101", end="20250101"):

    df = ak.stock_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date=start,
        end_date=end,
        adjust=""
    )

    df.rename(columns={
        "日期": "timestamps",
        "开盘": "open",
        "收盘": "close",
        "最高": "high",
        "最低": "low",
        "成交量": "volume",
        "成交额": "amount"
    }, inplace=True)

    df["timestamps"] = pd.to_datetime(df["timestamps"])

    df = df.sort_values("timestamps").reset_index(drop=True)

    return df