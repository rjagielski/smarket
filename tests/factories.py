from decimal import Decimal
import factory
from smarket.models import Stock, Trade


class StockFactory(factory.Factory):
    class Meta:
        model = Stock

    symbol = 'abc'
    stock_type = Stock.TYPE_COMMON
    last_divident = 10
    fixed_divident = None
    par_value = 100


class TradeFactory(factory.Factory):
    class Meta:
        model = Trade

    stock = factory.SubFactory(StockFactory)
    quantity = 5
    buy = True
    price = Decimal('1.5')
