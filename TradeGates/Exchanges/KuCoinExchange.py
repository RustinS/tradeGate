from Exchanges.BaseExchange import BaseExchange
from Utils import KuCoinHelpers

from kucoin.client import User, Trade, Market
from kucoin_futures.client import FuturesUser, FuturesTrade, FuturesMarket


class KuCoinExchange(BaseExchange):
    def __init__(self, credentials, sandbox=False, unifiedInOuts=True):
        self.spotApiKey = credentials['spot']['key']
        self.spotSecret = credentials['spot']['secret']
        self.spotPassphrase = credentials['spot']['passphrase']

        self.futuresApiKey = credentials['futures']['key']
        self.futuresSecret = credentials['futures']['secret']
        self.futuresPassphrase = credentials['futures']['passphrase']

        self.sandbox = sandbox
        self.unifiedInOuts = unifiedInOuts

        if sandbox:
            self.spotUser = User(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase,
                                 is_sandbox=True)
            self.spotTrade = Trade(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase,
                                   is_sandbox=True)
            self.spotMarket = Market(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase,
                                     is_sandbox=True)

            self.futuresUser = FuturesUser(key=self.futuresApiKey, secret=self.futuresSecret,
                                           passphrase=self.futuresPassphrase, is_sandbox=True)
            self.futuresTrade = FuturesTrade(key=self.futuresApiKey, secret=self.futuresSecret,
                                             passphrase=self.futuresPassphrase, is_sandbox=True)
            self.futuresMarket = FuturesMarket(key=self.futuresApiKey, secret=self.futuresSecret,
                                               passphrase=self.futuresPassphrase, is_sandbox=True)
        else:
            self.spotUser = User(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase)
            self.spotTrade = Trade(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase)
            self.spotMarket = Market(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase)

            self.futuresUser = FuturesUser(key=self.futuresApiKey, secret=self.futuresSecret,
                                           passphrase=self.futuresPassphrase)
            self.futuresTrade = FuturesTrade(key=self.futuresApiKey, secret=self.futuresSecret,
                                             passphrase=self.futuresPassphrase)
            self.futuresMarket = FuturesMarket(key=self.futuresApiKey, secret=self.futuresSecret,
                                               passphrase=self.futuresPassphrase)

    def getBalance(self, asset=None, futures=False):
        if futures:
            raise NotImplementedError()
        else:
            if asset is None:
                return KuCoinHelpers.unifyGetBalanceSpotOut(self.spotUser.get_account_list(currency=asset))
            else:
                return KuCoinHelpers.unifyGetBalanceSpotOut(self.spotUser.get_account_list(currency=asset),
                                                            isSingle=True)

    def symbolAccountTradeHistory(self, symbol, futures=False, fromId=None, limit=None):
        if futures:
            raise NotImplementedError()
        else:
            return self.spotTrade.get_fill_list(tradeType='TRADE', orderId=fromId)

    def testSpotOrder(self, orderData):
        pass

    def makeSpotOrder(self, orderData):
        pass

    def getSymbolOrders(self, symbol, futures=False, orderId=None, startTime=None, endTime=None, limit=None):
        pass

    def getOpenOrders(self, symbol, futures=False):
        pass

    def cancelAllSymbolOpenOrders(self, symbol, futures=False):
        pass

    def cancelOrder(self, symbol, orderId=None, localOrderId=None, futures=False):
        pass

    def getOrder(self, symbol, orderId=None, localOrderId=None, futures=False):
        pass

    def getTradingFees(self):
        pass

    def getSymbolTickerPrice(self, symbol, futures=False):
        pass

    def getSymbolKlines(self, symbol, interval, startTime=None, endTime=None, limit=None, futures=False, blvtnav=False,
                        convertDateTime=False, doClean=False, toCleanDataframe=False):
        pass

    def getExchangeTime(self, futures=False):
        pass

    def getSymbol24hTicker(self, symbol):
        pass

    def testFuturesOrder(self, futuresOrderData):
        pass

    def makeFuturesOrder(self, futuresOrderData):
        pass

    def makeBatchFuturesOrder(self, futuresOrderDatas):
        pass

    def changeInitialLeverage(self, symbol, leverage):
        pass

    def changeMarginType(self, symbol, marginType, params):
        pass

    def changePositionMargin(self, symbol, amount, marginType=None):
        pass

    def getPosition(self):
        pass

    def spotBestBidAsks(self, symbol=None):
        pass

    def getSymbolOrderBook(self, symbol, limit=None, futures=False):
        pass

    def getSymbolRecentTrades(self, symbol, limit=None, futures=False):
        pass

    def getPositionInfo(self, symbol=None):
        pass

    def getSymbolMinTrade(self, symbol, futures=False):
        pass
