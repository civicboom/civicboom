from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean

from civicboom.model.meta import Base
import civicboom.lib.services.warehouse as wh
import civicboom.lib.worker as worker

from pylons import config, app_globals # used in generation of URL's for media

import magic
import logging

log = logging.getLogger(__name__)

memcache_expire = 10*60 # 10 * 60 Seconds = 10 Minuets


class Media(Base):
    __tablename__ = "media"
    _media_types  = Enum("application", "audio", "example", "image", "message", "model", "multipart", "text", "video", name="media_types")
    id            = Column(Integer(),        primary_key=True)
    content_id    = Column(Integer(),        ForeignKey('content.id'), nullable=False)
    name          = Column(Unicode(250),     nullable=False)
    type          = Column(_media_types,     nullable=False, doc="MIME type, eg 'text', 'video'")
    subtype       = Column(String(32),       nullable=False, doc="MIME subtype, eg 'jpeg', '3gpp'")
    hash          = Column(String(40),       nullable=False, index=True)
    caption       = Column(UnicodeText(),    nullable=False)
    credit        = Column(UnicodeText(),    nullable=False)
    
    __to_dict__ = Base.__to_dict__.copy()
    __to_dict__.update({
        'list': {
            'id'           : None ,
            'name'         : None ,
            'type'         : None ,
            'subtype'      : None ,
            'caption'      : None ,
            'credit'       : None ,
            'media_url'    : None ,
            'original_url' : None ,
            'thumbnail_url': None ,
        },
    })



    def load_from_file(self, tmp_file=None, original_name=None, caption=None, credit=None):
        """
        Create a Media object from a blob of data + upload form details
        """

        # Generate Hash and move file locally
        self.hash               = wh.hash_file(tmp_file)

        # make a personal copy of the file; tmp_file may not be a real
        # file, and it will disappear when the request is over
        my_file = config["path.temp"]+"/media-"+self.hash
        wh.copy_cgi_file(tmp_file, my_file)

        # Set up metadata
        self.name               = original_name
        self.caption            = caption if caption else u""
        self.credit             = credit  if credit  else u""
        self.type, self.subtype = magic.from_file(my_file, mime=True).split("/")

        #def copy_config():
        #    d = {}
        #    for key in config.keys():
        #        d[key] = config[key]
        #    return d
        
        app_globals.memcache.set(str("media_processing_"+self.hash), "temp", time=memcache_expire) # Flag memcache to indicate this media is being processed

        wh.copy_to_warehouse("./civicboom/public/images/media_placeholder.gif", "media-thumbnail", self.hash, placeholder=True)

        worker.add_job({
            "task": "process_media",
            #"config": copy_config(),
            "tmp_file": my_file,
            "file_hash": self.hash,
            "file_type": self.type,
            "file_name": self.name,
            "delete_tmp": True,
        })

        return self

    def __unicode__(self):
        return self.name

    @property
    def mime_type(self):
        return self.type + "/" + self.subtype

    @property
    def media_name(self):
        exts = {
            "audio": "ogg",
            "image": self.subtype, # this just happens to work for PNG, GIF, JPEG
            "video": "flv"
        }
        return "%s.%s" % (self.name, exts[self.type])

    @property
    def original_url(self):
        "The URL of the original as-uploaded file"
        return "%s/media-original/%s"  % (config['warehouse_url'], self.hash) #/%s , self.name

    @property
    def media_url(self):
        "The URL of the processed media, eg .flv file for video"
        return "%s/media/%s"           % (config['warehouse_url'], self.hash) #/%s need to add filename to end for saving , self.name

    @property
    def thumbnail_url(self):
        "The URL of a JPEG-format thumbnail of this media"
        return "%s/media-thumbnail/%s" % (config['warehouse_url'], self.hash )
