from aiotg import Bot, Chat
from alerter.config import TELEGRAM_TOKEN
from alerter.Model import Subscriber
from alerter.BaseClasses import Manager

PIN_TYPE = "telegram"

assert TELEGRAM_TOKEN
bot = Bot(api_token=TELEGRAM_TOKEN)


class TelegramManager(Manager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_bot()

    def init_bot(self):
        @bot.command(r"/subscribe")
        async def subscribe(chat: Chat, match):
            subscriber = Subscriber(chat.id, PIN_TYPE, "deploy", None, None)
            print("(telegram) subscribe", subscriber)
            await self.subscribers.add(subscriber)
            return chat.reply("You have been subscribed successfully")
        return subscribe

    def loop(self):
        return bot.loop()