from typing import List, Iterator, Dict
from enum import Enum


"""
Stock names should be modelled as an enum in our solution 
because we don't need the flexibility of strings.
Searched for some example names.
"""
class StockName(Enum):
    META = "META"
    AAPL = "AAPL"
    MSFT = "MSFT"
    NVDA = "NVDA"
    AMZN = "AMZN"

# Pretty simple. We don't need to store historical prices so we just use a dict.
stock_prices: Dict[StockName, float] = {
    StockName.META: 100,
    StockName.AAPL: 150,
    StockName.MSFT: 200,
    StockName.NVDA: 250,
    StockName.AMZN: 300,
}


class Stock:
    """
    Simple stock class with name and amount. 
    Quick investigation shows that someone can own a fraction of a stock,
    and that's a big assumption in our solution.
    """
    def __init__(self, name: StockName, amount: float):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.name = name
        self.amount = amount
    
    @property
    def price(self) -> float:
        """
        Current price method (price comes from external source)
        """
        return stock_prices[self.name]
    
    def __str__(self) -> str:
        return f"{self.name.value} (price={self.price}) | {self.amount} shares"

class Allocation():
    """
    This class should be initialized with an allocation dict of type { stock_name: parts }.
    Parts may be in whatever units. They are normalized so that they sum to 1 upon initializing.
    Note that allocation is with respect to value; not amount of shares.
    
    Works like a dict, but only supports reading values (non-mutable pretty much)
    """
    def __init__(self, allocation_dict: Dict[StockName, float]):
        sum_parts = sum(allocation_dict.values())
        if any(parts < 0 for parts in allocation_dict.values()):
            raise ValueError("Allocation parts cannot be negative") 
        if sum_parts <= 0:
            raise ValueError("Total allocation must be positive")
        self._allocation_dict = {
            stock_name: parts / sum_parts for stock_name, parts in allocation_dict.items()
            }

    def __getitem__(self, stock_name: StockName) -> float:
        return self._allocation_dict[stock_name]

    def __iter__(self) -> Iterator[StockName]:    
        return iter(self._allocation_dict.keys())
    
    def __str__(self):
        return "\n".join([f"{k.value} | {v * 100}%" for k, v in self._allocation_dict.items()]
        )

class Portfolio:
    """
    Our main class to manage the portfolio :)
    """
    def __init__(self, allocation: Allocation, current_stocks: List[Stock]):
        # Check that stocks match allocations (even if stocks have amount = 0, i.e. not held)
        stock_names  = [stock.name for stock in current_stocks]
        if set(stock_names) != set(allocation):
            raise ValueError("Stocks must match allocation")
        if len(set(stock_names)) != len(stock_names):
            raise ValueError("Can't have duplicate stocks")

        self._allocation = allocation
        self._current_stocks = current_stocks
    
    @property
    def allocation(self):
        return str(self._allocation)
    
    @property
    def current_stocks(self):
        return "\n".join(map(lambda s: str(s), self._current_stocks))

    def value(self) -> float:
        """
        Total value of the portfolio.
        """
        return sum(stock.price * stock.amount for stock in self._current_stocks)

    def rebalance(self) -> dict[StockName, float]:
        """
        Tells us which stocks to buy or sell in the portfolio to match the given allocation.
        Since we aren't storing historical prices or the price at which we bought the stocks,
        our solution will be to just use the current price and sell / buy stocks such that
        the portfolio is rebalanced while maintaining the total value.
        Fractional stock amounts allow this without numerical magic.

        The net cost of rebalancing should always be 0 (or near 0 due to rounding error) 
        since we're maintaining the total value of the portfolio and buying/selling stocks 
        based on their value.
        """
        total_portfolio_value = self.value()
        adjustments: dict[StockName, float] = {}

        for stock in self._current_stocks:
            target_allocation = self._allocation[stock.name]
            target_value = target_allocation * total_portfolio_value
            current_value = stock.price * stock.amount

            stock_value_delta = (target_value - current_value)
            amount_delta = stock_value_delta / stock.price

            # delta may be positive or negative, signaling either selling or buying
            adjustments[stock.name] = amount_delta
        
        return adjustments
    
    def __str__(self):
        return "\n".join([str(s) for s in self._current_stocks])


if __name__ == "__main__":
    portfolio = Portfolio(
        allocation=Allocation({
            StockName.META: 30, 
            StockName.AAPL: 60, 
            StockName.NVDA: 10}),
        current_stocks=[
            Stock(StockName.META, amount=3), 
            Stock(StockName.AAPL, amount=0), 
            Stock(StockName.NVDA, amount=10)],
    )

    print(f"Portfolio value: ${portfolio.value()}")

    print(f"Allocations:\n{portfolio.allocation}")

    print(f"Current stocks:\n{portfolio.current_stocks}")

    for name, delta in portfolio.rebalance().items():
        if delta < 0:
            print(f"Sell {-delta} shares of {name.value}")
        elif delta > 0:
            print(f"Buy {delta} shares of {name.value}")
