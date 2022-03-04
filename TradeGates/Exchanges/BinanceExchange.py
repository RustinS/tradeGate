import logging
import time
import pandas as pd

from BaseExchange import BaseExchange
from datetime import datetime
from binance.spot import Spot
from Utils import DataHelpers
from binance.error import ClientError
from binance_f import RequestClient
from binance_f.model.constant import *
from binance_f.model.balance import Balance



class BinanceExchange(BaseExchange):
    def __init__(self, credentials, sandbox=False):
        self.credentials = credentials
        self.sandbox = sandbox

        if sandbox:
            self.client = Spot(key=credentials['spot']['key'], secret=credentials['spot']['secret'], base_url='https://testnet.binance.vision')
            self.futuresClient = RequestClient(api_key=credentials['futures']['key'], secret_key=credentials['futures']['secret'], url='https://testnet.binancefuture.com')
        else:
            self.client = Spot(key=credentials['spot']['key'], secret=credentials['spot']['secret'])
            self.futuresClient = RequestClient(api_key=credentials['futures']['key'], secret_key=credentials['futures']['secret'])

        self.timeIntervlas = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

        self.timeIndexesInCandleData = [0, 6]
        self.desiredCandleDataIndexes = [0, 1, 2, 3, 4, 5, 6, 8]


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

        if not order.callbackRate is None:
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
    def getOrderAsDict(order : DataHelpers.OrderData):
        if order.timestamp is None:
            raise Exception('Timestamp must be set')

        params = {}
        params['symbol'] = order.symbol
        params['side'] = order.side
        params['type'] = order.orderType
        params['timestamp'] = order.timestamp

        if not order.timeInForce is None:
            params['timeInForce'] = order.timeInForce

        if not order.quantity is None:
            params['quantity'] = order.quantity
        
        if not order.quoteOrderQty is None:
            params['quoteOrderQty'] = order.quoteOrderQty

        if not order.price is None:
            params['price'] = order.price
        
        if not order.newOrderRespType is None:
            params['newOrderRespType'] = order.newOrderRespType
        
        if not order.stopPrice is None:
            params['stopPrice'] = order.stopPrice
        
        if not order.icebergQty is None:
            params['icebergQty'] = order.icebergQty
        
        if not order.newClientOrderId is None:
            params['newOrderRespType'] = order.newOrderRespType
        
        if not order.recvWindow is None:
            params['recvWindow'] = order.recvWindow

        return params


    @staticmethod
    def getFuturesOrderAsDict(order : DataHelpers.futuresOrderData):
        params = {}
        params['symbol'] = order.symbol
        params['side'] = order.side
        params['ordertype'] = order.orderType

        if not order.positionSide is None:
            params['positionSide'] = order.positionSide

        if not order.timeInForce is None:
            params['timeInForce'] = order.timeInForce

        if not order.quantity is None:
            params['quantity'] = order.quantity
        
        if not order.reduceOnly is None:
            params['reduceOnly'] = order.reduceOnly

        if not order.price is None:
            params['price'] = order.price
        
        if not order.newClientOrderId is None:
            params['newClientOrderId'] = order.newClientOrderId
        
        if not order.stopPrice is None:
            params['stopPrice'] = order.stopPrice
        
        if not order.closePosition is None:
            params['closePosition'] = order.closePosition
        
        if not order.activationPrice is None:
            params['activationPrice'] = order.activationPrice
        
        if not order.callbackRate is None:
            params['callbackRate'] = order.callbackRate

        if not order.workingType is None:
            params['workingType'] = order.workingType

        if not order.priceProtect is None:
            params['priceProtect'] = order.priceProtect

        if not order.newOrderRespType is None:
            params['newOrderRespType'] = order.newOrderRespType

        if not order.recvWindow is None:
            params['recvWindow'] = order.recvWindow

        return params


    def getBalance(self, asset='', futures=False):
        if not futures:
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
        else:
            balances = []
            for balance in self.futuresClient.get_balance():
                balances.append(balance.toDict())

            if asset == '':
                return balances
            else:
                for balance in balances:
                    if balance['asset'] == asset:
                        return balance
                return Balance.makeFreeBalance(asset)
            return None
            

    def SymbolTradeHistory(self, symbol, futures=False, fromId=None, limit=None):
        try:
            if not futures:
                return self.client.my_trades(symbol, fromId=fromId, limit=limit)
            else:
                trades = []
                for trade in self.futuresClient.get_account_trades(symbol=symbol, fromId=fromId, limit=limit):
                    trades.append(trade.toDict())
                return trades

        except Exception:
            return None


    def testSpotOrder(self, orderData):
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


    def makeSpotOrder(self, orderData):
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


    def getSymbolOrders(self, symbol, futures=False):
        try:
            if not futures:
                return self.client.get_orders(symbol, timestamp=time.time())
            else:
                orders = []
                for order in self.futuresClient.get_all_orders(symbol):
                    orders.append(order.toDict())
                return orders
        except Exception:
            return None


    def getOpenOrders(self, symbol=None, futures=False):
        try:
            if not futures:
                return self.client.get_open_orders(symbol, timestamp=time.time())
            else:
                orders = []
                for order in self.futuresClient.get_open_orders(symbol=symbol):
                    orders.append(order.toDict())
                return orders
        except Exception:
            return None


    def cancelAllSymbolOpenOrders(self, symbol, futures=False):
        if not futures:
            openOrders = self.getOpenOrders(symbol)
            if len(openOrders) == 0:
                return []
            else:
                return self.client.cancel_open_orders(symbol, timestamp=time.time())
        else:
            openOrders = self.getOpenOrders(symbol, futures=True)

            if len(openOrders) == 0:
                return []
            else:
                orderIds = [order['orderId'] for order in openOrders]

                results = []
                for res in self.futuresClient.cancel_list_orders(symbol=symbol, orderIdList=orderIds):
                    results.append(res.toDict())

                return results


    def cancelOrder(self, symbol, orderId=None, localOrderId=None, futures=False):
        if not futures:
            if not orderId is None:
                return self.client.cancel_order(symbol, orderId=orderId, timestamp=time.time())
            elif not localOrderId is None:
                return self.client.cancel_order(symbol, origClientOrderId=localOrderId, timestamp=time.time())
            else:
                raise Exception('Specify either order Id in the exchange or local Id sent with the order')
        else:
            if not orderId is None:
                return self.futuresClient.cancel_order(symbol, orderId=orderId).toDict()
            elif not localOrderId is None:
                return self.futuresClient.cancel_order(symbol, origClientOrderId=localOrderId).toDict()
            else:
                raise Exception('Specify either order Id in the exchange or local Id sent with the order')
    

    def getOrder(self, symbol, orderId=None, localOrderId=None, futures=False):
        if not futures:
            if not orderId is None:
                return self.client.get_order(symbol, orderId=orderId, timestamp=time.time())
            elif not localOrderId is None:
                return self.client.get_order(symbol, origClientOrderId=localOrderId, timestamp=time.time())
            else:
                raise Exception('Specify either order Id in the exchange or local Id sent with the order')
        else:
            if not orderId is None:
                return self.futuresClient.get_order(symbol, orderId=orderId).toDict()
            elif not localOrderId is None:
                return self.futuresClient.get_order(symbol, origClientOrderId=localOrderId).toDict()
            else:
                raise Exception('Specify either order Id in the exchange or local Id sent with the order')
        

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


    def getSymbolTickerPrice(self, symbol):
        try:
            return self.client.ticker_price(symbol)['price']
        except Exception:
            return None


    def getSymbolKlines(self, symbol, interval, startTime=None, endTime=None, limit=None, futures=False, BLVTNAV=False, convertDateTime=False, doClean=False, toCleanDataframe=False):
        if not interval in self.timeIntervlas:
            raise Exception('Time interval is not valid.')

        if futures:
            data = []
            if BLVTNAV:
                candles = self.futuresClient.get_blvt_nav_candlestick_data(symbol=symbol, interval=interval, startTime=startTime, endTime=endTime, limit=limit)
            else:
                candles = self.futuresClient.get_candlestick_data(symbol=symbol, interval=interval, startTime=startTime, endTime=endTime, limit=limit)

            for candle in candles:
                data.append(candle.toArray())
        else:
            data = self.client.klines(symbol, interval, startTime=startTime, endTime=endTime, limit=limit)

            for datum in data:
                for idx in range(len(datum)):
                    if idx in self.timeIndexesInCandleData:
                        continue
                    datum[idx] = float(datum[idx])

        if convertDateTime or toCleanDataframe:
            for datum in data:
                for idx in self.timeIndexesInCandleData:
                    datum[idx] = datetime.fromtimestamp(float(datum[idx]) / 1000)

        if doClean or toCleanDataframe:
            outArray = []
            for datum in data:
                outArray.append([datum[index] for index in self.desiredCandleDataIndexes])

            if toCleanDataframe:
                df = pd.DataFrame(outArray, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'closeDate', 'tradesNum'])
                df.set_index('date', inplace=True)
                return df
            return outArray
        else:
            return data


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


    def getAllSymbolFuturesOrders(self, symbol):
        return self.futuresClient.get_all_orders(symbol=symbol)


    def makeFuturesOrder(self, futuresOrderData):
        params = self.getFuturesOrderAsDict(futuresOrderData)

        try:
            response = self.futuresClient.post_order(**params)
            return response.toDict()
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
        

    def cancellAllSymbolFuturesOrdersWithCountDown(self, symbol, countdownTime):
        return self.futuresClient.auto_cancel_all_orders(symbol, countdownTime)

    def changeInitialLeverage(self, symbol, leverage):
        return self.futuresClient.change_initial_leverage(symbol=symbol, leverage=leverage)

    def changeMarginType(self, symbol, marginType):
        if marginType not in ['ISOLATED', 'CROSSED']:
            raise Exception('Margin type specified is not acceptable')
        
        return self.futuresClient.change_margin_type(symbol=symbol, marginType=marginType)

    def changePositionMargin(self, symbol, amount, marginType):
        if marginType not in [1, 2]:
            raise Exception('Bad type specified.')
        self.futuresClient.change_position_margin(symbol=symbol, amount=amount, type=marginType)

    def getPosition(self):
        return self.futuresClient.get_position()

    def spotBestBidAsks(self, symbol=None):
        return self.client.book_ticker(symbol=symbol)

    def getSymbolOrderBook(self, symbol, limit=None, futures=False):
        if not futures:
            if limit is None:
                return self.client.depth(symbol)
            else:
                return self.clinet.depth(symbol, limit=limit)
        else:
            if limit is None:
                return self.futuresClient.get_order_book(symbol=symbol)
            else:
                return self.futuresClient.get_order_book(symbol=symbol, limit=limit)

    def getSymbolRecentTrades(self, symbol, limit=None, futures=False):
        if not limit is None:
            if limit > 1000: limit = 1000
            elif limit < 1: limit = 1
        if not futures:
            if limit is None:
                return self.client.trades(symbol)
            else:
                return self.clinet.trades(symbol, limit=limit)
        else:
            if limit is None:
                return self.futuresClient.get_recent_trades_list(symbol=symbol)
            else:
                return self.futuresClient.get_recent_trades_list(symbol=symbol, limit=limit)

        
