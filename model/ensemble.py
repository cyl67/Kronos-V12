import numpy as np

class EnsemblePredictor:

    def combine(self, kronos, lstm, transformer):

        pred = (
            kronos * 0.5 +
            lstm * 0.3 +
            transformer * 0.2
        )

        return pred