import asyncio
from BaseClasses import Pin


class PrinterPin(Pin):
    PIN_TYPE = "print"

    async def notify(self, notification):
        await asyncio.sleep(0.1)
        print(notification)
