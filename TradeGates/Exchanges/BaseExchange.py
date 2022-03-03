from abc import ABC, abstractmethod
from Utils import DataHelpers



class BaseExchange(ABC):
    @abstractmethod
    def __init__(self, credentials, sandbox=False):
        pass


    @abstractmethod
    @staticmethod
    def isOrderDataValid(order : DataHelpers.OrderData):
        pass


    @abstractmethod
    @staticmethod
    def isFuturesOrderDataValid(order : DataHelpers.futuresOrderData):
        pass

    
    @abstractmethod
    @staticmethod
    def getOrderAsDict(order : DataHelpers.OrderData):
        pass

    
    @abstractmethod
    @staticmethod
    def getFuturesOrderAsDict(order : DataHelpers.futuresOrderData):
        pass

    
    @abstractmethod
    def getBalance(self, asset='', futures=False):
        pass
            
    
    @abstractmethod
    def SymbolTradeHistory(self, symbol):
        pass


    @abstractmethod
    def testOrder(self, orderData):
        pass

    
    @abstractmethod
    def makeOrder(self, orderData):
        pass

    
    @abstractmethod
    def getSymbolOrders(self, symbol, futures=False):
        pass


    @abstractmethod
    def getOpenOrders(self, symbol=None):
        pass

    
    @abstractmethod
    def cancelAllSymbolOpenOrders(self, symbol):
        pass


    @abstractmethod
    def cancelSymbolOpenOrder(self, symbol, orderId=None, localOrderId=None):
        pass
    

    @abstractmethod
    def getOrder(self, symbol, orderId=None, localOrderId=None):
        pass
        

    @abstractmethod
    def getTradingFees(self):
        pass

    
    @abstractmethod
    def getSymbolAveragePrice(self, symbol):
        pass

    
    @abstractmethod
    def getSymbolLatestTrades(self, symbol, limit=None):
        pass


    @abstractmethod
    def getSymbolTickerPrice(self, symbol):
        pass

    
    @abstractmethod
    def getSymbolKlines(self, symbol, interval, startTime=None, endTime=None, limit=None, futures=False, BLVTNAV=False, convertDateTime=False, doClean=False, toCleanDataframe=False):
        pass

    
    @abstractmethod
    def getExchangeTime(self):
        pass

    
    @abstractmethod
    def getSymbol24hTicker(self, symbol):
        pass

    
    @abstractmethod
    def getAllSymbolFuturesOrders(self, symbol):
        pass

    
    @abstractmethod
    def makeFuturesOrder(self, futuresOrderData):
        pass
    

    @abstractmethod
    def cancelAllSymbolFuturesOpenOrders(self, symbol):
        pass


    @abstractmethod
    def cancelFuturesOrder(self, symbol, orderId=None, localOrderId=None):
        pass


    @abstractmethod
    def getAllFuturesOpenOrders(self, symbol=None):
        pass
    

    @abstractmethod
    def getFuturesOrder(self, symbol, orderId=None, localOrderId=None):
        pass


    @abstractmethod
    def cancellAllSymbolFuturesOrders(self, symbol, countdownTime):
        pass


    @abstractmethod
    def changeInitialLeverage(self, symbol, leverage):
        pass


    @abstractmethod
    def changeMarginType(self, symbol, marginType):
        pass

    
    @abstractmethod
    def changePositionMargin(self, symbol, amount, marginType):
        pass

    
    @abstractmethod
    def getPosition(self):
        pass


    @abstractmethod
    def spotBestBidAsks(self, symbol=None):
        pass


    @abstractmethod
    def getSymbolOrderBook(self, symbol, limit=None, futures=False):
        pass


    @abstractmethod
    def getSymbolRecentTrades(self, symbol, limit=None, futures=False):
        pass
