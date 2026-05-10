class RiskControl:

    def __init__(self):
        self.stop_loss = 0.03
        self.take_profit = 0.08

    def check(self, pnl):

        if pnl <= -self.stop_loss:
            return "STOP_LOSS"

        if pnl >= self.take_profit:
            return "TAKE_PROFIT"

        return "HOLD"