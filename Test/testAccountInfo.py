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
            if not gate.exchangeName == 'Binance':
                if not sorted(list(balance[0].keys())) == sorted(['asset', 'free', 'locked', 'exchangeSpecific']):
                    assert False, 'Bad fetch balance interface for {} exchange,'.format(gate.exchangeName)
            else:
                if not sorted(list(balance[0].keys())) == sorted(['asset', 'free', 'locked']):
                    assert False, 'Bad fetch balance interface for {} exchange,'.format(gate.exchangeName)
        except:
            assert False, 'Bad fetch single coin balance interface for {} exchange,'.format(gate.exchangeName)


def testSingleCoinBalance(getGates):
    for gate in getGates:
        balance = gate.getBalance('BTC')
        # print('\nSingle coin balance from {} exchange: {}'.format(gate.exchangeName, balance))
        assert balance is not None, 'Problem in fetching single coin balance from {} exchange.'.fomrat(gate.exchangeName)
        
        try:
            if not gate.exchangeName == 'Binance':
                if not sorted(list(balance.keys())) == sorted(['asset', 'free', 'locked', 'exchangeSpecific']):
                    assert False, 'Bad fetch balance interface for {} exchange,'.format(gate.exchangeName)
            else:
                if not sorted(list(balance.keys())) == sorted(['asset', 'free', 'locked']):
                    assert False, 'Bad fetch balance interface for {} exchange,'.format(gate.exchangeName)
        except:
            assert False, 'Bad fetch single coin balance interface for {} exchange,'.format(gate.exchangeName)
        

def testTradeHistory(getGates):
    for gate in getGates:
        tradeHistory = gate.symbolAccountTradeHistory('BTCUSDT')
        # print('\nTrade history from {} exchange: {}'.format(gate.exchangeName, tradeHisytory[0]))

        assert tradeHistory is not None, 'Problem in fetching trade history from {} exchange.'.format(gate.exchangeName)

        interface = ['symbol', 'id', 'orderId', 'orderListId', 'price', 'qty', 'quoteQty', 'commission', 'commissionAsset', 'time',
                        'isBuyer', 'isMaker', 'isBestMatch']

        try:
            if not gate.exchangeName == 'Binance':
                interface.append('exchangeSpecific')
                if not sorted(list(tradeHistory[0].keys())) == sorted(interface):
                    assert False, 'Bad fetch trade history interface for {} exchange,'.format(gate.exchangeName)
            else:
                if not sorted(list(tradeHistory[0].keys())) == sorted(interface):
                    assert False, 'Bad fetch trade history interface for {} exchange,'.format(gate.exchangeName)
        except:
            assert False, 'Bad fetch single coin balance interface for {} exchange,'.format(gate.exchangeName)

