import asyncio

from src.recording_data import get_price, high_price
from src.bot import send_message

async def Main_Buy_Sell():
    result = ''
    balance_price = 100000
    max_price = float(get_price())
    set_max(max_price=max_price)

    while True:
        with open('result.ssb', 'r') as file:
            result = file.readlines()[-1]
            file.close()
        with open('balance.ssb', 'r') as file:
            balance_price = float(file.readlines()[0])
            file.close()
        
        if result == 'UP':
            if balance_price > 0:
                balance_price -= float(get_price())
                buy_price = float(get_price())
            if float(get_price()) <= buy_price - 50:
                if balance_price > 0:
                    balance_price -= float(get_price())
            if float(get_price()) == buy_price - 200:
                balance_price += float(get_price())
            if float(get_price()) <= (max_price - buy_price) * .3:
                balance_price += float(get_price())
        if 'DOWN':
            if balance_price > 0:
                balance_price -= float(get_price())
        if balance_price < 0:
            balance_price = 0
        
        with open('balance.ssb', 'w+') as file:
            file.write(str(balance_price))
            file.close()
        
        print(str(balance_price))
        send_message(f'Текущий балик - ${round(balance_price, 2)}')
        await asyncio.sleep(1803)

def set_max(max_price):
    if (max_price < float(get_price())):
        max_price = float(get_price())