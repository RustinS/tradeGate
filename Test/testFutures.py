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

    def testSymbolFuturesOrders(self):
        # self.log.info('\BTCUSDT Futures Orders: {}'.format(self.tradeGate.getAllFuturesOrders('BTCUSDT')))
        self.assertIsNotNone(self.tradeGate.getSymbolFuturesOrders('BTCUSDT'))

    def testFuturesBalance(self):
        # self.log.info('\BTCUSDT Futures Balance: {}'.format(self.tradeGate.getFuturesBalance()))
        self.assertIsNotNone(self.tradeGate.getFuturesBalance())

    def testFuturesOrder(self):
        futuresOrderData = self.tradeGate.createAndTestFuturesOrder('BTCUSDT', 'BUY', 'MARKET', quantity=0.002)

        result = self.tradeGate.makeFuturesOrder(futuresOrderData)
        self.log.info('\nFutures Order Result: {}'.format(result))

        self.assertIsNotNone(result, 'Problem in submiting futures order.')
        


if __name__ == '__main__':
    unittest.main()