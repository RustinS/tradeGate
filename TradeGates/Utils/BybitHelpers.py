

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
        pass
    else:
        outData = []
        for history in data:
            corrHist = {}

            corrHist['symbol'] = history['symbol']
            corrHist['id'] = history['id']
            corrHist['orderId'] = history['orderId']
            corrHist['orderListId'] = -1
            corrHist['price'] = history['price']
            corrHist['qty'] = history['qty']
            corrHist['quoteQty'] = str(float(history['price']) * float(history['qty']))
            corrHist['commission'] = history['commission']
            corrHist['commissionAsset'] = history['commissionAsset']
            corrHist['time'] = history['time']
            corrHist['isBuyer'] = history['isBuyer']
            corrHist['isMaker'] = history['isMaker']
            corrHist['isBestMatch'] = None
            corrHist['exchangeSpecific'] = history

            outData.append(corrHist)
        return outData
