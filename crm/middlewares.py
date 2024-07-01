from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from yarl import URL

from collections.abc import Callable

from validators import DateActionValidator, ValidationError


@web.middleware
async def error_middleware(request: Request, handler: Callable) -> Response:
    """
    Middleware for validation input data.
    """
    if request.rel_url == URL('/'):
        return await handler(request)
    try:
        if 'date' not in request.match_info.keys():
            raise ValueError('Invalid URL!')
        DateActionValidator(date_action=request.match_info['date'])
        resp: Response = await handler(request)
        if resp.text == '[]':
            return web.json_response({'details': 'Data not found!'}, status=404)
        return resp
    except (ValidationError, ValueError) as er:
        return web.json_response({'details': str(er)}, status=400)

