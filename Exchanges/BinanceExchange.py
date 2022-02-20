from re import L
from binance.spot import Spot
from Utils import DataHelpers
import logging
from binance.error import ClientError
from binance_f import RequestClient

class BinanceExchange():
    def __init__(self, credentials, type='SPOT', sandbox=False):
        self.credentials = credentials
        self.sandbox = sandbox

        if type == 'SPOT':
            if sandbox:
                self.client = Spot(key=credentials['spot']['key'], secret=credentials['spot']['secret'], base_url='https://testnet.binance.vision')
                self.futuresClient = RequestClient(api_key=credentials['futures']['key'], secret_key=credentials['futures']['secret'], url='https://testnet.binancefuture.com')
            else:
                self.client = Spot(key=credentials['spot']['key'], secret=credentials['spot']['secret'])

        self.timeIntervlas = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

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
    def isFuturesOrderDataValid(order : DataHelpers.futuresOrderData):
        if order.side not in ['BUY', 'SELL']:
            return False

        if order.orderType not in ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET']:
            return False

        if order.positionSide not in [None, 'BOTH', 'LONG', 'SHORT']:
            return False

        if order.timeInForce not in [None, 'GTC', 'IOC', 'FOK', 'GTX']:
            return False

        if order.workingType not in [None, 'MARK_PRICE', 'CONTRACT_PRICE']:
            return False
        
        if order.newOrderRespType not in [None, 'ACK', 'RESULT']:
            return False

        if order.closePosition not in [True, False]:
            return False

        if not (0.1 <= order.callbackRate <= 5):
            return False

        if order.priceProtect not in [True, False]:
            return False

        if order.closePosition == True and order.quantity is not None:
            return False

        if order.reduceOnly not in [True, False]:
            return False

        if order.closePosition == True and order.reduceOnly is True:
            return False


        if order.orderType == 'LIMIT':
            if not (order.timeInForce is None or order.quantity is None or order.price is None):
                return True

        elif order.orderType == 'MARKET':
            if order.quantity is not None:
                return True

        elif order.orderType in ['STOP', 'TAKE_PROFIT']:
            if not (order.quantity is None or order.price is None or order.stopPrice is None):
                return True

        elif order.orderType in ['STOP_MARKET', 'TAKE_PROFIT_MARKET']:
            if order.stopPrice is not None:
                return True

        elif order.orderType == 'TRAILING_STOP_MARKET':
            if order.callbackRate is not None:
                return True

    @staticmethod
    def getOrderAsDict(self):
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
        params = self.getOrderAsDict(orderData)

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
        params = self.getOrderAsDict(orderData)

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
        if not interval in self.timeIntervlas:
            raise Exception('Time interval is not valid.')
        try:
            return self.client.klines(symbol, interval, startTime=startTime, endTime=endTime, limit=limit)
        except Exception:
            return None

    def getExchangeTime(self):
        try:
            return self.client.time()
        except Exception:
            return None

    def getSymbol24hTicker(self, symbol):
        try:
            return self.client.ticker_24hr(symbol)
        except Exception:
            return None

    def getSymbolFuturesOrders(self, symbol):
        return self.futuresClient.get_all_orders(symbol=symbol)

    def getFuturesBalance(self):
        return self.futuresClient.get_balance()

    def makeFuturesOrder(self, futuresOrderData):
