from aiotg import Bot, Chat
from alerter.config import TELEGRAM_TOKEN
from alerter.Subscribers import Subscriber
from alerter.BaseClasses import Manager

PIN_TYPE = "telegram"


HELP_MSG = """/subscriptions - show you current subscriptions (could you unsubscribe)
/subscribe [regex] - subscribe on all notifications or part, examples: /subscribe, /subscribe _uat, /subscribe RC180312
"""

assert TELEGRAM_TOKEN
bot = Bot(api_token=TELEGRAM_TOKEN)


class TelegramManager(Manager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_bot()

    def init_bot(self):
        @bot.command(r"/(help|start)")
        async def help(chat: Chat, match):
            return chat.send_text(HELP_MSG)

        @bot.command(r"/subscribe( .*)?")
        async def subscribe(chat: Chat, match):
            regex = ".*" if not match.group(1) else match.group(1).strip()
            subscriber = Subscriber(chat.id, PIN_TYPE, "deploy", None, regex)
            # print("(telegram) subscribe", subscriber)
            await self.subscribers.add(subscriber)
            return chat.send_text("You have been subscribed '%s' successfully" % regex)

        @bot.command(r"/unsubscribe.(\d+)")
        async def unsubscribe(chat: Chat, match):
            # print("(telegram)", match.group(1))
            sub_idx = int(match.group(1).strip())
            # print("(telegram) unsubscribe", chat.id, sub_idx)
            regex = await self.subscribers.remove(chat.id, sub_idx)
            return chat.send_text("You have been unsubscribed '%s' successfully" % regex)

        @bot.command(r"/subscriptions")
        async def subscriptions(chat: Chat, match):
            subs = await self.subscribers.get_subscriptions(chat.id)
            # print("(telegram)", subs)
            TEMPLATE = "'{1}'\n/unsubscribe_{0}"
            if subs:
                msg = "\n\n".join([TEMPLATE.format(i, sub.regex) for i, sub in enumerate(subs)])
            else:
                msg = "You don't have subscriptions"
            return chat.send_text(msg)

    def loop(self):
        return bot.loop()
