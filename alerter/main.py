import asyncio
from alerter import Alerter
from alerter.config import WEB_PORT
from alerter.Subscribers import subscribers
from alerter.Queues import NOTIFICATION_QUEUE

from alerter.sources.web_hook import WebHook
from alerter.pins.printer import PrinterPin
from alerter.pins.telegram import TelegramPin
from alerter.managers.telegram import TelegramManager

source_types = ["deploy"]

Alerter.register_manager(TelegramManager(subscribers, source_types))
Alerter.register_pin(PrinterPin())
Alerter.register_pin(TelegramPin())
Alerter.register_source(WebHook(NOTIFICATION_QUEUE))


async def get_tasks(loop):
    app = Alerter.create_web()
    server = loop.create_server(app.make_handler(), '127.0.0.1', WEB_PORT)
    tasks = []
    tasks.append(server)
    tasks.append(Alerter.notification_loop(NOTIFICATION_QUEUE, subscribers))
    tasks.extend(Alerter.get_tasks())
    tasks = asyncio.gather(*tasks)
    await tasks


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_tasks(loop))
    loop.run_forever()


if __name__ == '__main__':
    main()
