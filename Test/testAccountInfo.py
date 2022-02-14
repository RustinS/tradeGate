import unittest
import json
from TradeGates.TradeGate import TradeGate


class AccountInfoTest(unittest.TestCase):
    def setUp(self):
        with open('./config.json') as f:
            config = json.load(f)

        self.tradeGate = TradeGate(config['Binance'], sandbox=True)

    def testBalance(self):
        print(self.tradeGate.getBalance())
        self.assertIsNotNone(self.tradeGate.getBalance(), 'Assert fetching balance is not none')


if __name__ == '__main__':
    unittest.main()