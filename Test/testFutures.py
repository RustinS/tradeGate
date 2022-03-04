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
        assert symbolFutureOrders is not None, 'Problem in futures order list from {} exchange.'.format(gate.exchangeName)

def testFuturesBalance(getGates):
    for gate in getGates:
        balance = gate.getBalance(futures=True)
        # print('\nFutures balance from {} exchange: {}'.format(gate.exchangeName, balance))
        assert balance is not None, 'Problem in futures balance from {} exchange.'.format(gate.exchangeName)

def testFuturesSingleCoinBalance(getGates):
    for gate in getGates:
        balance = gate.getBalance('BTC', futures=True)
        # print('\nBTC Futures balance from {} exchange: {}'.format(gate.exchangeName, balance))
        assert balance is not None, 'Problem in fetching futures single coin balance from {} exchange.'.format(gate.exchangeName)

def testFuturesOrder(getGates):
    for gate in getGates:
        futuresOrderData = gate.createAndTestFuturesOrder('BTCUSDT', 'BUY', 'MARKET', quantity=0.002)
        result = gate.makeFuturesOrder(futuresOrderData)
        # print('\nFuture ordering in [] exchange: {}'.format(gate.exchangeName, result))
        assert result is not None, 'Problem in submiting futures order in {} exchange.'.format(gate.exchangeName)

def testCancelingAllFuturesOpenOrders(getGates):
    for gate in getGates:
        result = gate.cancelAllSymbolFuturesOpenOrders('BTCUSDT')

        print('\nFuture order canceling in [] exchange: {}'.format(gate.exchangeName, result))
        assert result is not None, 'Problem in canceling all futures orders in {} exchange.'.format(gate.exchangeName)

def testGetFuturesOpenOrders(getGates):
    for gate in getGates:
        openOrders = gate.getOpenOrders(futures=True)
        assert openOrders is not None, 'Problem in getting list of open orders without symbol from {} exchanghe.'.format(gate.exchangeName)

        symbolOpenOrders = gate.getOpenOrders('BTCUSDT', futures=True)
        assert symbolOpenOrders is not None, 'Problem in getting list of open orders with symbol from {} exchange.'.format(gate.exchangeName)

def testGetFutureOrder(getGates):
    for gate in getGates:
        futuresOrderData = gate.createAndTestFuturesOrder('BTCUSDT', 'BUY', 'MARKET', quantity=0.002)
        result = gate.makeFuturesOrder(futuresOrderData)
        order = gate.getOrder('BTCUSDT', orderId=result['orderId'], futures=True)

        assert order['clientOrderId'] == result['clientOrderId'], 'Futures fetch client orderID is not equal to the actual client orderID from {} exchange.'.format(gate.exchangeName)

        order = gate.getOrder('BTCUSDT', localOrderId=result['clientOrderId'], futures=True)
        assert order['orderId'] == result['orderId'], 'Futures fetch orderID is not equal to the actual orderID from {} exchange.'.format(gate.exchangeName)

def testCancelingAllFuturesOpenOrders(getGates):
    for gate in getGates:
        futuresOrderData = gate.createAndTestFuturesOrder('BTCUSDT', 'BUY', 'TAKE_PROFIT_MARKET', stopPrice=35000, quantity=0.002)
        gate.makeFuturesOrder(futuresOrderData)

        gate.cancelAllSymbolOpenOrders('BTCUSDT', futures=True)

        openOrders = gate.getOpenOrders('BTCUSDT', futures=True)
        assert len(openOrders) == 0, 'Problem in canceling all Open Orders in {} exchange.'.format(gate.exchangeName)

def testCancelingOrder(getGates):
    for gate in getGates:
        futuresOrderData = gate.createAndTestFuturesOrder('BTCUSDT', 'BUY', 'TAKE_PROFIT_MARKET', stopPrice=35000, quantity=0.002)
        result = gate.makeFuturesOrder(futuresOrderData)

        result = gate.cancelOrder(symbol='BTCUSDT', localOrderId=result['clientOrderId'], futures=True)
        assert result['status'] == 'CANCELED', 'Problem in canceling specified Open Orders from {} exchnage.'.format(gate.exchangeName)
