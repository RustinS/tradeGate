import unittest
import json
from TradeGates.TradeGate import TradeGate
import logging
import pytest



loglevel = logging.INFO
logging.basicConfig(level=loglevel)
log = logging.getLogger(__name__)

@pytest.fixture
def getGates():
    gates = []
    with open('./config.json') as f:
        config = json.load(f)

    for key in config.keys():
        gates.append(TradeGate(config[key], sandbox=True))

    return gates

def testSymbolFuturesOrders(getGates):
    for gate in getGates:
        symbolFutureOrders = gate.getSymbolOrders('BTCUSDT', futures=True)
        # print('\nSymbol future orders from {} exchange: {}'.format(gate.exchangeName, symbolFutureOrders))
        assert symbolFutureOrders is not None, 'Futures order list is none.'

def testFuturesBalance(getGates):
    for gate in getGates:
        balance = gate.getBalance(futures=True)
        print('\nFutures balance from {} exchange: {}'.format(gate.exchangeName, balance))
        assert balance is not None, 'Futures balance is none.'

def testFuturesSingleCoinBalance(getGates):
    for gate in getGates:
        balance = gate.getBalance('BTC', futures=True)
        # print('\nBTC Futures balance from {} exchange: {}'.format(gate.exchangeName, balance))
        assert balance is not None, 'Futures single coin balance is none.'

def testFuturesOrder(getGates):
    for gate in getGates:
        futuresOrderData = gate.createAndTestFuturesOrder('BTCUSDT', 'BUY', 'MARKET', quantity=0.002)
        result = gate.makeFuturesOrder(futuresOrderData)

        # print('\nFuture ordering in [] exchange: {}'.format(gate.exchangeName, result))
        assert result is not None, 'Problem in submiting futures order.'

def testCancelingAllFuturesOpenOrders(getGates):
    for gate in getGates:
        result = gate.cancelAllSymbolFuturesOpenOrders('BTCUSDT')

        print('\nFuture order canceling in [] exchange: {}'.format(gate.exchangeName, result))
        assert result is not None, 'Problem in canceling all futures orders'

def testGetFuturesOpenOrders(getGates):
    for gate in getGates:
        cancelAllOrdersResult = gate.getAllFuturesOpenOrders()
        assert cancelAllOrdersResult is not None, 'Problem in getting list of open orders without symbol.'

        cancelSingleSymbolOrdersResult = gate.getAllFuturesOpenOrders('BTCUSDT')
        assert cancelSingleSymbolOrdersResult is not None, 'Problem in getting list of open orders with symbol.'

def testGetFutureOrder(getGates):
    for gate in getGates:
        futuresOrderData = gate.createAndTestFuturesOrder('BTCUSDT', 'BUY', 'MARKET', quantity=0.002)
        result = gate.makeFuturesOrder(futuresOrderData)
        order = gate.getFuturesOrder('BTCUSDT', orderId=result.orderId)

        assert order.clientOrderId == result.clientOrderId, 'Futures fetch client orderID is not equal to the actual client orderID'

        order = gate.getFuturesOrder('BTCUSDT', localOrderId=result.clientOrderId)
        assert order.orderId == result.orderId, 'Futures fetch orderID is not equal to the actual orderID'

def testCancelingAllFuturesOpenOrders(getGates):
    for gate in getGates:
        futuresOrderData = gate.createAndTestFuturesOrder('BTCUSDT', 'BUY', 'TAKE_PROFIT_MARKET', stopPrice=35000, quantity=0.002)
        gate.makeFuturesOrder(futuresOrderData)

        gate.cancellAllSymbolFuturesOrders('BTCUSDT', 1)

        openOrders = gate.getAllFuturesOpenOrders('BTCUSDT')
        assert len(openOrders) == 0, 'Problem in canceling all Open Orders'

def testCancelingOrder(getGates):
    for gate in getGates:
        futuresOrderData = gate.createAndTestFuturesOrder('BTCUSDT', 'BUY', 'TAKE_PROFIT_MARKET', stopPrice=35000, quantity=0.002)
        result = gate.makeFuturesOrder(futuresOrderData)

        result = gate.cancelFuturesOrder(symbol='BTCUSDT', localOrderId=result.clientOrderId)
        assert result.status == 'CANCELED', 'Problem in canceling specified Open Orders'
