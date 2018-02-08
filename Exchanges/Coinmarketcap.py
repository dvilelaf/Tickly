# -*- coding: utf-8 -*-
import requests
import sys
import datetime


class Coinmarketcap:
    
    name = 'Coinmarketcap'
    
    api = 'https://api.coinmarketcap.com/v1/'

    wait_time = 1


    def __init__(self):
        
        self.lastCheck = datetime.datetime.fromtimestamp(0)
        
        data = requests.get(self.api + 'ticker/')

        if data.status_code != 200:
            print('Error')
            sys.exit()
            
        data = data.json()
            
        self.assets = []

        for d in data:
            self.assets.append(d['id'])
        


    def getData(self, asset):
        
        if asset not in self.assets:
            print('Error: coinmarketcap does not support ' + asset)
            sys.exit()
            
        data = requests.get(self.api + 'ticker/' + asset).json()

        if 'error' in data:
            print(self.name + ' error: ' + data['error'])
            return {}

        data = data[0]

        data['priceUSD'] = float(data.pop('price_usd'))
        data['priceBTC'] = float(data.pop('price_btc'))
        data['volume24h'] = float(data.pop('24h_volume_usd'))
        data['change1h'] = float(data.pop('percent_change_1h'))
        data['change24h'] = float(data.pop('percent_change_24h'))
        data['change7d'] = float(data.pop('percent_change_7d'))
        data['supply'] = float(data.pop('total_supply'))

        return data