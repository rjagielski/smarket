from __future__ import unicode_literals, division


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


class Trade(object):
    """Records single trade

    quantity -- quantity of shares
    buy -- True if buy, False if sell
    price -- traded price

    """
    def __init__(self, stock, quantity, buy, price):
        self.stock = stock
        self.quantity = quantity
        self.buy = buy
        self.price = price

    def __unicode__(self):
        template = '{buy} {quantity} {stock_symbol} for {price}'
        return template.format(buy=self.get_buy_display(),
                               quantity=self.quantity,
                               stock_symbol=self.stock.symbol,
                               price=self.price)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def get_buy_display(self):
        return 'Buy' if self.buy else 'Sell'
