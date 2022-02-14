from binance.spot import Spot

class BinanceExchange():
    def __init__(self, credentials, type='SPOT', isTestNet=False):
        self.credentials = credentials
        self.isTestNet = isTestNet

        if type == 'SPOT':
            if isTestNet:
                self.client = Spot(key=credentials['spot']['key'], secret=credentials['spot']['secret'], base_url='https://testnet.binance.vision')
            else:
                self.client = Spot(key=credentials['spot']['key'], secret=credentials['spot']['secret'])

        print(self.client.coin_info())
