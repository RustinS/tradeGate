from binance.spot import Spot

class BinanceExchange():
    def __init__(self, credentials, type='SPOT', sandbox=False):
        self.credentials = credentials
        self.sandbox = sandbox

        if type == 'SPOT':
            if sandbox:
                self.client = Spot(key=credentials['spot']['key'], secret=credentials['spot']['secret'], base_url='https://testnet.binance.vision')
            else:
                self.client = Spot(key=credentials['spot']['key'], secret=credentials['spot']['secret'])

    def fetchBalance(self, asset=''):
        try:
            balances = self.client.account()['balances']
        except:
            return None

        if asset == '':
            return balances
        else:
            for balance in balances:
                if balance['asset'] == asset:
                    return balance
        return None
