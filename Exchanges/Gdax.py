# -*- coding: utf-8 -*-
import requests
import datetime


class Gdax:
    
    name = 'Gdax'
    
    api = 'https://api.gdax.com/'

    wait_time = 1

    valid_pairs = {'BTC' : ['USD', 'EUR', 'GBP'], 
                   'BCH' : ['USD', 'EUR', 'BTC'], 
                   'ETH' : ['USD', 'EUR', 'BTC'], 
                   'LTC' : ['USD', 'EUR', 'BTC']
                   }
    
    responses = {
        200 : 'Success',
        400 : 'Bad Request – Invalid request format',
        401 : 'Unauthorized – Invalid API Key',
        403 : 'Forbidden – You do not have access to the requested resource',
        404 : 'Not Found',
        429 : 'Too many requests',
        500 : 'Internal Server Error – We had a problem with our server'
    }

    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)
        

    def getData(self, base, quote):
        
        currencyPair = base + '-' + quote      

        # Price

        data = requests.get(self.api + 'products/' + currencyPair + '/stats')

        if data.status_code != 200:
            print(self.name + ' error: ' + self.responses[data.status_code])
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