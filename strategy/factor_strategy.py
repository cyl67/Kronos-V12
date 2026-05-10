import pandas as pd

class FactorStrategy:

    def generate(self, df):

        score = 0

        if df["close"].iloc[-1] > df["close"].rolling(20).mean().iloc[-1]:
            score += 1

        if df["volume"].iloc[-1] > df["volume"].rolling(5).mean().iloc[-1]:
            score += 1

        if score >= 2:
            return 1

        return 0