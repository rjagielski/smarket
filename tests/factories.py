import datetime
from decimal import Decimal
import factory
from smarket.models import Stock, Trade


class StockFactory(factory.Factory):
    class Meta:
        model = Stock

    symbol = 'abc'
    stock_type = Stock.TYPE_COMMON
    last_divident = Decimal(10)
    fixed_divident = Decimal('2.5')
    par_value = Decimal(100)


class TradeFactory(factory.Factory):
    class Meta:
        model = Trade

    quantity = 5
    buy = 1
    price = Decimal('1.5')
    timestamp = datetime.datetime.now()
