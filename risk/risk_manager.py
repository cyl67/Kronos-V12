class RiskManager:

    def __init__(self, max_position=0.3, stop_loss=0.05):
        self.max_position = max_position
        self.stop_loss = stop_loss

    def check_position(self, cash, price):
        return min(cash * self.max_position / price, cash)

    def stop_loss_trigger(self, entry_price, current_price):
        return (current_price - entry_price) / entry_price < -self.stop_loss