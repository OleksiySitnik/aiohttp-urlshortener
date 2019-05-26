from . import views


def setup_routes(app):
    app.router.add_get('/', views.index, name='index')
    app.router.add_get('/login', views.login, name='login')
    app.router.add_post('/login', views.login, name='login')
    app.router.add_get('/logout', views.logout, name='logout')
    app.router.add_get('/signup', views.signup, name='signup')
    app.router.add_post('/signup', views.signup, name='signup')
    app.router.add_get('/urlshortener', views.url_shortener, name='urlshortener')
    app.router.add_get('/{short_id}', views.short_url_redirect, name='short')
    app.router.add_post('/short', views.short_url)
    app.router.add_get('/short', views.short_url)

    # app.router.add_get('/{short_url}', views.url_shortener, name='urlshortener')
