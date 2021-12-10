#%%
import sqlite3
import requests
import json

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

def getCandleData(pair, duration):
  r = requests.get(ENDPOINT + "api/v3/klines", params=dict(symbol=pair, interval=duration))
  return (json.loads(r.text))

# print(getCandleData('ETHBUSD', '5m'))
print(type(getCandleData('ETHBUSD', '5m')))

def jsonToDict(JSONfile='data.json'):
    with open(JSONfile) as json_data:
        data_dict = json.load(json_data)
    return(data_dict)

def storeCandleData(pair, duration, database="candleDatabase.db"):
    r = getCandleData(pair, duration)
    conn = sqlite3.connect(database, timeout=20)
    cur = conn.cursor()
    for tx in range(5):
        id = tx + 11000
        date = r[tx][0]
        open = r[tx][1]
        high = r[tx][2]
        low = r[tx][3]
        close = r[tx][4]
        volume = r[tx][5]
        quotevolume = r[tx][7]

        data = (id, date, open, high, low, close, volume, quotevolume)
        cur.executemany(" INSERT INTO Binance_ETHBUSD_5m (id, date, open, high, low, close, volume, quotevolume) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?) ", (data,))
        # the secure way to enter the variable
    conn.commit()
    conn.close() 

storeCandleData('ETHBUSD', '5m')
