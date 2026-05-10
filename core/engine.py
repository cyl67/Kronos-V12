import numpy as np

class KronosEngineV7:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def predict(self, df, pred_len=20):

        x = df[["open","high","low","close","volume","amount"]].values

        pred = self.model.predict(x, pred_len=pred_len)

        return pred