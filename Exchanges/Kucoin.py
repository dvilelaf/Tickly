# -*- coding: utf-8 -*-
import requests
import datetime

class Kucoin:
    
    name = 'Kucoin'
    
    api = 'https://api.kucoin.com/v1/open/'

    wait_time = 1

    valid_pairs = {'USD': ['BCH', 'BTC', 'DRGN', 'EOS', 'ETH', 'KCS', 'LTC', 'NEO', 'XRB'], 

                    'NEO': ['DBC', 'DRGN', 'EOS', 'GAS', 'LTC', 'PRL', 'QLC', 'RPX', 'TKY', 
                            'TNC', 'ZPT'], 
                            
                    'ETH': ['ACAT', 'ACT', 'ADB', 'AGI', 'AION', 'AIX', 'AMB', 'ARN', 'ARY', 
                            'AXP', 'BCD', 'BCH', 'BCPT', 'BNTY', 'BOS', 'BPT', 'BTG', 'BTM', 
                            'CAG', 'CAN', 'CAPP', 'CAT', 'CFD', 'CHSB', 'COFI', 'COV', 'CS', 
                            'CTR', 'CV', 'CVC', 'CXO', 'DADI', 'DASH', 'DAT', 'DBC', 'DEB', 
                            'DENT', 'DGB', 'DNA', 'DRGN', 'DTA', 'EBTC', 'ELEC', 'ELF', 'ELIX', 
                            'ENJ', 'EOS', 'ETC', 'ETN', 'EVX', 'EXY', 'FLIXX', 'FOTA', 'GAT', 
                            'GLA', 'GVT', 'HAT', 'HAV', 'HKN', 'HPB', 'HSR', 'HST', 'IHT', 
                            'ING', 'INS', 'IOST', 'ITC', 'J8T', 'JNT', 'KCS', 'KEY', 'KICK', 
                            'KNC', 'LA', 'LEND', 'LOCI', 'LOOM', 'LTC', 'LYM', 'MEE', 'MOD', 
                            'MTH', 'MTN', 'MWAT', 'NEBL', 'NEO', 'NULS', 'OCN', 'OMG', 'ONION', 
                            'PARETO', 'PAY', 'PBL', 'PLAY', 'POE', 'POLL', 'POLY', 'POWR', 'PPT', 
                            'PRL', 'PURA', 'QLC', 'QSP', 'R', 'RDN', 'REQ', 'RHOC', 'RPX', 'SAY', 
                            'SNC', 'SNM', 'SNOV', 'SNT', 'SPF', 'SPHTX', 'STK', 'STX', 'SUB', 
                            'TEL', 'TFL', 'TIME', 'TIO', 'TKY', 'TNC', 'TRAC', 'UKG', 'UTK', 
                            'VEN', 'WAX', 'XAS', 'XLR', 'XRB', 'ZIL', 'ZPT'], 
                            
                    'KCS': ['BCH', 'ETC', 'GAS', 'NEO', 'RPX'], 
                    
                    'BTC': ['ACAT', 'ACT', 'ADB', 'AGI', 'AION', 'AIX', 'AMB', 'ARN', 'ARY', 
                            'AXP', 'BCD', 'BCH', 'BCPT', 'BHC', 'BNTY', 'BOS', 'BPT', 'BTG', 'BTM', 
                            'CAG', 'CAN', 'CAPP', 'CAT', 'CHSB', 'COFI', 'COV', 'CS', 'CTR', 'CV', 
                            'CVC', 'CXO', 'DADI', 'DASH', 'DAT', 'DBC', 'DEB', 'DENT', 'DGB', 'DNA', 
                            'DRGN', 'DTA', 'EBTC', 'ELEC', 'ELF', 'ELIX', 'ENJ', 'EOS', 'ETC', 'ETH', 
                            'ETN', 'EVX', 'EXY', 'FLIXX', 'FOTA', 'GAS', 'GAT', 'GLA', 'GVT', 'HAT', 
                            'HAV', 'HKN', 'HPB', 'HSR', 'HST', 'IHT', 'ING', 'INS', 'IOST', 'ITC', 
                            'J8T', 'JNT', 'KCS', 'KEY', 'KICK', 'KNC', 'LA', 'LEND', 'LOCI', 'LOOM', 
                            'LTC', 'LYM', 'MEE', 'MOD', 'MTH', 'MTN', 'MWAT', 'NEBL', 'NEO', 'NULS', 
                            'OCN', 'OMG', 'ONION', 'PARETO', 'PAY', 'PBL', 'PLAY', 'POE', 'POLL', 
                            'POLY', 'POWR', 'PPT', 'PRL', 'PURA', 'QLC', 'QSP', 'QTUM', 'R', 'RDN', 
                            'REQ', 'RHOC', 'RPX', 'SAY', 'SNC', 'SNM', 'SNOV', 'SNT', 'SPF', 'SPHTX', 
                            'STK', 'STX', 'SUB', 'TEL', 'TFL', 'TIME', 'TIO', 'TKY', 'TNC', 'TRAC', 
                            'UKG', 'UTK', 'VEN', 'WAX', 'WTC', 'XAS', 'XLR', 'XRB', 'ZIL', 'ZPT']
                    }

    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def getData(self, base, quote):
        
        if base == 'USD':
            base = 'USDT'

        if quote == 'USD':
            quote = 'USDT'
            
        currencyPair = quote + '-' + base 

        data = requests.get(self.api + 'tick').json()

        if data['success'] != True:
            print(self.name + ' error: ' + data['code'])
            return {}

        data = data['data']
        
        for i in data:
    
            if i['symbol'] == currencyPair:
                data = i
                break

        out = {}

        out['base'] = 'USD' if base == 'USDT' else base
        out['quote'] = 'USD' if quote == 'USDT' else quote
        out['price' ] = 1.0 / float(data['lastDealPrice'])
        out['low24h' ] = 1.0 / float(data['high'])
        out['high24h'] = 1.0 / float(data['low'])
        out['change24h'] = float(data['changeRate'])
        out['volume24hbase'] = -1
        out['volume24hquote'] = float(data['volValue'])

        return out