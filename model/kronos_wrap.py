import torch
from model import Kronos, KronosTokenizer, KronosPredictor

class KronosEngine:
    def __init__(self):
        self.tokenizer = KronosTokenizer.from_pretrained(
            "NeoQuasar/Kronos-Tokenizer-base"
        )

        self.model = Kronos.from_pretrained(
            "NeoQuasar/Kronos-mini"
        )

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)

        self.predictor = KronosPredictor(self.model, self.tokenizer)

    def predict(self, df, pred_len):
        x_df = df[["open","high","low","close","volume","amount"]]

        return self.predictor.predict(
            df=x_df,
            x_timestamp=df["timestamp"],
            y_timestamp=df["timestamp"].iloc[-pred_len:],
            pred_len=pred_len
        )