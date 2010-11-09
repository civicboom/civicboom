"""
Workaround for beaker's insecure cookie settings


Beaker has a config-time on/off setting for secure cookies, where
we want it to be secure if possible and insecure as a fallback.

--> https://bitbucket.org/bbangert/beaker/issue/63


Also, there is no way to set httponly, to protect against XSS
cookie theft.

--> https://bitbucket.org/bbangert/beaker/issue/62
"""

class SecurifyCookiesMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def secure_start_response(status, headers, exc_info = None):
            new_headers = []
            for k, v in headers:
                if k.lower() == "set-cookie":
                    if "; secure" not in v and environ['wsgi.url_scheme']=="https":
                        v = v + "; secure"
                    if "; httponly" not in v:
                        v = v + "; httponly"
                new_headers.append((k, v))
            return start_response(status, new_headers, exc_info)
        return self.app(environ, secure_start_response)
