from __future__ import unicode_literals, division
import datetime


class Stock(object):
    """Represents single stock on market

    symbol -- normalized stock symbol, converted to uppercase
    stock_type -- one of Stock.TYPE_PREFERRED, Stock.TYPE_COMMON
    par_value -- par value in pennies
    last_divident -- last divident in pennies
    fixed_divident -- fixed divident in %, as Decimal

    """
    TYPE_PREFERRED = 'p'
    TYPE_COMMON = 'c'
    TYPE_CHOICES = (
        ('p', 'Preferred'),
        ('c', 'Common'),
    )

    def __init__(self, symbol, stock_type, par_value, last_divident, fixed_divident=None):
        if stock_type not in (Stock.TYPE_PREFERRED, Stock.TYPE_COMMON):
            raise ValueError('stock_type must be one of (Stock.TYPE_PREFERRED, Stock.TYPE_COMMON)')

        if stock_type == Stock.TYPE_PREFERRED and fixed_divident is None:
            raise ValueError('Preferred stock requires fixed divident')

        self.symbol = symbol.upper()
        self.stock_type = stock_type
        self.last_divident = last_divident
        self.fixed_divident = fixed_divident
        self.par_value = par_value
        self.trades = []  # trades ordered by timestamp

    def __unicode__(self):
        return '{symbol} - {stock_type}'.format(symbol=self.symbol,
                                                stock_type=self.get_stock_type_display())

    def __str__(self):
        return unicode(self).encode('utf-8')

    def get_stock_type_display(self):
        for k, v in self.TYPE_CHOICES:
            if k == self.stock_type:
                return v
        raise ValueError('Invalid stock type "{}"'.format(self.stock_type))

    def divident_yield(self, price):
        """Returns divident yield

        price -- price in pennies

        """
        if price == 0:
            return 0

        if self.stock_type == Stock.TYPE_COMMON:
            return self.last_divident / price
        else:
            # fixed divident is in %, converting to fraction
            return (self.fixed_divident * self.par_value / 100) / price

    def per(self, price):
        """Returns P/E ratio (price/earnings ratio)

        price -- price in pennies

        """
        divident = self.divident_yield(price)
        if divident == 0:
            return 0

        return price / divident

    def add_trade(self, buy, quantity, price):
        """Helper to add trade with timestamp defaulting to now()

        quantity -- quantity of shares
        buy -- True if buy, False if sell
        price -- traded price

        """
        self.trades.append(Trade(quantity=quantity, buy=buy, price=price,
                                 timestamp=datetime.datetime.now()))

    def _recent_trades(self):
        """Yields trades made in last 15 minutes"""
        time_boundry = datetime.datetime.now() - datetime.timedelta(minutes=15)
        for trade in reversed(self.trades):
            if trade.timestamp > time_boundry:
                yield trade
            else:
                raise StopIteration()

    def volume_weight_price(self):
        """Returns Volume Weighted Stock Price based on trades in past 15 minutes"""
        traded_value = 0
        traded_quantity = 0
        for trade in self._recent_trades():
            traded_value += trade.price * trade.quantity
            traded_quantity += trade.quantity

        if traded_quantity == 0:
            return 0
        return float(traded_value) / traded_quantity


class Trade(object):
    """Records single trade

    quantity -- quantity of shares
    buy -- 1 for buy, -1 for sell
    price -- traded price

    """
    def __init__(self, quantity, buy, price, timestamp):
        if buy not in (-1, 1):
            raise ValueError('Buy must be 1 (buy) or -1 (sell)')
        if quantity < 0:
            raise ValueError('Quantity must be positive')
        self.quantity = quantity
        self.buy = buy
        self.price = price
        self.timestamp = timestamp

    def __unicode__(self):
        template = '{buy} {quantity} for {price}'
        return template.format(buy=self.get_buy_display(),
                               quantity=self.quantity,
                               price=self.price)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def get_buy_display(self):
        return 'Buy' if self.buy == 1 else 'Sell'
