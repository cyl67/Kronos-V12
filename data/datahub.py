from data.akshare_source import get_akshare_data
from data.tushare_source import get_tushare_data


def load_stock(symbol):

    try:
        print("使用 AkShare 数据源")
        return get_akshare_data(symbol)

    except Exception as e:
        print("AkShare失败:", e)

    try:
        print("切换 Tushare 数据源")
        return get_tushare_data(symbol)

    except Exception as e:
        print("Tushare失败:", e)

    raise Exception("所有数据源失效")