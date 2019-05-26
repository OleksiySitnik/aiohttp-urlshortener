from . import models as m

async def validate_login_form(conn, form):

    username = form['username']
    password = form['password']

    if not username:
        return 'username is required'
    if not password:
        return 'password is required'

    user = await m.get_user_by_name(conn, username)

    if not user:
        return 'Invalid username'
    else:
        if password == user['password_hash']:
            return None
        else:
            return 'Invalid password'


async def validation_signup(conn, form):
    username = form['username']
    password = form['password']
    email = form['email']

    if not username:
        return 'username is required'
    if not password:
        return 'password is required'
    if not email:
        return 'email is required'

    user = await m.get_user_by_name(conn, username)

    if user:
        return 'User with this name is already exist'

    return None