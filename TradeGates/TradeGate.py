import ccxt
import json
import time
from Exchanges import BinanceExchange


class TradeGate():
    def __init__(self, configDict, exchangeName, spot=False, sandbox=False):
        exchangeClass = self.getCorrectExchange(exchangeName)
        if sandbox:
            self.apiKey = configDict['credentials']['test']['spot']['key']
            self.apiSecret = configDict['credentials']['test']['spot']['secret']

            self.exchange = exchangeClass(configDict['credentials']['test'], type='SPOT', sandbox=True)
        else:
            self.apiKey = configDict['credentials']['main']['spot']['key']
            self.apiSecret = configDict['credentials']['main']['spot']['secret']

            self.exchange = exchangeClass(configDict['credentials']['test'], type='SPOT', sandbox=False)

    def getBalance(self, asset=''):
        return self.exchange.fetchBalance(asset)

    def getSymbolTradeHistory(self, symbol):
        return self.exchange.SymbolTradeHistory(symbol)


    @staticmethod
    def getCorrectExchange(exchangeName):
        if exchangeName == 'Binance':
            return BinanceExchange.BinanceExchange

class order():
    def __init__(self, symbol, side, orderType):
        self.symbol = symbol
        self.side = side
        self.orderType = orderType

        self.timeInForce = None
        self.quantity = None
        self.quoteOrderQty = None
        self.price = None
        self.newClientOrderId = None
        self.stopPrice = None
        self.icebergQty = None
        self.newOrderRespType = None
        self.recvWindow = None

    def setTimeInForce(self, timeInForce):
        self.timeInForce = timeInForce

    def setQuantity(self, quantity):
        self.quantity = quantity

    def setQuoteOrderQty(self, quoteOrderQty):
        self.quoteOrderQty = quoteOrderQty
    
    def setPrice(self, price):
        self.price = price
    
    def setNewClientOrderId(self, newClientOrderId):
        self.newClientOrderId = newClientOrderId

    def setStopPrice(self, stopPrice):
        self.stopPrice = stopPrice

    def setIcebergQty(self, icebergQty):
        self.icebergQty = icebergQty
    
    def setNewOrderRespType(self, newOrderRespType):
        self.newOrderRespType = newOrderRespType

    def setRecvWindow(self, recvWindow):
        self.recvWindow = recvWindow
    
    def setTimeStamp(self):
        self.timeStamp = time.time()

    
