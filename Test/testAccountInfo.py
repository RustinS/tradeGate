import unittest
import json
from TradeGates.TradeGate import TradeGate


class BinanceAccountInfoTest(unittest.TestCase):
    def setUp(self):
        with open('./config.json') as f:
            config = json.load(f)

        self.tradeGate = TradeGate(config['Binance'], 'Binance', sandbox=True)

    def testFullBalance(self):
        self.assertIsNotNone(self.tradeGate.getBalance(), 'Assert fetching balance is not none')

    def testSingleCoinBalance(self):
        self.assertIsNotNone(self.tradeGate.getBalance('BTC'), 'Assert fetching single coin balance is not none')


if __name__ == '__main__':
    unittest.main()