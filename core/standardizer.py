import pandas as pd


COL_MAP = {
    "日期": "timestamp",
    "date": "timestamp",
    "timestamps": "timestamp",

    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume",
    "成交额": "amount",
}


def standardize(df):

    df = df.copy()

    df.rename(columns=COL_MAP, inplace=True)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    required = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount"
    ]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"缺少字段: {col}")

    return df