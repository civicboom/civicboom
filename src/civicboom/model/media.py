from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, DateTime
from sqlalchemy import func
from sqlalchemy.schema import CheckConstraint
from geoalchemy import GeometryColumn as Golumn, Point, GeometryDDL

from cbutils.misc import now

from civicboom.model.meta import Base
import cbutils.warehouse as wh
import cbutils.worker as worker

from pylons import config, app_globals # used in generation of URL's for media

import magic
import mimetypes
import copy
import logging
import os

log = logging.getLogger(__name__)


class Media(Base):
    __tablename__ = "media"
    _media_types  = Enum("application", "audio", "example", "image", "message", "model", "multipart", "text", "video", name="media_types")
    id            = Column(Integer(),        primary_key=True)
    content_id    = Column(Integer(),        ForeignKey('content.id'), nullable=False, index=True)
    name          = Column(Unicode(250),     nullable=False)
    type          = Column(_media_types,     nullable=False, doc="MIME type, eg 'text', 'video'")
    subtype       = Column(String(32),       nullable=False, doc="MIME subtype, eg 'jpeg', '3gpp'")
    hash          = Column(String(40),       nullable=False, index=True)
    caption       = Column(UnicodeText(),    nullable=False, default='')
    credit        = Column(UnicodeText(),    nullable=False, default='')
    filesize      = Column(Integer(),        nullable=True, doc="the length of the processed media file in bytes")
    location      = Golumn(Point(2),         nullable=True)
    timestamp     = Column(DateTime(),       nullable=False, default=now)

    __table_args__ = (
        CheckConstraint("length(subtype) > 0"),
        CheckConstraint("length(hash) = 40"),
        {}
    )
    
    __to_dict__ = Base.__to_dict__.copy()
    __to_dict__.update({
        'default': {
            'id'           : None ,
            'name'         : None ,
            'type'         : None ,
            'subtype'      : None ,
            #'mime_type'    : None ,
            'caption'      : None ,
            'credit'       : None ,
            'media_url'    : None ,
            'original_url' : None ,
            'thumbnail_url': None ,
            'filesize'     : None ,
            'hash'         : None ,
        },
    })
    __to_dict__.update({
        'full'        : copy.deepcopy(__to_dict__['default']) ,
        #'full+actions': copy.deepcopy(__to_dict__['default']) ,
    })
    __to_dict__['full'].update({
            'processing_status' : lambda media: app_globals.memcache.get(str("media_processing_%s" % media.id)) ,
    })



    def load_from_file(self, tmp_file=None, original_name=None, caption=None, credit=None):
        """
        Create a Media object from a blob of data + upload form details
        """
        # Generate Hash and move file locally
        self.hash               = wh.hash_file(tmp_file)

        # make a personal copy of the file; tmp_file may not be a real
        # file, and it will disappear when the request is over
        if not os.path.exists(config["path.temp"]):
            os.makedirs(config["path.temp"])
        my_file = config["path.temp"]+"/media-"+self.hash
        wh.copy_cgi_file(tmp_file, my_file)

        # Set up metadata
        self.name               = original_name
        self.caption            = caption if caption else u""
        self.credit             = credit  if credit  else u""
        self.type, self.subtype = magic.from_file(my_file, mime=True).split("/")
        
        # libmagic is not magical enough (*cries*) to detect all types (e.g. MPEG)
        #  need to detect by extension when fails - Greg M
        if self.type == "application" and self.subtype == 'octet-stream':
            mtype, msubtype = mimetypes.guess_type(self.name)
            if mtype:
                self.type, self.subtype = mtype.split("/")

        app_globals.memcache.set(str("media_processing_"+self.hash), "Media queued")

        worker.add_job({
            "task": "process_media",
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
        #return "https://%s/media-original/%s"  % (config['warehouse.url'], self.hash) #/%s , self.name
        return self._url_gen('media-original')

    @property
    def media_url(self):
        "The URL of the processed media, eg .flv file for video"
        #return "https://%s/media/%s"           % (config['warehouse.url'], self.hash) #/%s need to add filename to end for saving , self.name
        return self._url_gen('media')

    @property
    def thumbnail_url(self):
        "The URL of a JPEG-format thumbnail of this media"
        #return "https://%s/media-thumbnail/%s" % (config['warehouse.url'], self.hash )
        return self._url_gen('media-thumbnail')

    def _url_gen(self, media_type):
        if config['warehouse.type'] == 'local':
            return "%s/%s/%s" % (config['warehouse.url'], media_type, self.hash)
        return "https://%s/%s/%s" % (config['warehouse.url'], media_type, self.hash)

GeometryDDL(Media.__table__)
