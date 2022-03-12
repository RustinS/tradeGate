import logging

from pybit import HTTP

from BaseExchange import BaseExchange
from Utils import DataHelpers, BybitHelpers


class PyBitHTTP(HTTP):
    def __init__(self, endpoint=None, api_key=None, api_secret=None, logging_level=logging.INFO, log_requests=False,
                 request_timeout=10, recv_window=5000, force_retry=False, retry_codes=None, ignore_codes=None,
                 max_retries=3, retry_delay=3, referral_id=None, spot=False):
        super().__init__(endpoint, api_key, api_secret, logging_level, log_requests, request_timeout, recv_window,
                         force_retry, retry_codes, ignore_codes, max_retries, retry_delay, referral_id, spot)

    def query_history_order(self, **kwargs):
        if self.spot is True:
            suffix = '/spot/v1/history-orders'

            return self._submit_request(
                method='GET',
                path=self.endpoint + suffix,
                query=kwargs,
                auth=True
            )
        else:
            raise NotImplementedError('Not implemented for futures market.')


class BybitExchange(BaseExchange):
    def __init__(self, credentials, sandbox=False, unifiedInOuts=True):
        self.apiKey = credentials['spot']['key']
        self.secret = credentials['spot']['secret']
        self.sandbox = sandbox
        self.unifiedInOuts = unifiedInOuts

        if sandbox:
            self.spotSession = PyBitHTTP("https://api-testnet.bybit.com", api_key=self.apiKey, api_secret=self.secret,
                                         spot=True)
            self.futuresSession = PyBitHTTP("https://api-testnet.bybit.com", api_key=self.apiKey,
                                            api_secret=self.secret)
        else:
            self.spotSession = PyBitHTTP("https://api.bybit.com", api_key=self.apiKey, api_secret=self.secret,
                                         spot=True)
            self.futuresSession = PyBitHTTP("https://api.bybit.com", api_key=self.apiKey, api_secret=self.secret)

        self.timeIndexesInCandleData = [0, 6]
        self.desiredCandleDataIndexes = [0, 1, 2, 3, 4, 5, 6, 8]

        self.futuresSymbols = []
        for symbol in self.futuresSession.query_symbol()['result']:
            if symbol['name'].endswith('USDT'):
                self.futuresSymbols.append(symbol['name'])

    @staticmethod
    def isOrderDataValid(order: DataHelpers.OrderData):
        pass

    @staticmethod
    def isFuturesOrderDataValid(order: DataHelpers.futuresOrderData):
        pass

    @staticmethod
    def getOrderAsDict(order: DataHelpers.OrderData):
        pass

    @staticmethod
    def getFuturesOrderAsDict(order: DataHelpers.futuresOrderData):
        pass

    def getBalance(self, asset='', futures=False):
        if futures:
            if asset in [None, '']:
                return BybitHelpers.getBalanceOut(self.futuresSession.get_wallet_balance()['result'], futures=True)
            else:
                return BybitHelpers.getBalanceOut(self.futuresSession.get_wallet_balance(coin=asset)['result'],
                                                  single=True, futures=True)
        else:
            if asset in [None, '']:
                return BybitHelpers.getBalanceOut(self.spotSession.get_wallet_balance()['result']['balances'])
            else:
                assets = self.spotSession.get_wallet_balance()['result']['balances']
                for coin in assets:
                    if asset == coin['coin']:
                        return BybitHelpers.getBalanceOut(coin, single=True)
                return None

    def symbolAccountTradeHistory(self, symbol, futures=False, fromId=None, limit=None):
        if futures:
            tradeHistory = self.futuresSession.user_trade_records(symbol=symbol, limit=limit, fromId=fromId)
            return BybitHelpers.getMyTradeHistory(tradeHistory['result'])
        else:
            tradeHistory = self.spotSession.user_trade_records(symbol=symbol, limit=limit, fromId=fromId)
            return BybitHelpers.getMyTradeHistory(tradeHistory['result'])

    def testSpotOrder(self, orderData):
        pass

    def makeSpotOrder(self, orderData):
        pass

    def getSymbolOrders(self, symbol, futures=False, orderId=None, startTime=None, endTime=None, limit=None):
        if futures:
            historyList = []
            pageNumber = 1
            endTimeString = None
            startTimeString = None
            done = False
            while not done:
                history = self.futuresSession.get_active_order(symbol=symbol, page=pageNumber, limit=50)

                if startTime is not None:
                    startTimeString = startTime.strftime('%Y-%m-%dT%H:%M:%SZ')
                if endTime is not None:
                    endTimeString = endTime.strftime('%Y-%m-%dT%H:%M:%SZ')

                for order in history['result']['data']:
                    if endTime is not None:
                        if endTimeString < order['create_time']:
                            continue

                    if startTime is not None:
                        if order['created_time'] < startTimeString:
                            done = True
                            break

                    historyList.append(order)

                if limit is not None and limit <= len(historyList):
                    done = True

                if len(history['result']['data']) < 50:
                    done = True

                pageNumber += 1

            return historyList
        else:
            history = self.spotSession.query_history_order(symbol=symbol, orderId=orderId, startTime=startTime,
                                                           endtime=endTime, limit=limit)
            return history['result']

    def getOpenOrders(self, symbol=None):
        pass

    def cancelAllSymbolOpenOrders(self, symbol, futures=False):
        pass

    def cancelOrder(self, symbol, orderId=None, localOrderId=None, futures=False):
        pass

    def getOrder(self, symbol, orderId=None, localOrderId=None, futures=False):
        pass

    def getTradingFees(self):
        pass

    def getSymbolAveragePrice(self, symbol):
        pass

    def getSymbolTickerPrice(self, symbol):
        pass

    def getSymbolKlines(self, symbol, interval, startTime=None, endTime=None, limit=None, futures=False, blvtnav=False,
                        convertDateTime=False, doClean=False, toCleanDataframe=False):
        pass

    def getExchangeTime(self):
        pass

    def getSymbol24hTicker(self, symbol):
        pass

    def getAllSymbolFuturesOrders(self, symbol):
        pass

    def makeFuturesOrder(self, futuresOrderData):
        pass

    def makeBatchFuturesOrder(self, futuresOrderDatas):
        pass

    def cancellAllSymbolFuturesOrdersWithCountDown(self, symbol, countdownTime):
        pass

    def changeInitialLeverage(self, symbol, leverage):
        pass

    def changeMarginType(self, symbol, marginType):
        pass

    def changePositionMargin(self, symbol, amount, marginType):
        pass

    def getPosition(self):
        pass

    def spotBestBidAsks(self, symbol=None):
        pass

    def getSymbolOrderBook(self, symbol, limit=None, futures=False):
        pass

    def getSymbolRecentTrades(self, symbol, limit=None, futures=False):
        pass
