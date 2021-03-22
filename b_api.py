import urequests
import ntptime
import time
import json

def ask():
    current_rates = urequests.get('https://api.binance.com/api/v1/depth?symbol=BTCUSDT'); current_rates = json.loads(current_rates.text)

    #bid=float(current_rates['bids'][0][0]) ; bid
    ask=float(current_rates['asks'][0][0]) ; ask
    return ask

def bid():
    current_rates = urequests.get('https://api.binance.com/api/v1/depth?symbol=BTCUSDT'); current_rates = json.loads(current_rates.text)

    bid=float(current_rates['bids'][0][0]) ; bid
    #ask=float(current_rates['asks'][0][0]) ; ask
    return bid


def btime():
    btime = urequests.request(method= 'GET', url='https://api.binance.com/api/v1/time', data="" ); btime = json.loads(btime.text)
    btime=int(btime['serverTime'])
    return btime
#btime ()


def price():
    response = urequests.request(method= 'GET', url="https://api.binance.com/api/v3/ticker/price?symbol=LTCUSDT", data="")
    if 'code' in response.text:
        raise Exception(response.text)
    print (response.json())

def sync():
    #if needed, overwrite default time server
    ntptime.host = "1.europe.pool.ntp.org"

    try:
        print("Local time before synchronization：%s" %str(time.localtime()))
        #make sure to have internet connection
        ntptime.settime()
        print("Local time after synchronization：%s" %str(time.localtime()))
    except:
        print("Error syncing time")
#sync()
    