from aiohttp import web
from aiohttp.web_app import Application

from middlewares import error_middleware
from views import routes
from settings import config
from db import init_db


async def init_app() -> Application:
    """
    Initializes the application.
    """
    app = web.Application(middlewares=[error_middleware,])
    app.add_routes(routes)
    app['config'] = config
    app.cleanup_ctx.append(init_db)
    return app


if __name__ == '__main__':
    web.run_app(init_app())
