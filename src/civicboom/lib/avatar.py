import tempfile
import urllib2
import Image
import cbutils.warehouse as wh


def process_avatar(file_obj=None, url=None):
    """
    This should always be surrounded by a try/except
    """
    assert not isinstance(file_obj, None.__class__) or url # AllanC - this fails with a non-null file_obj!? wtf?
    with tempfile.NamedTemporaryFile(suffix=".jpg") as original:
        filename = None
        if url:
            original.write(urllib2.urlopen(url).read())
            original.flush()
        if not isinstance(file_obj, None.__class__): # AllanC - same as assertion above .. why the **** do I need to check the instance is not 'None'? why cant I do if file_obj?
            wh.copy_cgi_file(file_obj, original.name)
            filename = file_obj.filename
        h = wh.hash_file(original.name)
        wh.copy_to_warehouse(original.name, "avatars-original", h, filename)
        
        with tempfile.NamedTemporaryFile(suffix=".jpg") as processed:
            im  = Image.open(original.name)
            if im.mode == "RGBA":
                # AllanC - PNG's can have a 'background colour' set that the user is unaware of and the transparancy is silently converted to this colour by PIL
                #          create a new RGB image with a white background to paste avatar onto - this disposes of the avatars original backgourd colour
                thumbnail_im = Image.new("RGB", im.size, (255,255,255))
                thumbnail_im.paste(im, (0,0), im)
                im = thumbnail_im
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.thumbnail((160, 160), Image.ANTIALIAS)
            im.save(processed.name, "JPEG")
            wh.copy_to_warehouse(processed.name, "avatars", h, filename)
        
        return h