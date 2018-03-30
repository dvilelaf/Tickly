import curses
import time
import sys
import Portfolio
import UI
import socket

def InternetConnection(host="8.8.8.8", port=53):
    
    try:
        socket.setdefaulttimeout(1)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
        
    except Exception as ex:
        pass

    return False

# Check connection
if not InternetConnection():
    print('No Internet connection detected. Exiting...')
    sys.exit()
    

# Init portfolio
if len(sys.argv) > 1:
    portfolio = Portfolio.Portfolio(sys.argv[1])
else:
    portfolio = Portfolio.Portfolio()
nwallets = len(portfolio.wallets)

# Init ncurses
screen = curses.initscr() # Init screen
curses.start_color() # Needed to use colors
curses.use_default_colors() # Needed to use default terminal colors
curses.curs_set(0) # Hide cursor
screen.nodelay(1) # Do not wait for user input
curses.noecho() # Do not write user input to screen

# Set custom colors
curses.init_pair(1, curses.COLOR_WHITE, -1)
curses.init_pair(2, curses.COLOR_GREEN, -1)
curses.init_pair(3, curses.COLOR_RED, -1)
curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLUE)

exc = []

try:

    key = 0

    # Create UI
    UI = UI.Table(screen, nwallets, portfolio.base)

    UIfitsWindow = UI.UIfitsWindow(screen)

    if UIfitsWindow:
        UI.printTable(screen)
    else:
        UI.printSizeMessage(screen)

    # Main loop
    while key != ord('q') and key != ord('Q'):
        
        # Handle resize
        if key == curses.KEY_RESIZE:
            screen.clear()
            UIfitsWindow = UI.UIfitsWindow(screen)

            if UIfitsWindow:
                UI.printTable(screen)
            else:
                UI.printSizeMessage(screen)
            
        # Get mode change
        elif key == ord('\t'):
            screen.clear()
            UI.changeMode(screen)
            UIfitsWindow = UI.UIfitsWindow(screen)

            if UIfitsWindow:
                UI.printTable(screen)

        if UIfitsWindow:

            # Print wallet data
            for i in range(nwallets):
                UI.printRow(screen, portfolio.wallets[i], i+1)

            # Print portfolio value
            portfolio.updateValue()
            UI.printTitle(screen, portfolio)
        
        # Refresh screen
        screen.refresh()

        # Wait
        time.sleep(0.2)

        # Get user input
        key = screen.getch()

except Exception as e:

    exc = e

finally:

    portfolio.stop_thread.set() # Kill all threads
    curses.endwin()

    if exc:
        print(exc)
        
    print('Waiting for all threads to be ended...')