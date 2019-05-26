from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime
)
from datetime import datetime as dt


metadata = MetaData()

users = Table(
    'users', metadata,

    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=False, unique=True),
    Column('email', String(120)),
    Column('password_hash', String(128), nullable=False)
)

urls = Table(
    'urls', metadata,

    Column('id', Integer, primary_key=True),
    Column('url', String(250), unique=True),
    Column('short_url', String(140)),
    Column('timestamp', DateTime, index=True, default=dt.utcnow),
    Column('user_id',
           Integer,
           ForeignKey('users.id'))
)


async def get_user_by_name(conn, username):
    user = await conn.fetchrow(
        users.select()
             .where(users.c.username == username)
    )

    return user

async def get_url_by_lurl(conn, lurl):
    url = await conn.fetchrow(
        urls.select()
            .where(urls.c.url == lurl)
    )

    return url


async def create_user(conn, username, password, email):
    await conn.execute(
        users.insert().values(
            username=username,
            password_hash=password,
            email=email
        )
    )


async def add_url(conn, url, short_url, user_id):
    await conn.execute(
        urls.insert().values(
            url=url,
            short_url=short_url,
            user_id=user_id
        )
    )


async def get_urls_by_user(conn, userid):
    user_urls = await conn.fetch(
        urls.select()
            .where(urls.c.user_id == userid)
            .order_by(urls.c.timestamp.desc())
    )

    return user_urls


async def delete_url(conn, del_url):
    await conn.execute(
        urls.delete(urls.c.url == del_url)
    )
