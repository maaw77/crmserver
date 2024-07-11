from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from asyncpg import Record, Connection

from datetime import date

from db import (Pool,
                SELECT_GSM_TABLE,
                SELECT_TANK_TABLE,
                SELECT_SHEET_TABLE,
                SELECT_AZS_TABLE,
                SELECT_EXCHANGE_TABLE,
                SELECT_REMAINS_TABLE)
from validators import (GsmTableValidator,
                        TankTableValidator,
                        SheetTableValidator,
                        AZSTableValidator,
                        ExchangeTableValidator,
                        RemainsTableValidator,)

routes = web.RouteTableDef()


@routes.get('/')
async def get_index(request: Request) -> Response:
    """
    A view of a list of URLs.
    """
    return web.json_response({"urls": ['/gsm_table', '/tank_table',
                                       '/sheet_table', '/azs_table',
                                       '/exchange_table', '/remains_table']})


@routes.get('/gsm_table/{date}')
async def get_gsm_table(request: Request) -> Response:
    """
    Table "Priem" view.
    """
    pool: Pool = request.app['db']
    date_action = date.fromisoformat(request.match_info['date'])
    conn: Connection
    async with pool.acquire() as conn:
        rec: list[Record] = await conn.fetch(SELECT_GSM_TABLE, date_action, date_action)
        return web.json_response([GsmTableValidator(**r).model_dump() for r in rec])


@routes.get('/tank_table/{date}')
async def get_tank_table_get(request: Request) -> Response:
    """
    Table "Vidacha v ATZ" view.
    """
    pool: Pool = request.app['db']
    date_action = date.fromisoformat(request.match_info['date'])
    conn: Connection
    async with pool.acquire() as conn:
        rec: list[Record] = await conn.fetch(SELECT_TANK_TABLE, date_action, date_action)
        return web.json_response([TankTableValidator(**r).model_dump() for r in rec])


@routes.get('/sheet_table/{date}')
async def get_sheet_table_get(request: Request) -> Response:
    """
    Table "Vidacha iz ATZ" view.
    """
    pool: Pool = request.app['db']
    date_action = date.fromisoformat(request.match_info['date'])
    conn: Connection
    async with pool.acquire() as conn:
        rec: list[Record] = await conn.fetch(SELECT_SHEET_TABLE, date_action, date_action)
        return web.json_response([SheetTableValidator(**r).model_dump() for r in rec])


@routes.get('/azs_table/{date}')
async def get_azs_table(request: Request) -> Response:
    """
    Table "Vidacha iz TRK" view.
    """
    pool: Pool = request.app['db']
    date_action = date.fromisoformat(request.match_info['date'])
    conn: Connection
    async with pool.acquire() as conn:
        rec: list[Record] = await conn.fetch(SELECT_AZS_TABLE, date_action, date_action)
        return web.json_response([AZSTableValidator(**r).model_dump() for r in rec])


@routes.get('/exchange_table/{date}')
async def get_exchange_table(request: Request) -> Response:
    """
    Table "Obmen megdu rezervuarami" view.
    """
    pool: Pool = request.app['db']
    date_action = date.fromisoformat(request.match_info['date'])
    conn: Connection
    async with pool.acquire() as conn:
        rec: list[Record] = await conn.fetch(SELECT_EXCHANGE_TABLE, date_action, date_action)
        return web.json_response([ExchangeTableValidator(**r).model_dump() for r in rec])


@routes.get('/remains_table/{date}')
async def get_remains_table(request: Request) -> Response:
    """
    Table "Snyatie ostatkov" view.
    """
    pool: Pool = request.app['db']
    date_action = date.fromisoformat(request.match_info['date'])
    conn: Connection
    async with pool.acquire() as conn:
        rec: list[Record] = await conn.fetch(SELECT_REMAINS_TABLE, date_action, date_action)
        # print([dict(r) for r in rec])
        # return web.json_response(['dfsdds'])
        return web.json_response([RemainsTableValidator(**r).model_dump() for r in rec])

