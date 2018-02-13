# -*- coding: utf-8 -*-
import requests
import datetime


class Gemini:
    
    name = 'Gemini'
    
    api = ' https://api.gemini.com/v1/'

    wait_time = 1

    valid_pairs = {'BTC' : ['USD',],
                   'ETH' : ['USD', 'BTC',],
                   }


    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def getData(self, base, quote):
            
        currencyPair = base + quote

        data = requests.get(self.api + 'pubticker/' + currencyPair).json()

        if 'result' in data and data['result'] == 'error':
            print(self.name + ' error: ' + data['reason'])
            return {}

        data = data['data']

        out = {}

        out['base'] = base
        out['quote'] = quote
        out['price' ] = float(data['last'])
        out['low24h' ] = -1
        out['high24h'] = -1
        out['change24h'] = -1
        out['volume24hbase'] = float(data['volume'][base])
        out['volume24hquote'] = float(data['volume'][quote])

        return out