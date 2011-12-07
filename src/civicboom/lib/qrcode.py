import qrencode
import StringIO

import Image

def qrcode_stream(text, pixel_size=8, format='png', **kwargs):
    (version, size, im) = qrcode_scale(qrencode.encode(text, **kwargs), pixel_size)
    
    buf = StringIO.StringIO()
    #qrencode.encode_scaled(text, size, **kwargs)[2].save(buf, format=format) # AllanC - encode_scaled dose not include the border reuiqred by the standard
    im.save(buf, format=format)
    return buf.getvalue()

def qrcode_scale(qrcode, pixel_size):
    """
    Copy of qrencode.encode_scaled
    The original method does not support the standard 4 unit pixel border
    reference for standard - http://www.denso-wave.com/qrcode/qrgene4-e.html
    """
    version, src_size, im = qrcode
    
    qr_image_size    = src_size * pixel_size
    padding_size     = 4 * pixel_size
    final_image_size = (src_size * pixel_size) + (2 * padding_size)
    
    new_img = Image.new("L", (final_image_size, final_image_size), 255)
    new_img.paste(im.resize((qr_image_size, qr_image_size), Image.NEAREST), (padding_size, padding_size))
    
    return (version, final_image_size, new_img)


from pylons import tmpl_context as c, response
from civicboom.lib.web import action_error

def cb_qrcode(cb_url, **kwargs):
    kwargs['format'        ] = c.format if c.format in ['png', 'jpeg', 'gif', 'bmp', 'tiff'] else 'png'
    kwargs['pixel_size'    ] = int(kwargs.get('pixel_size', 8))
    kwargs['level'         ] = int(kwargs.get('level', qrencode.QR_ECLEVEL_M))
    #kwargs['case_sensitive'] = kwargs.get('case_sensitive', False)
    
    try:
        qr_stream = qrcode_stream(cb_url, **kwargs)
        response.headers['Content-type'] = "image/%s" % kwargs['format']
        return qr_stream
    except Exception as e:
        response.headers['Content-type'] = "text/html; charset=utf-8"
        raise action_error('error generating QRCode: %s' % e)
