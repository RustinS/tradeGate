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

    def testSymbollFuturesOrders(self):
        # self.log.info('\BTCUSDT Futures Orders: {}'.format(self.tradeGate.getAllFuturesOrders('BTCUSDT')))
        self.assertIsNotNone(self.tradeGate.getSymbolFuturesOrders('BTCUSDT'))

    def testFuturesBalance(self):
        # self.log.info('\BTCUSDT Futures Balance: {}'.format(self.tradeGate.getFuturesBalance()))
        self.assertIsNotNone(self.tradeGate.getFuturesBalance())
        


if __name__ == '__main__':
    unittest.main()