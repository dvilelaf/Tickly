import collections
import re
import curses

class Table:
    
    def __init__(self, screen, nentries, base):
        
        self.nentries = nentries
        self.base = base
        self.headers = collections.OrderedDict()

        # Sizes
        self.headerRows = 7
        self.headerCols = []
        self.tableRows = self.headerRows + 2 * self.nentries
        self.tableCols = 0
        self.row0 = 0
        self.col0 = 0
        self.titleCol = 0

        # Column padding
        self.colPadding = 2
        self.colPaddingStr = ''

        for i in range(self.colPadding):
            self.colPaddingStr += ' '

        # Colors
        self.colors = {'white' : curses.color_pair(1), 
                       'green' : curses.color_pair(2), 
                       'red' : curses.color_pair(3), 
                       'footer' : curses.color_pair(4),
                       'warning' : curses.color_pair(5)}

        # Set mode
        self.setMode(1) # Full mode by default


    def setMode(self, mode):

        if mode == 1:
            self.setFullMode()
        else:
            self.setSimpleMode()


    def changeMode(self, screen):
        
        self.setMode(-1 * self.mode)


    def setSimpleMode(self):
        
        self.mode = -1

        # Table headers
        self.headers.clear()
        self.headers['ASSET'] = ('{:^5.5}')
        self.headers['EXCHANGE'] = '{:^10.10}'
        self.headers['PRICE (USD)'] = '{:12.4f}'
        self.headers['HOLDINGS'] = '{:12.4f}'
        self.headers['VALUE (' + self.base + ')'] = '{:13.2f}'

        self.calculateTableWidth()


    def setFullMode(self):
        
        self.mode = 1

        # Table headers
        self.headers.clear()
        self.headers['ASSET'] = '{:^5.5}'
        self.headers['EXCHANGE'] = '{:^10.10}'
        self.headers['PRICE (USD)'] = '{:12.4f}'
        self.headers['%24H'] = '{:+7.2f}'
        self.headers['LOW 24H (USD)'] = '{:12.4f}'
        self.headers['HIGH 24H (USD)'] = '{:12.4f}'
        self.headers['VOLUME'] = '{:12.2f}'
        self.headers['HOLDINGS'] = '{:12.4f}'
        self.headers['VALUE (' + self.base + ')'] = '{:13.2f}'

        self.calculateTableWidth()

    
    def calculateTableWidth(self):
        
        self.tableCols = 0
        self.headerCols = []

        for h in self.headers:

            match = re.search('[0-9]{1,2}', self.headers[h]).group()
            self.headerCols.append(int(match) + 2 * self.colPadding)
            self.tableCols += self.headerCols[-1]

        self.tableCols += (1 + len(self.headers)) # vertical separators


    def UIfitsWindow(self, screen):
        
        ttyRows, ttyCols = screen.getmaxyx()
        
        if ttyRows < self.tableRows + 3 or \
           ttyCols < self.tableCols + 3:

            if self.mode == 1:
                self.setMode(-1)
                return self.UIfitsWindow(screen)

            else:
                return False

        else:
            return True


    def printTable(self, screen):
        
        # Get window size
        ttyRows, ttyCols = screen.getmaxyx()
        
        # Calculate table origin
        self.row0 = int((ttyRows - self.tableRows) / 2)
        self.col0 = int((ttyCols - self.tableCols) / 2)

        # Draw border
        border = screen.derwin(self.tableRows, self.tableCols, self.row0, self.col0)
        border.box()

        # Draw row lines
        for r in range(self.row0 + self.headerRows - 3, self.row0 + self.tableRows - 1, 2):

            screen.addch(r, self.col0, curses.ACS_LTEE)
            screen.hline(r, self.col0+1, curses.ACS_HLINE, self.tableCols - 2)
            screen.addch(r, self.col0 + self.tableCols - 1, curses.ACS_RTEE)

        # Title
        title = 'PORTFOLIO VALUE =                '
        self.titleCol = self.col0 + int((self.tableCols - len(title)) / 2)
        screen.addstr(self.row0 + 2, self.titleCol, title)

        # Headers
        row = self.row0 + self.headerRows - 2
        col = self.col0 + 1
        i = 0

        for header in self.headers:
            
            padding = int((self.headerCols[i] - len(header)) / 2)
            
            col += padding
            screen.addstr(row, col, header)
            col = col - padding + self.headerCols[i] + 1
            i += 1

        # Vertical separator
        row = self.row0 + self.headerRows - 2
        col = self.col0
        i = 0

        for i in range(len(self.headers) - 1):
            
            col += (self.headerCols[i] + 1)
            
            screen.addch(row, col, curses.ACS_VLINE)
            screen.addch(row - 1, col, curses.ACS_TTEE)
            screen.addch(row + 1, col, curses.ACS_BTEE)

        # Footer
        screen.hline(ttyRows - 1, 0, ' ', ttyCols, self.colors['footer'])
        screen.addstr(ttyRows - 1, 0, ' q : Quit  |  tab : Toggle simple/full mode (full mode requires a wide window)', self.colors['footer'])


    def selectColor(self, value, oldValue):
        
        if value > oldValue:
            return self.colors['green']
        elif value < oldValue:
            return self.colors['red']
        else:
            return self.colors['white']
    
    
    def printRow(self, screen, wallet, row):

        # Build data
        data = {}
        data['ASSET'] = wallet.asset
        data['EXCHANGE'] = wallet.exchange
        data['PRICE (USD)'] = 1.0 / wallet.data['priceUSD']

        if wallet.data['change24h'] == -1:
            data['%24H'] = -1
        else:
            data['%24H'] = -1.0 * wallet.data['change24h']

        data['LOW 24H (USD)'] = 1.0 / wallet.data['high24h']
        data['HIGH 24H (USD)'] = 1.0 / wallet.data['low24h']
        data['VOLUME'] = wallet.data['volume24hquote']
        data['HOLDINGS'] = wallet.holdings
        data['VALUE (' + self.base + ')'] = wallet.data['value']

        # Calculate position
        r = self.row0 + self.headerRows - 2 + 2 *row
        c = self.col0 + 1
            
        # Print data
        for h in self.headers:
            
            string = self.colPaddingStr + self.headers[h].format(data[h]) + self.colPaddingStr
            
            if data[h] == -1:
                     
                fmt = '{{:^{0}.{0}}}'.format(len(string))
                string = fmt.format('N/A')

            color = self.selectColor(wallet.data['priceBASE'], wallet.data['oldPriceBASE'])

            screen.addstr(r, c, string, color)

            c += (len(string) + 1)

    
    def printTitle(self, screen, portfolio):

        color = self.selectColor(portfolio.value, portfolio.oldValue)

        screen.addstr(self.row0 + 2, self.titleCol + 18, \
            '{:11.2f} '.format(portfolio.value) + portfolio.base, color)


    def printSizeMessage(self, screen):
        
        ttyRows, ttyCols = screen.getmaxyx()

        message = ' A bigger window is needed to print data '
        message = ' Tickly feels a little bit uncomfortable in this tiny space '

        if ttyRows * ttyCols > len(message) + 2:
            
            if ttyCols > len(message) + 1:
                
                row = int(ttyRows / 2)
                col = int((ttyCols - len(message)) / 2)
                screen.addstr(row, col, message, self.colors['footer'])

            else:
                row = int(ttyRows / 2)
                screen.addstr(row - 1, 0, message, self.colors['footer'])

        else:
            
            screen.addstr(0, 0, message[:ttyRows * ttyCols - 1], self.colors['footer'])
