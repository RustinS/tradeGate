def getBalanceOut(data, single=False, futures=False):
    if not single:
        outData = []
        if not futures:
            for asset in data:
                coinData = {}
                coinData['asset'] = asset['coin']
                coinData['free'] = asset['free']
                coinData['locked'] = asset['locked']
                coinData['exchangeSpecific'] = asset
                outData.append(coinData)
            return outData
        else:
            for key, value in data.items():
                coinData = {}
                coinData['asset'] = key
                coinData['free'] = value['available_balance']
                coinData['locked'] = value['used_margin']
                coinData['exchangeSpecific'] = value
                outData.append(coinData)
            return outData
    else:
        if not futures:
            outData = {}
            outData['asset'] = data['coin']
            outData['free'] = data['free']
            outData['locked'] = data['locked']
            outData['exchangeSpecific'] = data
            return outData
        else:
            outData = {}
            key = list(data.keys())[0]

            outData['asset'] = key
            outData['free'] = data[key]['available_balance']
            outData['locked'] = data[key]['used_margin']
            outData['exchangeSpecific'] = data[key]
            return outData


def getMyTradeHistory(data, futures=False):
    if futures:
        outData = []
        for history in data:
            outData.append({'symbol': history['symbol'], 'id': history['exec_id'], 'orderId': history['order_id'],
                            'orderListId': history['order_link_id'], 'price': history['price'],
                            'qty': history['order_qty'],
                            'quoteQty': str(float(history['price']) * float(history['order_qty'])),
                            'commission': None, 'commissionAsset': None, 'time': history['trade_time_ms'],
                            'isBuyer': None, 'isMaker': None, 'isBestMatch': None, 'exchangeSpecific': history})
    else:
        outData = []
        for history in data:
            outData.append({'symbol': history['symbol'], 'id': history['id'], 'orderId': history['orderId'],
                            'orderListId': -1, 'price': history['price'], 'qty': history['qty'],
                            'quoteQty': str(float(history['price']) * float(history['qty'])),
                            'commission': history['commission'], 'commissionAsset': history['commissionAsset'],
                            'time': history['time'], 'isBuyer': history['isBuyer'], 'isMaker': history['isMaker'],
                            'isBestMatch': None, 'exchangeSpecific': history})
    return outData
