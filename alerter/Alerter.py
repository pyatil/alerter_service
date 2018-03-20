import asyncio
from aiohttp import web


sources = []
pins = {}
managers = []
web_routes = []


def register_source(source):
    sources.append(source)
    web_routes.extend(source.get_routers())


def register_pin(pin):
    pins[pin.PIN_TYPE] = pin


def register_manager(manager):
    managers.append(manager)
    web_routes.extend(manager.get_routers())


def get_pin_handler_by_type(pin_type):
    return pins[pin_type]


def create_web():
    app = web.Application()
    for web_route in web_routes:
        app.router.add_post(*web_route)
    return app


def get_tasks(loop):
    tasks = []
    for resource in managers + sources:
        loop = resource.loop()
        if loop:
            task = asyncio.ensure_future(loop)
            tasks.append(task)
    return tasks
