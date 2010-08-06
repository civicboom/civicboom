
class HttpsDetectionMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['wsgi.url_scheme'] = environ.get('HTTP_X_URL_SCHEME', 'http')
        return self.app(environ, start_response)
