import asyncio


from helpers import msg_handler as mh
from src.recording_data import Main_RD
from src.recording_data import Main_High
from src.solves import Main_Solves
from src.bs import Main_Buy_Sell

async def main():
    await asyncio.gather(Main_RD(), Main_Solves(), Main_High(), Main_Buy_Sell())

asyncio.run(main())