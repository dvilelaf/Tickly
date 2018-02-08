# -*- coding: utf-8 -*-
import requests
import datetime


class Poloniex:
    
    name = 'Poloniex'
    
    api = 'https://poloniex.com/'

    wait_time = 1

    valid_pairs = {'BTC'  : ['AMP', 'ARDR', 'BCH', 'BCN', 'BCY', 'BELA', 'BLK', 'BTCD', 'BTM',
                             'BTS', 'BURST', 'CLAM', 'CVC', 'DASH', 'DCR', 'DGB', 'DOGE', 'EMC2',
                             'ETC', 'ETH', 'EXP', 'FCT', 'FLDC', 'FLO', 'GAME', 'GAS', 'GNO',
                             'GNT', 'GRC', 'HUC', 'LBC', 'LSK', 'LTC', 'MAID', 'NAV', 'NEOS',
                             'NMC', 'NXC', 'NXT', 'OMG', 'OMNI', 'PASC', 'PINK', 'POT', 'PPC',
                             'RADS', 'REP', 'RIC', 'SBD', 'SC', 'STEEM', 'STORJ', 'STR', 'STRAT',
                             'SYS', 'VIA', 'VRC', 'VTC', 'XBC', 'XCP', 'XEM', 'XMR', 'XPM',
                             'XRP', 'XVC', 'ZEC', 'ZRX'], 

                   'ETH'  : ['BCH', 'CVC', 'ETC', 'GAS', 'GNO', 'GNT', 'LSK', 'OMG', 'REP',
                             'STEEM', 'ZEC', 'ZRX'],

                   'XMR'  : ['BCN', 'BLK', 'BTCD', 'DASH', 'LTC', 'MAID', 'NXT', 'ZEC'],

                   'USD' : ['BCH', 'BTC', 'DASH', 'ETC', 'ETH', 'LTC', 'NXT', 'REP', 'STR',
                             'XMR', 'XRP', 'ZEC']
                    }

    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)
    

    def getData(self, base, quote):
        
        if base == 'USD':
            base = 'USDT'

        if quote == 'USD':
            quote = 'USDT'
            
        currencyPair = base + '_' + quote      

        data = requests.get(self.api + 'public?command=returnTicker').json()

        if 'error' in data:
            print(self.name + ' error: ' + data['error'])
            return {}

        data = data[currencyPair]

        out = {}

        out['base'] = 'USD' if base == 'USDT' else base
        out['quote'] = 'USD' if quote == 'USDT' else quote
        out['price' ] = 1.0 / float(data.pop('last'))
        out['low24h' ] = -1
        out['high24h'] = -1
        out['change24h'] = float(data.pop('percentChange'))
        out['volume24hbase'] = float(data.pop('baseVolume'))
        out['volume24hquote'] = float(data.pop('quoteVolume'))

        return out