import unittest
import json
from TradeGates.TradeGate import TradeGate
import logging


class BinanceAccountInfoTest(unittest.TestCase):
    def setUp(self):
        with open('./config.json') as f:
            config = json.load(f)

        self.tradeGate = TradeGate(config['Binance'], 'Binance', sandbox=True)
        loglevel = logging.INFO
        logging.basicConfig(level=loglevel)
        self.log = logging.getLogger(__name__)

    def testAveragePrice(self):
        # self.log.info('\BTCUSDT Future Orders: {}'.format(self.tradeGate.getAllFuturesOrders('BTCUSDT')))
        self.assertIsNotNone(self.tradeGate.getAllFuturesOrders('BTCUSDT'))
        


if __name__ == '__main__':
    unittest.main()