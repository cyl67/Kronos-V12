class KronosEngineV8:

    def __init__(self, model):
        self.model = model

    def predict(self, df, pred_len):

        x = df[["open","high","low","close","volume","amount"]].values

        return self.model.predict(x, pred_len=pred_len)