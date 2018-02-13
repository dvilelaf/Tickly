# -*- coding: utf-8 -*-
import requests
import datetime


class Kraken:
    
    name = 'Kraken'
    
    api = 'https://api.kraken.com/'

    wait_time = 1

    valid_pairs = {'BCH' : ['EUR', 'USD', 'XBT'],
                   'DASH' : ['EUR', 'USD', 'XBT'],
                   'EOS' : ['ETH', 'XBT'],
                   'GNO' : ['ETH', 'XBT'],
                   'USDT' : ['USD',],
                   'ETC' : ['ETH', 'XBT', 'EUR', 'USD'],
                   'ETH' : ['XBT', 'XBT', 'CAD', 'CAD', 'EUR', 'EUR', 'GBP', 'GBP', 'JPY', 'JPY', 'USD', 'USD'],
                   'ICN' : ['ETH', 'XBT'],
                   'LTC' : ['XBT', 'EUR', 'USD'],
                   'MLN' : ['ETH', 'XBT'],
                   'REP' : ['ETH', 'XBT', 'EUR'],
                   'XBT' : ['CAD', 'CAD', 'EUR', 'EUR', 'GBP', 'GBP', 'JPY', 'JPY', 'USD', 'USD'], 
                   'XDG' : ['XBT',],
                   'XLM' : ['XBT',],
                   'XMR' : ['XBT', 'EUR', 'USD'],
                   'XRP' : ['XBT', 'EUR', 'USD'],
                   'ZEC' : ['XBT', 'EUR', 'USD'],
                    }


    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def getData(self, base, quote):
            
        currencyPair = base + quote

        data = requests.get(self.api + '0/public/Ticker?pair=' + currencyPair).json()

        if data['error']:
            print(self.name + ' error: ' + data['error'])
            return {}

        data = data['result']

        pairName = list(data.keys())[0]

        data = data[pairName]

        out = {}

        out['base'] = base
        out['quote'] = quote
        out['price' ] = float(data['c'][0])
        out['low24h' ] = float(data['l'][1])
        out['high24h'] = float(data['h'][1])
        out['change24h'] = -1
        out['volume24hbase'] = -1
        out['volume24hquote'] = float(data['v'][1])

        return out