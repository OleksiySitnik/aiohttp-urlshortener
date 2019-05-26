import aiohttp_jinja2
import jinja2

from sqlalchemy import create_engine
from cryptography import fernet
import base64
from aiohttp import web
from aiohttp_security import(
    SessionIdentityPolicy, setup as setup_security,
    authorized_userid
)

from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from url_shorter.db import init_db, close_pg, create_tables, construct_db_url
from url_shorter.settings import CONFIG
from url_shorter.routes import setup_routes
from url_shorter.db_auth import DBAuthorizationPolicy


async def current_user_ctx_processor(request):
    username = await authorized_userid(request)
    is_anonymous = not bool(username)
    return {'current_user': {'is_anonymous': is_anonymous}}


def datetimeformat(value, format='%d-%m-%Y / %H:%M'):
    return value.strftime(format)


async def init_app(config):
    app = web.Application()
    app['config'] = config

    db = await init_db(app)

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)

    db_url = construct_db_url(CONFIG['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)

    setup_session(
        app,
        EncryptedCookieStorage(secret_key)
    )

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('url_shorter','templates'),
        context_processors=[current_user_ctx_processor],
        filters={'datetimeformat': datetimeformat}
    )

    setup_security(
        app,
        SessionIdentityPolicy(),
        DBAuthorizationPolicy(db)
    )

    setup_routes(app)
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_pg)
    return app

if __name__ == '__main__':
    app = init_app(config=CONFIG)
    web.run_app(app)
