import json
from uuid import uuid4
from aiotg import Bot, Chat
from asyncio import Queue
from alerter.config import TELEGRAM_TOKEN
from alerter.Subscribers import Subscriber
from alerter.BaseClasses import Manager

PIN_TYPE = "telegram"


HELP_MSG = """/subscriptions - show you current subscriptions (could you unsubscribe)
/subscribe [regex] - subscribe on all notifications or part, examples: /subscribe, /subscribe _uat, /subscribe RC180312
"""

assert TELEGRAM_TOKEN
bot = Bot(api_token=TELEGRAM_TOKEN)


def inl_button(text, callback_name):
    return {
        'type': 'InlineKeyboardButton',
        'text': text,
        'callback_data': '%s' % (callback_name),
    }


def get_subscribe_markup(source_types, callback_name):
    return {
        'type': 'ReplyKeyboardMarkup',
        'inline_keyboard': [
            [inl_button(source_type, '%s-%s' % (callback_name, source_type))]
            for source_type in source_types
        ]
    }


def get_subscriptions_markup(subscriptions, callback_name):
    return {
        'type': 'ReplyKeyboardMarkup',
        'inline_keyboard': [
            [inl_button("unsubscribe from '%s'" % sub.regex, '%s-%s' % (callback_name, i))]
            for i, sub in enumerate(subscriptions)
        ]
    }


# TODO: remove this hook after done
def get_hook(queue):
    async def hook(chat: Chat, cq, match):
        print("called hook", chat, match.group())
        await queue.put(match)
    return hook


class TelegramManager(Manager):

    def __init__(self, subscribers, source_types):
        super().__init__(subscribers)
        self.source_types = source_types
        self.init_bot()

    def init_bot(self):
        @bot.command(r"/(help|start)")
        async def help(chat: Chat, match):
            return chat.send_text(HELP_MSG)

        @bot.command(r"/subscribe( .*)?")
        async def subscribe(chat: Chat, match):
            regex = ".*" if not match.group(1) else match.group(1).strip()
            queue = Queue()
            rnd_name = str(uuid4())
            hook = get_hook(queue)
            bot.add_callback(rnd_name + "-(.*)", hook)
            markup = get_subscribe_markup(["any"] + self.source_types, rnd_name)
            sended_msg = await chat.send_text("Choose source type", reply_markup=json.dumps(markup))
            # print("SENDED", sended_msg)
            sended_message_id = sended_msg['result']['message_id']
            nmatch = await queue.get()
            choosed_source_type = nmatch.group(1)
            source_type = ".*" if choosed_source_type == "any" else choosed_source_type
            subscriber = Subscriber(chat.id, PIN_TYPE, source_type, None, regex)
            await self.subscribers.add(subscriber)
            return chat.edit_text(sended_message_id, "You have been subscribed '%s' from source '%s'" % (regex, source_type))

        @bot.command(r"/subscriptions")
        async def subscriptions(chat: Chat, match):
            subs = await self.subscribers.get_subscriptions(chat.id)
            # print("(telegram)", subs)
            if not subs:
                return chat.send_text("You dont have subscriptions")
            queue = Queue()
            rnd_name = str(uuid4())
            hook = get_hook(queue)
            bot.add_callback(rnd_name + "-(.*)", hook)
            markup = get_subscriptions_markup(subs, rnd_name)
            sended_msg = await chat.send_text("Subscriptions:", reply_markup=json.dumps(markup))
            sended_message_id = sended_msg['result']['message_id']
            nmatch = await queue.get()
            choosed_id = int(nmatch.group(1))
            removed_sub = await self.subscribers.remove(chat.id, choosed_id)
            msg = "Unsubscribed from '%s'" % removed_sub
            return chat.edit_text(sended_message_id, msg)

        @bot.default
        async def default(chat: Chat, message):
            print('Unhandled callback fired', message)
            # chat.send_text('Unhandled callback fired')

    def loop(self):
        return bot.loop()
