import numpy as np

def generate_signal(df, pred_df):

    last = float(df["close"].iloc[-1])
    next_ = float(pred_df["close"].iloc[0])

    ret = (next_ - last) / last

    if ret > 0.02:
        sig = 1
    elif ret < -0.02:
        sig = -1
    else:
        sig = 0

    return np.full(len(pred_df), sig)