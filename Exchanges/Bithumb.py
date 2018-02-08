# -*- coding: utf-8 -*-
import requests
import datetime


class Bithumb:
    
    name = 'Bithumb'
    
    api = 'https://api.coinone.co.kr/'

    wait_time = 1

    valid_pairs = {'BTC' : ['BCH', 'ETH', 'ETC', 'XRP', 'QTUM', 'IOTA', 'LTC', 'BTG'],}


    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def getData(self, base, quote):
            
        currencyPair = quote.lower()

        data = requests.get(self.api + 'ticker/?currency=' + currencyPair).json()

        if data['result'] == 'error':
            print(self.name + ' error: ' + data['errorMsg'])
            return {}

        out = {}

        out['base'] = base
        out['quote'] = quote
        out['price' ] = float(data.pop('last')) # Not instant price
        out['low24h' ] = float(data.pop('low'))
        out['high24h'] = float(data.pop('high'))
        out['change24h'] = -1
        out['volume24hbase'] = -1
        out['volume24hquote'] = float(data.pop('volume'))

        return out