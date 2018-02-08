# -*- coding: utf-8 -*-
import requests
import datetime


class Coinbase:
    
    name = 'Coinbase'

    api = 'https://api.coinbase.com/v2/'

    wait_time = 1

    valid_pairs = {'BTC' : ['USD', 'EUR', 'GBP'], 
                   'BCH' : ['USD', 'EUR', 'GBP'], 
                   'ETH' : ['USD', 'EUR', 'GBP'], 
                   'LTC' : ['USD', 'EUR', 'GBP']
                   }

    responses = {
        200 : 'OK: successful request',
        201 : 'Created: new object saved',
        204 : 'No content: object deleted',
        400 : 'Bad Request: read JSON error message',
        401 : 'Unauthorized: couldn’t authenticate your request',
        402 : '2FA Token required: re-try request with user’s 2FA token as CB-2FA-Token header',
        403 : 'Invalid scope: user hasn’t authorized necessary scope',
        404 : 'Not Found: no such object',
        429 : 'Too Many Requests: your connection is being rate limited',
        500 : 'Internal Server Error: something went wrong',
        503 : 'Service Unavailable: your connection is being throttled \
               or the service is down for maintenance'
    }

    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def getData(self, base, quote):
        
        currencyPair = base + '-' + quote

        data = requests.get(self.api + 'prices/' + currencyPair + '/spot')

        if data.status_code != 200:
            print(self.name + ' error: ' + self.responses[data.status_code])
            return {}

        data = data.json()['data']

        out = {}

        out['base'] = base
        out['quote'] = quote
        out['price' ] = float(data.pop('amount'))
        out['low24h' ] = -1
        out['high24h'] = -1
        out['change24h'] = -1
        out['volume24hbase'] = -1
        out['volume24hquote'] = -1

        return out