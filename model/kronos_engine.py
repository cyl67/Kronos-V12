import torch

from model import Kronos
from model import KronosTokenizer
from model import KronosPredictor


class KronosEngine:

    def __init__(self):

        tokenizer = KronosTokenizer.from_pretrained(
            "NeoQuasar/Kronos-Tokenizer-base"
        )

        model = Kronos.from_pretrained(
            "NeoQuasar/Kronos-mini"
        )

        device = "cuda" if torch.cuda.is_available() else "cpu"

        model = model.to(device)

        self.predictor = KronosPredictor(model, tokenizer)

    def predict(self, df, pred_len=20):

        x_df = df[[
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount"
        ]]

        x_timestamp = df["timestamp"]

        future_timestamp = pd.date_range(
            start=df["timestamp"].iloc[-1],
            periods=pred_len + 1,
            freq="B"
        )[1:]

        pred_df = self.predictor.predict(
            df=x_df,
            x_timestamp=x_timestamp,
            y_timestamp=future_timestamp,
            pred_len=pred_len
        )

        return pred_df