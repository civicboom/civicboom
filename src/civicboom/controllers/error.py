import cgi

from paste.urlparser import PkgResourcesParser
from pylons import request, tmpl_context as c
#from pylons.templating        import render_mako
from pylons.controllers.util import forward
#from pylons.middleware import error_document_template
from webhelpers.html.builder import literal

from civicboom.lib.base import BaseController

from civicboom.lib.web import auto_format_output

class ErrorController(BaseController): # pragma: no cover -- if this is covered, then something has gone wrong...

    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """

    @auto_format_output()
    def document(self):
        """Render the error document"""
        resp    = request.environ.get('pylons.original_response')
        content = literal(resp.body) or cgi.escape(request.GET.get('message', ''))
        #page    = error_document_template % \
        #    dict(prefix  = request.environ.get('SCRIPT_NAME', ''),
        #         code    = cgi.escape(request.GET.get('code', str(resp.status_int))),
        #         message = content)
        
        #c.error_prefix  = request.environ.get('SCRIPT_NAME', '')
        #c.error_code    = cgi.escape(request.GET.get('code', str(resp.status_int)))
        #c.error_message = content
        #if c.format == 'html':
        #    page = render_mako("web/error.mako")
        #else:
        #    page = content
        #return page
        return {
            'status'  :'error' ,
            'code'    : cgi.escape(request.GET.get('code', str(resp.status_int))) ,
            'message' : content ,
            'template': 'error'
        }

    def img(self, id):
        """Serve Pylons' stock images"""
        return self._serve_file('/'.join(['media/img', id]))

    def style(self, id):
        """Serve Pylons' stock stylesheets"""
        return self._serve_file('/'.join(['media/style', id]))

    def _serve_file(self, path):
        """Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        request.environ['PATH_INFO'] = '/%s' % path
        return forward(PkgResourcesParser('pylons', 'pylons'))
