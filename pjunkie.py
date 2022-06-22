import requests
import math
from time import sleep

def getCurrentPrice():
    req = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    out = req.json()
    price = out['bpi']['USD']['rate_float']
    return price

class PriceJunkie(object):
    direction = 0
    avg = 0.0
    interval = 60
    nextPrice = 0.0
    nextFigure = 0.0
    avgNext = 0.0
    hourOut = 0.0
    high = 0
    low = 0
    lastPrice = 0.0
    currentPrice = 0.0
    total = 0.0
    priceHistory = []
    def guessNextPrice(self):
        diff = self.currentPrice - self.lastPrice
        if diff < 0:
            diff *= -1
        diff = math.sqrt(diff)
        p = math.sqrt(math.sqrt(diff) * math.sqrt(self.avg))
        if self.direction != 0:
            p *= self.direction
        return p * -1

    def guessHourPrice(self):
        m = self.direction
        if m < 0:
            m *= -1
        if m == 0:
            m == 1
        p = (self.avg - self.guessNextPrice() + (self.avgNext * m))
        return p

    def run(self):
        c = 1
        while True:
            self.lastPrice = self.currentPrice
            self.currentPrice = getCurrentPrice()
            #self.priceHistory.append(self.currentPrice)
            self.total += self.currentPrice
            self.avg = self.total / c
            diff = self.currentPrice - (self.lastPrice)
            if diff < 0:
                diff *= -1
            if self.currentPrice > self.lastPrice:
                self.direction += 1
            else:
                self.direction -= 1
            if self.direction > self.high:
                self.peak = self.direction
            if self.direction < self.low:
                self.low = self.direction
            self.nextFigure = self.guessNextPrice()
            self.avgNext += self.nextFigure / c
            self.nextPrice = self.currentPrice - self.nextFigure
            self.hourOut = self.guessHourPrice()
            c += 1
            print("price: ", self.currentPrice, "lastPrice: ", self.lastPrice, "avg: ", self.avg, "nextPrice: ", self.nextPrice, "direction: ", self.direction, "diff: ", diff, "nextFigure: ", self.nextFigure, "hourOut: ", self.hourOut)
            sleep(self.interval)

pjunkie = PriceJunkie()
pjunkie.run()
