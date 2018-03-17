import asyncio
from sources.web_hook import notification_source
from Queues import NOTIFICATION_QUEUE
from Model import Notification
from config import WEB_PORT
from pins import printer


async def alerter(loop):
    while True:
        notification = await NOTIFICATION_QUEUE.get()
        subsribers = [
            asyncio.ensure_future(printer.notification_subscriber(notification))
        ]
        done, pending = await asyncio.wait(subsribers)
        print(done, pending)


async def main(loop):
    app = notification_source(NOTIFICATION_QUEUE, Notification)
    server = await loop.create_server(app.make_handler(), '127.0.0.1', WEB_PORT)
    return server


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.run_until_complete(alerter(loop))
    loop.run_forever()
