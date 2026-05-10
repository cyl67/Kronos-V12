import torch
import pandas as pd

from config.settings import *
from data.loader import load_data
from strategy.signal import generate_signal
from backtest.engine import backtest
from model import Kronos, KronosTokenizer, KronosPredictor


# =====================
# 数据
# =====================
df = load_data(SYMBOL)

df = df.tail(LOOKBACK + PRED_LEN).reset_index(drop=True)

x_df = df.iloc[:LOOKBACK][["open","high","low","close","volume","amount"]]
x_ts = df.iloc[:LOOKBACK]["timestamps"]
y_ts = df.iloc[LOOKBACK:LOOKBACK+PRED_LEN]["timestamps"]


# =====================
# 模型
# =====================
tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
model = Kronos.from_pretrained("NeoQuasar/Kronos-mini")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

predictor = KronosPredictor(model, tokenizer)


# =====================
# 预测
# =====================
pred_df = predictor.predict(
    df=x_df,
    x_timestamp=x_ts,
    y_timestamp=y_ts,
    pred_len=PRED_LEN
)

print("预测完成")


# =====================
# 信号
# =====================
signals = generate_signal(df.iloc[:LOOKBACK], pred_df, THRESHOLD)

print("信号:", signals)


# =====================
# 回测
# =====================
equity = backtest(df.iloc[LOOKBACK:LOOKBACK+PRED_LEN], signals)

print("最终资金:", equity[-1])