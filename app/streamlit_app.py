import streamlit as st

from data.loader import load_stock
from engine.kronos_engine import KronosEngineV8
from strategy.signal import generate_signal
from backtest.engine import backtest

st.title("🚀 Kronos V8 工业级量化系统")

symbol = st.text_input("股票代码", "600033")
lookback = st.slider("历史窗口", 50, 300, 100)
pred_len = st.slider("预测长度", 5, 50, 20)

if st.button("运行系统"):

    df = load_stock(symbol)

    df = df.tail(lookback)

    st.write("📊 数据预览")
    st.dataframe(df.tail())

    # 模拟预测（可替换真实 Kronos）
    pred_df = df.copy()

    signals = generate_signal(df, pred_df)

    st.write("📡 信号:", signals)

    result = backtest(df, signals)

    st.success(f"💰 最终资金: {result:.2f}")