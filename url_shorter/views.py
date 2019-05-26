import aiohttp_jinja2
from . import models as m
from aiohttp import web
from aiohttp_security import authorized_userid, remember, forget
from .utils import generate_key, fetch_url
from .forms import validate_login_form, validation_signup


@aiohttp_jinja2.template('index.html')
async def index(request):
    username = await authorized_userid(request)
    if not username:
        raise web.HTTPFound('login')

    async with request.app['db'].acquire() as conn:
        user = await m.get_user_by_name(conn, username)
        urls = await m.get_urls_by_user(conn, user['id'])
        return {'user': user, 'urls': urls}


def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)


@aiohttp_jinja2.template('login.html')
async def login(request):
    username = await authorized_userid(request)
    if username:
        raise redirect(request.app.router, 'index')

    if request.method == 'POST':
        form = await request.post()

        async with request.app['db'].acquire() as conn:
            error = await validate_login_form(conn, form)

            if error:
                 return {'error': error}

            response = web.HTTPFound('/')

            user = await m.get_user_by_name(conn, form['username'])
            await remember(request, web.HTTPFound('/'), user['username'])

            raise response

    return {}


async def logout(request):
    response = web.HTTPFound('login')
    await forget(request, response)
    return response


@aiohttp_jinja2.template('signup.html')
async def signup(request):
    if request.method == "POST":
        form = await request.post()

        async with request.app['db'].acquire() as conn:
            error = await validation_signup(conn, form)

            if error:
                return {'error': error}

            await m.create_user(conn, form['username'], form['password'], form['email'])
            raise web.HTTPFound('/')



@aiohttp_jinja2.template('url_shortener.html')
async def url_shortener(request):
    return {}

async def short_url(request):
    if request.method == "POST":

        config = request.app['config']
        username = await authorized_userid(request)

        data = await request.json()
        url = fetch_url(data)

        async with request.app['db'].acquire() as conn:
            if username:

                last_url = await conn.fetchrow(
                    m.urls.select().order_by(m.urls.c.id.desc()).limit(1)
                )

                _url = await m.get_url_by_lurl(conn, url)
                if _url:
                    await m.delete_url(conn, url)
                current_user = await m.get_user_by_name(conn, username)

                short_url = "http://{host}/{path}".format(
                    host=config['host'],
                    path=generate_key(last_url['id'] + 1 if last_url else 1)
                )

                await m.add_url(conn, url, short_url, current_user['id'])

                return web.json_response({'url': short_url, 'long_url': url })


async def short_url_redirect(request):
    short_url = request.match_info['short_id']

    async with request.app['db'].acquire() as conn:
        url_row = await m.get_url_by_lurl(conn, short_url)

        location = url_row['url']
        return web.HTTPFound(location)
