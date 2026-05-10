import torch
from model import Kronos, KronosTokenizer, KronosPredictor
from data.akshare_loader import load_data
from strategy.signal import generate_signal
from backtest.engine import backtest

# ======================
# 1. 数据
# ======================
df = load_data("600977")

lookback = 100
pred_len = 20

x_df = df[["open","high","low","close","volume","amount"]].iloc[:lookback]
x_timestamp = df["date"].iloc[:lookback]

y_timestamp = df["date"].iloc[lookback:lookback+pred_len]

# ======================
# 2. 模型
# ======================
tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
model = Kronos.from_pretrained("NeoQuasar/Kronos-mini")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

predictor = KronosPredictor(model, tokenizer)

# ======================
# 3. 预测
# ======================
pred_df = predictor.predict(
    df=x_df,
    x_timestamp=x_timestamp.reset_index(drop=True),
    y_timestamp=y_timestamp.reset_index(drop=True),
    pred_len=pred_len
)

print(pred_df)

# ======================
# 4. 信号
# ======================
signals = generate_signal(df.iloc[:lookback], pred_df)

print("交易信号：", signals)

# ======================
# 5. 回测
# ======================
result = backtest(df.iloc[lookback:lookback+pred_len], signals)

print("回测结果：", result)