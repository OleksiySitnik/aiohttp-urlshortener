from sqlalchemy import  MetaData
import asyncpgsa

from .models import users, urls


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[users, urls])


async def init_db(app):
    dsn = construct_db_url(app['config']['postgres'])
    pool = await asyncpgsa.create_pool(dsn=dsn)
    app['db'] = pool
    return pool


async def close_pg(app):
     await app['db'].close()


def construct_db_url(config):
    DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
    return DSN.format(
        database=config['database'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port'],
    )
