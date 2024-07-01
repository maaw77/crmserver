import asyncpg
from asyncpg.pool import Pool
from aiohttp.web_app import Application


from settings import Settings

SELECT_GSM_TABLE = \
                    '''
                    SELECT gsm_table.dt_receiving,
                           gsm_table.dt_crch,
                           gsm_table.been_changed,
                           sites.name AS site,
                           gsm_table.income_kg,
                           operators.name AS operator,
                           providers.name AS provider,
                           contractors.name AS contractor,
                           license_plates.name AS license_plate,
                           statuses.name AS status
                           FROM gsm_table 
                           JOIN sites ON gsm_table.site_id = sites.id
                           JOIN operators ON gsm_table.operator_id = operators.id
                           JOIN providers ON gsm_table.provider_id = providers.id
                           JOIN contractors ON gsm_table.contractor_id = contractors.id
                           JOIN license_plates ON gsm_table.license_plate_id = license_plates.id
                           JOIN statuses ON gsm_table.status_id = statuses.id
                           WHERE gsm_table.dt_receiving >= $1
                                 and gsm_table.dt_receiving <= $2
                           ORDER BY gsm_table.dt_receiving DESC;
                    '''


SELECT_TANK_TABLE = \
                    '''
                    SELECT tank_table.dt_giveout,
                           tank_table.dt_crch,
                           tank_table.been_changed,
                           sites.name AS site,
                           onboard_nums.name AS onboard_num,
                           dest_sites.name AS dest_site,
                           tank_table.given_kg,
                           statuses.name AS status
                           FROM tank_table
                           JOIN sites ON tank_table.site_id = sites.id
                           JOIN onboard_nums ON tank_table.onboard_num_id = onboard_nums.id
                           JOIN sites dest_sites ON tank_table.dest_site_id = dest_sites.id
                           JOIN statuses ON tank_table.status_id = statuses.id
                           WHERE tank_table.dt_giveout >= $1
                                 and tank_table.dt_giveout <= $2
                           ORDER BY tank_table.dt_giveout DESC;
                    '''

SELECT_SHEET_TABLE = \
                    '''
                    SELECT sheet_table.dt_giveout,
                           sheet_table.dt_crch,
                           sheet_table.been_changed,
                           sites.name AS site,
                           atzs.name AS atz,
                           give_sites.name AS give_site,
                           sheet_table.given_litres,
                           sheet_table.given_kg,
                           statuses.name AS status
                           FROM sheet_table
                           JOIN sites ON sheet_table.site_id = sites.id
                           JOIN atzs ON sheet_table.atz_id = atzs.id
                           JOIN sites give_sites ON sheet_table.give_site_id = give_sites.id
                           JOIN statuses ON sheet_table.status_id = statuses.id
                           WHERE sheet_table.dt_giveout >= $1
                                 and sheet_table.dt_giveout <= $2
                           ORDER BY sheet_table.dt_giveout DESC;
                    '''

SELECT_AZS_TABLE = \
                    '''
                    SELECT azs_table.dt_giveout,
                           azs_table.dt_crch,
                           azs_table.been_changed,
                           sites.name AS site,
                           storekeepers.name AS storekeeper,
                           azs_table.counter_azs_bd,
                           azs_table.counter_azs_ed,
                           azs_table.given_litres,
                           azs_table.given_kg,
                           statuses.name AS status
                           FROM azs_table
                           JOIN sites ON azs_table.site_id = sites.id
                           JOIN storekeepers ON azs_table.storekeeper_id = storekeepers.id
                           JOIN statuses ON azs_table.status_id = statuses.id
                           WHERE azs_table.dt_giveout >= $1
                                 and azs_table.dt_giveout <= $2
                           ORDER BY azs_table.dt_giveout DESC;
                    '''

SELECT_EXCHANGE_TABLE = \
                    '''
                    SELECT exchange_table.dt_change,
                           exchange_table.dt_crch,
                           exchange_table.been_changed,
                           sites.name AS site,
                           operators.name AS operator,
                           tin.name AS tanker_in,
                           tout.name AS tanker_out,
                           exchange_table.litres,
                           statuses.name AS status 
                           FROM exchange_table
                           JOIN sites ON exchange_table.site_id = sites.id
                           JOIN operators ON exchange_table.operator_id = operators.id
                           JOIN tankers tin ON exchange_table.tanker_in_id = tin.id
                           JOIN tankers tout ON exchange_table.tanker_out_id = tout.id
                           JOIN statuses ON exchange_table.status_id = statuses.id
                           WHERE exchange_table.dt_change >= $1
                                 and exchange_table.dt_change <= $2
                           ORDER BY exchange_table.dt_change DESC;
                    '''


SELECT_REMAINS_TABLE = \
                    '''
                    SELECT remains_table.dt_inspection,
                           sites.name AS site,
                           inspectors.name AS inspector,
                           tankers.name AS tanker_num,
                           remains_table.remains_kg,
                           fuel_marks.name AS fuel_mark,
                           statuses.name AS status 
                           FROM remains_table
                           JOIN sites ON remains_table.site_id = sites.id
                           JOIN inspectors ON remains_table.inspector_id = inspectors.id
                           JOIN tankers ON remains_table.tanker_num_id = tankers.id
                           JOIN fuel_marks ON remains_table.fuel_mark_id = fuel_marks.id
                           JOIN statuses ON remains_table.status_id = statuses.id
                           WHERE remains_table.dt_inspection >= $1
                                 and remains_table.dt_inspection <= $2
                           ORDER BY remains_table.dt_inspection DESC;
                    '''


async def init_db(app: Application):
    """
    Configures and creates a Postgresql connection pool.
    Then closes the connection pool.
    """
    try:
        conf: Settings = app['config']
        pool: Pool = await asyncpg.create_pool(host=conf.HOST_DB,
                                               port=conf.PORT_DB,
                                               user=conf.POSTGRES_USER,
                                               database=conf.POSTGRES_DB,
                                               password=conf.POSTGRES_PASSWORD.get_secret_value())
        app['db']: Pool = pool
        yield
    finally:
        pool: Pool = app['db']
        await pool.close()
