from pybit import HTTP

from BaseExchange import BaseExchange
from Utils import DataHelpers



class BybitExchange(BaseExchange):
    def __init__(self, credentials, sandbox=False):
        self.apiKey = credentials['spot']['key']
        self.secret = credentials['spot']['secret']
        self.sandbox = sandbox

        if sandbox:
            self.spotSession = HTTP("https://api-testnet.bybit.com", api_key=self.apiKey, api_secret=self.secret, spot=True)
            self.futuresSession = HTTP("https://api-testnet.bybit.com", api_key=self.apiKey, api_secret=self.secret)
        else:
            self.spotSession = HTTP("https://api.bybit.com", api_key=self.apiKey, api_secret=self.secret, spot=True)
            self.futuresSession = HTTP("https://api.bybit.com", api_key=self.apiKey, api_secret=self.secret)

        self.timeIndexesInCandleData = [0, 6]
        self.desiredCandleDataIndexes = [0, 1, 2, 3, 4, 5, 6, 8]
        
        self.futuresSymbols = []
        for symbol in self.futuresSession.query_symbol()['result']:
            if symbol['name'].endswith('USDT'):
                self.futuresSymbols.append(symbol['name']) 


    @staticmethod
    def isOrderDataValid(order : DataHelpers.OrderData):
        pass


    @staticmethod
    def isFuturesOrderDataValid(order : DataHelpers.futuresOrderData):
        pass

    
    @staticmethod
    def getOrderAsDict(order : DataHelpers.OrderData):
        pass

    
    @staticmethod
    def getFuturesOrderAsDict(order : DataHelpers.futuresOrderData):
        pass

    
    def getBalance(self, asset='', futures=False):
        if futures:
            if asset is None or asset == '':
                return self.futuresSession.get_wallet_balance()['result']
            else:
                return self.futuresSession.get_wallet_balance(coin=asset)['result']
        else:
            if asset is None or asset == '':
                return self.spotSession.get_wallet_balance()['result']
            else:
                assets = self.spotSession.get_wallet_balance()['result']
                for coin in assets:
                    if asset == coin['name']:
                        return coin
                return None
            
    
    def SymbolTradeHistory(self, symbol, futures=False, fromId=None, limit=None):
        pass


    def testSpotOrder(self, orderData):
        pass

    
    def makeSpotOrder(self, orderData):
        pass

    
    def getSymbolOrders(self, symbol, futures=False):
        pass


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

    
    def getSymbolKlines(self, symbol, interval, startTime=None, endTime=None, limit=None, futures=False, BLVTNAV=False, convertDateTime=False, doClean=False, toCleanDataframe=False):
        pass

    
    def getExchangeTime(self):
        pass

    
    def getSymbol24hTicker(self, symbol):
        pass

    
    def getAllSymbolFuturesOrders(self, symbol):
        pass

    
    def makeFuturesOrder(self, futuresOrderData):
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
