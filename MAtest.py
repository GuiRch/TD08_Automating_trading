import pandas as pd
import requests, json
from ta.trend import SMAIndicator, EMAIndicator

ENDPOINT = "https://api.binance.com/"

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


r = getCandleData('ETHBUSD', '5m')

print(r)
print(len(r))
