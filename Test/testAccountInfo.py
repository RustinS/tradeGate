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

def testFullBalance(getGates):
    for gate in getGates:
        balance = gate.getBalance()
        # print('\nFull Balance from {} exchange: {}'.format(gate.exchangeName, balance))
        assert balance is not None, 'Problem in fetching balance from {} exchange.'.format(gate.exchangeName)

        try:
            for asset in balance:
                if not sorted(list(asset.keys())) == sorted(['asset', 'free', 'locked']):
                    assert False, 'Bad fetch balance interface for {} exchange,'.format(gate.exchangeName)
        except:
            assert False, 'Bad fetch balance interface for {} exchange,'.format(gate.exchangeName)

def testSingleCoinBalance(getGates):
    for gate in getGates:
        balance = gate.getBalance('BTC')
        # print('\nSingle coin balance from {} exchange: {}'.format(gate.exchangeName, balance))
        assert balance is not None, 'Problem in fetching single coin balance from {} exchange.'.fomrat(gate.exchangeName)

        try:
            if not sorted(list(balance.keys())) == sorted(['asset', 'free', 'locked']):
                assert False, 'Bad fetch balance interface for {} exchange,'.format(gate.exchangeName)
        except:
            assert False, 'Bad fetch single coin balance interface for {} exchange,'.format(gate.exchangeName)

def testTradeHistory(getGates):
    for gate in getGates:
        tradeHisytory = gate.getSymbolTradeHistory('BTCUSDT')
        # print('\nTrade history from {} exchange: {}'.format(gate.exchangeName, tradeHisytory))
        assert tradeHisytory is not None, 'Problem in fetching trade history from {} exchange.'.format(gate.exchangeName)
