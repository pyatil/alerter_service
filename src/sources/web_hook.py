from aiohttp import web


def get_handler(notification_queue, notification_creater):
    async def new_notification(request):
        data = await request.json()
        await notification_queue.put(notification_creater(**data))
        print("Notification has been added")
        return web.Response()
    return new_notification


def notification_source(notification_queue, notification_creater):
    app = web.Application()
    app.router.add_post("/notifications", get_handler(notification_queue, notification_creater))
    return app
