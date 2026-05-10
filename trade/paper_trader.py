class PaperTrader:

    def __init__(self, cash=100000):

        self.cash = cash
        self.position = 0

    def buy(self, price, qty):

        cost = price * qty

        if self.cash >= cost:
            self.cash -= cost
            self.position += qty

    def sell(self, price, qty):

        if self.position >= qty:
            self.cash += price * qty
            self.position -= qty