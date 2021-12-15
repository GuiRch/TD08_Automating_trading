#%%
import pandas as pd
import sqlite3, requests, json
from ta.trend import SMAIndicator, EMAIndicator

#%%
ENDPOINT = "https://api.binance.com/"

# Check for connection to the API
r = requests.get(ENDPOINT + "api/v3/exchangeInfo")
r.status_code

#%%

# Get all avaible cryptocurrencies
def avaibleCrypto():
  r = requests.get(ENDPOINT + "api/v3/exchangeInfo")
  assets = json.loads(r.text)
  ListSymbols = assets["symbols"]
  baseAsset = []
  for elem in ListSymbols:
    baseAsset.append(elem['baseAsset'])

  return baseAsset

print(avaibleCrypto())

#%%

# Get the order book for the required pair 
def orderBook(pair):
  r = requests.get(ENDPOINT + "api/v3/depth", params=dict(symbol=pair))
  return (json.loads(r.text))

# print(orderBook('ETHBUSD'))

#%%

# Get ask or bids for different cryptocurrencies
def getDepth(direction, pair):
  r = orderBook(pair)
  return r[direction][0][0]

# print(getDepth('asks','ETHBUSD'))

#%%

# def getCandleData(pair, duration):
#   r = requests.get(ENDPOINT + "api/v3/klines", params=dict(symbol=pair, interval=duration))
#   return (json.loads(r.text))

def getCandleData(pair, duration):
  r = requests.get(ENDPOINT + "api/v3/klines", params=dict(symbol=pair, interval=duration))
  bars = json.loads(r.text)
  df = pd.DataFrame(bars, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'No trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
  
  sma7 = SMAIndicator(df['Close'], 7, False)
  ema7 = EMAIndicator(df['Close'], 7, False)

  sma30 = SMAIndicator(df['Close'], 30, False)
  ema30 = EMAIndicator(df['Close'], 30, False)

  sma200 = SMAIndicator(df['Close'], 200, False)
  ema200 = EMAIndicator(df['Close'], 200, False)
  
  df['SMA 7'] = sma7.sma_indicator()
  df['EMA 7'] = ema7.ema_indicator()

  df['SMA 30'] = sma30.sma_indicator()
  df['EMA 30'] = ema30.ema_indicator()

  df['SMA 200'] = sma200.sma_indicator()
  df['EMA 200'] = ema200.ema_indicator()

  return (df)

# print(getCandleData('ETHBUSD', '5m'))
# print(type(getCandleData('ETHBUSD', '5m')))


def jsonToDict(JSONfile='data.json'):
    with open(JSONfile) as json_data:
        data_dict = json.load(json_data)
    return(data_dict)


def storeCandleData(pair, duration, database="candleDatabase.db"):
    df = getCandleData(pair, duration)

    _date = df['Open time'].tolist()
    _open = df['Open'].tolist()
    _high = df['High'].tolist()
    _low = df['Low'].tolist()
    _close = df['Close'].tolist()
    _volume = df['Volume'].tolist()
    _quotevolume = df['Quote asset volume'].tolist()

    _sma7 = df['SMA 7'].tolist()
    _ema7 = df['EMA 7'].tolist()
    _sma30 = df['SMA 30'].tolist()
    _ema30 = df['EMA 30'].tolist()
    _sma200 = df['SMA 200'].tolist()
    _ema200 = df['EMA 200'].tolist()

    conn = sqlite3.connect(database, timeout=20)
    cur = conn.cursor()
    for tx in range(len(df)):
        id = _date[tx]
        date = _date[tx]
        open = _open[tx]
        high = _high[tx]
        low = _low[tx]
        close = _close[tx]
        volume = _volume[tx]
        quotevolume = _quotevolume[tx]

        sma7 = _sma7[tx]
        ema7 = _ema7[tx]
        sma30 = _sma30[tx]
        ema30 = _ema30[tx]
        sma200 = _sma200[tx]
        ema200 = _ema200[tx]

        data = (id, date, open, high, low, close, volume, quotevolume, sma7, ema7, sma30, ema30, sma200, ema200)
        cur.executemany(" INSERT INTO Binance_ETHBUSD_5m (id, date, open, high, low, close, volume, quotevolume, sma_7, ema_7, sma_30, ema_30, sma_200, ema_200) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ", (data,))
        # the secure way to enter the variable
    conn.commit()
    conn.close() 

storeCandleData('ETHBUSD', '5m')
