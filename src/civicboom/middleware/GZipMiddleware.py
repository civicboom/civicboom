# GZip Middleware
# http://pylonsbook.com/en/1.1/the-web-server-gateway-interface-wsgi.html#altering-the-response

import gzip
import StringIO
from decorator import decorator
from pylons import request

gzip_environ_key = 'GZIP_ENCODE_RESPONSE'

# Decorator for controler action to trigger the response should be GZiped
def gzip_response(func, *args, **kargs):
  request.environ[gzip_environ_key] = "True"
  return func(*args, **kargs)
gzip_response = decorator(gzip_response)



class GZipMiddleware(object):

  def __init__(self, app, compresslevel=9):
    self.app = app
    self.compresslevel = compresslevel
    
  def __call__(self, environ, start_response):
    # If decorator has not been activated or client does not support gzip encoding then do not GZip
    if 'gzip' not in environ.get('HTTP_ACCEPT_ENCODING', ''):
      return self.app(environ, start_response)
    
    # UNFINISHED - AllanC - the environ was ment to be set by the decorator above, however ...
    #                       the environ is set AFTER start_response is called, it has not been set here.
    #                       the issue is that the dummy_start_response needs a writeable stream, 
    if not environ.has_key(gzip_environ_key):
      return self.app(environ, start_response)
    
    print "Gzip Middleware unfinished and should not be called!"
    
    buffer = StringIO.StringIO()
    output = gzip.GzipFile(mode='wb', compresslevel=self.compresslevel, fileobj=buffer)
    
    # Setup dummy response (because of scope we cant access variables until they are called, use this to collect the nessisary variables)
    # See pylons book documenation (linked above for more info)
    start_response_args = []
    def dummy_start_response(status, headers, exc_info=None):
      start_response_args.append(status)
      start_response_args.append(headers)
      start_response_args.append(exc_info)
      return output.write

    # Call lower middleware and get get full response to gzip encode
    app_iter = self.app(environ, dummy_start_response)

    # AllanC - This is the point where the gzip_env will be set with the decorator above. but it is too late :(

    for line in app_iter:
      output.write(line)
    if hasattr(app_iter, 'close'): app_iter.close()
    output.close()
    buffer.seek(0)
    result = buffer.getvalue()
    
    # Recreate http header - removing content-length (because the length has changed)
    headers = []
    for name, value in start_response_args[1]: #Remove existing content-length field (could use a list comprehention?)
      if name.lower() != 'content-length':
        headers.append((name, value))
    headers.append(('Content-Length', str(len(result)))) # Add correct content-length field
    headers.append(('Content-Encoding', 'gzip'))         # Set encoding to gzip
    
    # Call the next middleware in the stack with the updated headers (passing up any errors/status)
    start_response(start_response_args[0], headers, start_response_args[2])
    buffer.close()
    return [result]
