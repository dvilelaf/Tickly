# -*- coding: utf-8 -*-
import requests
import datetime


class Bittrex:
    
    name = 'Bittrex'
    
    api = 'https://bittrex.com/api/v1.1/public/'

    wait_time = 1

    valid_pairs = { 'BTC' : ['1ST', '2GIVE', 'ABY', 'ADA', 'ADT', 'ADX', 'AEON', 'AGRS', 
                             'AMP', 'ANT', 'APX', 'ARDR', 'ARK', 'AUR', 'BAT', 'BAY', 
                             'BCC', 'BCY', 'BITB', 'BLITZ', 'BLK', 'BLOCK', 'BNT', 'BRK', 
                             'BRX', 'BSD', 'BTCD', 'BTG', 'BURST', 'BYC', 'CANN', 'CFI', 
                             'CLAM', 'CLOAK', 'CLUB', 'COVAL', 'CPC', 'CRB', 'CRW', 'CURE', 
                             'CVC', 'DASH', 'DCR', 'DCT', 'DGB', 'DMD', 'DNT', 'DOGE', 
                             'DOPE', 'DTB', 'DYN', 'EBST', 'EDG', 'EFL', 'EGC', 'EMC', 
                             'EMC2', 'ENG', 'ENRG', 'ERC', 'ETC', 'ETH', 'EXCL', 'EXP', 
                             'FAIR', 'FCT', 'FLDC', 'FLO', 'FTC', 'FUN', 'GAM', 'GAME', 
                             'GBG', 'GBYTE', 'GCR', 'GEO', 'GLD', 'GNO', 'GNT', 'GOLOS', 
                             'GRC', 'GRS', 'GUP', 'HMQ', 'INCNT', 'INFX', 'IOC', 'ION', 
                             'IOP', 'KMD', 'KORE', 'LBC', 'LGD', 'LMC', 'LSK', 'LTC', 
                             'LUN', 'MAID', 'MANA', 'MCO', 'MEME', 'MER', 'MLN', 'MONA', 
                             'MUE', 'MUSIC', 'MYST', 'NAV', 'NBT', 'NEO', 'NEOS', 'NLG', 
                             'NMR', 'NXC', 'NXS', 'NXT', 'OK', 'OMG', 'OMNI', 'PART', 'PAY', 
                             'PDC', 'PINK', 'PIVX', 'PKB', 'POT', 'POWR', 'PPC', 'PTC', 'PTOY', 
                             'QRL', 'QTUM', 'QWARK', 'RADS', 'RBY', 'RCN', 'RDD', 'REP', 'RISE', 
                             'RLC', 'SALT', 'SBD', 'SC', 'SEQ', 'SHIFT', 'SIB', 'SLR', 'SLS', 
                             'SNRG', 'SNT', 'SPHR', 'SPR', 'START', 'STEEM', 'STORJ', 'STRAT', 
                             'SWIFT', 'SWT', 'SYNX', 'SYS', 'THC', 'TIX', 'TKS', 'TRST', 'TRUST', 
                             'TX', 'UBQ', 'UKG', 'UNB', 'VIA', 'VIB', 'VOX', 'VRC', 'VRM', 'VTC', 
                             'VTR', 'WAVES', 'WINGS', 'XCP', 'XDN', 'XEL', 'XEM', 'XLM', 'XMG', 
                             'XMR', 'XMY', 'XRP', 'XST', 'XVC', 'XVG', 'XWC', 'XZC', 'ZCL', 'ZEC', 
                             'ZEN', ],

                    'USD' : ['ADA', 'BCC', 'BTC', 'BTG', 'DASH', 'ETC', 'ETH', 'LTC', 
                             'NEO', 'NXT', 'OMG', 'XMR', 'XRP', 'XVG', 'ZEC', ],
                    
                    'ETH' : ['1ST', 'ADA', 'ADT', 'ADX', 'ANT', 'BAT', 'BCC', 'BNT', 'BTG', 
                             'CFI', 'CRB', 'CVC', 'DASH', 'DGB', 'DNT', 'ENG', 'ETC', 'FCT', 
                             'FUN', 'GNO', 'GNT', 'GUP', 'HMQ', 'LGD', 'LTC', 'LUN', 'MANA', 
                             'MCO', 'MYST', 'NEO', 'NMR', 'OMG', 'PAY', 'POWR', 'PTOY', 'QRL', 
                             'QTUM', 'RCN', 'REP', 'RLC', 'SALT', 'SC', 'SNT', 'STORJ', 'STRAT', 
                             'TIX', 'TRST', 'UKG', 'VIB', 'WAVES', 'WINGS', 'XEM', 'XLM', 'XMR', 
                             'XRP', 'ZEC', ]
                  }


    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def getData(self, base, quote):
            
        if base == 'USD':
            base = 'USDT'

        if quote == 'USD':
            quote = 'USDT'

        currencyPair = base + '-' + quote

        data = requests.get(self.api + 'getmarketsummaries').json()

        if data['success'] == 'false':
            print(self.name + ' error: ' + data['message'])
            return {}

        data = data['result'][currencyPair]

        out = {}

        out['base'] = 'USD' if base == 'USDT' else base
        out['quote'] = 'USD' if quote == 'USDT' else quote
        out['price' ] = 1.0 / float(data.pop('Last'))
        out['low24h' ] = float(data.pop('Low'))
        out['high24h'] = float(data.pop('High'))
        out['change24h'] = -1
        out['volume24hbase'] = float(data.pop('BaseVolume'))
        out['volume24hquote'] = float(data.pop('Volume'))

        return out