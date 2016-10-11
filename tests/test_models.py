import datetime
import pytest
from decimal import Decimal
from smarket.models import Stock, Market
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

    def test_common_divident_yield(self):
        stock = StockFactory(stock_type=Stock.TYPE_COMMON, last_divident=Decimal(12))
        assert stock.divident_yield(10) == Decimal('1.2')

    def test_preferred_divident_yield(self):
        stock = StockFactory(stock_type=Stock.TYPE_PREFERRED,
                             fixed_divident=Decimal(2), par_value=Decimal(150))
        assert stock.divident_yield(10) == Decimal('0.3')

    def test_zero_price_divident_yield(self):
        stock = StockFactory()
        assert stock.divident_yield(0) == 0

    def test_per(self):
        stock = StockFactory(stock_type=Stock.TYPE_COMMON, last_divident=Decimal(10))
        assert stock.per(Decimal(5)) == Decimal('2.5')

    def test_record_trace(self):
        stock = StockFactory()
        stock.add_trade(1, 5, 10)
        stock.add_trade(-1, 1, 1)
        assert len(stock.trades) == 2
        assert stock.trades[1].timestamp > stock.trades[0].timestamp

    def test_volume_weight_price(self):
        stock = StockFactory()
        stock.add_trade(1, 1000, 1)  # this will be ignored because trade is too old
        stock.trades[0].timestamp -= datetime.timedelta(minutes=16)

        stock.add_trade(1, 2, 5)
        stock.add_trade(-1, 4, 2)
        stock.add_trade(1, 4, 2)
        # (2 * 5 +  4 * 2 + 4 * 2) / 10 == (10 + 8 + 8) / 10 == 2.6
        assert stock.volume_weight_price() == 2.6


class TestTrade(object):

    def test_unicde(self):
        trade = TradeFactory(quantity=5, buy=1, price=Decimal('1.5'))
        assert unicode(trade) == 'Buy 5 for 1.5'


class TestMarket(object):

    def test_add_stock(self):
        market = Market()
        market.add_stock(symbol='abc', stock_type=Stock.TYPE_COMMON,
                         par_value=1.1, last_divident=1)
        assert len(market.stocks) == 1
        assert 'ABC' in market.stocks

    def test_unicode(self):
        stocks = [StockFactory(symbol='abc'), StockFactory(symbol='xyz')]
        market = Market()
        market.stocks = {s.symbol: s for s in stocks}
        assert unicode(market) == 'Market with 2 stocks'
