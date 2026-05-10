import pandas as pd
from core.schema import STANDARD_COLUMNS

def validate(df: pd.DataFrame):

    # 自动补字段（防崩关键）
    for col in STANDARD_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"❌ 缺失字段: {col}")

    df = df[STANDARD_COLUMNS]

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df