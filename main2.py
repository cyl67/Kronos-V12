import torch
import pandas as pd

from data.ak_loader import load_data
from model.kronos import Kronos, KronosTokenizer, KronosPredictor
from strategy.signal import generate_signal
from execution.paper import PaperTrader

# =========================
# 数据
# =========================
df = load_data("600977")

lookback = 100
pred_len = 20

x_df = df[["open","high","low","close","volume","amount"]].iloc[:lookback]
x_ts = df["date"].iloc[:lookback].reset_index(drop=True)

y_ts = df["date"].iloc[lookback:lookback+pred_len].reset_index(drop=True)

# =========================
# 模型
# =========================
tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
model = Kronos.from_pretrained("NeoQuasar/Kronos-mini")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

predictor = KronosPredictor(model, tokenizer)

# =========================
# 预测
# =========================
pred_df = predictor.predict(
    df=x_df,
    x_timestamp=x_ts,
    y_timestamp=y_ts,
    pred_len=pred_len
)

print("预测完成")

# =========================
# 信号
# =========================
signals = generate_signal(pred_df)

print("信号:", signals)

# =========================
# 模拟交易
# =========================
trader = PaperTrader()

prices = df["close"].iloc[lookback:lookback+pred_len].values

for i in range(len(signals)):
    trader.step(signals[i], prices[i])

    print(
        f"Day {i} | Signal={signals[i]} | Value={trader.value(prices[i])}"
    )

print("最终资产:", trader.value(prices[-1]))