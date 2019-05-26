from string import ascii_letters, digits
from aiohttp import web
import trafaret as t


CHARS = ascii_letters + digits


def generate_key(id, alphabet=CHARS):
    length = len(alphabet)
    result = ''

    while id:
        id, mod = divmod(id, length)
        result = alphabet[mod - 1] + result

    return result


ShortifyRequest = t.Dict({
    t.Key('url'): t.URL
})


def fetch_url(data):
    try:
        data = ShortifyRequest(data)
    except t.DataError:
        raise web.HTTPBadRequest()
    return data['url']
