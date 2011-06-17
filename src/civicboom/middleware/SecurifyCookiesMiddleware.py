"""
Workaround for beaker's insecure cookie settings


Beaker has a config-time on/off setting for secure cookies, where
we want it to be secure if possible and insecure as a fallback.

--> https://bitbucket.org/bbangert/beaker/issue/63


Also, there is no way to set httponly, to protect against XSS
cookie theft.

--> https://bitbucket.org/bbangert/beaker/issue/62

~~~~~~~~~~~

If there is a "Cache-Control: public" header, then strip the
"Set-Cookie" header -- otherwise proxies could cache the
set-cookie, and all users behind the proxy would get the
same session ID
"""


class SecurifyCookiesMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def secure_start_response(status, headers, exc_info = None):
            # check to see if this is a static page
            static = False
            for k, v in headers:
                if k.lower() == "cache-control" and "public" in v:
                    static = True
                if k.lower() == "host" and "widget" in v:
                    static = True

            new_headers = []
            for k, v in headers:
                # if the header is set-cookie and we are dynamic,
                # set a secure-as-possible cookie
                if k.lower() == "set-cookie":
                    # if static:
                    #     pass  # set-cookie is only appropriate for dynamic pages
                    if not static:
                        if "; secure" not in v and environ['wsgi.url_scheme'] == "https":
                            v = v + "; secure"
                        if "; httponly" not in v:
                            v = v + "; httponly"
                        new_headers.append((k, v))
                # all other headers are fine
                else:
                    new_headers.append((k, v))

            return start_response(status, new_headers, exc_info)
        return self.app(environ, secure_start_response)
