import akshare as ak
import pandas as pd
import torch
import matplotlib.pyplot as plt

from model import Kronos, KronosTokenizer, KronosPredictor

# =========================
# 参数
# =========================
symbol = "600977"

lookback = 100     # 先用小一点，避免报错
pred_len = 20

# =========================
# 1. 下载A股日线数据（稳定版）
# =========================
print("正在下载数据...")

df = ak.stock_zh_a_hist(
    symbol=symbol,
    period="daily",
    start_date="20240101",
    end_date="20250101",
    adjust=""
)

print("原始字段：", df.columns.tolist())

# =========================
# 2. 自动字段适配（关键修复）
# =========================
col_map = {}

for col in df.columns:
    col_str = str(col)

    if "日期" in col_str or "date" in col_str.lower():
        col_map[col] = "timestamps"

    elif "开盘" in col_str:
        col_map[col] = "open"

    elif "收盘" in col_str:
        col_map[col] = "close"

    elif "最高" in col_str:
        col_map[col] = "high"

    elif "最低" in col_str:
        col_map[col] = "low"

    elif "成交量" in col_str:
        col_map[col] = "volume"

    elif "成交额" in col_str:
        col_map[col] = "amount"

df = df.rename(columns=col_map)

print("重命名后字段：", df.columns.tolist())

# =========================
# 3. 时间处理
# =========================
df["timestamps"] = pd.to_datetime(df["timestamps"])

# =========================
# 4. 取最近数据
# =========================
df = df.tail(lookback + 50).reset_index(drop=True)

x_df = df.loc[:lookback-1, ["open", "high", "low", "close", "volume", "amount"]]
x_timestamp = df.loc[:lookback-1, "timestamps"].reset_index(drop=True)

# 未来时间（交易日近似）
future_times = pd.date_range(
    start=df["timestamps"].iloc[lookback-1],
    periods=pred_len + 1,
    freq="D"
)[1:]

y_timestamp = df["timestamps"].iloc[lookback:lookback+pred_len].reset_index(drop=True)

# =========================
# 5. 加载模型
# =========================
print("加载 Kronos 模型...")

tokenizer = KronosTokenizer.from_pretrained(
    "NeoQuasar/Kronos-Tokenizer-base"
)

model = Kronos.from_pretrained(
    "NeoQuasar/Kronos-mini"
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

print("当前设备:", device)

predictor = KronosPredictor(model, tokenizer)

# =========================
# 6. 预测
# =========================
print("开始预测...")

pred_df = predictor.predict(
    df=x_df,
    x_timestamp=x_timestamp,
    y_timestamp=y_timestamp,
    pred_len=pred_len
)

print("预测结果：")
print(pred_df)

# =========================
# 7. 可视化
# =========================
plt.figure(figsize=(12, 6))

plt.plot(
    x_timestamp,
    x_df["close"],
    label="History"
)

plt.plot(
    y_timestamp,
    pred_df["close"],
    label="Prediction"
)

plt.legend()
plt.title(f"Kronos Prediction - {symbol}")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("pred.png")
plt.show()

print("已保存预测图: pred.png")