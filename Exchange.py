# -*- coding: utf-8 -*-

import sys
import time
import datetime
import requests
import Exchanges.Coinbase
import Exchanges.Gdax
import Exchanges.Poloniex
import Exchanges.Binance
import Exchanges.Bitfinex
import Exchanges.Bitstamp
import Exchanges.Bittrex
import Exchanges.Bithumb


class Exchange:
    
    exchanges = {'Coinbase' : Exchanges.Coinbase.Coinbase(),
                 'Gdax' : Exchanges.Gdax.Gdax(),
                 'Poloniex' : Exchanges.Poloniex.Poloniex(),
                 'Binance' : Exchanges.Binance.Binance(),
                 'Bitfinex' : Exchanges.Bitfinex.Bitfinex(),
                 'Bitstamp' : Exchanges.Bitstamp.Bitstamp(),
                 'Bittrex' : Exchanges.Bittrex.Bittrex(),
                 'Bithumb' : Exchanges.Bithumb.Bithumb(),
                 
                 }

    
    def __init__(self):
        
        self.valid_pairs = {self.exchanges[e].name : self.exchanges[e].valid_pairs for e in self.exchanges}

        rates = requests.get('https://api.fixer.io/latest?base=USD').json()['rates']

        self.fiatRates = {r : float(rates[r]) for r in rates}
        self.supportedFiat = [r for r in self.fiatRates]
        self.supportedFiat.append('USD')


    def getFiatRate(self, base, quote):
        
        if base == quote:
            return 1.0

        if base == 'USD':
            return self.fiatRates[quote]

        if quote == 'USD':
            return 1.0 / self.fiatRates[base]

        return self.fiatRates[quote] / self.fiatRates[base]


    def getDataTimed(self, exchange, base, quote):
        
        delta = (datetime.datetime.now() - self.exchanges[exchange].lastCheck).total_seconds();

        while delta < self.exchanges[exchange].wait_time:
            
            time.sleep(0.1)

            delta = (datetime.datetime.now() - self.exchanges[exchange].lastCheck).total_seconds();

        data = self.exchanges[exchange].getData(base, quote)

        self.exchanges[exchange].lastCheck = datetime.datetime.now()
        
        return data


    def reverseData(self, data):
        
        data['base'], data['quote'] = data['quote'], data['base']
        
        data['price'] = 1.0 / data['price']

        data['volume24hbase'], data['volume24hquote'] = data['volume24hquote'], data['volume24hbase']

        data['high24h'], data['low24h'] = 1.0 / data['high24h'], 1.0 / data['low24h']

        if data['change24h'] != -1:
            data['change24h'] = -1.0 * data['change24h']
    
        return data


    def getData(self, exchange, base, quote):
        
        # Base direct rate
        if base in self.valid_pairs[exchange] and quote in self.valid_pairs[exchange][base]:
            return self.getDataTimed(exchange, base, quote)

        # Base inverse rate
        if quote in self.valid_pairs[exchange] and base in self.valid_pairs[exchange][quote]:
            return self.reverseData(self.getDataTimed(exchange, quote, base))

        # USD direct rate
        if 'USD' in self.valid_pairs[exchange] and quote in self.valid_pairs[exchange]['USD']:
            return self.getDataTimed(exchange, 'USD', quote)

        # USD inverse rate
        if quote in self.valid_pairs[exchange] and 'USD' in self.valid_pairs[exchange][quote]:
            return self.reverseData(self.getDataTimed(exchange, quote, 'USD'))

        # BTC rate
        if 'BTC' in self.valid_pairs[exchange] and quote in self.valid_pairs[exchange]['BTC']:
            dataBTC = self.getDataTimed(exchange, 'BTC', quote)
            dataUSD = self.getData(exchange, 'USD', 'BTC')

            data = {}

            data['base'] = 'USD'
            data['quote'] = quote
            data['price'] = dataBTC['price'] * dataUSD['price']
            data['low24h' ] = -1
            data['high24h'] = -1
            data['change24h'] = -1
            data['volume24hbase'] = -1
            data['volume24hquote'] = dataBTC['volume24hquote']

            return data

        # BTC inverse rate
        if quote in self.valid_pairs[exchange] and 'BTC' in self.valid_pairs[exchange][quote]:
            dataBTC = self.reverseData(self.getDataTimed(exchange, quote, 'BTC'))
            dataUSD = self.getData(exchange, 'USD', 'BTC')

            data = {}

            data['base'] = 'USD'
            data['quote'] = quote
            data['price'] = dataBTC['price'] * dataUSD['price']
            data['low24h' ] = -1
            data['high24h'] = -1
            data['change24h'] = -1
            data['volume24hbase'] = -1
            data['volume24hquote'] = dataBTC['volume24hquote']

            return data

        print('Error getting rates for ' + quote + ' in ' + exchange)
        sys.exit()