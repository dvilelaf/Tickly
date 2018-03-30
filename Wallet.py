import Exchange
import sys


class Wallet:
    
    valid_wallet = r'\S{2,5} *\d+(\.\d+)? *\S+'

    def __init__(self, line, base, rateUSD):
        
        data = line.split()

        self.asset = data[0].upper()
        self.holdings = float(data[1])
        self.exchange = data[2].capitalize()
        self.base = base
        self.rateUSD = rateUSD
        self.valueIncreased = True

        self.data = {
            'priceBASE' : -1,
            'oldPriceBASE' : -1,
            'priceUSD' : -1,
            'value' : -1,
            'low24h' : -1, 
            'high24h' : -1, 
            'change24h' : -1,
            'volume24hbase' : -1, 
            'volume24hquote' : -1
        }


        if self.asset == 'USDT':
            self.asset = 'USD'


        # Check if exchange is supported
        if self.exchange not in Exchange.Exchange.exchanges:
            
            print('Error: exchange not supported (' + self.exchange + ')')
            sys.exit()


        # Check if asset is supported in exchange
        supportedAsset = False
        
        for base in Exchange.Exchange.exchanges[self.exchange].valid_pairs:
            if self.asset == base \
            or self.asset in Exchange.Exchange.exchanges[self.exchange].valid_pairs[base]:
                supportedAsset = True
                break
        
        if not supportedAsset:
            print('Error: ' + self.exchange + ' does not support ' + self.asset + ' currency.')
            sys.exit()


    def update(self, data):
        
        # Check correct quote
        if data['quote'] != self.asset:
            print('Error: bad quote received')
            sys.exit()

        self.data['oldPriceBASE'] = self.data['priceBASE'] 
        self.data['priceBASE'] = data['price'] 
        self.data['priceUSD'] = self.data['priceBASE'] * self.rateUSD 

        self.data['value'] = self.holdings / self.data['priceBASE']

        self.data['low24h'] = data['low24h']
        self.data['high24h'] = data['high24h']
        self.data['change24h'] = data['change24h']
        self.data['volume24hbase'] = data['volume24hbase']
        self.data['volume24hquote'] = data['volume24hquote']