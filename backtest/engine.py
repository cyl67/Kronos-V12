import numpy as np
from execution.paper import PaperTraderV8

def backtest(df, signals):

    if isinstance(signals, int):
        signals = np.array([signals])

    trader = PaperTraderV8()

    for i in range(min(len(df), len(signals))):

        price = float(df["close"].iloc[i])
        trader.step(price, signals[i])

    return trader.value(float(df["close"].iloc[-1]))