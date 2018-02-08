# -*- coding: utf-8 -*-
import requests
import datetime


class Bitfinex:
    
    name = 'Bitfinex'
    
    api = 'https://api.bitfinex.com/v1/'

    wait_time = 1

    valid_pairs = {'ETH' : ['BTC', 'USD'],
                   'ZEC' : ['BTC', 'USD'],
                   'ETC' : ['BTC', 'USD'],
                   'OMG' : ['BTC', 'ETH', 'USD'],
                   'QTM' : ['BTC', 'ETH', 'USD'],
                   'SPK' : ['BTC', 'ETH', 'USD'],
                   'ETP' : ['BTC', 'ETH', 'USD'],
                   'SNT' : ['BTC', 'ETH', 'USD'],
                   'MNA' : ['BTC', 'ETH', 'USD'],
                   'BTC' : ['EUR', 'USD'],
                   'RRT' : ['BTC', 'USD'],
                   'EOS' : ['BTC', 'ETH', 'USD'],
                   'GNT' : ['BTC', 'ETH', 'USD'],
                   'TNB' : ['BTC', 'ETH', 'USD'],
                   'ZRX' : ['BTC', 'ETH', 'USD'],
                   'YYW' : ['BTC', 'ETH', 'USD'],
                   'IOT' : ['BTC', 'ETH', 'EUR', 'USD'],
                   'EDO' : ['BTC', 'ETH', 'USD'],
                   'QSH' : ['BTC', 'ETH', 'USD'],
                   'XMR' : ['BTC', 'USD'],
                   'AVT' : ['BTC', 'ETH', 'USD'],
                   'BAT' : ['BTC', 'ETH', 'USD'],
                   'DSH' : ['BTC', 'USD'],
                   'BCH' : ['BTC', 'ETH', 'USD'],
                   'DAT' : ['BTC', 'ETH', 'USD'],
                   'SAN' : ['BTC', 'ETH', 'USD'],
                   'XRP' : ['BTC', 'USD'],
                   'FUN' : ['BTC', 'ETH', 'USD'],
                   'BTG' : ['BTC', 'USD'],
                   'NEO' : ['BTC', 'ETH', 'USD'],
                   'LTC' : ['BTC', 'USD'],
                    }


    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def getData(self, base, quote):
            
        currencyPair = base.lower() + quote.lower()

        data = requests.get(self.api + 'pubticker/' + currencyPair).json()

        if 'message' in data:
            print(self.name + ' error: ' + data['message'])
            return {}

        if 'error' in data:
            print(self.name + ' error: ' + data['error'])
            return {}

        out = {}

        out['base'] = base
        out['quote'] = quote
        out['price' ] = float(data.pop('last_price'))
        out['low24h' ] = float(data.pop('low'))
        out['high24h'] = float(data.pop('high'))
        out['change24h'] = -1
        out['volume24hbase'] = -1
        out['volume24hquote'] = float(data.pop('volume'))

        return out