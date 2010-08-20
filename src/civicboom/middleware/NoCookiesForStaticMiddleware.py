"""
If there is a "Cache-Control: public" header, then strip the
"Set-Cookie" header -- otherwise proxies could cache the
set-cookie, and all users behind the proxy would get the
same session ID
"""

class NoCookiesForStaticMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def stripper_start_response(status, headers, exc_info = None):
            static = False
            new_headers = []
            for k, v in headers:
                if k.lower() == "cache-control" and "public" in v:
                    static = True
            if static:
                for k, v in headers:
                    if k.lower() != "set-cookie":
                        new_headers.append((k, v))
            else:
                new_headers = headers
            return start_response(status, new_headers, exc_info)
        return self.app(environ, stripper_start_response)
