# -*- coding: utf-8 -*-
import requests
import datetime


class Coinone:
    
    name = 'Coinone'
    
    api = 'https://api.bithumb.com/public/'

    wait_time = 1

    valid_pairs = {'BTC' : ['ETH', 'DASH', 'LTC', 'ETC', 'XRP', 'BCH', 
                            'XMR', 'ZEC', 'QTUM', 'BTG', 'EOS'],
                   }


    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def getData(self, base, quote):
            
        currencyPair = quote

        data = requests.get(self.api + 'ticker/' + currencyPair).json()

        if data['status'] != '0000:
            print(self.name + ' error: ' + data['message'])
            return {}

        data = data['data']

        out = {}

        out['base'] = base
        out['quote'] = quote
        out['price' ] = float(data.pop('average_price')) # Not instant price
        out['low24h' ] = float(data.pop('min_price'))
        out['high24h'] = float(data.pop('max_price'))
        out['change24h'] = -1
        out['volume24hbase'] = -1
        out['volume24hquote'] = float(data.pop('volume_1day'))

        return out