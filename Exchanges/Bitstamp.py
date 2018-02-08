# -*- coding: utf-8 -*-
import requests
import datetime


class Bitstamp:
    
    name = 'Bitstamp'
    
    api = 'https://www.bitstamp.net/api/v2/'

    wait_time = 1

    valid_pairs = {'BTC' : ['USD', 'EUR'],
                   'EUR' : ['USD',],
                   'XRP' : ['USD','EUR','BTC'],
                   'LTC' : ['USD','EUR','BTC'],
                   'ETH' : ['USD','EUR','BTC'],
                   'BCH' : ['USD','EUR','BTC']
                    }


    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def getData(self, base, quote):
            
        currencyPair = base.lower() + quote.lower()

        data = requests.get(self.api + 'ticker/' + currencyPair)

        if data.status_code != 200:
            print(self.name + ' connection error')
            return {}

        data = data.json()

        out = {}

        out['base'] = base
        out['quote'] = quote
        out['price' ] = float(data.pop('last'))
        out['low24h' ] = float(data.pop('low'))
        out['high24h'] = float(data.pop('high'))
        out['change24h'] = -1
        out['volume24hbase'] = -1
        out['volume24hquote'] = float(data.pop('volume'))

        return out