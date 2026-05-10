class PaperTrader:

    def __init__(self):
        self.cash = 100000
        self.position = 0

    def buy(self, price, amount=100):

        cost = price * amount

        if self.cash >= cost:
            self.cash -= cost
            self.position += amount

    def sell(self, price, amount=100):

        if self.position >= amount:
            self.cash += price * amount
            self.position -= amount