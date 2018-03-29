# -*- coding: utf-8 -*-
import requests
import datetime


class Hitbtc:
    
    name = 'Hitbtc'
    
    api = 'https://api.hitbtc.com/api/2/'

    wait_time = 1

    valid_pairs = {'USD': ['ADX', 'AIR', 'AMM', 'ATB', 'ATM', 'B2X', 'BAR', 'BCH', 
                            'BCN', 'BMC', 'BNT', 'BQX', 'BTC', 'BTCA', 'BTG', 'BTM', 
                            'CAS', 'CAT', 'CDT', 'CHAT', 'CL', 'CLD', 'CND', 'CTR', 
                            'CVC', 'DASH', 'DATA', 'DCN', 'DGB', 'DIM', 'DOGE', 'EBTCNEW', 
                            'EBTCOLD', 'EDO', 'EET', 'EMGO', 'ENJ', 'EOS', 'ETC', 'ETH', 
                            'ETP', 'EVX', 'FLP', 'FUEL', 'FUN', 'ICOS', 'ICX', 'KMD', 
                            'LOC', 'LSK', 'LTC', 'MAID', 'MANA', 'MCO', 'NEO', 'NEU', 
                            'NGC', 'NXT', 'OAX', 'OMG', 'PLR', 'PPC', 'PRG', 'QTUM', 
                            'SENT', 'SMART', 'SMS', 'SMT', 'SNC', 'SNT', 'STRAT', 'STU', 
                            'STX', 'SUB', 'SUR', 'SWFTC', 'TIO', 'TNT', 'TRX', 'UGT', 'UTK', 
                            'UTT', 'VEN', 'VERI', 'VIB', 'WAX', 'WMGO', 'WRC', 'XDN', 'XEM', 
                            'XMR', 'XTZ', 'XUC', 'XVG', 'ZEC', 'ZRX', 'ZSC'], 
                    
                    'BTC': ['1ST', 'ADX', 'AE', 'AEON', 'AIR', 'AMM', 'AMP', 'ANT', 'ARDR', 
                            'ARN', 'ART', 'ATB', 'ATL', 'ATM', 'ATS', 'AVH', 'B2X', 'BAR', 
                            'BCH', 'BCN', 'BKB', 'BMC', 'BMT', 'BNT', 'BOS', 'BQX', 'BTCA', 
                            'BTG', 'BTM', 'BTX', 'BUS', 'C20', 'CAS', 'CAT', 'CDT', 'CFI', 
                            'CHAT', 'CHSB', 'CL', 'CLD', 'CLOUT', 'CND', 'CNX', 'COSS', 'COV', 
                            'CSNO', 'CTR', 'CTX', 'DASH', 'DATA', 'DBIX', 'DCT', 'DGB', 'DGD', 
                            'DICE', 'DIM', 'DLT', 'DNT', 'DOGE', 'DOV', 'DRPU', 'DSH', 'EBTCNEW', 
                            'EBTCOLD', 'ECH', 'EDG', 'EDO', 'EET', 'EKO', 'ELE', 'ELM', 'EMC', 
                            'EMGO', 'ENJ', 'EOS', 'ERO', 'ETBS', 'ETC', 'ETH', 'ETP', 'EVX', 
                            'EXN', 'FCN', 'FLP', 'FRD', 'FUEL', 'FUN', 'FYP', 'GAME', 'GNO', 
                            'GRMD', 'GUP', 'HAC', 'HPC', 'HSR', 'HVN', 'ICN', 'ICO', 'ICOS', 
                            'ICX', 'IDH', 'INDI', 'IPL', 'ITS', 'IXT', 'KBR', 'KICK', 'KMD', 
                            'LAT', 'LEND', 'LIFE', 'LOC', 'LRC', 'LSK', 'LTC', 'LUN', 'MAID', 
                            'MANA', 'MCAP', 'MCO', 'MEK', 'MIPS', 'MNE', 'MTH', 'NEBL', 'NEO', 
                            'NEU', 'NGC', 'NTO', 'NXC', 'NXT', 'OAX', 'ODN', 'OMG', 'OPT', 'ORME', 
                            'OTN', 'OTX', 'PAY', 'PING', 'PIX', 'PLBT', 'PLR', 'PLU', 'POE', 'POLL', 
                            'PPC', 'PPT', 'PRE', 'PRG', 'PTOY', 'QAU', 'QCN', 'QTUM', 'REP', 'RLC', 
                            'RVT', 'SBD', 'SBTC', 'SC', 'SCL', 'SENT', 'SISA', 'SKIN', 'SMART', 
                            'SMS', 'SMT', 'SNC', 'SNGLS', 'SNT', 'STEEM', 'STORM', 'STRAT', 'STU', 
                            'STX', 'SUB', 'SUR', 'SWFTC', 'SWT', 'TAAS', 'TAU', 'TBT', 'TGT', 
                            'TIME', 'TIO', 'TKN', 'TNT', 'TRST', 'TRX', 'UGT', 'ULTC', 'UTK', 
                            'UTT', 'VEN', 'VERI', 'VIB', 'VIBE', 'VOISE', 'W3C', 'WAVES', 'WAX', 
                            'WINGS', 'WMGO', 'WRC', 'WTC', 'XAUR', 'XDN', 'XDNCO', 'XEM', 'XMR', 
                            'XRP', 'XTZ', 'XUC', 'XVG', 'YOYOW', 'ZAP', 'ZEC', 'ZRC', 'ZRX', 'ZSC'], 
                            
                    'USDT': ['AVH', 'BTX', 'CLOUT', 'DRT', 'EKO', 'EMC', 'REP', 'SBTC', 'XRP'], 

                    'ETH': ['1ST', 'ADX', 'AIR', 'AMM', 'ARN', 'ATB', 'ATM', 'ATS', 'AVH', 'AVT', 
                            'B2X', 'BAR', 'BAS', 'BCH', 'BCN', 'BET', 'BMC', 'BMT', 'BNT', 'BQX', 
                            'BTCA', 'BTG', 'BTM', 'C20', 'CAS', 'CAT', 'CCT', 'CDT', 'CDX', 'CFI', 
                            'CHAT', 'CHSB', 'CL', 'CLD', 'CLOUT', 'CND', 'COSS', 'COV', 'CPAY', 
                            'CTR', 'CTX', 'DASH', 'DATA', 'DCN', 'DDF', 'DENT', 'DGB', 'DICE', 
                            'DIM', 'DOGE', 'DOV', 'DRPU', 'DRT', 'EBET', 'EBTCNEW', 'EBTCOLD', 
                            'EDO', 'EET', 'EKO', 'EMC', 'ENG', 'ENJ', 'EOS', 'ETC', 'ETP', 'EVX', 
                            'FLP', 'FUEL', 'FUN', 'FYN', 'GNO', 'GNX', 'GVT', 'HDG', 'HGT', 'HVN', 
                            'ICOS', 'ICX', 'IDH', 'IGNIS', 'IND', 'IXT', 'JNT', 'KMD', 'LA', 'LEND', 
                            'LOC', 'LRC', 'LSK', 'LTC', 'MAID', 'MANA', 'MCO', 'MSP', 'MTH', 'MYB', 
                            'NDC', 'NEBL', 'NEO', 'NET', 'NEU', 'NGC', 'NXT', 'OAX', 'OMG', 'PAY', 
                            'PIX', 'PLR', 'PLU', 'POE', 'PPT', 'PRG', 'PRO', 'PTOY', 'QAU', 'QTUM', 
                            'QVT', 'REP', 'RKC', 'SAN', 'SBTC', 'SENT', 'SISA', 'SMART', 'SMS', 'SMT', 
                            'SNC', 'SNM', 'SNT', 'SPF', 'STAR', 'STRAT', 'STU', 'STX', 'SUB', 'SUR', 
                            'SWFTC', 'SWT', 'TAAS', 'TIME', 'TIO', 'TIX', 'TKR', 'TNT', 'TRAC', 'TRX', 
                            'UET', 'UGT', 'UTK', 'UTT', 'VEN', 'VERI', 'VIB', 'W3C', 'WAX', 'WRC', 
                            'XAUR', 'XDN', 'XEM', 'XMR', 'XRP', 'XTZ', 'XUC', 'XVG', 'ZEC', 'ZRX', 'ZSC']
                    }

    responses = {
        200 : 'OK Successful request',
        400 : 'Bad Request. Returns JSON with the error message',
        401 : 'Unauthorized. Authorisation required or failed',
        403 : 'Forbidden. Action is forbidden for API key',
        429 : 'Too Many Requests. Your connection is being rate limited',
        500 : 'Internal Server. Internal Server Error',
        503 : 'Service Unavailable. Service is down for maintenance',
        504 : 'Gateway Timeout. Request timeout expired',
    }


    def __init__(self):
        self.lastCheck = datetime.datetime.fromtimestamp(0)


    def getData(self, base, quote):
            
        currencyPair = quote + base

        data = requests.get(self.api + 'public/ticker/' + currencyPair)

        if data.status_code != 200:
            print(self.name + ' error: ' + self.responses[data.status_code])
            return {}

        data = data.json()

        if 'error' in data:
            print(self.name + ' error: ' + data['error']['message'])
            return {}


        out = {}

        out['base'] = base
        out['quote'] = quote
        out['price' ] = 1.0 / float(data['last']) # Prices are reversed
        out['low24h' ] = 1.0 / float(data['high'])
        out['high24h'] = 1.0 / float(data['low'])
        out['change24h'] = -1
        out['volume24hbase'] = float(data['volume'])
        out['volume24hquote'] = float(data['volumeQuote'])

        return out