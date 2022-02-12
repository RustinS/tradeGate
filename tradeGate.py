import ccxt
import json


class TradeGate():
    def __init__(self, configAddress):
        configFile = open(configAddress)
        config = json.load(configFile)
        self.apiKey = config['key']
        self.apiSecret = config['secret']
        self.apiPassphrase = config['passphrase']
        
        self.exchange = ccxt.kucoin({
            'apiKey': self.apiKey,
            'secret': self.apiSecret,
            'password': self.apiPassphrase,
        })
        
        self.markets = self.exchange.loadMarkets()