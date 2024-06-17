from math import exp

class ContCouponBond:
    def __init__(self, p, c, t, mrr):
        self.p = p
        self.c = c / 100
        self.t = t
        self.mrr = mrr / 100

    def PV(self, p, t):
        return p * exp(-self.mrr * t)

    def calPrice(self):
        price = 0
        for i in range(1, self.t + 1):
            price += self.PV(self.p * self.c, i)
        price += self.PV(self.p, self.t)
        return price

def main():
    # Example values
    principal = 1000
    coupon_rate = 5  # in percentage
    time_to_maturity = 10  # in years
    market_rate_of_return = 3  # in percentage

    bond = ContCouponBond(principal, coupon_rate, time_to_maturity, market_rate_of_return)
    price = bond.calPrice()
    print(f"The calculated price of the bond is: ${price:.2f}")

if __name__ == "__main__":
    main()
