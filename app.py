import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from data.loader import load_stock
from model.kronos_wrap import KronosEngine
from strategy.strategy_v12 import generate_signal
from backtest.engine import backtest
from trade.paper_trade import PaperTrader

# =========================
# 页面配置
# =========================
st.set_page_config(
    page_title="Kronos V12 AI Quant",
    layout="wide"
)

st.title("🚀 Kronos V12 云端AI量化系统")

# =========================
# 侧边栏
# =========================
st.sidebar.header("参数设置")

symbol = st.sidebar.text_input(
    "股票代码",
    "600033"
)

lookback = st.sidebar.slider(
    "历史窗口",
    50,
    300,
    120
)

pred_len = st.sidebar.slider(
    "预测长度",
    5,
    60,
    20
)

run_btn = st.sidebar.button("开始AI预测")

# =========================
# 主逻辑
# =========================
if run_btn:

    with st.spinner("正在加载数据..."):

        df = load_stock(symbol)

    st.success("数据加载成功")

    st.subheader("📊 原始数据")
    st.dataframe(df.tail(20))

    # =========================
    # AI预测
    # =========================
    engine = KronosEngine()

    pred_df = engine.predict(
        df.iloc[:lookback],
        pred_len
    )

    st.subheader("🤖 AI预测结果")
    st.dataframe(pred_df)

    # =========================
    # 信号
    # =========================
    signal = generate_signal(
        df.iloc[:lookback],
        pred_df
    )

    st.subheader("📡 AI交易信号")

    if signal == 1:
        st.success("BUY 买入")

    elif signal == -1:
        st.error("SELL 卖出")

    else:
        st.warning("HOLD 观望")

    # =========================
    # 回测
    # =========================
    signals = [signal] * pred_len

    result = backtest(
        df.iloc[lookback:lookback+pred_len],
        signals
    )

    st.subheader("💰 回测结果")
    st.write(result)

    # =========================
    # 模拟交易
    # =========================
    trader = PaperTrader()

    last_price = float(df["close"].iloc[-1])

    if signal == 1:
        trader.buy(last_price)

    elif signal == -1:
        trader.sell(last_price)

    st.subheader("🏦 模拟账户")

    st.write({
        "cash": trader.cash,
        "position": trader.position
    })

    # =========================
    # K线图
    # =========================
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["close"],
            name="历史价格"
        )
    )

    if "close" in pred_df.columns:

        pred_x = pd.date_range(
            start=df["timestamp"].iloc[-1],
            periods=len(pred_df)+1,
            freq="D"
        )[1:]

        fig.add_trace(
            go.Scatter(
                x=pred_x,
                y=pred_df["close"],
                name="AI预测"
            )
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )