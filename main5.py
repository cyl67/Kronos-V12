import streamlit as st
import pandas as pd
import akshare as ak

from model.kronos_engine import KronosEngine
from strategy.strategy_v5 import generate_signal
from backtest.engine import backtest


# =========================
# 1. 数据标准化（核心）
# =========================
def load_data(symbol: str):

    df = ak.stock_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date="20240101",
        end_date="20250101",
        adjust=""
    )

    # 重命名为统一英文字段
    col_map = {}

    for c in df.columns:
        c = str(c)

        if "日期" in c:
            col_map[c] = "timestamps"
        elif "开盘" in c:
            col_map[c] = "open"
        elif "收盘" in c:
            col_map[c] = "close"
        elif "最高" in c:
            col_map[c] = "high"
        elif "最低" in c:
            col_map[c] = "low"
        elif "成交量" in c:
            col_map[c] = "volume"
        elif "成交额" in c:
            col_map[c] = "amount"

    df = df.rename(columns=col_map)

    # 必须字段检查（防止 silent bug）
    required = ["open","high","low","close","volume","amount","timestamps"]

    missing = [x for x in required if x not in df.columns]
    if missing:
        raise ValueError(f"缺少字段: {missing} 当前字段: {df.columns.tolist()}")

    df["timestamps"] = pd.to_datetime(df["timestamps"])

    return df[required]


# =========================
# 2. UI
# =========================
st.set_page_config(page_title="Kronos V5 AI量化系统", layout="wide")

st.title("🚀 Kronos V5 实盘量化系统")

symbol = st.text_input("股票代码", "600033")

lookback = st.slider("历史窗口", 50, 300, 100)
pred_len = st.slider("预测长度", 5, 50, 20)


# =========================
# 3. 加载数据
# =========================
if st.button("开始分析"):

    st.write("正在加载数据...")

    df = load_data(symbol)

    st.write(df.tail())


    # =========================
    # 4. Kronos预测
    # =========================
    engine = KronosEngine()

    pred_df = engine.predict(
        df=df.iloc[:lookback],
        pred_len=pred_len
    )

    st.subheader("📊 预测结果")
    st.write(pred_df)


    # =========================
    # 5. 生成信号
    # =========================
    signals = generate_signal(
        df.iloc[:lookback],
        pred_df
    )

    st.subheader("📡 交易信号")
    st.write(signals)


    # =========================
    # 6. 回测
    # =========================
    result = backtest(
        df.iloc[lookback:lookback+pred_len],
        signals
    )

    st.subheader("💰 回测结果")
    st.write(result)