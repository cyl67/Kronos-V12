class Portfolio:

    def __init__(self, cash=100000):
        self.cash = cash
        self.position = 0
        self.entry_price = 0

    def buy(self, price, amount):
        self.position = amount
        self.entry_price = price
        self.cash -= price * amount

    def sell(self, price):
        self.cash += self.position * price
        self.position = 0