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

    def testNewTestOrderBadOrderType(self):
        try:
            res = self.tradeGate.createAndTestOrder('BTCUSDT', 'SELL', 'LINIT', timeInForce='GTC', quantity=0.002, price=49500)
        except Exception as e:
            return
        
        self.fail('Problem in validating order data')

    def testNewOrder(self):
        try:
            verifiedOrder = self.tradeGate.createAndTestOrder('BTCUSDT', 'BUY', 'MARKET', quantity=0.002)
        except Exception as e:
            self.fail('Problem in order data: {}'.format(str(e)))

        try:
            self.tradeGate.makeOrder(verifiedOrder)
        except Exception as e:
            self.fail('Problem in making order: {}'.format(str(e)))

    def testGetOrders(self):
        # self.log.info('\nOrders: {}'.format(self.tradeGate.getSymbolOrders('BTCUSDT')))
        self.assertIsNotNone(self.tradeGate.getSymbolOrders('BTCUSDT'), 'Problem in getting list of all orders')

    def testGetOpenOrders(self):
        # self.log.info('\nOrders: {}'.format(self.tradeGate.getSymbolOrders('BTCUSDT')))
        self.assertIsNotNone(self.tradeGate.getOpenOrders(), 'Problem in getting list of open orders without symbol.')
        self.assertIsNotNone(self.tradeGate.getOpenOrders('BTCUSDT'), 'Problem in getting list of open orders with symbol.')


if __name__ == '__main__':
    unittest.main()