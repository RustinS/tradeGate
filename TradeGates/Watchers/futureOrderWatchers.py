import time


def watchFuturesLimitTrigger(gate, symbol, orderId, doPutTpSl, cancelIfNotOpened, **params):
    if doPutTpSl:
        if 'tpSlOrderSide' not in params.keys() or 'stopLoss' not in params.keys() or 'takeProfit' not in params.keys():
            raise ValueError('Must specify \'tpSlOrderSide\' and \'stopLoss\' and \'takeProfit\'')

    if cancelIfNotOpened:
        if 'timeFrame' not in params.keys() or 'delayNum' not in params.keys():
            raise ValueError('Must specify \'timeFrame\' and \'delayNum\'')

    done = False
    while not done:
        time.sleep(0.1)
        order = gate.getOrder(symbol=symbol, orderId=orderId, futures=True)
        if order['status'] == 'NEW':
            continue
        elif order['status'] == 'FILLED':
            if doPutTpSl:
                orderSide = params.get('tpSlOrderSide')
                stopLoss = params.get('stopLoss')
                takeProfit = params.get('takeProfit')

                stopLossOrder = gate.createAndTestFuturesOrder(symbol, orderSide, 'STOP_MARKET',
                                                               stopPrice=stopLoss, closePosition=True,
                                                               priceProtect=True, workingType='MARK_PRICE',
                                                               timeInForce='GTC')

                takeProfitOrder = gate.createAndTestFuturesOrder(symbol, orderSide, 'TAKE_PROFIT_MARKET',
                                                                 closePosition=True, stopPrice=takeProfit,
                                                                 priceProtect=True, workingType='MARK_PRICE',
                                                                 timeInForce='GTC')
                result = gate.makeBatchFuturesOrder([stopLossOrder, takeProfitOrder])
                print(result)
                break
        elif order['status'] == 'CANCELED':
            break
