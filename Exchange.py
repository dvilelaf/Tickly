# -*- coding: utf-8 -*-

import sys
import time
import datetime
import requests

import Exchanges.Binance
import Exchanges.Bitfinex
import Exchanges.Bithumb
import Exchanges.Bitstamp
import Exchanges.Bittrex
import Exchanges.Coinbase
import Exchanges.Coinone
import Exchanges.Gdax
import Exchanges.Gemini
import Exchanges.Hitbtc
import Exchanges.Kraken
import Exchanges.Kucoin
import Exchanges.Poloniex


class Exchange:

    exchanges = {'Binance' : Exchanges.Binance.Binance(),
                 'Bitfinex' : Exchanges.Bitfinex.Bitfinex(),
                 'Bithumb' : Exchanges.Bithumb.Bithumb(),
                 'Bitstamp' : Exchanges.Bitstamp.Bitstamp(),
                 'Bittrex' : Exchanges.Bittrex.Bittrex(),
                 'Coinbase' : Exchanges.Coinbase.Coinbase(),
                 'Coinone' : Exchanges.Coinone.Coinone(),
                 'Gdax' : Exchanges.Gdax.Gdax(),
                 'Gemini' : Exchanges.Gemini.Gemini(),
                 'Hitbtc' : Exchanges.Hitbtc.Hitbtc(),
                 'Kraken' : Exchanges.Kraken.Kraken(),
                 'Kucoin' : Exchanges.Kucoin.Kucoin(),
                 'Poloniex' : Exchanges.Poloniex.Poloniex(),
                }


    def __init__(self):

        self.valid_pairs = {self.exchanges[e].name : self.exchanges[e].valid_pairs for e in self.exchanges}

        rates = requests.get('https://api.exchangeratesapi.io/latest?base=USD').json()['rates']

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

        data['high24h'], data['low24h'] = 1.0 / data['low24h'], 1.0 / data['high24h']

        if data['change24h'] != -1:
            data['change24h'] = -1.0 * data['change24h']

        return data


    def getData(self, exchange, base, quote):

        baseIsFiat = True if base in self.supportedFiat else False
        quoteIsFiat = True if quote in self.supportedFiat else False

        # Fiat to fiat
        if baseIsFiat and quoteIsFiat:
            return self.getFiatRate(base, quote)


        # Get assets info
        class AssetInfo:

            def __init__(self):
                self.exists = False
                self.isBase = False
                self.bases = []


        baseInfo = AssetInfo()
        quoteInfo = AssetInfo()

        for i in self.valid_pairs[exchange]:

            if i == base:
                baseInfo.exists = True
                baseInfo.isBase = True

            if i == quote:
                quoteInfo.exists = True
                quoteInfo.isBase = True

            if base in self.valid_pairs[exchange][i]:
                baseInfo.exists = True
                baseInfo.bases.append(i)

            if quote in self.valid_pairs[exchange][i]:
                quoteInfo.exists = True
                quoteInfo.bases.append(i)


        # None of assets exist in the exchange
        if not baseInfo.exists and not quoteInfo.exists:
            data = {}
            data['base'] = base
            data['quote'] = quote
            data['price'] = -1
            data['low24h' ] = -1
            data['high24h'] = -1
            data['change24h'] = -1
            data['volume24hbase'] = -1
            data['volume24hquote'] = -1

            return data


        # Both assets exist in the exchange
        if baseInfo.exists and quoteInfo.exists:

            # Direct rate
            if baseInfo.isBase and base in quoteInfo.bases:
                return self.getDataTimed(exchange, base, quote)

            # Inverse rate
            if quoteInfo.isBase and quote in baseInfo.bases:
                return self.reverseData(self.getDataTimed(exchange, quote, base))

            # Both are quotes
            if not baseInfo.isBase and not quoteInfo.isBase:

                # Common base
                for baseBase in baseInfo.bases:
                    if baseBase in quoteInfo.bases:
                        dataBase = self.getDataTimed(exchange, baseBase, base)
                        dataQuote = self.getDataTimed(exchange, baseBase, quote)

                        data = {}

                        data['base'] = base
                        data['quote'] = quote
                        data['price'] = dataQuote['price'] / dataBase['price']
                        data['low24h' ] = -1
                        data['high24h'] = -1
                        data['change24h'] = -1
                        data['volume24hbase'] = dataBase['volume24hquote']
                        data['volume24hquote'] = dataQuote['volume24hquote']

                        return data

                # Different base
                for baseBase in baseInfo.bases:
                    for quoteBase in quoteInfo.bases:

                        if baseBase in self.valid_pairs[exchange][quoteBase]:

                            dataBase = self.getDataTimed(exchange, baseBase, base)
                            dataQuote = self.getDataTimed(exchange, quoteBase, quote)
                            dataBaseBase = self.getDataTimed(exchange, quoteBase, baseBase)

                            data = {}
                            data['base'] = base
                            data['quote'] = quote
                            data['price'] = dataQuote['price'] / (dataBase['price'] * dataBaseBase['price'])
                            data['low24h' ] = -1
                            data['high24h'] = -1
                            data['change24h'] = -1
                            data['volume24hbase'] = dataBase['volume24hquote']
                            data['volume24hquote'] = dataQuote['volume24hquote']

                            return data


                        if quoteBase in self.valid_pairs[exchange][baseBase]:

                            dataBase = self.getDataTimed(exchange, baseBase, base)
                            dataQuote = self.getDataTimed(exchange, quoteBase, quote)
                            dataQuoteBase = self.getDataTimed(exchange, baseBase, quoteBase)

                            data = {}
                            data['base'] = base
                            data['quote'] = quote
                            data['price'] = (dataQuote['price'] * dataQuoteBase['price']) / dataBase['price']
                            data['low24h' ] = -1
                            data['high24h'] = -1
                            data['change24h'] = -1
                            data['volume24hbase'] = dataBase['volume24hquote']
                            data['volume24hquote'] = dataQuote['volume24hquote']

                            return data


                        for peer in self.valid_pairs[exchange][baseBase]:

                            if peer in self.valid_pairs[exchange][quoteBase]:

                                dataBase = self.getDataTimed(exchange, baseBase, base)
                                dataQuote = self.getDataTimed(exchange, quoteBase, quote)
                                dataPeerBase = self.getDataTimed(exchange, baseBase, peer)
                                dataPeerQuote = self.getDataTimed(exchange, quoteBase, peer)

                                data = {}
                                data['base'] = base
                                data['quote'] = quote
                                data['price'] = (dataQuote['price'] * dataPeerBase['price']) / (dataBase['price'] * dataPeerQuote['price'])
                                data['low24h' ] = -1
                                data['high24h'] = -1
                                data['change24h'] = -1
                                data['volume24hbase'] = dataBase['volume24hquote']
                                data['volume24hquote'] = dataQuote['volume24hquote']

                                return data

            # One is base, one is quote
            if baseInfo.isBase and not quoteInfo.isBase:

                for quoteBase in quoteInfo.bases:

                    if quoteBase in self.valid_pairs[exchange][base]:

                        dataBase = self.getDataTimed(exchange, base, quoteBase)
                        dataQuote = self.getDataTimed(exchange, quoteBase, quote)

                        data = {}
                        data['base'] = base
                        data['quote'] = quote
                        data['price'] = dataBase['price'] * dataQuote['price']
                        data['low24h' ] = -1
                        data['high24h'] = -1
                        data['change24h'] = -1
                        data['volume24hbase'] = dataBase['volume24hbase']
                        data['volume24hquote'] = dataQuote['volume24hquote']

                        return data

            if not baseInfo.isBase and quoteInfo.isBase:

                for baseBase in baseInfo.bases:

                    if baseBase in self.valid_pairs[exchange][quote]:

                        dataBase = self.getDataTimed(exchange, baseBase, base)
                        dataQuote = self.getDataTimed(exchange, quote, baseBase)

                        data = {}
                        data['base'] = base
                        data['quote'] = quote
                        data['price'] = 1 / (dataBase['price'] * dataQuote['price'])
                        data['low24h' ] = -1
                        data['high24h'] = -1
                        data['change24h'] = -1
                        data['volume24hbase'] = dataBase['volume24hquote']
                        data['volume24hquote'] = dataQuote['volume24hbase']

                        return data


        # Only one of the assets exist in the exchange
        else:

            if not baseInfo.exists and baseIsFiat:

                baseRate = self.getFiatRate('USD', base)
                dataQuote =  self.getData(exchange, 'USD', quote)

                data = {}
                data['base'] = base
                data['quote'] = quote
                data['price'] = dataQuote['price'] / baseRate
                data['low24h' ] = -1
                data['high24h'] = -1
                data['change24h'] = -1
                data['volume24hbase'] = -1
                data['volume24hquote'] = dataQuote['volume24hquote']

                return data


            if not quoteInfo.exists and quoteIsFiat:

                dataBase =  self.getData(exchange, 'USD', base)
                quoteRate = self.getFiatRate('USD', quote)

                data = {}
                data['base'] = base
                data['quote'] = quote
                data['price'] = quoteRate / dataBase['price']
                data['low24h' ] = -1
                data['high24h'] = -1
                data['change24h'] = -1
                data['volume24hbase'] = dataBase['volume24hquote']
                data['volume24hquote'] = -1

                return data


        # Couldn't find rate
        data = {}
        data['base'] = base
        data['quote'] = quote
        data['price'] = -1
        data['low24h' ] = -1
        data['high24h'] = -1
        data['change24h'] = -1
        data['volume24hbase'] = -1
        data['volume24hquote'] = -1

        return data
