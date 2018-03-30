# -*- coding: utf-8 -*-

import re
import sys
import os
import threading
import Exchange
import Wallet

class Portfolio:

    def __init__(self, filePath=None):
        
        try:

            self.exchange = Exchange.Exchange()
            self.value = 0
            self.oldValue = 0
            self.base = 'USD'
            self.wallets = []
            self.daemons = []
            self.valueIncreased = True
            self.stop_thread = threading.Event()

            # Default file
            if filePath is None:
                filePath='portfolio'

            # Load portfolio file
            with open(filePath, 'r') as file:

                content = file.readlines()

                if not content:
                    print('Error: empty portfolio')
                    sys.exit()


                variableRegex = r'\S+ *\= *\w+'

                n = len(content)
                i = 0

                # Search for variables
                while i < n:
                    
                    line = content[i].strip()

                    if line == '':
                        content.pop(i)
                        n = len(content)
                        i = i - 1
                        continue

                    if line[0] == '#':
                        content.pop(i)
                        n = len(content)
                        i = i - 1
                        continue

                    if re.match(variableRegex, line):
                        
                        data = line.split('=')

                        variable = data[0].strip().upper()
                        value = data[1].strip().upper()

                        if variable == 'FIAT' and value in self.exchange.supportedFiat:
                            self.base = value
                        else:
                            print('Error: variable not supported (' + variable + ')')
                            sys.exit()

                        content.pop(i)
                        n = len(content)
                        i = i - 1

                    i = i + 1


                # Search for wallets
                n = len(content)
                i = 0

                while i < n:
                    
                    line = content[i]

                    if re.match(Wallet.Wallet.valid_wallet, line):
                       
                        self.wallets.append(Wallet.Wallet(line, self.base, self.exchange.getFiatRate('USD', self.base)))

                        self.daemons.append(threading.Thread(target=self.walletUpdater, args=(self.wallets[-1], self.stop_thread)))
                        self.daemons[-1].setName(self.wallets[-1].exchange + '/' + self.wallets[-1].asset)
                        self.daemons[-1].start()

                        content.pop(i)
                        n = len(content)
                        i = i - 1

                    i = i + 1


                # Remaining lines
                if len(content) > 0:
                        
                    print('Error: invalid line at portfolio file:\n')
                    print(content[0])
                    print('Lines must follow the formats:')
                    print('"TICK AMOUNT EXCHANGE", e.g: "BTC 5.68 Gdax"')
                    print('"VARIABLE=VALUE", e.g: "BASE=EUR"')
                    sys.exit()


        except FileNotFoundError:

            print('Error: portfolio file not found')
            sys.exit()

    
    def updateValue(self):
        
        self.oldValue = self.value
        
        self.value = 0
        
        for w in self.wallets:
            
            v = w.data['value']
            
            if v > 0:
                
                self.value += v



    def walletUpdater(self, wallet, stop_thread):
        
        while not stop_thread.is_set():
        
            wallet.update(self.exchange.getData(wallet.exchange, wallet.base, wallet.asset))

        print(wallet.exchange + ' ' + wallet.base + '/' + wallet.asset + ' updater has ended')