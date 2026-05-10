class PaperTraderV8:

    def __init__(self, cash=100000):
        self.cash = cash
        self.pos = 0

    def step(self, price, signal):

        if signal == 1:
            self.pos += self.cash / price
            self.cash = 0

        elif signal == -1:
            self.cash += self.pos * price
            self.pos = 0

    def value(self, price):
        return self.cash + self.pos * price