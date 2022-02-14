import ccxt
import json
from Exchanges.BinanceExchange import BinanceExchange


class TradeGate():
    def __init__(self, configDict, spot=False, sandbox=False, threeCred=False):
        self.apiKey = configDict['credentials']['test']['spot']['key'] if spot else configDict['credentials']['test']['futures']['key']
        self.apiSecret = configDict['credentials']['test']['spot']['secret'] if spot else configDict['credentials']['test']['futures']['secret']

        self.exchange = BinanceExchange(configDict['credentials']['test'], 'SPOT', True)

        # if threeCred:
        #     self.apiPassphrase = configDict['spot']['passphrase'] if spot else configDict['futures']['passphrase']
        #     self.exchange.password = self.apiPassphrase

        # if sandbox:
        #     self.exchange.set_sandbox_mode(True)
        
        # print(self.exchange.urls)
        
        # self.markets = self.exchange.loadMarkets()

    def getBalance(self, coin=''):
        if coin != '':
            return self.exchange.fetchBalance({'coin': coin})
        else:
            return self.exchange.fetchBalance()

if __name__ == '__main__':
    config = {}
    with open('./config.json') as f:
        config = json.load(f)

    gate = TradeGate(config['Binance'], sandbox=True)
    # print(gate.getBalance())