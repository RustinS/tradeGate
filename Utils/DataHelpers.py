import time


class OrderData():
    def __init__(self, symbol, side, orderType):
        self.symbol = symbol
        self.side = side
        self.orderType = orderType

        self.timeInForce = None
        self.quantity = None
        self.quoteOrderQty = None
        self.price = None
        self.newClientOrderId = None
        self.stopPrice = None
        self.icebergQty = None
        self.newOrderRespType = None
        self.recvWindow = None
        self.timestamp = None

    def setTimeInForce(self, timeInForce):
        self.timeInForce = timeInForce

    def setQuantity(self, quantity):
        self.quantity = quantity

    def setQuoteOrderQty(self, quoteOrderQty):
        self.quoteOrderQty = quoteOrderQty
    
    def setPrice(self, price):
        self.price = price
    
    def setNewClientOrderId(self, newClientOrderId):
        self.newClientOrderId = newClientOrderId

    def setStopPrice(self, stopPrice):
        self.stopPrice = stopPrice

    def setIcebergQty(self, icebergQty):
        self.icebergQty = icebergQty
    
    def setNewOrderRespType(self, newOrderRespType):
        self.newOrderRespType = newOrderRespType

    def setRecvWindow(self, recvWindow):
        self.recvWindow = recvWindow
    
    def setTimestamp(self):
        self.timestamp = time.time()
        
