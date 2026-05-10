import akshare as ak
import pandas as pd
import time
import os

class DataEngine:

    def __init__(self, cache=True):
        self.cache = cache

    def load(self, symbol, start="20240101", end="20250101"):

        cache_file = f"cache_{symbol}.csv"

        # ======================
        # 1. 本地缓存优先
        # ======================
        if self.cache and os.path.exists(cache_file):
            print("📦 使用本地缓存数据")
            return pd.read_csv(cache_file)

        # ======================
        # 2. 网络重试机制
        # ======================
        for i in range(5):
            try:
                print(f"📡 第{i+1}次请求AKShare...")

                df = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="daily",
                    start_date=start,
                    end_date=end,
                    adjust=""
                )

                if df is not None and len(df) > 0:
                    df.to_csv(cache_file, index=False)
                    return df

            except Exception as e:
                print("⚠️ 请求失败:", e)
                time.sleep(2)

        raise Exception("❌ 数据源不可用")