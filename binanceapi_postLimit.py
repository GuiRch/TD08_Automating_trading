import time, hmac, requests, json

API_KEY = ''
API_SECRET = ''
ENDPOINT = 'https://api.binance.com/'

order_api_url = 'api/v3/order'


def get_signed_url(dataQueryString, secret_key):
    signature = hmac.new(API_SECRET.encode(), dataQueryString.encode(), 'sha256').hexdigest()
    return (ENDPOINT + order_api_url + '?' + dataQueryString + '&signature=' + signature)


def createOrder(api_key, secret_key, direction, price, amount, pair='BTCUSDT', orderType='LimitOrder'):
    type = ''
    if orderType == 'LimitOrder':
        type = 'LIMIT'
    
    # dataQueryString = 'symbol=BTCUSDT&side=BUY&type=LIMIT&timeInForce=GTC&quantity=0.0015&price=30000&recvWindow=20000&timestamp=' + str(int(time.time()*1000))
    dataQueryString = 'symbol=' + pair +'&side=' + direction.upper() + '&type=' + type + '&timeInForce=GTC&quantity=' + str(amount) + '&price=' + str(price) + '&recvWindow=20000&timestamp=' + str(int(time.time()*1000))
    
    headers = {'X-MBX-APIKEY': api_key}
    url = get_signed_url(dataQueryString, secret_key)

    response = requests.post(url, headers=headers)
    r = json.loads(response.text)

    print(r['orderId'])
    return r


def cancelOrder(api_key, secret_key, uuid, pair='BTCUSDT'):
    
    # dataQueryString = 'symbol=BTCUSDT&orderId=8617530103&recvWindow=20000&timestamp=' + str(int(time.time()*1000))
    dataQueryString = 'symbol=' + pair + '&orderId=' + str(uuid) + '&recvWindow=20000&timestamp=' + str(int(time.time()*1000))
    
    headers = {'X-MBX-APIKEY': api_key}
    url = get_signed_url(dataQueryString, secret_key)

    response = requests.delete(url, headers=headers)
    r = json.loads(response.text)

    return r


# CREATE ORDER
r = createOrder(API_KEY, API_SECRET, 'buy', 30000, 0.001)

# DELETE ORDER
# uuid = 8618063338
# r = cancelOrder(API_KEY, API_SECRET, uuid)

print(r)

