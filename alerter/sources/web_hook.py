from aiohttp import web
from alerter.BaseClasses import Source
from alerter.Model import Notification


class WebHook(Source):

    async def web_hook_handler(self, request):
        data = await request.json()
        await self.notification_queue.put(Notification(**data))
        print("Notification has been added")
        return web.Response()

    def get_routers(self):
        return [
            ("/notifications", self.web_hook_handler)
        ]
