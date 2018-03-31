# Tickly

Tickly is a cryptocurrency ticker and portfolio for your terminal. It is coded in Python, using ncurses for the graphical interface and several cryptocurrency exchanges APIs to get fresh data.

![Imgur](https://i.imgur.com/v356oGz.png)

![Imgur](https://i.imgur.com/bDFLTMD.png)

## Supported exchanges

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
- Kucoin
- Poloniex

## Installation

### GNU/Linux

- Ensure you have Python and Git installed:

    ```bash
    sudo apt install git python3
    ```

- Download or clone this repository:

    ```bash
    git clone https://github.com/derkomai/Tickly && cd Tickly
    ```

- Run Tickly:

  ```bash
  python3 Tickly.py
  ```

### Mac OS

- Install brew

    ```bash
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    ```

- Ensure you have Python and Git installed

    ```bash
    brew install git python3
    ```

- Download or clone this repository:

    ```bash
    git clone https://github.com/derkomai/Tickly && cd Tickly
    ```

- Run Tickly:

  ```bash
  python3 Tickly.py
  ```

### Windows 10

- Install Ubuntu terminal from the [Microsoft Store](https://www.microsoft.com/en-us/store/p/ubuntu/9nblggh4msv6). The first time you launch the terminal you will be asked to create a user and set a password.

- Ensure you have Python and Git installed:

    ```bash
    sudo apt install git python3
    ```

- Download or clone this repository:

    ```bash
    cd ~ && git clone https://github.com/derkomai/Tickly && cd Tickly
    ```

- Run Tickly:

  ```bash
  python3 Tickly.py
  ```

## Setting up your portfolio

Your portfolio is just a plain text file which contains your asset list. You can place a file named *"portfolio"* (with no extensions) next to Tickly so it will automatically find your file, or you can pass any other file as an argument.

  ```bash
  python3 Tickly.py /path/to/my/portfolio
  ```

You can see a sample file in the repository, but as a quick lesson:

- You can comment using #

  ```python
  # This is a comment
  ```

- Every asset is declared in a new line like this: *asset code (space) holdings (space) exchange*, for example

  ```python
  ETH 0.5 Gdax
  ```

- The default fiat in which the portfolio value is expressed is USD. If you want to use another fiat like EUR, just add a line like the following to your portfolio file:

  ```python
  FIAT=EUR
  ```

## Known issues

- The *advanced* section (high 24h, low 24h, volume and change 24h) is still experimental and usually shows wrong data.

## Bug reports

If you detect a bug or find Tickly showing incorrect data, please report it in the issues section in this repository.

## Donations

If you find Tickly useful, you can support it by making a small donation through Paypal or sending some
cryptocurrency to any of this addresses.

- *Ethereum/ERC20:* 0x0Ddc94917100387909cb6141c2e7e453bd31D3f7

- *Litecoin:* MVXhiKnsMTiZYWfzdQ9BdJT8wDpSNrBme1

- *Ripple:* rKYkrKq8vcCYkHWQT9DJSH4FbhqJ7zsSbm

- *Stellar:* GBON6KJYAQMRYTMEOSZQI22MOGZK7FWKDLAIWXRLZSG2XEZ6RG73PUGT

- *Neo:* AGehUh61V2mjmhwsk3sGus5hEVYQZxexZa

- *Bitcoin:* 3F888TKJvWvkRmGVDyeCFAoBbFnLoYsrYP

- *Bitcoin Cash:* 1LfY7Mjh3z11ek1A2exKm3JdXw8VheNHdU

- *Paypal:*  [![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.me/dvilela)
