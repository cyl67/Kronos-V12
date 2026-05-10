import akshare as ak

def get_universe():
    df = ak.stock_zh_a_spot_em()
    return df["代码"].tolist()