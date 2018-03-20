# import asyncio
from aiotg import Bot
from alerter.BaseClasses import Pin
from alerter.config import TELEGRAM_TOKEN


bot = Bot(api_token=TELEGRAM_TOKEN)


class TelegramPin(Pin):
    PIN_TYPE = "telegram"

    async def notify(self, notification, subscriber):
        await bot.send_message(subscriber.pin_id, "%s" % notification.data)
        print("(telegram) massage has been sent", notification)
