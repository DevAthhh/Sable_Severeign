import asyncio
import requests

from helpers import msg_handler as mh
from src.recording_data import Main_RD
from src.recording_data import Main_High

async def User_requests():
    while True:
        await asyncio.sleep(2)
        print('This is Egor')

async def main():
    await asyncio.gather(User_requests(), Main_RD(), Main_High())

asyncio.run(main())