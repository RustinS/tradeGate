from binance.spot import Spot
from Utils import DataHelpers

class BinanceExchange():
    def __init__(self, credentials, type='SPOT', sandbox=False):
        self.credentials = credentials
        self.sandbox = sandbox

        if type == 'SPOT':
            if sandbox:
                self.client = Spot(key=credentials['spot']['key'], secret=credentials['spot']['secret'], base_url='https://testnet.binance.vision')
            else:
                self.client = Spot(key=credentials['spot']['key'], secret=credentials['spot']['secret'])

    def fetchBalance(self, asset=''):
        try:
            balances = self.client.account()['balances']
        except Exception:
            return None

        if asset == '':
            return balances
        else:
            for balance in balances:
                if balance['asset'] == asset:
                    return balance
        return None

    def SymbolTradeHistory(self, symbol):
        try:
            return self.client.my_trades(symbol)
        except Exception:
            return None

    @staticmethod
    def isOrderDataValid(order : DataHelpers.OrderData):
        if order.orderType == 'LIMIT':
            if not (order.timeInForce is None or order.quantity is None or order.price is None):
                return True

        elif order.orderType == 'MARKET':
            if not (order.quantity is None and order.quoteOrderQty is None):
                return True

        elif order.orderType == 'STOP_LOSS':
            if not (order.quantity is None or order.stopPrice is None):
                return True

        elif order.orderType == 'STOP_LOSS_LIMIT':
            if not (order.timeInForce is None or order.quantity is None or order.price is None or order.stopPrice is None):
                return True

        elif order.orderType == 'TAKE_PROFIT':
            if not (order.quantity is None or order.stopPrice is None):
                return True

        elif order.orderType == 'TAKE_PROFIT_LIMIT':
            if not (order.timeInForce is None or order.quantity is None or order.price is None or order.stopPrice is None):
                return True

        elif order.orderType == 'LIMIT_MAKER':
            if not (order.quantity is None or order.price is None):
                return True
        
        return False

    def createOrder(self, params):
        pass
