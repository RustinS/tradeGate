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
        testOrder = OrderData('BTCUSDT', 'SELL', 'LIMIT')

        testOrder.setTimeInForce('GTC')
        testOrder.setQuantity(0.002)
        testOrder.setPrice(49500)
        res = self.tradeGate.createAndTestOrder('BTCUSDT', 'SELL', 'LIMIT', timeInForce='GTC', quantity=0.002, price=49500)
        self.log.info('\n {}'.format(res))


if __name__ == '__main__':
    unittest.main()