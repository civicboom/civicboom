import qrencode
import StringIO


def qrcode_stream(text, size=210, format='png', **kwargs):
    buf = StringIO.StringIO()
    qrencode.encode_scaled(text, size, **kwargs)[2].save(buf, format=format)
    return buf.getvalue()


from pylons import tmpl_context as c, response
from civicboom.lib.web import action_error

def cb_qrcode(cb_url, **kwargs):
    kwargs['format'        ] = c.format if c.format in ['png', 'jpeg', 'gif', 'bmp', 'tiff'] else 'png'
    kwargs['size'          ] = int(kwargs.get('size', 210))
    kwargs['level'         ] = int(kwargs.get('level', qrencode.QR_ECLEVEL_M))
    #kwargs['case_sensitive'] = kwargs.get('case_sensitive', False)
    try:
        qr_stream = qrcode_stream(cb_url, **kwargs)
        response.headers['Content-type'] = "image/%s" % kwargs['format']
        return qr_stream
    except Exception as e:
        raise action_error('error generating QRCode: %s' % e)
