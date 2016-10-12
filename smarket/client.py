"""

This is a simple client that can be used to test Super Simple Stock Market in
practice. It has only the basic features that author wanted to show for the app demo.

"""
from __future__ import unicode_literals
from decimal import Decimal
import sys
from smarket.models import Market


HELP = {
    'help': 'This is a basic CLI interface for Super Simple Stock Market.'
        ' Use one of the commands below. Type `help <command>` to get detailed'
        ' help about specific command.',
    'add_stock': 'Add stock to the market. The arguments are:\n'
        '\tsymbol -- stock symbol, it will become uppercase\n'
        '\tstock_type -- p for preferred or c for common\n'
        '\tpar_value -- par value in pennies\n'
        '\tlast_divident -- last divident in pennies\n'
        '\tfixed_divident -- fixed divident as percentage (optional)\n\n'
        '\tExample 1: `add stock ABC c 60 20`\n'
        '\tExample 2: `add stock BCD p 80 10 2`',
    'add_trade': 'Add trade to the specific stock. Time of adding is automaticaly recorded. The arguments are:\n'
        '\tstock -- stock symbol. Stock must already exist\n'
        '\tbuy -- b for buy, s for sell\n'
        '\tquantity -- integer\n'
        '\tprice -- price in pennies',
    'stock_info': 'Show divident yield, P/E ratio and Volume Weighted Stock Price for some stock. The arguments are:\n'
        '\tstock -- stock symbol.\n'
        '\tprice -- price in pennies\n',
    'market_info': 'Show All Share Index',
    'exit': 'Close the app. Warning: all market data will be lost',
}


class SMarketClient(object):

    INVALID_ARGS = 'Invalid arguments. See help {}'

    def __init__(self):
        self.market = Market()

    def run_cli(self, stock=None):
        try:
            command = raw_input("Type `help` for instructions:\n").decode(sys.stdin.encoding)
        except EOFError:
            self.exit()

        args = command.split(' ')
        if args[0] not in HELP:
            args = ['help',]
        getattr(self, args[0])(args[1:])
        print ''

    def help(self, args):
        if args and args[0] in HELP:
            print '\n{} - {}'.format(args[0], HELP[args[0]])
        else:
            print HELP['help']
            print '\n'.join(sorted(HELP.keys()))

    def add_stock(self, args):
        if len(args) == 4:
            args.append(None)

        if len(args) != 5:
            print self.INVALID_ARGS.format('add_stock')
            return

        symbol, stock_type, par_value, last_divident, fixed_divident = args
        if symbol.upper() in self.market.stocks:
            print 'Stock already exists'
            return

        if stock_type not in ['c', 'p']:
            print self.INVALID_ARGS.format('add_stock')
            return

        if stock_type == 'p' and fixed_divident is None:
            print 'Preferred stock requires fixed divident'

        try:
            par_value = int(par_value)
            last_divident = int(par_value)
            if fixed_divident is not None:
                fixed_divident = Decimal(fixed_divident)
        except ValueError:
            print self.INVALID_ARGS.format('add_stock')
            return

        self.market.add_stock(symbol=symbol, stock_type=stock_type,
                              par_value=par_value, last_divident=last_divident,
                              fixed_divident=fixed_divident)
        print 'Stock {} added'.format(symbol)

    def add_trade(self, args):
        if len(args) != 4:
            print self.INVALID_ARGS.format('add_trade')
            return

        symbol, buy, quantity, price = args
        try:
            stock = self.market.stocks[symbol.upper()]
        except KeyError:
            print 'Stock does not exit. Add it first'
            return

        if buy not in ['s', 'b']:
            print self.INVALID_ARGS.format('add_trade')
            return
        buy = -1 if buy == 's' else 1

        try:
            quantity = int(quantity)
            price = int(price)
        except ValueError:
            print self.INVALID_ARGS.format('add_trade')
            return

        stock.add_trade(buy, quantity, price)
        print 'Trade added to stock {}'.format(symbol)

    def stock_info(self, args):
        if len(args) != 2:
            print self.INVALID_ARGS.format('stock_info')
            return

        symbol, price = args
        try:
            stock = self.market.stocks[symbol.upper()]
        except KeyError:
            print 'Stock does not exit. Add it first'
            return

        try:
            price = int(price)
        except ValueError:
            print self.INVALID_ARGS.format('stock_info')
            return

        print 'Divident Yield: {}'.format(stock.divident_yield(price))
        print 'P/E Ratio: {}'.format(stock.per(price))
        print 'Volume Weighted Stock Price based on trades in past 15 minutes: {}' \
                .format(stock.volume_weight_price())

    def market_info(self, args):
        print 'All Share Index {}'.format(self.market.all_share_index())

    def exit(self):
        sys.exit()
