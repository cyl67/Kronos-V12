class RiskManager:

    def __init__(self):

        self.max_position = 0.3
        self.stop_loss = -0.05
        self.take_profit = 0.1

    def check(self, pnl):

        if pnl <= self.stop_loss:
            return "STOP_LOSS"

        if pnl >= self.take_profit:
            return "TAKE_PROFIT"

        return "HOLD"