
class EnvironMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['wsgi.url_scheme'] = environ.get('HTTP_X_URL_SCHEME', 'http')
        environ['REMOTE_ADDR']     = environ.get('HTTP_X_REAL_IP', environ.get('REMOTE_ADDR', '0.0.0.0'))
        return self.app(environ, start_response)
