import pytest
from decimal import Decimal
from smarket.models import Stock
from tests.factories import StockFactory, TradeFactory


class TestStock(object):

    def test_stock_type_init(self):
        StockFactory(symbol='abc', stock_type=Stock.TYPE_COMMON)
        StockFactory(symbol='abc', stock_type=Stock.TYPE_PREFERRED)
        with pytest.raises(ValueError):
            StockFactory(symbol='abc', stock_type='x')

    def test_stock_type_display(self):
        common = StockFactory(symbol='abc', stock_type=Stock.TYPE_COMMON)
        preferred = StockFactory(symbol='abc', stock_type=Stock.TYPE_PREFERRED)
        invalid = StockFactory(symbol='abc', stock_type=Stock.TYPE_COMMON)
        invalid.stock_type = 'x'

        assert common.get_stock_type_display() == 'Common'
        assert preferred.get_stock_type_display() == 'Preferred'
        with pytest.raises(ValueError):
            invalid.get_stock_type_display()

    def test_unicode(self):
        stock = StockFactory(symbol='abc', stock_type=Stock.TYPE_COMMON)
        assert unicode(stock) == 'ABC - Common'


class TestTrade(object):

    def test_unicde(self):
        stock = StockFactory(symbol='abc')
        trade = TradeFactory(stock=stock, quantity=5, buy=True, price=Decimal('1.5'))
        assert unicode(trade) == 'Buy 5 ABC for 1.5'
