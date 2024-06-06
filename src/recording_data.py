import requests
import time
import asyncio
import math

from helpers import msg_handler as mh

high_price = 0.0

open_price = 0.0
close_price = 0.0

class File_Actions:
    def write_to_file(name, data):
        if name != 'balance':
            with open(f'{name}.ssb', 'a+') as f:
                f.write(data)
                f.close()
        else:
            with open(f'{name}.ssb', 'w+') as f:
                f.write(data)
                f.close()

async def Main_RD():
    global open_price
    global close_price

    file = File_Actions

    while True:
        open_price = float(get_price())
        await asyncio.sleep(5)
        close_price = float(get_price())

        data_kline = {'Open': 0.0, 'Close': 0.0, 'High': 0.0, 'Low': 0.0, 'Color': '', 'Size': 0.0}

        #   Handler for recording data
        data_kline['Open'] = open_price
        data_kline['Close'] = close_price
        data_kline['High'] = high_price
        data_kline['Size'] = abs(close_price - open_price)

        if open_price > close_price:
            data_kline['Color'] = 'green'
        else:
            data_kline['Color'] = 'red'
        
        file.write_to_file('klines', str(data_kline) + '\n')
        print(data_kline)
        
async def Main_High():
    global high_price
    high_price = float(get_price())
    while True:
        now_price = float(get_price())
        if high_price < now_price:
            high_price = now_price
        print('High price is ' + str(high_price))

        await asyncio.sleep(180)

def get_price():
    try:
        url = "https://api.bybit.com/v2/public/tickers"
        params = {
            'symbol': 'BTCUSDT'
        }

        response = requests.get(url, params=params)
        data = response.json()

        return data['result'][0]['last_price']
    
    except Exception as e:

        print(mh.Debug_msg('Data processing', f'Error: \'{e}\'', 0))
        return str(0.0)
