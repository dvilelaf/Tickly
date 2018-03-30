# -*- coding: utf-8 -*-
import requests
import datetime

class Binance:
    
    name = 'Binance'
    
    api = 'https://api.binance.com/api/v1/'

    wait_time = 1

    valid_pairs = {'BNB' : ['CND', 'NEO', 'XLM', 'VEN', 'LTC', 'ICX', 'ADX', 'IOTA', 'BCC',
                            'AMB', 'QSP', 'GTO', 'NEBL', 'APPC', 'NULS', 'YOYO', 'BTS', 'WABI',
                            'POWR', 'CMT', 'WTC', 'OST', 'TRIG', 'BCPT', 'AION', 'DLT', 'BAT', 
                            'LSK', 'BRD', 'RDN', 'RCN', 'RLC', 'MCO', 'XZC', 'NAV', 'WAVES'], 

                   'BTC' : ['TRX', 'CND', 'ETH', 'XRP', 'NEO', 'BNB', 'VEN', 'VIBE', 'XVG',
                            'ELF', 'EOS', 'ICX', 'ADA', 'POE', 'TNB', 'WTC', 'LTC', 'XLM',
                            'BCD', 'CDT', 'HSR', 'FUN', 'ETC', 'BCC', 'IOTA', 'BTG', 'INS',
                            'APPC', 'QTUM', 'NEBL', 'GTO', 'BRD', 'OMG', 'LEND', 'ZRX', 'BTS',
                            'XMR', 'KNC', 'AION', 'QSP', 'WABI', 'EVX', 'AMB', 'REQ', 'CTR',
                            'LRC', 'ARN', 'ENG', 'MANA', 'GAS', 'ZEC', 'NULS', 'STRAT', 'SALT',
                            'LINK', 'SUB', 'OST', 'MTL', 'TRIG', 'POWR', 'STORJ', 'MCO', 'BQX',
                            'LSK', 'ENJ', 'WINGS', 'DASH', 'MTH', 'FUEL', 'CMT', 'SNT', 'BAT',
                            'EDO', 'DLT', 'YOYO', 'TNT', 'AST', 'GXS', 'SNM', 'MOD', 'ADX',
                            'WAVES', 'GVT', 'RCN', 'ARK', 'RDN', 'RLC', 'BCPT', 'LUN', 'DNT',
                            'VIB', 'SNGLS', 'KMD', 'NAV', 'MDA', 'XZC', 'PPT', 'OAX', 'BNT',
                            'DGD', 'ICN'], 

                   'ETH' : ['TRX', 'CND', 'XRP', 'EOS', 'NEO', 'VEN', 'ADA', 'ICX', 'BNB',
                            'XVG', 'POE', 'XLM', 'VIBE', 'ELF', 'TNB', 'FUN', 'LTC', 'IOTA',
                            'CDT', 'BCD', 'REQ', 'ZRX', 'ETC', 'APPC', 'LEND', 'AION', 'BCC',
                            'QTUM', 'OMG', 'INS', 'KNC', 'LRC', 'NEBL', 'QSP', 'XMR', 'HSR',
                            'ENG', 'WTC', 'BTG', 'GTO', 'OST', 'NULS', 'SUB', 'LINK', 'WABI',
                            'BTS', 'AMB', 'POWR', 'CTR', 'EVX', 'ENJ', 'BAT', 'SALT', 'DASH',
                            'MANA', 'ARN', 'SNT', 'BQX', 'CMT', 'FUEL', 'RDN', 'ZEC', 'TRIG',
                            'STORJ', 'LSK', 'STRAT', 'AST', 'GXS', 'MTL', 'MCO', 'DLT', 'MTH',
                            'TNT', 'BRD', 'EDO', 'GVT', 'ADX', 'RLC', 'RCN', 'SNGLS', 'YOYO',
                            'SNM', 'BCPT', 'MOD', 'PPT', 'DNT', 'ARK', 'LUN', 'MDA', 'VIB',
                            'WAVES', 'KMD', 'OAX', 'DGD', 'BNT', 'NAV', 'ICN', 'XZC', 'WINGS'], 

                   'USD' : ['BTC', 'ETH', 'NEO', 'BNB', 'LTC', 'BCC']
                  }


    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def getData(self, base, quote):
        
        if base == 'USD':
            base = 'USDT'

        if quote == 'USD':
            quote = 'USDT'
            
        currencyPair = quote + base 

        data = requests.get(self.api + 'ticker/24hr?symbol=' + currencyPair).json()

        if 'code' in data:
            print(self.name + ' error: ' + data['code'])
            return {}

        out = {}

        out['base'] = 'USD' if base == 'USDT' else base
        out['quote'] = 'USD' if quote == 'USDT' else quote
        out['price' ] = 1.0 / float(data['lastPrice'])
        out['low24h' ] = 1.0 / float(data['highPrice'])
        out['high24h'] = 1.0 / float(data['lowPrice'])
        out['change24h'] = -1.0 * float(data['priceChangePercent'])
        out['volume24hbase'] = float(data['volume'])
        out['volume24hquote'] = float(data['quoteVolume'])

        return out