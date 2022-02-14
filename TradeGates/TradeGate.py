import ccxt
import json
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

    # def getSymbolTradeHistory(self, symbol):


    @staticmethod
    def getCorrectExchange(exchangeName):
        if exchangeName == 'Binance':
            return BinanceExchange.BinanceExchange

