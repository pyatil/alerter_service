import asyncio
from BaseClasses import Pin


class PrinterPin(Pin):
    PIN_TYPE = "telegram"

    async def notify(self, notification, subscriber):
        await asyncio.sleep(0.1)
        print(notification)
