import asyncio
import Alerter
from config import WEB_PORT
from Model import subscribers
from Queues import NOTIFICATION_QUEUE

from sources.web_hook import WebHook
from pins.printer import PrinterPin
from pins.telegram import TelegramPin
from managers.telegram import TelegramManager


Alerter.register_manager(TelegramManager(subscribers))
Alerter.register_pin(PrinterPin())
Alerter.register_pin(TelegramPin())
Alerter.register_source(WebHook(NOTIFICATION_QUEUE))


async def alerter():
    while True:
        notification = await NOTIFICATION_QUEUE.get()
        tasks = []
        for subscriber in subscribers:
            handler = Alerter.get_pin_handler_by_type(subscriber.pin_type).notify
            task = handler(notification, subscriber)
            tasks.append(task)
        if tasks:
            await asyncio.gather(*tasks)


async def main(loop):
    app = Alerter.create_web()
    server = loop.create_server(app.make_handler(), '127.0.0.1', WEB_PORT)
    tasks = []
    tasks.append(server)
    tasks.append(alerter())
    tasks.extend(Alerter.get_tasks(loop))
    tasks = asyncio.gather(*tasks)
    await tasks
    # await asyncio.wait(tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.run_forever()
