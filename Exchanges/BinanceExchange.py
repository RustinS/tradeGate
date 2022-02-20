from re import L
from binance.spot import Spot
from Utils import DataHelpers
import logging
from binance.error import ClientError

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
        if order.orderType not in ['LIMIT', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT', 'TAKE_PROFIT_LIMIT', 'LIMIT_MAKER']:
            return False

        if order.side not in ['BUY', 'SELL']:
            return False
        
        if order.newOrderRespType not in [None, 'ACK', 'RESULT', 'FULL']:
            return False
        
        if order.timeInForce not in [None, 'GTC', 'IOC', 'FOK']:
            return False
            
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

    @staticmethod
    def getAsDict(self):
        if self.timestamp is None:
            raise Exception('Timestamp must be set')

        params = {}
        params['symbol'] = self.symbol
        params['side'] = self.side
        params['type'] = self.orderType
        params['timestamp'] = self.timestamp

        if not self.timeInForce is None:
            params['timeInForce'] = self.timeInForce

        if not self.quantity is None:
            params['quantity'] = self.quantity
        
        if not self.quoteOrderQty is None:
            params['quoteOrderQty'] = self.quoteOrderQty

        if not self.price is None:
            params['price'] = self.price
        
        if not self.newClientOrderId is None:
            params['newClientOrderId'] = self.newClientOrderId
        
        if not self.stopPrice is None:
            params['stopPrice'] = self.stopPrice
        
        if not self.icebergQty is None:
            params['icebergQty'] = self.icebergQty
        
        if not self.newClientOrderId is None:
            params['newOrderRespType'] = self.newOrderRespType
        
        if not self.recvWindow is None:
            params['recvWindow'] = self.recvWindow

        return params

    def testOrder(self, orderData):
        orderData.setTimestamp()
        params = self.getAsDict(orderData)

        try:
            response = self.client.new_order_test(**params)
            logging.info(response)
            return response
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def makeOrder(self, orderData):
        params = self.getAsDict(orderData)

        try:
            response = self.client.new_order(**params)
            logging.info(response)
            return response
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def getSymbolOrders(self, symbol):
        try:
            return self.client.get_orders(symbol)
        except Exception:
            return None

    def getOpenOrders(self, symbol=None):
        try:
            return self.client.get_open_orders(symbol)
        except Exception:
            return None

    def cancelAllSymbolOpenOrders(self, symbol):
        try:
            return self.client.cancel_open_orders(symbol)
        except Exception:
            return None

    def cancelSymbolOpenOrder(self, symbol, orderId=None, localOrderId=None):
        try:
            if not orderId is None:
                return self.client.cancel_order(symbol, orderId=orderId)
            elif not localOrderId is None:
                return self.client.cancel_order(symbol, origClientOrderId=localOrderId)
            else:
                raise Exception('Specify either order Id in the exchange or local Id sent with the order')
        except Exception:
            return None
        
    def getTradingFees(self):
        try:
            return self.client.trade_fee()
        except Exception:
            return None

    def getSymbolAveragePrice(self, symbol):
        try:
            return self.client.avg_price(symbol)
        except Exception:
            return None

    def getSymbolLatestTrades(self, symbol, limit=None):
        try:
            if not limit is None:
                if limit > 1000: limit = 1000
                elif limit < 1: limit = 1

                return self.client.trades(symbol, limit)
            else:
                return self.client.trades(symbol)
        except Exception:
            return None

    def getSymbolTickerPrice(self, symbol):
        try:
            return self.client.ticker_price(symbol)['price']
        except Exception:
            return None

    def getSymbolKlines(self, symbol, interval, startTime=None, endTime=None, limit=None):
        try:
            return self.client.klines(symbol, interval, startTime=startTime, endTime=endTime, limit=limit)
        except Exception:
            return None
