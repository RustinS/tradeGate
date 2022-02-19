import unittest
import json
from TradeGates.TradeGate import TradeGate
from Utils.DataHelpers import OrderData
import logging


class BinanceOrderingTest(unittest.TestCase):
    def setUp(self):
        with open('./config.json') as f:
            config = json.load(f)

        self.tradeGate = TradeGate(config['Binance'], 'Binance', sandbox=True)
        loglevel = logging.INFO
        logging.basicConfig(level=loglevel)
        self.log = logging.getLogger(__name__)

    def testNewTestOrder(self):
        try:
            res = self.tradeGate.createAndTestOrder('BTCUSDT', 'SELL', 'LIMIT', timeInForce='GTC', quantity=0.002, price=49500)
        except Exception as e:
            self.fail('Problem in order data')

    def testNewOrder(self):
        try:
            verifiedOrder = self.tradeGate.createAndTestOrder('BTCUSDT', 'BUY', 'MARKET', quantity=0.002)
        except Exception as e:
            self.fail('Problem in order data: {}'.format(str(e)))

        try:
            self.tradeGate.makeOrder(verifiedOrder)
        except Exception as e:
            self.fail('Problem in making order: {}'.format(str(e)))

if __name__ == '__main__':
    unittest.main()