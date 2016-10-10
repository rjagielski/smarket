from __future__ import unicode_literals


class Stock(object):
    """Represents single stock on market

    symbol -- normalized stock symbol, converted to uppercase
    stock_type -- one of Stock.TYPE_PREFERRED, Stock.TYPE_COMMON

    """
    TYPE_PREFERRED = 'p'
    TYPE_COMMON = 'c'
    TYPE_CHOICES = (
        ('p', 'Preferred'),
        ('c', 'Common'),
    )

    def __init__(self, symbol, stock_type, last_divident, fixed_divident, par_value):
        self.symbol = symbol.upper()
        if stock_type not in (Stock.TYPE_PREFERRED, Stock.TYPE_COMMON):
            raise ValueError('stock_type must be one of (Stock.TYPE_PREFERRED, Stock.TYPE_COMMON)')
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
