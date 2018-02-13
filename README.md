# Tickly
Tickly is a cryptocurrency ticker and portfolio for your terminal. It is coded in Python, using ncurses for the graphical interface and several cryptocurrency exchanges APIs to get fresh data.



<p align="center">
  <img src="https://i.imgur.com/v356oGz.png">
</p>

<p align="center">
  <img src="https://i.imgur.com/bDFLTMD.png">
</p>

# Supported exchanges

- Binance
- Bitfinex
- Bithumb
- Bitstamp
- Bittrex
- Coinbase
- Coinone
- Gdax
- Gemini
- Hitbtc
- Kraken
- Poloniex



# Installation


## GNU/Linux

- Ensure you have Python and Git installed:

    ```
    sudo apt install git python3
    ```
- Download or clone this repository:
    ```
    git clone https://github.com/derkomai/Tickly && cd Tickly
    ```

- Run Tickly:
  ```
  python3 Tickly.py
  ```


## Mac OS

- Install brew
    ```
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    ```
- Ensure you have Python and Git installed
    ```
    brew install git python3
    ```

- Download or clone this repository:
    ```
    git clone https://github.com/derkomai/Tickly && cd Tickly
    ```

- Run Tickly:
  ```
  python3 Tickly.py
  ```


## Windows 10

- Install Ubuntu terminal from the [Microsoft Store](https://www.microsoft.com/en-us/store/p/ubuntu/9nblggh4msv6). The first time you launch the terminal you will be asked to create a user and set a password.

- Download or clone this repository:
    ```
    cd ~ && git clone https://github.com/derkomai/Tickly && cd Tickly
    ```

- Ensure you have Python and Git installed:
    ```
    sudo apt install git python3
    ```

- Run Tickly:
  ```
  python3 Tickly.py
  ```



# Setting up your portfolio
Your portfolio is just a plain text file which contains your asset list. You can place a file named *"portfolio"* (with no extensions) next to Tickly so it will automatically find your file, or you can pass any other file as an argument.
  ```
  python3 Tickly.py /path/to/my/portfolio
  ```


You can see a sample file in the repository, but as a quick lesson:

- You can comment using #
  ```
  # This is a comment
  ```

- Every asset is declared in a new line like this: *asset code (space) holdings (space) exchange*, for example
  ```
  ETH 0.5 Gdax
  ```
- The default fiat in which the portfolio value is expressed is USD. If you want to use another fiat like EUR, just add a line like the following to your portfolio file:
  ```
  FIAT=EUR
  ```



# Bug report

If you detect a bug or find Tickly showing incorrect data, please report it in the issues section in this repository.



# Donation
If you find Tickly useful, you can support it by making a small donation through Paypal or sending some 
cryptocurrency to any of this addresses.

*Ethereum:* 0xca59e0b52c48a894155b4b1f17d843afe4fe83ae  
*Litecoin:* LQPkKfq3uPm7T54ht33xgxtNP38ARYpEsQ  
*Ripple:* rwxQHDS6HnwXgZbRobZgC1ysfmaPM2Tkbi  
*Bitcoin:* 1J5zEeRwiL5MRUGe4NAdcoyghCxZhiRB5N  
*Bitcoin Cash:* 1FJMh712UM5FAbzEk8ox8Kexb6uxWu5f9u  

*Paypal:*  [![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.me/dvilela)
