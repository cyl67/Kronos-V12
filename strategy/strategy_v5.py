def generate_signal(df, pred_df):

    # 强制字段检查
    required = ["open","high","low","close","volume","amount"]

    for r in required:
        if r not in df.columns:
            raise ValueError(f"缺少字段 {r}, 当前列: {df.columns.tolist()}")

    last_price = float(df["close"].iloc[-1])
    pred_price = float(pred_df["close"].iloc[-1])

    ret = (pred_price - last_price) / last_price

    if ret > 0.02:
        return 1
    elif ret < -0.02:
        return -1
    else:
        return 0