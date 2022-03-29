def unifyGetBalanceSpotOut(data, isSingle=False):
    allAssets = []

    for asset in data:
        assetIndex = getAssetIndexInList(asset['currency'], allAssets)
        if assetIndex == -1:
            assetInfo = newEmptyAsset(asset['currency'])
        else:
            assetInfo = allAssets[assetIndex]

        assetInfo['free'] += float(asset['available'])
        assetInfo['locked'] += float(asset['holds'])
        assetInfo['exchangeSpecific'].append(asset)

        if assetIndex == -1:
            allAssets.append(assetInfo)

    if isSingle:
        return allAssets[0]
    else:
        return allAssets


def newEmptyAsset(assetName):
    return {
        'asset': assetName,
        'free': 0.0,
        'locked': 0.0,
        'exchangeSpecific': []
    }


def getAssetIndexInList(assetName, allAssets):
    for i in range(len(allAssets)):
        if assetName == allAssets[i]['asset']:
            return i
    return -1
